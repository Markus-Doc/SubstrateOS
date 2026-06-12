from pathlib import Path

import pytest
from typer.testing import CliRunner

from labctl.cli import MEMORY_DB_REL, app
from labctl.memory import SQLiteMemory

runner = CliRunner()


@pytest.fixture
def in_repo(repo: Path, monkeypatch):
    monkeypatch.chdir(repo)
    runner.invoke(app, ["init"])
    return repo


def test_ingest_end_to_end(in_repo: Path):
    src = in_repo / "note.md"
    src.write_text("# Quantum harness\n\nOrchestration notes about capsules.\n", encoding="utf-8")

    result = runner.invoke(app, ["ingest", str(src), "--namespace", "cli-test"])
    assert result.exit_code == 0, result.output
    assert "ingested" in result.output
    assert "chunks indexed: 1" in result.output

    with SQLiteMemory(in_repo / MEMORY_DB_REL) as memory:
        hits = memory.search_keyword("cli-test", "capsules orchestration")
        assert hits
        assert "capsules" in hits[0].content
        assert not memory.search_keyword("other-ns", "capsules")


def test_reingest_reports_unchanged(in_repo: Path):
    src = in_repo / "note.md"
    src.write_text("# Same\n\ncontent\n", encoding="utf-8")
    runner.invoke(app, ["ingest", str(src), "--namespace", "cli-test"])
    result = runner.invoke(app, ["ingest", str(src), "--namespace", "cli-test"])
    assert result.exit_code == 0
    assert "unchanged" in result.output


def test_ingest_url_without_key_is_actionable_error(in_repo: Path, monkeypatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    result = runner.invoke(app, ["ingest", "https://example.com", "--namespace", "cli-test"])
    assert result.exit_code == 1
    assert "FIRECRAWL_API_KEY" in result.output
    assert "Traceback" not in result.output


def test_ingest_missing_file_is_error(in_repo: Path):
    result = runner.invoke(app, ["ingest", str(in_repo / "nope.md")])
    assert result.exit_code == 1
    assert "error:" in result.output


def test_review_flow_end_to_end(in_repo: Path, monkeypatch):
    monkeypatch.setattr(
        "labctl.review.run_claude_summary",
        lambda body: "# Summary\n\nDerived capsule summary text.\n",
    )
    src = in_repo / "note.md"
    src.write_text("# Quantum harness\n\nOrchestration notes about capsules.\n", encoding="utf-8")
    runner.invoke(app, ["ingest", str(src), "--namespace", "cli-test"])
    # Relative paths exercise the resolve() in the review commands.
    ingested = Path("artifacts/ingest/cli-test/note.md")

    assert "empty" in runner.invoke(app, ["review", "list"]).output

    result = runner.invoke(app, ["review", "generate", str(ingested)])
    assert result.exit_code == 0, result.output
    derived = Path("artifacts/ingest/cli-test/derived/note-summary.md")
    assert (in_repo / derived).is_file()
    assert "PENDING" in runner.invoke(app, ["review", "list"]).output

    # Unpromoted derived content must not be searchable.
    with SQLiteMemory(in_repo / MEMORY_DB_REL) as memory:
        assert not memory.search_keyword("cli-test", "Derived summary")

    result = runner.invoke(app, ["review", "approve", str(derived)])
    assert result.exit_code == 0, result.output
    assert "promoted" in result.output
    with SQLiteMemory(in_repo / MEMORY_DB_REL) as memory:
        assert memory.search_keyword("cli-test", "Derived summary")
    assert "promoted" in runner.invoke(app, ["review", "list"]).output
