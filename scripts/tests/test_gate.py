"""Tests for the release gate module.

Fake secrets are constructed at runtime via concatenation and written only
into tmp_path git repos, never into this repo's source.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from labctl import gate

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def no_gitleaks(monkeypatch: pytest.MonkeyPatch):
    """Force the fallback scanner regardless of whether gitleaks is installed."""
    monkeypatch.setattr(gate.shutil, "which", lambda _name: None)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _make_repo(tmp_path: Path, files: dict[str, str]) -> Path:
    _git(tmp_path, "init", "-q")
    for rel, content in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    _git(tmp_path, "add", "-A")
    return tmp_path


def test_fallback_flags_fake_aws_key(tmp_path: Path, no_gitleaks):
    fake_key = "AKIA" + "X" * 16
    repo = _make_repo(tmp_path, {"leaky.txt": f"id = {fake_key}\n"})
    result = gate.scan_secrets(repo)
    assert not result.passed
    assert "leaky.txt:1" in result.detail
    assert fake_key not in result.detail  # never leak the secret itself


def test_fallback_flags_private_key_header(tmp_path: Path, no_gitleaks):
    header = "-----" + "BEGIN " + "RSA " + "PRIVATE" + " KEY" + "-----"
    repo = _make_repo(tmp_path, {"keys/server.pem": header + "\nabc\n"})
    result = gate.scan_secrets(repo)
    assert not result.passed
    assert "keys/server.pem:1" in result.detail


def test_fallback_passes_clean_repo(tmp_path: Path, no_gitleaks):
    repo = _make_repo(tmp_path, {"README.md": "# Clean\n", "src/app.py": "x = 1\n"})
    result = gate.scan_secrets(repo)
    assert result.passed
    assert result.name == "secret-scan"


def test_fallback_skips_binaryish_files(tmp_path: Path, no_gitleaks):
    fake_key = "AKIA" + "Y" * 16
    repo = _make_repo(tmp_path, {"image.png": fake_key + "\n"})
    result = gate.scan_secrets(repo)
    assert result.passed


def test_run_ruff_passes_on_real_repo():
    result = gate.run_ruff(REPO_ROOT)
    assert result.passed, result.detail
    assert result.name == "lint"


def test_run_pytest_passes_on_mini_suite(tmp_path: Path):
    test_file = tmp_path / "test_mini_pass.py"
    test_file.write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    result = gate.run_pytest(tmp_path, args=[str(test_file), "-q"])
    assert result.passed, result.detail
    assert result.name == "tests"


def test_run_pytest_fails_on_failing_mini_suite(tmp_path: Path):
    test_file = tmp_path / "test_mini_fail.py"
    test_file.write_text("def test_bad():\n    assert False\n", encoding="utf-8")
    result = gate.run_pytest(tmp_path, args=[str(test_file), "-q"])
    assert not result.passed


def test_run_gate_runs_all_stages_without_short_circuit(
    tmp_path: Path, no_gitleaks, monkeypatch: pytest.MonkeyPatch
):
    fake_key = "AKIA" + "Z" * 16
    repo = _make_repo(tmp_path, {"oops.txt": fake_key + "\n"})

    def fake_run_pytest(root: Path, args: list[str] | None = None) -> gate.GateStage:
        return gate.GateStage("tests", True, "stubbed: mini suite")

    monkeypatch.setattr(gate, "run_pytest", fake_run_pytest)
    results = gate.run_gate(repo)
    names = [r.name for r in results]
    assert names == ["secret-scan", "lint", "tests"]
    assert not results[0].passed  # secret found, but later stages still ran


def test_run_gate_can_exclude_tests(tmp_path: Path, no_gitleaks):
    repo = _make_repo(tmp_path, {"README.md": "ok\n"})
    results = gate.run_gate(repo, include_tests=False)
    assert [r.name for r in results] == ["secret-scan", "lint"]
