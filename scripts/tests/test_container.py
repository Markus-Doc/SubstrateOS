"""Tests for M4: in-container capsule execution plumbing (ADR-025)."""

from __future__ import annotations

import json
from pathlib import Path

from labctl import capsule as capsule_mod
from labctl.capsule import (
    OAUTH_TOKEN_ENV,
    build_docker_argv,
    run_container_build,
    scaffold_capsule,
)


def test_docker_argv_mounts_and_token_by_name_only():
    argv = build_docker_argv(
        Path("/work/myproj"), Path("/ns/myproj"), "substrateos-capsule:latest", "cn-1"
    )
    assert argv[:4] == ["docker", "run", "--rm", "-i"]
    assert "--name" in argv and "cn-1" in argv
    assert "-w" in argv and "/workspace" in argv
    assert any(a.endswith(":/workspace") for a in argv)
    assert any(a.endswith(":/memory") for a in argv)
    # token passed by NAME only — the value must never be in argv
    assert "-e" in argv
    assert OAUTH_TOKEN_ENV in argv
    assert not any("=" in a and OAUTH_TOKEN_ENV in a for a in argv)
    assert "claude" in argv and "--dangerously-skip-permissions" in argv


class _FakeStdin:
    def write(self, _s): ...
    def close(self): ...


class _FakeProc:
    """Streams stream-json lines; the last event blows the token budget."""

    def __init__(self):
        big = {"type": "assistant", "message": {"usage": {"output_tokens": 10_000_000}}}
        self.stdout = [json.dumps(big) + "\n"]
        self.stdin = _FakeStdin()
        self.pid = 4321

    def wait(self):
        return 0


def test_container_build_breaker_kills_container(tmp_path: Path):
    # scaffold a real capsule so load_capsule_manifest works
    root = tmp_path / "SubstrateOS"
    (root / ".git").mkdir(parents=True)
    (root / "templates/capsule-devcontainer").mkdir(parents=True)
    for name in ("Dockerfile", "devcontainer.json"):
        (root / "templates/capsule-devcontainer" / name).write_text("x\n", encoding="utf-8")
    scaffold_capsule(root, "proj", mission="do a thing", token_budget=1000)

    killed: list[str] = []

    def fake_spawn(_mission, _cwd):
        return _FakeProc()

    def fake_kill(_proc):
        killed.append("killed")

    result = run_container_build(
        root, "proj", token="tok-abc", spawn=fake_spawn, kill=fake_kill
    )
    assert result.breaker_tripped
    assert killed == ["killed"]  # breaker used the container kill, not the host tree


def test_oauth_env_constant():
    assert capsule_mod.OAUTH_TOKEN_ENV == "CLAUDE_CODE_OAUTH_TOKEN"
