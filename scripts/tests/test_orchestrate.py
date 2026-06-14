"""Tests for M-E: multi-agent / sub-agent orchestration (Dynamic Workflows)."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from labctl.cli import app
from labctl.orchestrate import _extract_text, run_workflow


def _runner(role, name, prompt, budget):
    """Default fake runner: architect plans, judge accepts."""
    if role == "architect":
        return ("1. step one\n2. step two", 100, False)
    if role == "judge":
        return ("ACCEPT looks good", 30, False)
    return (f"{name} output", 50, False)


def test_full_workflow_accept(tmp_path: Path):
    res = run_workflow("build a thing", runner=_runner, n_workers=2, log_dir=tmp_path)
    assert res.accepted
    assert res.verdict.upper().startswith("ACCEPT")
    # architect + 2 workers + reviewer + judge
    assert [s.name for s in res.stages] == [
        "architect", "worker-1", "worker-2", "reviewer", "judge",
    ]
    assert res.metrics["task_completion"] == 1.0
    assert res.run_log is not None and res.run_log.exists()
    lines = res.run_log.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1 + 5 + 1  # mission + stages + verdict


def test_judge_reject_not_accepted(tmp_path: Path):
    def runner(role, name, prompt, budget):
        if role == "judge":
            return ("REJECT missing tests", 10, False)
        return ("ok", 10, False)

    res = run_workflow("m", runner=runner, n_workers=1, log_dir=tmp_path)
    assert not res.accepted
    assert res.verdict.upper().startswith("REJECT")


def test_verdict_accepts_robust_to_preamble():
    from labctl.orchestrate import _verdict_accepts

    # verdict after a verification preamble (the real-world failure case)
    assert _verdict_accepts("Let me verify.\nGate is green.\nACCEPT - all good")
    assert not _verdict_accepts("Checking the diff...\nREJECT: tests missing")
    # markdown / labelled verdicts
    assert _verdict_accepts("**ACCEPT**")
    assert _verdict_accepts("Verdict: ACCEPT")
    # mere mentions mid-sentence are NOT a verdict; no explicit token => not accepted
    assert not _verdict_accepts("I will ACCEPT or REJECT once I have verified.")
    assert not _verdict_accepts("Everything passed and looks correct.")


def test_workflow_accepts_judge_with_preamble(tmp_path: Path):
    def runner(role, name, prompt, budget):
        if role == "judge":
            return ("I verified the gate is green.\nACCEPT", 10, False)
        return ("ok", 10, False)

    res = run_workflow("m", runner=runner, n_workers=1, log_dir=tmp_path)
    assert res.accepted


def test_architect_breaker_aborts_early(tmp_path: Path):
    def runner(role, name, prompt, budget):
        if role == "architect":
            return ("", budget + 1, True)
        return ("ok", 10, False)

    res = run_workflow("m", runner=runner, n_workers=3, log_dir=tmp_path)
    assert not res.accepted
    assert "aborted" in res.verdict
    assert len(res.stages) == 1  # stopped after the architect tripped


def test_handoff_packets_flow(tmp_path: Path):
    seen: dict[str, str] = {}

    def runner(role, name, prompt, budget):
        seen[name] = prompt
        if role == "architect":
            return ("PLAN-XYZ", 10, False)
        if role == "judge":
            return ("ACCEPT", 10, False)
        return ("worker-out", 10, False)

    run_workflow("MISSION-ABC", runner=runner, n_workers=1, log_dir=tmp_path)
    assert "MISSION-ABC" in seen["architect"]
    assert "PLAN-XYZ" in seen["worker-1"]  # architect plan handed to worker


def test_metrics_budget_utilisation(tmp_path: Path):
    def runner(role, name, prompt, budget):
        return ("ACCEPT" if role == "judge" else "x", 100, False)

    res = run_workflow(
        "m",
        runner=runner,
        n_workers=2,
        budgets={"architect": 1000, "worker": 1000, "reviewer": 1000, "judge": 1000},
        log_dir=tmp_path,
    )
    assert res.metrics["tokens_used"] == 500  # 5 stages * 100
    assert res.metrics["budget_utilisation"] == 0.1


def test_no_log_dir_returns_none():
    def runner(role, name, prompt, budget):
        return ("ACCEPT" if role == "judge" else "x", 10, False)

    res = run_workflow("m", runner=runner, n_workers=1)
    assert res.run_log is None


def test_extract_text_variants():
    assert _extract_text({"message": {"content": [{"type": "text", "text": "hi"}]}}) == "hi"
    assert _extract_text({"content": "plain"}) == "plain"
    assert _extract_text({"content": [{"type": "tool_use"}]}) == ""


def test_cli_workflow_dry_run():
    result = CliRunner().invoke(app, ["workflow", "run", "build a thing", "--dry-run", "--workers", "3"])
    assert result.exit_code == 0
    assert "architect" in result.stdout
    assert "worker-3" in result.stdout
    assert "verify-before-accept" in result.stdout
