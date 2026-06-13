"""Tests for M5: codebase audit Dynamic Workflow + structured handoff packets."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from labctl.audit import build_audit_packet, run_audit
from labctl.cli import app


def _runner(role, name, prompt, budget):
    if role == "architect":
        return ("plan: review modules", 100, False)
    if role == "judge":
        return ("ACCEPT findings verified", 30, False)
    return (f"{name}: finding noted", 50, False)


def _ground(query: str) -> list[str]:
    return [f"chunk relevant to: {query}"]


def test_handoff_packet_render_is_complete():
    packet = build_audit_packet("myrepo", ["a known risk"])
    text = packet.render()
    assert "Repo: myrepo" in text
    assert "Objective:" in text
    assert "Out of scope:" in text
    assert "Verification commands:" in text
    assert "Stop conditions:" in text
    assert "a known risk" in text  # grounding flows in


def test_audit_objective_is_engineering_not_pentest():
    packet = build_audit_packet("r", [])
    assert "not a penetration test" in packet.objective.lower()
    assert any("Penetration testing" in s for s in packet.out_of_scope)


def test_run_audit_writes_report_and_accepts(tmp_path: Path):
    report = tmp_path / "evidence" / "audit-r.md"
    result = run_audit(
        tmp_path / "myrepo",
        runner=_runner,
        ground=_ground,
        n_workers=2,
        log_dir=tmp_path / "logs",
        report_path=report,
    )
    assert result.accepted
    assert report.is_file()
    body = report.read_text(encoding="utf-8")
    assert "audit report" in body.lower()
    assert "architect" in body and "judge" in body


def test_run_audit_grounding_flows_into_packet(tmp_path: Path):
    captured: dict[str, str] = {}

    def runner(role, name, prompt, budget):
        if role == "architect":
            captured["architect_prompt"] = prompt
        return ("ACCEPT" if role == "judge" else "ok", 10, False)

    run_audit(tmp_path / "r", runner=runner, ground=lambda q: ["GROUND-XYZ"], n_workers=1)
    assert "GROUND-XYZ" in captured["architect_prompt"]


def test_cli_audit_dry_run_shows_packet():
    result = CliRunner().invoke(app, ["audit", ".", "--dry-run", "--workers", "2"])
    assert result.exit_code == 0
    assert "Handoff packet" in result.stdout
    assert "architect ->" in result.stdout
