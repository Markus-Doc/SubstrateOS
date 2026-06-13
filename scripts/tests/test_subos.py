"""Tests for M-C: engine adapters, spec compiler, and the subos launcher."""

from __future__ import annotations

from pathlib import Path

import pytest

from labctl.compile_spec import MANAGED_MARKER, compile_to, is_managed, render
from labctl.engines import get_adapter
from labctl.subos import build_plan, main

SPEC = "# SubstrateOS Methodology\n\nMUST go through labctl.\n"


def _write_spec(tmp: Path) -> Path:
    p = tmp / "methodology.md"
    p.write_text(SPEC, encoding="utf-8")
    return p


# --- engines ---

def test_get_adapter_known_and_unknown():
    assert get_adapter("claude").instruction_file == "CLAUDE.md"
    assert get_adapter("codex").instruction_file == "AGENTS.md"
    with pytest.raises(KeyError):
        get_adapter("nope")


# --- compiler ---

def test_render_carries_marker_and_body():
    out = render(SPEC, get_adapter("claude"))
    assert MANAGED_MARKER in out
    assert "engine: claude" in out
    assert SPEC.strip() in out


def test_compile_writes_instruction_file(tmp_path: Path):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    written = compile_to(spec, get_adapter("codex"), target)
    assert written == target / "AGENTS.md"
    assert MANAGED_MARKER in written.read_text(encoding="utf-8")


def test_compile_refuses_unmanaged_then_force(tmp_path: Path):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    (target).mkdir()
    handwritten = target / "CLAUDE.md"
    handwritten.write_text("# my hand-authored file\n", encoding="utf-8")
    assert not is_managed(handwritten)
    with pytest.raises(FileExistsError):
        compile_to(spec, get_adapter("claude"), target)
    # force overwrites and the result is now managed
    compile_to(spec, get_adapter("claude"), target, force=True)
    assert is_managed(handwritten)


def test_compile_overwrites_managed_without_force(tmp_path: Path):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    compile_to(spec, get_adapter("claude"), target)  # creates managed
    # second compile succeeds without force because the file is managed
    compile_to(spec, get_adapter("claude"), target)


# --- launcher plan ---

def test_build_plan_posture_flags():
    plan_default = build_plan("claude", target_dir=Path("/p"), posture="platform-default")
    assert plan_default.argv == ["claude"]
    plan_full = build_plan("claude", target_dir=Path("/p"), posture="full-auto")
    assert plan_full.argv == ["claude", "--dangerously-skip-permissions"]
    plan_codex = build_plan("codex", target_dir=Path("/p"), posture="full-auto")
    assert plan_codex.argv == ["codex", "--dangerously-bypass-approvals-and-sandbox"]


def test_main_dry_run_compiles_and_reports(tmp_path: Path, capsys):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    rc = main(
        ["claude", "--target", str(target), "--full-auto", "--spec", str(spec), "--dry-run"]
    )
    assert rc == 0
    assert (target / "CLAUDE.md").is_file()
    out = capsys.readouterr().out
    assert "dry run" in out
    assert "--dangerously-skip-permissions" in out


def test_main_unknown_engine_errors(tmp_path: Path):
    spec = _write_spec(tmp_path)
    rc = main(["bogus", "--target", str(tmp_path), "--spec", str(spec), "--dry-run"])
    assert rc == 2
