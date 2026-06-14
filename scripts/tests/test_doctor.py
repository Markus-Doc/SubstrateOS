from pathlib import Path

import pytest

from labctl import doctor
from labctl.config import init_project
from labctl.doctor import has_errors, run_checks, warnings


def test_checks_on_initialised_repo(repo: Path):
    init_project(repo)
    results = run_checks(repo)
    by_name = {r.name: r for r in results}
    assert by_name["python"].ok
    assert by_name["sqlite-fts5"].ok
    assert by_name["required-dirs"].ok
    assert by_name["manifest"].ok


def test_missing_manifest_is_warning_not_error(repo: Path):
    for rel in ("docs/decisions", "docs/planning", "docs/research", "scripts", "artifacts"):
        (repo / rel).mkdir(parents=True)
    results = run_checks(repo)
    by_name = {r.name: r for r in results}
    assert not by_name["manifest"].ok
    assert by_name["manifest"].severity == "warning"
    assert any(w.name == "manifest" for w in warnings(results))


def test_missing_dirs_is_error(repo: Path):
    results = run_checks(repo)
    assert has_errors(results)


class _FakeProc:
    def __init__(self, returncode: int, stdout: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = ""


def test_git_check_exercises_git_and_passes(repo: Path):
    # repo fixture is a real `git init` work tree, so the live check passes.
    result = doctor._check_git(repo)
    assert result.ok
    assert "git ok" in result.detail


def test_git_check_flags_dubious_ownership(repo: Path, monkeypatch: pytest.MonkeyPatch):
    # Simulate the post-move broken state: git refuses with dubious ownership.
    fake = _FakeProc(128)
    fake.stderr = (
        f"fatal: detected dubious ownership in repository at '{repo}'"
    )
    monkeypatch.setattr(doctor, "_run_git", lambda *_a, **_kw: fake)
    result = doctor._check_git(repo)
    assert not result.ok
    assert result.severity == "error"
    assert "safe.directory" in result.detail
    assert "ownership" in result.detail.lower()
    # the whole report must now carry an error
    monkeypatch.setattr(doctor, "_run_git", lambda *_a, **_kw: fake)
    assert has_errors(run_checks(repo))


def test_git_check_surfaces_other_failures(repo: Path, monkeypatch: pytest.MonkeyPatch):
    fake = _FakeProc(128)
    fake.stderr = "fatal: not a git repository"
    monkeypatch.setattr(doctor, "_run_git", lambda *_a, **_kw: fake)
    result = doctor._check_git(repo)
    assert not result.ok
    assert "not a git repository" in result.detail


def test_git_check_missing_cli_skips_invocation(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(doctor.shutil, "which", lambda name: None)

    def explode(*_a, **_kw):
        raise AssertionError("git must not be invoked when the CLI is absent")

    monkeypatch.setattr(doctor, "_run_git", explode)
    result = doctor._check_git(repo)
    assert not result.ok
    assert "git not on PATH" in result.detail


def test_tool_checks_are_warning_severity(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(doctor.shutil, "which", lambda name: None)
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    results = run_checks(repo)
    by_name = {r.name: r for r in results}
    for name in (
        "gitleaks", "trivy", "semgrep", "node", "resynth", "firecrawl-key",
        "subos-on-path", "engines",
    ):
        assert not by_name[name].ok
        assert by_name[name].severity == "warning"
    # missing tools must never make doctor exit non-zero on their own
    assert not any(
        r.severity == "error" and not r.ok
        for r in results
        if r.name
        in (
            "gitleaks", "trivy", "semgrep", "node", "resynth", "docling", "firecrawl-key",
            "subos-on-path", "spec-resolvable", "engines",
        )
    )


def test_install_health_checks_present(repo: Path):
    results = run_checks(repo)
    by_name = {r.name: r for r in results}
    assert {"subos-on-path", "spec-resolvable", "engines"} <= set(by_name)
    # the spec ships as package data, so it resolves regardless of cwd
    assert by_name["spec-resolvable"].ok
    assert by_name["spec-resolvable"].severity == "warning"


def test_cli_tool_check_reports_path(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(doctor.shutil, "which", lambda name: f"C:/tools/{name}.exe")
    result = doctor._check_cli_tool("gitleaks", "unused")
    assert result.ok
    assert "gitleaks.exe" in result.detail


def test_semgrep_check_falls_back_to_wsl(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        doctor.shutil, "which", lambda name: "wsl" if name == "wsl" else None
    )
    monkeypatch.setattr(
        doctor.subprocess, "run", lambda *a, **kw: _FakeProc(0, stdout="1.166.0")
    )
    result = doctor._check_semgrep()
    assert result.ok
    assert "WSL" in result.detail


def test_semgrep_check_warns_when_nowhere(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(doctor.shutil, "which", lambda name: None)
    result = doctor._check_semgrep()
    assert not result.ok
    assert result.severity == "warning"


def test_firecrawl_key_from_environment(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test-not-a-real-key")
    result = doctor._check_firecrawl_key(repo)
    assert result.ok
    assert "fc-test" not in result.detail  # never echo the value


def test_firecrawl_key_from_env_file(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    (repo / ".env").write_text("FIRECRAWL_API_KEY=placeholder\n", encoding="utf-8")
    result = doctor._check_firecrawl_key(repo)
    assert result.ok
    assert "placeholder" not in result.detail


def test_firecrawl_key_missing_is_warning(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    result = doctor._check_firecrawl_key(repo)
    assert not result.ok
    assert result.severity == "warning"
