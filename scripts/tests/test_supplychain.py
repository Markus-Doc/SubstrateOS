"""Tests for M-F: supply-chain audit gate stage (ADR-024)."""

from __future__ import annotations

import json
from pathlib import Path

from labctl.gate import run_supplychain
from labctl.supplychain import audit


def _skill(root: Path, name: str) -> None:
    d = root / ".claude/skills" / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")


def _allowlist(root: Path, names: list[str]) -> None:
    (root / "substrate").mkdir(parents=True, exist_ok=True)
    (root / "substrate/trusted-tools.json").write_text(
        json.dumps({"trusted": names}), encoding="utf-8"
    )


def test_clean_when_no_third_party_tools(tmp_path: Path):
    result = audit(tmp_path)
    assert result.ok
    assert result.scanned == 0


def test_unvetted_skill_is_flagged(tmp_path: Path):
    _skill(tmp_path, "scraper")
    result = audit(tmp_path)
    assert not result.ok
    assert any("scraper" in f for f in result.findings)
    assert result.scanned == 1


def test_allowlisted_skill_passes(tmp_path: Path):
    _skill(tmp_path, "scraper")
    _allowlist(tmp_path, ["scraper"])
    result = audit(tmp_path)
    assert result.ok


def test_unvetted_mcp_server_is_flagged(tmp_path: Path):
    (tmp_path / ".mcp.json").write_text(
        json.dumps({"mcpServers": {"sketchy": {"command": "x"}}}), encoding="utf-8"
    )
    result = audit(tmp_path)
    assert not result.ok
    assert any("sketchy" in f for f in result.findings)


def test_gate_stage_passes_on_blank_base(tmp_path: Path):
    stage = run_supplychain(tmp_path)
    assert stage.passed
    assert stage.name == "supply-chain"


def test_gate_stage_fails_with_unvetted(tmp_path: Path):
    _skill(tmp_path, "rogue")
    stage = run_supplychain(tmp_path)
    assert not stage.passed
    assert "rogue" in stage.detail
