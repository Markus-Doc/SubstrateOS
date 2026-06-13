"""Tests for M-F: cross-engine conformance suite (ADR-019)."""

from __future__ import annotations

from typer.testing import CliRunner

from labctl.cli import app
from labctl.conformance import SCENARIOS, check_conformance


def test_compliant_engine_passes_all():
    # An engine that does the expected thing for every scenario.
    result = check_conformance("good-engine", lambda sc: sc.expect)
    assert result.ok
    assert len(result.passed) == len(SCENARIOS)
    assert result.failed == []


def test_gate_bypasser_fails():
    def responder(sc):
        # Complies with everything, including things it should refuse.
        return "comply"

    result = check_conformance("bad-engine", responder)
    assert not result.ok
    # the refuse-scenarios are the failures
    refuse_count = sum(1 for sc in SCENARIOS if sc.expect == "refuse")
    assert len(result.failed) == refuse_count


def test_cli_conformance_lists_contract():
    result = CliRunner().invoke(app, ["conformance"])
    assert result.exit_code == 0
    assert "conformance" in result.stdout.lower()
    assert "release gate" in result.stdout
