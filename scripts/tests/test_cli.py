from pathlib import Path

import pytest
from typer.testing import CliRunner

from labctl.cli import app

runner = CliRunner()


@pytest.fixture
def in_repo(repo: Path, monkeypatch):
    monkeypatch.chdir(repo)
    return repo


def test_init_then_doctor(in_repo: Path):
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "SubstrateOS" in result.output

    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "sqlite-fts5" in result.output


def test_doctor_fails_on_broken_repo(in_repo: Path):
    # no init: required dirs missing -> error severity -> exit 1
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 1
