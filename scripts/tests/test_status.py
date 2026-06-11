from pathlib import Path

from typer.testing import CliRunner

from labctl.cli import app
from labctl.config import init_project
from labctl.ingest import ingest_file
from labctl.status import build_report, parse_decisions, parse_open_questions, render

runner = CliRunner()

ADR_INLINE_STATUS = """# ADR-101: Test decision inline

Date: 2026-06
Status: Accepted

## Decision

Something.
"""

ADR_SECTION_STATUS = """# ADR-102: Test decision sectioned

## Status

Accepted

## Context

Words.
"""

OPEN_QUESTIONS = """# Open Questions

## OQ-001: First question

Status: CLOSED
Resolved: yes.

## OQ-002: Second question

Status: OPEN
"""


def make_fixture_repo(repo: Path) -> Path:
    init_project(repo)
    (repo / "docs/decisions/ADR-101-inline.md").write_text(ADR_INLINE_STATUS, encoding="utf-8")
    (repo / "docs/decisions/ADR-102-section.md").write_text(ADR_SECTION_STATUS, encoding="utf-8")
    (repo / "docs/planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs/planning/open-questions.md").write_text(OPEN_QUESTIONS, encoding="utf-8")
    (repo / "MASTER_AI_System_Research.md").write_text("# Master\n", encoding="utf-8")
    return repo


def test_parse_decisions_both_status_formats(repo: Path):
    make_fixture_repo(repo)
    decisions = parse_decisions(repo)
    by_title = {d.title: d.status for d in decisions}
    assert by_title["ADR-101: Test decision inline"] == "Accepted"
    assert by_title["ADR-102: Test decision sectioned"] == "Accepted"


def test_parse_open_questions(repo: Path):
    make_fixture_repo(repo)
    questions = parse_open_questions(repo)
    assert [q.qid for q in questions] == ["OQ-001", "OQ-002"]
    assert questions[0].closed and not questions[1].closed


def test_report_covers_all_oq006_fields(repo: Path):
    make_fixture_repo(repo)
    ingest_file(repo, repo / "MASTER_AI_System_Research.md", "test-ns")
    report = build_report(repo)

    assert report.manifest is not None and report.manifest.project == "Agent Brain"
    assert report.source_of_truth_exists
    assert len(report.decisions) == 2
    assert len(report.open_questions) == 2
    assert "memory" in report.providers
    assert any("unconfigured" in m for m in report.missing_config)  # firecrawl optional
    assert report.last_ingest is not None
    assert isinstance(report.env_warnings, list)
    assert any("OQ-002" in a for a in report.next_actions)  # open question surfaced


def test_render_contains_every_dashboard_section(repo: Path):
    make_fixture_repo(repo)
    output = render(build_report(repo))
    for fragment in (
        "Agent Brain - phase 1",
        "source of truth",
        "confirmed decisions",
        "open questions (1/2 closed)",
        "providers:",
        "missing configuration:",
        "last ingestion run:",
        "environment warnings:",
        "next recommended actions:",
    ):
        assert fragment in output, f"missing: {fragment}"


def test_status_cli_smoke(repo: Path, monkeypatch):
    make_fixture_repo(repo)
    monkeypatch.chdir(repo)
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "next recommended actions" in result.output
