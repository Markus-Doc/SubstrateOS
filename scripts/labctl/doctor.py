"""Environment health checks for the Lab Controller."""

from __future__ import annotations

import importlib.util
import os
import shutil
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from labctl.config import MANIFEST_NAME, REQUIRED_DIRS, load_manifest


@dataclass
class CheckResult:
    name: str
    ok: bool
    severity: str  # "error" | "warning"
    detail: str


def _check_python() -> CheckResult:
    ok = sys.version_info >= (3, 11)
    return CheckResult(
        "python",
        ok,
        "error",
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        + ("" if ok else " (need >= 3.11)"),
    )


def _check_venv() -> CheckResult:
    in_venv = sys.prefix != sys.base_prefix
    return CheckResult(
        "venv",
        in_venv,
        "warning",
        sys.prefix if in_venv else "not running inside a virtual environment",
    )


def _check_git(root: Path) -> CheckResult:
    has_git_dir = (root / ".git").exists()
    has_git_cli = shutil.which("git") is not None
    ok = has_git_dir and has_git_cli
    detail = []
    if not has_git_dir:
        detail.append("no .git directory")
    if not has_git_cli:
        detail.append("git not on PATH")
    return CheckResult("git", ok, "error", "; ".join(detail) or "repo and CLI present")


def _check_dirs(root: Path) -> CheckResult:
    missing = [rel for rel in REQUIRED_DIRS if not (root / rel).is_dir()]
    return CheckResult(
        "required-dirs",
        not missing,
        "error",
        f"missing: {', '.join(missing)}" if missing else "all present",
    )


def _check_fts5() -> CheckResult:
    try:
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE VIRTUAL TABLE t USING fts5(content)")
        conn.close()
        return CheckResult("sqlite-fts5", True, "error", "available")
    except sqlite3.OperationalError as exc:
        return CheckResult("sqlite-fts5", False, "error", f"unavailable: {exc}")


def _check_manifest(root: Path) -> CheckResult:
    manifest = load_manifest(root)
    if manifest is None:
        return CheckResult(
            "manifest", False, "warning", f"{MANIFEST_NAME} missing — run `labctl init`"
        )
    return CheckResult("manifest", True, "warning", f"project: {manifest.project}")


def _check_cli_tool(name: str, purpose: str) -> CheckResult:
    """Warning-severity presence check for an external gate/ingestion tool."""
    path = shutil.which(name)
    return CheckResult(
        name,
        path is not None,
        "warning",
        path if path else f"not on PATH ({purpose})",
    )


def _check_semgrep() -> CheckResult:
    """Semgrep is reachable natively or via WSL (ADR-013)."""
    path = shutil.which("semgrep")
    if path is not None:
        return CheckResult("semgrep", True, "warning", path)
    if shutil.which("wsl") is not None:
        probe = subprocess.run(
            ["wsl", "-e", "semgrep", "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if probe.returncode == 0:
            return CheckResult(
                "semgrep", True, "warning", f"via WSL ({probe.stdout.strip()})"
            )
    return CheckResult(
        "semgrep", False, "warning", "not on PATH or in WSL (sast stage skipped)"
    )


def _check_docling() -> CheckResult:
    found = importlib.util.find_spec("docling") is not None
    return CheckResult(
        "docling",
        found,
        "warning",
        "importable" if found else "not installed (PDF ingestion unavailable)",
    )


def _check_firecrawl_key(root: Path) -> CheckResult:
    """Report only whether FIRECRAWL_API_KEY is configured — never its value."""
    if os.environ.get("FIRECRAWL_API_KEY"):
        return CheckResult("firecrawl-key", True, "warning", "set in environment")
    env_file = root / ".env"
    if env_file.is_file() and "FIRECRAWL_API_KEY" in env_file.read_text(
        encoding="utf-8", errors="ignore"
    ):
        return CheckResult("firecrawl-key", True, "warning", "set in .env")
    return CheckResult(
        "firecrawl-key", False, "warning", "not set (web ingestion unavailable)"
    )


def run_checks(root: Path) -> list[CheckResult]:
    return [
        _check_python(),
        _check_venv(),
        _check_git(root),
        _check_dirs(root),
        _check_fts5(),
        _check_manifest(root),
        _check_cli_tool("gitleaks", "secret-scan uses fallback scanner"),
        _check_cli_tool("trivy", "vuln-scan stage skipped"),
        _check_semgrep(),
        _check_cli_tool("node", "evals stage skipped"),
        _check_docling(),
        _check_firecrawl_key(root),
    ]


def has_errors(results: list[CheckResult]) -> bool:
    return any(not r.ok and r.severity == "error" for r in results)


def warnings(results: list[CheckResult]) -> list[CheckResult]:
    return [r for r in results if not r.ok and r.severity == "warning"]
