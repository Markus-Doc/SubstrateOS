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
    assert names == ["secret-scan", "lint", "tests", "sast", "vuln-scan", "evals"]
    assert not results[0].passed  # secret found, but later stages still ran


def test_run_gate_can_exclude_tests(tmp_path: Path, no_gitleaks):
    repo = _make_repo(tmp_path, {"README.md": "ok\n"})
    results = gate.run_gate(repo, include_tests=False)
    assert [r.name for r in results] == [
        "secret-scan", "lint", "sast", "vuln-scan", "evals"
    ]


class _FakeProc:
    def __init__(self, returncode: int, stdout: str = "", stderr: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _which_map(monkeypatch: pytest.MonkeyPatch, available: dict[str, str]) -> None:
    monkeypatch.setattr(gate.shutil, "which", lambda name: available.get(name))


# --- sast (Semgrep) ---


def test_semgrep_skips_when_unavailable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _which_map(monkeypatch, {})
    result = gate.run_semgrep(tmp_path)
    assert result.passed
    assert result.detail == "skipped: semgrep not installed"


def test_semgrep_passes_natively(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _which_map(monkeypatch, {"semgrep": "semgrep"})
    monkeypatch.setattr(
        gate.subprocess, "run", lambda *a, **kw: _FakeProc(0)
    )
    result = gate.run_semgrep(tmp_path)
    assert result.passed
    assert result.name == "sast"


def test_semgrep_fails_on_findings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _which_map(monkeypatch, {"semgrep": "semgrep"})
    monkeypatch.setattr(
        gate.subprocess, "run", lambda *a, **kw: _FakeProc(1, stdout="1 finding")
    )
    result = gate.run_semgrep(tmp_path)
    assert not result.passed
    assert "finding" in result.detail


def test_semgrep_falls_back_to_wsl(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _which_map(monkeypatch, {"wsl": "wsl"})
    calls: list[list[str]] = []

    def fake_run(cmd, **kw):
        calls.append(cmd)
        return _FakeProc(0, stdout="1.166.0")

    monkeypatch.setattr(gate.subprocess, "run", fake_run)
    result = gate.run_semgrep(tmp_path)
    assert result.passed
    assert calls[0][:3] == ["wsl", "-e", "semgrep"]  # version probe
    assert calls[1][:3] == ["wsl", "-e", "semgrep"]  # actual scan


# --- vuln-scan (Trivy) ---


def test_trivy_skips_when_absent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _which_map(monkeypatch, {})
    result = gate.run_trivy(tmp_path)
    assert result.passed
    assert result.detail == "skipped: trivy not installed"


def test_trivy_passes_on_clean_scan(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _which_map(monkeypatch, {"trivy": "trivy"})
    monkeypatch.setattr(gate.subprocess, "run", lambda *a, **kw: _FakeProc(0))
    result = gate.run_trivy(tmp_path)
    assert result.passed
    assert result.name == "vuln-scan"


def test_trivy_fails_on_findings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _which_map(monkeypatch, {"trivy": "trivy"})
    monkeypatch.setattr(
        gate.subprocess, "run", lambda *a, **kw: _FakeProc(1, stdout="CVE-2026-0001")
    )
    result = gate.run_trivy(tmp_path)
    assert not result.passed


# --- evals (promptfoo) ---


def test_evals_skip_without_node(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _which_map(monkeypatch, {})
    result = gate.run_evals(tmp_path)
    assert result.passed
    assert "npx" in result.detail


def test_evals_skip_without_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _which_map(monkeypatch, {"npx": "npx"})
    result = gate.run_evals(tmp_path)
    assert result.passed
    assert "promptfooconfig" in result.detail


def test_evals_pass_and_disable_telemetry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    (tmp_path / "evals").mkdir()
    (tmp_path / "evals" / "promptfooconfig.yaml").write_text(
        "providers: [echo]\n", encoding="utf-8"
    )
    _which_map(monkeypatch, {"npx": "npx"})
    seen_env: dict[str, str] = {}

    def fake_run(cmd, **kw):
        seen_env.update(kw.get("env") or {})
        return _FakeProc(0)

    monkeypatch.setattr(gate.subprocess, "run", fake_run)
    result = gate.run_evals(tmp_path)
    assert result.passed
    assert result.name == "evals"
    assert seen_env.get("PROMPTFOO_DISABLE_TELEMETRY") == "1"


def test_evals_fail_on_assertion_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    (tmp_path / "evals").mkdir()
    (tmp_path / "evals" / "promptfooconfig.yaml").write_text(
        "providers: [echo]\n", encoding="utf-8"
    )
    _which_map(monkeypatch, {"npx": "npx"})
    monkeypatch.setattr(
        gate.subprocess, "run", lambda *a, **kw: _FakeProc(100, stderr="1 failed")
    )
    result = gate.run_evals(tmp_path)
    assert not result.passed


# --- strict mode ---


def test_strict_turns_skips_into_failures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(
        gate, "scan_secrets", lambda root: gate.GateStage("secret-scan", True, "ok")
    )
    monkeypatch.setattr(
        gate, "run_ruff", lambda root: gate.GateStage("lint", True, "ok")
    )
    monkeypatch.setattr(
        gate, "run_semgrep",
        lambda root: gate.GateStage("sast", True, "skipped: semgrep not installed"),
    )
    monkeypatch.setattr(
        gate, "run_trivy", lambda root: gate.GateStage("vuln-scan", True, "ok")
    )
    monkeypatch.setattr(
        gate, "run_evals", lambda root: gate.GateStage("evals", True, "ok")
    )
    lax = gate.run_gate(tmp_path, include_tests=False)
    assert all(r.passed for r in lax)
    strict = gate.run_gate(tmp_path, include_tests=False, strict=True)
    by_name = {r.name: r for r in strict}
    assert not by_name["sast"].passed
    assert by_name["sast"].detail.endswith("(strict)")
    assert by_name["vuln-scan"].passed  # genuine passes untouched
