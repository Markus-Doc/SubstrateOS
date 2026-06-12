import json
import subprocess
from pathlib import Path

import pytest

from labctl.capsule import (
    DEFAULT_TOKEN_BUDGET,
    load_capsule_manifest,
    monitor_stream,
    run_build,
    scaffold_capsule,
)

TEMPLATE_JSON = (
    '{"mounts": ["source=__MEMORY_NAMESPACE_DIR__,target=/memory,type=bind"],\n'
    ' "containerEnv": {"CAPSULE_NAMESPACE": "__CAPSULE_NAMESPACE__"}}\n'
)


@pytest.fixture
def lab(repo: Path) -> Path:
    """Repo fixture with the capsule template present."""
    template_dir = repo / "templates" / "capsule-devcontainer"
    template_dir.mkdir(parents=True)
    (template_dir / "devcontainer.json").write_text(TEMPLATE_JSON, encoding="utf-8")
    (template_dir / "Dockerfile").write_text("FROM python:3.11-slim\n", encoding="utf-8")
    return repo


def usage_line(tokens: int) -> str:
    return json.dumps(
        {"type": "assistant", "message": {"usage": {"input_tokens": tokens, "output_tokens": 0}}}
    )


class FakeProc:
    """Stand-in for a claude subprocess: stdout iterable, kill/wait tracked."""

    def __init__(self, lines: list[str]):
        self.stdout = iter(lines)
        self.killed = False
        self.returncode = 0

    def kill(self):
        self.killed = True

    def wait(self):
        return self.returncode


def test_scaffold_substitutes_tokens_and_inits_git(lab: Path, tmp_path: Path):
    dest = tmp_path / "siblings"
    capsule_dir = scaffold_capsule(
        lab, "demo-capsule", mission="Build a thing.", dest_parent=dest
    )
    assert capsule_dir == dest / "demo-capsule"

    devcontainer = (capsule_dir / ".devcontainer" / "devcontainer.json").read_text(
        encoding="utf-8"
    )
    assert "__MEMORY_NAMESPACE_DIR__" not in devcontainer
    assert "__CAPSULE_NAMESPACE__" not in devcontainer
    assert "demo-capsule" in devcontainer
    namespace_dir = lab / "artifacts" / "memory-namespaces" / "demo-capsule"
    assert namespace_dir.is_dir()
    assert namespace_dir.resolve().as_posix() in devcontainer

    assert "MIT License" in (capsule_dir / "LICENSE").read_text(encoding="utf-8")
    assert "M. Walker" in (capsule_dir / "LICENSE").read_text(encoding="utf-8")
    assert "Build a thing." in (capsule_dir / "CLAUDE.md").read_text(encoding="utf-8")

    manifest = load_capsule_manifest(capsule_dir)
    assert manifest["namespace"] == "demo-capsule"
    assert manifest["token_budget"] == DEFAULT_TOKEN_BUDGET

    author = subprocess.run(
        ["git", "-C", str(capsule_dir), "log", "-1", "--format=%an <%ae>"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert author == "M. Walker <178984035+Markus-Doc@users.noreply.github.com>"


def test_scaffold_rejects_existing_dir_and_bad_names(lab: Path, tmp_path: Path):
    dest = tmp_path / "siblings"
    scaffold_capsule(lab, "demo", dest_parent=dest)
    with pytest.raises(FileExistsError):
        scaffold_capsule(lab, "demo", dest_parent=dest)
    with pytest.raises(ValueError):
        scaffold_capsule(lab, "bad name!", dest_parent=dest)


def test_monitor_stream_accumulates_and_trips():
    lines = [usage_line(400), "not json", usage_line(400), usage_line(400)]
    logged: list[str] = []
    tokens, tripped = monitor_stream(lines, token_budget=1000, log_line=logged.append)
    assert tripped
    assert tokens == 1200
    assert len(logged) == 4  # every line logged, iteration stops at the tripping line

    tokens, tripped = monitor_stream(
        [usage_line(100)], token_budget=1000, log_line=logged.append
    )
    assert not tripped
    assert tokens == 100


def test_run_build_trips_breaker_and_kills(lab: Path, tmp_path: Path):
    dest = tmp_path / "siblings"
    scaffold_capsule(lab, "demo", mission="m", token_budget=500, dest_parent=dest)
    proc = FakeProc([usage_line(300), usage_line(300), usage_line(300)])

    result = run_build(lab, "demo", dest_parent=dest, spawn=lambda m, cwd: proc)
    assert result.breaker_tripped
    assert proc.killed
    assert result.exit_code == 1
    assert result.tokens_used == 600
    log = result.run_log.read_text(encoding="utf-8")
    assert "circuit-breaker" in log
    assert "token budget exceeded" in log


def test_run_build_completes_within_budget(lab: Path, tmp_path: Path):
    dest = tmp_path / "siblings"
    scaffold_capsule(lab, "demo", mission="m", dest_parent=dest)
    proc = FakeProc([usage_line(100), json.dumps({"type": "result"})])

    result = run_build(lab, "demo", dest_parent=dest, spawn=lambda m, cwd: proc)
    assert not result.breaker_tripped
    assert not proc.killed
    assert result.exit_code == 0
    assert result.tokens_used == 100
    assert result.token_budget == DEFAULT_TOKEN_BUDGET


def test_run_build_budget_override_beats_manifest(lab: Path, tmp_path: Path):
    dest = tmp_path / "siblings"
    scaffold_capsule(lab, "demo", token_budget=10_000, dest_parent=dest)
    proc = FakeProc([usage_line(150)])

    result = run_build(
        lab, "demo", token_budget=100, dest_parent=dest, spawn=lambda m, cwd: proc
    )
    assert result.breaker_tripped
    assert result.token_budget == 100


def test_run_build_requires_capsule_manifest(lab: Path, tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        run_build(lab, "ghost", dest_parent=tmp_path, spawn=lambda m, cwd: FakeProc([]))
