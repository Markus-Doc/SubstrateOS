"""Status dashboard: the Phase 1 success metric (OQ-006).

CLI-rendered from local repo files only — manifest, decision records, open
questions, ingest log, and doctor checks. No web UI, no model involvement.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from labctl import doctor as doctor_mod
from labctl.config import Manifest, load_manifest
from labctl.ingest import last_ingest_record

DECISIONS_DIR_REL = "docs/decisions"
OPEN_QUESTIONS_REL = "docs/planning/open-questions.md"


@dataclass
class Decision:
    file: str
    title: str
    status: str


@dataclass
class OpenQuestion:
    qid: str
    title: str
    closed: bool


@dataclass
class StatusReport:
    manifest: Manifest | None
    source_of_truth: str
    source_of_truth_exists: bool
    decisions: list[Decision] = field(default_factory=list)
    open_questions: list[OpenQuestion] = field(default_factory=list)
    providers: dict[str, str] = field(default_factory=dict)
    missing_config: list[str] = field(default_factory=list)
    last_ingest: dict | None = None
    env_warnings: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)


def parse_decisions(root: Path) -> list[Decision]:
    decisions: list[Decision] = []
    decisions_dir = root / DECISIONS_DIR_REL
    if not decisions_dir.is_dir():
        return decisions
    for path in sorted(decisions_dir.glob("*.md")):
        title, status = path.stem, "unknown"
        lines = path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if line.startswith("# ") and title == path.stem:
                title = line[2:].strip()
            if match := re.match(r"^Status:\s*(.+)$", line):
                status = match.group(1).strip()
            elif line.strip() == "## Status" and i + 2 < len(lines):
                status = lines[i + 2].strip() or status
        decisions.append(Decision(file=path.name, title=title, status=status))
    return decisions


def parse_open_questions(root: Path) -> list[OpenQuestion]:
    questions: list[OpenQuestion] = []
    path = root / OPEN_QUESTIONS_REL
    if not path.exists():
        return questions
    current: OpenQuestion | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if match := re.match(r"^##\s+(OQ-\d+):\s*(.+)$", line):
            current = OpenQuestion(qid=match.group(1), title=match.group(2).strip(), closed=False)
            questions.append(current)
        elif current and re.match(r"^Status:\s*CLOSED", line, re.IGNORECASE):
            current.closed = True
    return questions


def build_report(root: Path) -> StatusReport:
    manifest = load_manifest(root)
    sot = manifest.source_of_truth if manifest else "unknown (no manifest)"
    report = StatusReport(
        manifest=manifest,
        source_of_truth=sot,
        source_of_truth_exists=(root / sot).exists() if manifest else False,
        decisions=parse_decisions(root),
        open_questions=parse_open_questions(root),
        providers=dict(manifest.providers) if manifest else {},
        last_ingest=last_ingest_record(root),
    )

    if manifest is None:
        report.missing_config.append("agentbrain.json (run `labctl init`)")
    report.missing_config.extend(
        f"provider '{name}': {value}"
        for name, value in report.providers.items()
        if "unconfigured" in value
    )

    checks = doctor_mod.run_checks(root)
    report.env_warnings = [
        f"{r.name}: {r.detail}" for r in checks if not r.ok
    ]

    if manifest is None:
        report.next_actions.append("run `labctl init`")
    if not report.source_of_truth_exists:
        report.next_actions.append(f"add source-of-truth document {sot}")
    open_qs = [q for q in report.open_questions if not q.closed]
    if open_qs:
        report.next_actions.append(
            f"resolve open questions: {', '.join(q.qid for q in open_qs)}"
        )
    if report.last_ingest is None:
        report.next_actions.append("run `labctl ingest <source>` for the first time")
    if doctor_mod.has_errors(checks):
        report.next_actions.append("fix doctor errors (`labctl doctor`)")
    if not report.next_actions:
        report.next_actions.append("all green - proceed with phase plan")

    return report


def render(report: StatusReport) -> str:
    lines: list[str] = []
    name = report.manifest.project if report.manifest else "unknown"
    phase = report.manifest.phase if report.manifest else "?"
    lines.append("=" * 60)
    # ASCII-only output: Windows consoles default to legacy codepages.
    lines.append(f" {name} - phase {phase}")
    lines.append("=" * 60)

    sot_mark = "present" if report.source_of_truth_exists else "MISSING"
    lines.append(f"source of truth : {report.source_of_truth} [{sot_mark}]")

    lines.append(f"\nconfirmed decisions ({len(report.decisions)}):")
    for d in report.decisions:
        lines.append(f"  [{d.status:<8}] {d.title}")

    closed = sum(q.closed for q in report.open_questions)
    lines.append(f"\nopen questions ({closed}/{len(report.open_questions)} closed):")
    for q in report.open_questions:
        lines.append(f"  [{'closed' if q.closed else 'OPEN  '}] {q.qid}: {q.title}")

    lines.append("\nproviders:")
    for key, value in report.providers.items():
        lines.append(f"  {key:<12}: {value}")

    lines.append("\nmissing configuration:")
    if report.missing_config:
        lines.extend(f"  - {item}" for item in report.missing_config)
    else:
        lines.append("  none")

    lines.append("\nlast ingestion run:")
    if report.last_ingest:
        li = report.last_ingest
        lines.append(
            f"  {li['captured_utc']}  {li['output']}  "
            f"(chunks: {li['chunks_stored']}, sha256: {li['sha256'][:12]}...)"
        )
    else:
        lines.append("  never")

    lines.append("\nenvironment warnings:")
    if report.env_warnings:
        lines.extend(f"  - {w}" for w in report.env_warnings)
    else:
        lines.append("  none")

    lines.append("\nnext recommended actions:")
    lines.extend(f"  -> {a}" for a in report.next_actions)
    return "\n".join(lines)
