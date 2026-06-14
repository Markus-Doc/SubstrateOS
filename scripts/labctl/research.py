"""`labctl research`: scheduled best-practices research/review pipeline (ADR-021).

Keeps SubstrateOS current with AI best practices. **RESYNTH** (a separate,
optional CLI with zero runtime AI dependency) supplies the synthesis half: it
consolidates deep-research reports into a candidate master document. `labctl
research` drives RESYNTH and adds the SubstrateOS half — diff the candidate
against the current design (master research, ADRs, tooling, the watch-list) and
surface a **human-promoted** review report proposing ADRs / tooling swaps /
deprecations (never auto-merged).

By default the pipeline is OPERATED BY THE INTERACTIVE SESSION you launched with
`subos <engine>`: labctl provides deterministic, file-backed commands and the
session does the thinking. There is **no headless model call and no Agent-SDK
credit spend** unless you pass ``--auto`` (explicitly labelled at the call site).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime

# importlib.resources is stdlib since 3.9; this project requires Python >= 3.11,
# so the python37-compatibility rule is a false positive here.
from importlib import resources  # nosemgrep
from pathlib import Path

from labctl.config import find_repo_root
from labctl.ingest import INGEST_DIR_REL
from labctl.orchestrate import HandoffPacket, StageRunner, claude_stage_runner
from labctl.review import DERIVED_SUBDIR, _derived_frontmatter

RESEARCH_DIR_REL = "artifacts/research"
WATCH_FILE_NAME = "research-watch.json"
SUBSTRATE_WATCH_REL = ("substrate", WATCH_FILE_NAME)
REVIEW_NAMESPACE = "research-review"
AUTO_BUDGET = 500_000  # per-step token cap for --auto (ADR-016 circuit breaker)

# --- watch-list resolution: repo-first, packaged fallback (mirrors subos) ---


def _packaged_watch_path() -> Path | None:
    try:
        resource = resources.files("labctl.data").joinpath(WATCH_FILE_NAME)
    except (ModuleNotFoundError, AttributeError):
        return None
    try:
        if resource.is_file():
            return Path(str(resource))
    except (OSError, AttributeError):
        return None
    return None


def watch_list_path(root: Path | None = None) -> Path:
    """Resolve the watch-list: repo source first, packaged copy as fallback."""
    if root is not None:
        candidate = root.joinpath(*SUBSTRATE_WATCH_REL)
        if candidate.is_file():
            return candidate
    try:
        candidate = find_repo_root().joinpath(*SUBSTRATE_WATCH_REL)
        if candidate.is_file():
            return candidate
    except FileNotFoundError:
        pass
    packaged = _packaged_watch_path()
    if packaged is not None:
        return packaged
    return (root or Path.cwd()).joinpath(*SUBSTRATE_WATCH_REL)


def load_watch_list(root: Path | None = None) -> dict:
    return json.loads(watch_list_path(root).read_text(encoding="utf-8"))


# --- RESYNTH driver (injectable; the real runner shells out to `resynth`) ---


@dataclass
class ResynthResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


ResynthRunner = Callable[[list[str], Path], ResynthResult]


def default_resynth_runner(args: list[str], cwd: Path) -> ResynthResult:
    resynth = shutil.which("resynth")
    if resynth is None:
        raise RuntimeError(
            "resynth CLI not found on PATH; the research pipeline needs RESYNTH "
            "(see docs/planning/research-pipeline.md)"
        )
    proc = subprocess.run(
        [resynth, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return ResynthResult(proc.returncode, proc.stdout, proc.stderr)


def slugify(topic: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
    return slug or "research"


def research_dir(root: Path, topic: str) -> Path:
    return root / RESEARCH_DIR_REL / slugify(topic)


# --- RESYNTH operator protocol: the per-thinking-stage agent instructions ---
# (verbatim intent from the RESYNTH operator protocol; the gate command must
# report PASS before the next stage can run).

EXTRACT_PROMPT = (
    "Run `resynth extract {slug} --json`, read claims/EXTRACTION-INSTRUCTIONS.md, "
    "and for each source append its claims to claims/S<NN>-claims.jsonl in the "
    "documented schema (restate in your own words, one claim per line, record the "
    "source's stated confidence). Then run `resynth extract-verify {slug} --json` "
    "and fix every violation until the gate reports PASS."
)
RECONCILE_PROMPT = (
    "Run `resynth reconcile {slug} --json`, read index/RECONCILIATION-INSTRUCTIONS.md, "
    "index/claims-index.md and index/candidates.jsonl, and classify every claim into "
    "exactly one decision group in index/reconciliation.jsonl (CORROBORATED / UNIQUE / "
    "SUPERSEDED-with-merge-rule / CONFLICT-never-resolved / OUT_OF_SCOPE-with-reason). "
    "Re-run `resynth reconcile {slug} --json` until the gate reports PASS."
)
SYNTHESISE_PROMPT = (
    "Run `resynth synthesise {slug} --json`, then replace every todo callout in "
    "output/MASTER.md with prose working ONLY from the claims index and the "
    "reconciliation decisions; end every paragraph with provenance markers (e.g. "
    "[S01-C003]); cite every winning claim; describe each conflict without resolving "
    "it; fill the Gaps section. Run `resynth synth-verify {slug} --json` until PASS."
)


@dataclass
class Stage:
    name: str
    prompt: str  # operator instruction (interactive) or agent prompt (--auto)
    gate: str  # resynth subcommand whose exit 0 means this stage is satisfied


THINKING_STAGES = (
    Stage("extract", EXTRACT_PROMPT, "extract-verify"),
    Stage("reconcile", RECONCILE_PROMPT, "reconcile"),
    Stage("synthesise", SYNTHESISE_PROMPT, "synth-verify"),
)
SEAL_STAGES = ("audit", "seal", "export")


@dataclass
class BriefResult:
    project_dir: Path
    slug: str
    actions: list[str]
    next_steps: list[str]


def brief(
    root: Path,
    topic: str,
    *,
    runner: ResynthRunner | None = None,
) -> BriefResult:
    """Scaffold a RESYNTH project and generate the per-platform research prompts."""
    runner = runner or default_resynth_runner
    slug = slugify(topic)
    proj = research_dir(root, topic)
    proj.mkdir(parents=True, exist_ok=True)
    actions: list[str] = []
    init = runner(["init", slug, "--json"], proj)
    actions.append(f"resynth init {slug}: {'ok' if init.ok else 'already exists / failed'}")
    bref = runner(["brief", slug, "--topic", topic, "--json"], proj)
    actions.append(f"resynth brief {slug}: {'ok' if bref.ok else 'failed'}")
    # SubstrateOS pointer, so `research status` can find this sweep.
    (proj / "research.json").write_text(
        json.dumps(
            {
                "topic": topic,
                "slug": slug,
                "created_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "watch_items": [i["name"] for i in load_watch_list(root).get("items", [])],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    next_steps = [
        f"Run the generated per-platform prompts in {proj} on your deep-research platforms.",
        "Save each report as a file, then: labctl research sync \""
        + topic
        + "\" --reports <folder>",
    ]
    return BriefResult(proj, slug, actions, next_steps)


@dataclass
class SyncResult:
    slug: str
    completed: list[str]
    operator_action: Stage | None  # set when an interactive thinking step is required
    auto: bool


def _run_stage_auto(prompt: str, cwd: Path, runner: StageRunner) -> tuple[int, bool]:
    """Perform one thinking stage headlessly (Agent-SDK spend). Returns (tokens, tripped)."""
    _output, tokens, tripped = runner("operator", "research", prompt, AUTO_BUDGET)
    return tokens, tripped


def headless_default() -> bool:
    """Opt-in headless posture from the environment (mirrors subos._full_auto_default).

    ``SUBSTRATEOS_RESEARCH_HEADLESS`` truthy makes ``--headless`` the default for
    research thinking stages. The public Base ships safe (unset); an Overlay sets
    it in user-scope config, never in the Base.
    """
    return os.environ.get("SUBSTRATEOS_RESEARCH_HEADLESS", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def sync(
    root: Path,
    topic: str,
    *,
    reports_dir: Path | None = None,
    auto: bool = False,
    resynth_runner: ResynthRunner | None = None,
    stage_runner: StageRunner | None = None,
) -> SyncResult:
    """Drive RESYNTH's stages to produce the candidate master.

    Default (interactive): runs deterministic resynth commands and, at the first
    thinking stage whose gate is not yet PASS, returns ``operator_action`` so the
    interactive ``subos`` session can do it, then re-run ``sync`` to continue.
    ``auto``: performs each thinking stage headlessly (metered, ADR-016 breaker).
    """
    resynth_runner = resynth_runner or default_resynth_runner
    slug = slugify(topic)
    proj = research_dir(root, topic)
    completed: list[str] = []

    if reports_dir is not None:
        for report in sorted(Path(reports_dir).glob("*")):
            if report.is_file():
                resynth_runner(["intake", slug, "--source", str(report)], proj)
        completed.append("intake")

    runner = stage_runner or (claude_stage_runner(proj) if auto else None)
    for stage in THINKING_STAGES:
        if resynth_runner([stage.gate, slug, "--json"], proj).ok:
            completed.append(stage.name)
            continue
        if auto:
            assert runner is not None
            _run_stage_auto(stage.prompt.format(slug=slug), proj, runner)
            if not resynth_runner([stage.gate, slug, "--json"], proj).ok:
                return SyncResult(slug, completed, stage, auto=True)
            completed.append(stage.name)
        else:
            return SyncResult(slug, completed, stage, auto=False)

    for cmd in SEAL_STAGES:
        if resynth_runner([cmd, slug, "--json"], proj).ok:
            completed.append(cmd)
    return SyncResult(slug, completed, None, auto=auto)


# --- review: diff a candidate against the current design; emit a report ---


def adr_index(root: Path) -> list[tuple[str, str]]:
    """(filename, status) for every ADR, deterministic, for the diff inputs."""
    out: list[tuple[str, str]] = []
    decisions = root / "docs" / "decisions"
    if not decisions.is_dir():
        return out
    for path in sorted(decisions.glob("ADR-*.md")):
        status = ""
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "Status:" in line:
                status = line.split("Status:", 1)[1].strip()
                break
        out.append((path.name, status))
    return out


def build_review_packet(root: Path, topic: str, candidate: Path | None) -> HandoffPacket:
    watch = load_watch_list(root)
    grounding = [f"{i['name']}: {i['current_choice']} ({', '.join(i['adr_refs'])})" for i in watch.get("items", [])]
    cand = str(candidate) if candidate else "(no fresh RESYNTH candidate; review against current master research)"
    return HandoffPacket(
        repo=root.name,
        objective=(
            f"Diff the current AI best-practice research against SubstrateOS's design for "
            f"the topic '{topic}'. Candidate: {cand}. For each watch-list item, decide "
            f"whether the current choice still holds or should change, and propose ADRs / "
            f"tooling swaps / deprecations. Report only; never edit ADRs or merge changes."
        ),
        in_scope=[
            "docs/research/master-research.md",
            "docs/decisions/ (ADR statuses and choices)",
            "substrate/trusted-tools.json",
            "the research watch-list items",
        ],
        out_of_scope=[
            "editing or creating ADR files (the human authors them after promotion)",
            "changing tooling or code",
        ],
        expected_evidence="A review report: per-watch-item verdict + a Proposed-changes section.",
        verification_commands=["labctl research status", "labctl gate"],
        stop_conditions=["every watch item has a verdict", "proposed changes each cite an ADR"],
        grounding=grounding,
    )


def review_report_dir(root: Path) -> Path:
    return root / INGEST_DIR_REL / REVIEW_NAMESPACE / DERIVED_SUBDIR


def _scaffold_report_body(root: Path, topic: str, candidate: Path | None) -> str:
    watch = load_watch_list(root)
    adrs = adr_index(root)
    lines = [
        f"# Research review — {topic}",
        "",
        "_Generated by `labctl research review` (AI-derived, unpromoted). The "
        "interactive `subos` session fills the verdicts below; you then author any "
        "ADRs and run `labctl review approve` to promote this record._",
        "",
        f"Candidate: {candidate if candidate else '(none supplied — reviewing against current master research)'}",
        "",
        "## Watch-list verdicts",
        "",
        "| Watch item | Current choice | ADRs | Verdict (hold / change → why) |",
        "| --- | --- | --- | --- |",
    ]
    for item in watch.get("items", []):
        lines.append(
            f"| {item['name']} | {item['current_choice']} | {', '.join(item['adr_refs'])} | _TODO_ |"
        )
    lines += [
        "",
        "## Proposed changes",
        "",
        "_TODO: proposed ADRs / tooling swaps / deprecations, each with rationale and "
        "the ADR it would add or amend. Leave empty if nothing changed._",
        "",
        "## Current ADR ledger (for reference)",
        "",
    ]
    lines += [f"- {name}: {status}" for name, status in adrs]
    return "\n".join(lines) + "\n"


@dataclass
class ReviewResult:
    report_path: Path
    auto: bool
    packet: HandoffPacket


def review(
    root: Path,
    topic: str,
    *,
    candidate: Path | None = None,
    auto: bool = False,
    stage_runner: StageRunner | None = None,
) -> ReviewResult:
    """Write an AI-derived, unpromoted review report into the review queue.

    Default (interactive): writes a scaffold pre-filled with the watch-list and the
    current ADR ledger for the ``subos`` session to complete. ``auto``: generates
    the full report body headlessly (metered).
    """
    packet = build_review_packet(root, topic, candidate)
    if auto:
        runner = stage_runner or claude_stage_runner(root)
        prompt = packet.render() + "\n\nOutput only the review report body in Markdown."
        body, _tokens, _tripped = runner("reviewer", "research-review", prompt, AUTO_BUDGET)
        body = (body.strip() or _scaffold_report_body(root, topic, candidate)) + "\n"
    else:
        body = _scaffold_report_body(root, topic, candidate)

    out_dir = review_report_dir(root)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    out_path = out_dir / f"research-review-{slugify(topic)}-{stamp}.md"
    from labctl.ingest import sha256_hex

    captured = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_path.write_text(
        _derived_frontmatter(
            sha256_hex(body.encode("utf-8")),
            captured,
            source=str(candidate) if candidate else f"research:{slugify(topic)}",
            namespace=REVIEW_NAMESPACE,
            promoted=False,
        )
        + body,
        encoding="utf-8",
    )
    return ReviewResult(out_path, auto, packet)
