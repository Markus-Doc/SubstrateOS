"""Tests for M-D: capability handshake + /substrateos warm-activation compile."""

from __future__ import annotations

from pathlib import Path

import pytest

from labctl.compile_spec import MANAGED_MARKER, compile_warm_command
from labctl.engines import get_adapter
from labctl.handshake import MUST, build_handshake, render_handshake


def test_claude_all_native_no_gaps():
    hs = build_handshake(get_adapter("claude"))
    assert hs.gaps == []
    assert all(status == "native" for (_f, status, _c) in hs.should)
    assert hs.must == list(MUST)


def test_gemini_reports_gaps():
    hs = build_handshake(get_adapter("gemini"))
    # gemini declares only mcp -> the other SHOULD features degrade
    assert "in-session activation (/substrateos)" in hs.gaps
    assert "sub-agent orchestration" in hs.gaps


def test_render_warm_mode_surfaces_relaunch_caveat():
    hs = build_handshake(get_adapter("codex"))
    text = render_handshake(hs, mode="warm")
    assert "warm mode" in text
    assert "relaunch via `subos`" in text


def test_warm_command_compiles_for_claude(tmp_path: Path):
    out = compile_warm_command(get_adapter("claude"), tmp_path)
    assert out == tmp_path / ".claude/commands/substrateos.md"
    body = out.read_text(encoding="utf-8")
    assert MANAGED_MARKER in body
    assert "/substrateos" in body
    assert "never bypass the release gate" in body


def test_warm_command_none_for_engine_without_slot(tmp_path: Path):
    assert compile_warm_command(get_adapter("gemini"), tmp_path) is None


def test_warm_command_refuses_unmanaged(tmp_path: Path):
    target = tmp_path
    cmd = target / ".codex/prompts/substrateos.md"
    cmd.parent.mkdir(parents=True)
    cmd.write_text("# hand-authored prompt\n", encoding="utf-8")
    with pytest.raises(FileExistsError):
        compile_warm_command(get_adapter("codex"), target)
