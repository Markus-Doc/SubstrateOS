"""Environment health checks for the Lab Controller."""

from __future__ import annotations

import shutil
import sqlite3
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


def run_checks(root: Path) -> list[CheckResult]:
    return [
        _check_python(),
        _check_venv(),
        _check_git(root),
        _check_dirs(root),
        _check_fts5(),
        _check_manifest(root),
    ]


def has_errors(results: list[CheckResult]) -> bool:
    return any(not r.ok and r.severity == "error" for r in results)


def warnings(results: list[CheckResult]) -> list[CheckResult]:
    return [r for r in results if not r.ok and r.severity == "warning"]
