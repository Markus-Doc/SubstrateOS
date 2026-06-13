"""Codebase-wide audit as a Dynamic Workflow (Phase 2 M5, capstone capability).

`labctl audit <repo>` runs an **engineering / code-quality** audit (deliberately
not pentest language — the master research notes cyber-classifier rerouting) as
the architect → workers → reviewer → judge Dynamic Workflow (M-E), grounded by
BM25 retrieval over the repo's memory namespace (hybrid retrieval deferred per
ADR-017). It produces a committed findings report.

The grounding and the stage runner are injected, so the capability is fully
testable without spending tokens; the live capstone run (real engine, real
token spend, ideally in-container) is owner-triggered.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from labctl import orchestrate
from labctl.orchestrate import HandoffPacket, StageRunner, WorkflowResult

# Grounding query seeds the architect with the most relevant repo knowledge.
GROUNDING_QUERY = "architecture decisions risks code quality tests security"

AUDIT_OBJECTIVE = (
    "Perform an engineering and code-quality audit of this repository: "
    "architecture coherence, decision-record consistency, test coverage gaps, "
    "dead/duplicated code, and maintainability risks. This is a code-quality "
    "review, not a penetration test."
)


@dataclass
class AuditResult:
    repo: str
    workflow: WorkflowResult
    report: str
    report_path: Path | None

    @property
    def accepted(self) -> bool:
        return self.workflow.accepted


def build_audit_packet(repo: str, grounding: list[str]) -> HandoffPacket:
    return HandoffPacket(
        repo=repo,
        objective=AUDIT_OBJECTIVE,
        in_scope=[
            "Source under scripts/ and substrate/",
            "ADRs in docs/decisions/ and their consistency",
            "Test coverage and gate stages",
        ],
        out_of_scope=[
            "Penetration testing / exploit development",
            "Sibling repos and anything outside this repo",
            "Editing files (audit is read-and-report only)",
        ],
        expected_evidence="A findings report: issue, location, severity, suggested fix.",
        verification_commands=["labctl gate", "labctl status"],
        stop_conditions=[
            "Token budget exhausted (circuit breaker)",
            "Judge rejects the findings as unverified",
        ],
        grounding=grounding,
    )


def render_report(repo: str, packet: HandoffPacket, wf: WorkflowResult) -> str:
    ts = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"# SubstrateOS audit report — {repo}",
        f"\nGenerated: {ts}",
        f"\nVerdict: {wf.verdict}  (accepted: {wf.accepted})",
        f"\nMetrics: {wf.metrics}\n",
        "## Objective\n",
        packet.objective,
        "\n## Stage outputs\n",
    ]
    for stage in wf.stages:
        lines.append(f"### {stage.name} ({stage.tokens_used}/{stage.budget} tokens)\n")
        lines.append(stage.output or "(no output)")
        lines.append("")
    return "\n".join(lines)


def run_audit(
    repo_root: Path,
    *,
    runner: StageRunner,
    ground: Callable[[str], list[str]],
    n_workers: int = 2,
    log_dir: Path | None = None,
    report_path: Path | None = None,
) -> AuditResult:
    """Run the audit Dynamic Workflow and produce (and optionally write) a report."""
    grounding = ground(GROUNDING_QUERY)
    packet = build_audit_packet(repo_root.name, grounding)
    wf = orchestrate.run_workflow(
        packet.render(), runner=runner, n_workers=n_workers, log_dir=log_dir
    )
    report = render_report(repo_root.name, packet, wf)
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
    return AuditResult(repo_root.name, wf, report, report_path)
