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
