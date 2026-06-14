"""Tests for M-C: engine adapters, spec compiler, and the subos launcher."""

from __future__ import annotations

from pathlib import Path

import pytest

from labctl import subos
from labctl.compile_spec import MANAGED_MARKER, compile_to, is_managed, render
from labctl.engines import get_adapter
from labctl.subos import build_plan, main

SPEC = "# SubstrateOS Methodology\n\nMUST go through labctl.\n"


def _raise_no_repo(*_args, **_kwargs):
    raise FileNotFoundError("no repo root (simulated)")


def _posture_line(out: str) -> str:
    return next(line for line in out.splitlines() if line.startswith("posture"))


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


def test_render_stamps_operating_version():
    from labctl import __version__

    out = render(SPEC, get_adapter("claude"))
    assert f"SubstrateOS version: {__version__}" in out


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
    from labctl import __version__

    assert __version__ in out


def test_main_unknown_engine_errors(tmp_path: Path):
    spec = _write_spec(tmp_path)
    rc = main(["bogus", "--target", str(tmp_path), "--spec", str(spec), "--dry-run"])
    assert rc == 2


def test_main_version_flag(capsys):
    from labctl import __version__

    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


# --- spec-as-package-data fallback (ADR-026) ---

def test_dry_run_without_spec_uses_packaged(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    # Outside any repo, the resolver falls back to the bundled package-data spec.
    monkeypatch.setattr(subos, "find_repo_root", _raise_no_repo)
    target = tmp_path / "proj"
    rc = main(["claude", "--target", str(target), "--dry-run"])
    assert rc == 0
    # CLAUDE.md is only written if the packaged spec was found and compiled.
    compiled = (target / "CLAUDE.md").read_text(encoding="utf-8")
    assert "SubstrateOS" in compiled


def test_packaged_spec_path_resolves():
    spec = subos._packaged_spec_path()
    assert spec is not None
    assert spec.is_file()
    assert spec.name == "methodology.md"


# --- full-auto env posture hook (ADR-026 §6) ---

def test_full_auto_env_default(tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    monkeypatch.setenv("SUBSTRATEOS_FULL_AUTO", "1")
    rc = main(["claude", "--target", str(target), "--spec", str(spec), "--dry-run"])
    assert rc == 0
    assert _posture_line(capsys.readouterr().out).endswith("full-auto")


def test_platform_default_overrides_env(tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    monkeypatch.setenv("SUBSTRATEOS_FULL_AUTO", "1")
    rc = main(
        ["claude", "--target", str(target), "--spec", str(spec),
         "--platform-default", "--dry-run"]
    )
    assert rc == 0
    assert _posture_line(capsys.readouterr().out).endswith("platform-default")


def test_env_unset_is_platform_default(tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    monkeypatch.delenv("SUBSTRATEOS_FULL_AUTO", raising=False)
    rc = main(["claude", "--target", str(target), "--spec", str(spec), "--dry-run"])
    assert rc == 0
    assert _posture_line(capsys.readouterr().out).endswith("platform-default")


# --- boot reflects workspace init state (ADR-029) ---

def test_dry_run_reports_uninitialized_workspace(tmp_path: Path, capsys):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    rc = main(["claude", "--target", str(target), "--spec", str(spec), "--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out
    ws = next(line for line in out.splitlines() if line.startswith("workspace"))
    assert "NOT initialized" in ws
    assert "labctl init" in ws


def test_dry_run_reports_initialized_workspace(tmp_path: Path, capsys):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    target.mkdir()
    (target / "substrateos.json").write_text(
        '{"project": "Demo"}', encoding="utf-8"
    )
    rc = main(["claude", "--target", str(target), "--spec", str(spec), "--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out
    ws = next(line for line in out.splitlines() if line.startswith("workspace"))
    assert "initialized" in ws
    assert "Demo" in ws
    assert "NOT initialized" not in ws


def test_init_flag_initializes_before_launch(tmp_path: Path, capsys):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    rc = main(
        ["claude", "--target", str(target), "--spec", str(spec), "--init", "--dry-run"]
    )
    assert rc == 0
    assert (target / "substrateos.json").is_file()
    out = capsys.readouterr().out
    assert "init:" in out  # init actions were reported
    ws = next(line for line in out.splitlines() if line.startswith("workspace"))
    assert "initialized" in ws and "NOT initialized" not in ws


# --- launch resolution (Windows npm shim: claude.CMD, not claude.exe) ---

def test_launch_uses_resolved_binary_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    captured: dict = {}
    monkeypatch.setattr(subos.shutil, "which", lambda name: "C:/tools/claude.CMD")

    class _Result:
        returncode = 0

    def fake_run(argv, cwd=None):
        captured["argv"] = list(argv)
        return _Result()

    monkeypatch.setattr(subos.subprocess, "run", fake_run)
    rc = main(["claude", "--target", str(target), "--spec", str(spec)])
    assert rc == 0
    # the resolved path must be launched, never the bare name
    assert captured["argv"][0] == "C:/tools/claude.CMD"


def test_launch_engine_not_on_path_returns_127(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    spec = _write_spec(tmp_path)
    target = tmp_path / "proj"
    monkeypatch.setattr(subos.shutil, "which", lambda name: None)
    rc = main(["claude", "--target", str(target), "--spec", str(spec)])
    assert rc == 127
