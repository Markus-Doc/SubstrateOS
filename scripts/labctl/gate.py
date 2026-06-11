"""Release gate: secret scan, lint, and test stages.

Stage 1 prefers gitleaks when available and falls back to a built-in
regex scanner over git-tracked files. Stages 2 and 3 shell out to ruff
and pytest. ``run_gate`` runs every stage and reports all results
without short-circuiting.

Note: the fallback scanner's patterns are deliberately assembled from
concatenated fragments so this source file never matches its own rules.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# Extensions the fallback scanner treats as binary-ish and skips.
SKIP_EXTENSIONS = frozenset(
    {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".sqlite", ".db", ".pyc", ".zip"}
)

_MAX_DETAIL_HITS = 10


@dataclass
class GateStage:
    name: str
    passed: bool
    detail: str


def _build_patterns() -> list[tuple[str, re.Pattern[str]]]:
    """Compile secret-detection patterns.

    Pattern strings are built by concatenation so the literals in this
    file cannot trip the scanner when it scans this repo.
    """
    quote = "['\"]"
    pem_head = "-----" + "BEGIN "
    pem_tail = "PRIVATE" + " KEY" + "-----"
    return [
        ("aws-access-key-id", re.compile("AKIA" + "[0-9A-Z]{16}")),
        (
            "generic-credential-assignment",
            re.compile(
                "(?i)(api[_-]?key|secr" + "et|tok" + "en|passw" + "ord)"
                + r"\s*[:=]\s*" + quote + r"[A-Za-z0-9_\-/+=]{16,}" + quote
            ),
        ),
        (
            "private-key-header",
            re.compile(pem_head + "(RSA |EC |OPENSSH |DSA )?" + pem_tail),
        ),
        ("github-token", re.compile("gh[pousr]" + "_" + "[A-Za-z0-9]{36,}")),
        ("anthropic-key", re.compile("sk-" + "ant-" + r"[A-Za-z0-9_\-]{20,}")),
        ("generic-sk-key", re.compile("sk-" + "[A-Za-z0-9]{32,}")),
        ("slack-token", re.compile("xox" + "[baprs]-")),
    ]


def _git_tracked_files(root: Path) -> list[Path]:
    proc = subprocess.run(
        ["git", "-C", str(root), "ls-files"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [root / line for line in proc.stdout.splitlines() if line.strip()]


def _fallback_scan(root: Path) -> GateStage:
    patterns = _build_patterns()
    hits: list[str] = []
    for path in _git_tracked_files(root):
        if path.suffix.lower() in SKIP_EXTENSIONS:
            continue
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(root).as_posix()
        for lineno, line in enumerate(text.splitlines(), start=1):
            for rule, pattern in patterns:
                if pattern.search(line):
                    hits.append(f"{rel}:{lineno} ({rule})")
    if hits:
        shown = hits[:_MAX_DETAIL_HITS]
        suffix = "" if len(hits) <= _MAX_DETAIL_HITS else f" (+{len(hits) - _MAX_DETAIL_HITS} more)"
        return GateStage(
            "secret-scan", False, f"fallback scanner: {'; '.join(shown)}{suffix}"
        )
    return GateStage("secret-scan", True, "fallback scanner: no secrets found in tracked files")


def scan_secrets(root: Path) -> GateStage:
    """Scan the repo for secrets using gitleaks if present, else the fallback."""
    if shutil.which("gitleaks") is not None:
        proc = subprocess.run(
            ["gitleaks", "detect", "--source", str(root), "--no-banner", "--redact"],
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            return GateStage("secret-scan", True, "gitleaks: no leaks found")
        tail = "\n".join(proc.stderr.strip().splitlines()[-5:])
        return GateStage(
            "secret-scan", False, f"gitleaks exit {proc.returncode}: {tail}"
        )
    return _fallback_scan(root)


def run_ruff(root: Path) -> GateStage:
    proc = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "scripts"],
        capture_output=True,
        text=True,
        cwd=root,
    )
    if proc.returncode == 0:
        return GateStage("lint", True, "ruff: clean")
    tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-10:])
    return GateStage("lint", False, f"ruff exit {proc.returncode}: {tail}")


def run_pytest(root: Path, args: list[str] | None = None) -> GateStage:
    """Run the test suite. ``args`` overrides the default target for testing."""
    if args is None:
        args = ["scripts/tests", "-q"]
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", *args],
        capture_output=True,
        text=True,
        cwd=root,
    )
    if proc.returncode == 0:
        summary = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else "passed"
        return GateStage("tests", True, f"pytest: {summary}")
    tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-10:])
    return GateStage("tests", False, f"pytest exit {proc.returncode}: {tail}")


def run_gate(root: Path, include_tests: bool = True) -> list[GateStage]:
    """Run all gate stages in order and return every result (no short-circuit)."""
    results = [scan_secrets(root), run_ruff(root)]
    if include_tests:
        results.append(run_pytest(root))
    return results
