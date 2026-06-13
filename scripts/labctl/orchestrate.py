"""Dynamic Workflows: multi-agent / sub-agent orchestration (Phase 2, ADR-019).

The frontier model acts as planner/architect/judge while sub-agents do the work,
following the master-research pattern **architect → workers → reviewer → judge**
with handoff packets and *verify-before-accept* (the judge gates acceptance).

Each stage is budget-capped by the same token circuit breaker used for capsule
builds (`labctl.capsule`). The engine is pure and takes an injectable
``runner`` so it is fully testable without spawning real sub-agents; the default
``claude_stage_runner`` wraps the headless-claude machinery. Every run writes a
JSONL trace and computes agentic-eval trace metrics (branch-2 P2-B).
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from labctl import capsule as capsule_mod

DEFAULT_STAGE_BUDGET = 500_000
RUN_LOG_DIR_REL = ".substrateos/workflows"

# A runner executes one stage: (role, name, prompt, budget) -> (output, tokens, tripped)
StageRunner = Callable[[str, str, str, int], tuple[str, int, bool]]

ARCHITECT_PROMPT = (
    "You are the ARCHITECT. Mission:\n{mission}\n\nProduce a concise numbered "
    "build plan as the handoff packet for the workers. Output only the plan."
)
WORKER_PROMPT = (
    "You are WORKER {n}. The architect's plan:\n{plan}\n\nExecute your portion "
    "and output only your result as a handoff packet."
)
REVIEWER_PROMPT = (
    "You are the REVIEWER. Mission:\n{mission}\n\nWorker outputs:\n{outputs}\n\n"
    "List concrete issues/findings. Output only the findings."
)
JUDGE_PROMPT = (
    "You are the JUDGE. Mission:\n{mission}\n\nReviewer findings:\n{findings}\n\n"
    "Verify before accepting. Reply on the first line with ACCEPT or REJECT and "
    "a one-line reason."
)


@dataclass
class HandoffPacket:
    """Self-contained work order passed to a sub-agent (master research pattern).

    Carries everything a bounded worker needs and nothing it must guess: the
    target, the exact objective, in/out of scope, the evidence expected back,
    how to verify it, and when to stop.
    """

    repo: str
    objective: str
    in_scope: list[str]
    out_of_scope: list[str]
    expected_evidence: str
    verification_commands: list[str]
    stop_conditions: list[str]
    grounding: list[str] = field(default_factory=list)

    def render(self) -> str:
        def bullets(items: list[str]) -> str:
            return "\n".join(f"- {i}" for i in items) if items else "- (none)"

        ground = "\n".join(f"  > {g}" for g in self.grounding) if self.grounding else "  (none)"
        return (
            f"# Handoff packet\n\n"
            f"Repo: {self.repo}\n\n"
            f"Objective:\n{self.objective}\n\n"
            f"In scope:\n{bullets(self.in_scope)}\n\n"
            f"Out of scope:\n{bullets(self.out_of_scope)}\n\n"
            f"Expected evidence:\n{self.expected_evidence}\n\n"
            f"Verification commands:\n{bullets(self.verification_commands)}\n\n"
            f"Stop conditions:\n{bullets(self.stop_conditions)}\n\n"
            f"Grounding (BM25 retrieval over the repo namespace):\n{ground}\n"
        )


@dataclass
class StageResult:
    role: str
    name: str
    output: str
    tokens_used: int
    budget: int
    ok: bool
    breaker_tripped: bool


@dataclass
class WorkflowResult:
    mission: str
    stages: list[StageResult]
    verdict: str
    accepted: bool
    run_log: Path | None
    metrics: dict = field(default_factory=dict)


def _verdict_accepts(text: str) -> bool:
    first = text.strip().splitlines()[0] if text.strip() else ""
    upper = first.upper()
    return "ACCEPT" in upper and "REJECT" not in upper


def _metrics(stages: list[StageResult], accepted: bool) -> dict:
    tokens = sum(s.tokens_used for s in stages)
    budget = sum(s.budget for s in stages)
    return {
        "stages_total": len(stages),
        "stages_ok": sum(1 for s in stages if s.ok),
        "breaker_trips": sum(1 for s in stages if s.breaker_tripped),
        "tokens_used": tokens,
        "tokens_budget": budget,
        "budget_utilisation": round(tokens / budget, 4) if budget else 0.0,
        "task_completion": 1.0 if accepted else 0.0,
    }


def run_workflow(
    mission: str,
    *,
    runner: StageRunner,
    n_workers: int = 2,
    budgets: dict[str, int] | None = None,
    log_dir: Path | None = None,
) -> WorkflowResult:
    """Run architect → workers → reviewer → judge with verify-before-accept."""
    budgets = budgets or {}

    def budget_for(role: str) -> int:
        return budgets.get(role, DEFAULT_STAGE_BUDGET)

    stages: list[StageResult] = []

    def run_stage(role: str, name: str, prompt: str) -> StageResult:
        budget = budget_for(role)
        output, tokens, tripped = runner(role, name, prompt, budget)
        result = StageResult(role, name, output, tokens, budget, not tripped, tripped)
        stages.append(result)
        return result

    arch = run_stage("architect", "architect", ARCHITECT_PROMPT.format(mission=mission))
    if arch.breaker_tripped:
        return _finalise(mission, stages, "aborted: architect over budget", False, log_dir)

    worker_outputs: list[str] = []
    for i in range(1, n_workers + 1):
        w = run_stage("worker", f"worker-{i}", WORKER_PROMPT.format(n=i, plan=arch.output))
        worker_outputs.append(f"[worker-{i}]\n{w.output}")

    reviewer = run_stage(
        "reviewer",
        "reviewer",
        REVIEWER_PROMPT.format(mission=mission, outputs="\n\n".join(worker_outputs)),
    )
    judge = run_stage(
        "judge", "judge", JUDGE_PROMPT.format(mission=mission, findings=reviewer.output)
    )

    accepted = judge.ok and _verdict_accepts(judge.output)
    verdict = judge.output.strip().splitlines()[0] if judge.output.strip() else "no verdict"
    return _finalise(mission, stages, verdict, accepted, log_dir)


def _finalise(
    mission: str,
    stages: list[StageResult],
    verdict: str,
    accepted: bool,
    log_dir: Path | None,
) -> WorkflowResult:
    metrics = _metrics(stages, accepted)
    run_log = _write_log(mission, stages, verdict, accepted, metrics, log_dir)
    return WorkflowResult(mission, stages, verdict, accepted, run_log, metrics)


def _write_log(
    mission: str,
    stages: list[StageResult],
    verdict: str,
    accepted: bool,
    metrics: dict,
    log_dir: Path | None,
) -> Path | None:
    if log_dir is None:
        return None
    log_dir.mkdir(parents=True, exist_ok=True)
    started = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = log_dir / f"workflow-{started}.jsonl"
    with path.open("w", encoding="utf-8") as fh:
        fh.write(json.dumps({"type": "mission", "mission": mission}) + "\n")
        for s in stages:
            fh.write(json.dumps({"type": "stage", **asdict(s)}) + "\n")
        fh.write(
            json.dumps(
                {"type": "verdict", "verdict": verdict, "accepted": accepted, "metrics": metrics}
            )
            + "\n"
        )
    return path


def _extract_text(event: dict) -> str:
    """Pull assistant text from a stream-json event (best effort)."""
    message = event.get("message") if isinstance(event.get("message"), dict) else event
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return ""


def claude_stage_runner(root: Path, *, spawn=None) -> StageRunner:
    """Default runner: each stage is a headless claude sub-agent, budget-capped.

    Reuses the capsule circuit-breaker machinery; ``spawn`` is injectable for
    tests (defaults to the real headless-claude spawn).
    """
    spawn = spawn or capsule_mod._spawn_claude

    def runner(role: str, name: str, prompt: str, budget: int) -> tuple[str, int, bool]:
        proc = spawn(prompt, root)
        assert proc.stdout is not None
        tokens = 0
        text_parts: list[str] = []
        tripped = False
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            tokens += capsule_mod._usage_tokens(event)
            text_parts.append(_extract_text(event))
            if tokens > budget:
                tripped = True
                capsule_mod._kill_build(proc)
                break
        if not tripped:
            proc.wait()
        return "".join(text_parts).strip(), tokens, tripped

    return runner
