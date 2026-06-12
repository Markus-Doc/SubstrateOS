"""Capsule lifecycle: scaffold (labctl new) and headless build (labctl build).

A capsule is scaffolded as a SIBLING directory of the SubstrateOS repo because
it becomes its own GitHub repo (ADR-014). Its memory namespace directory lives
under SubstrateOS artifacts/memory-namespaces/<project>/ and is the only thing
bind-mounted besides the workspace (template isolation guarantees).

``labctl build`` is host-scoped in Phase 1 (ADR-015): it runs claude headlessly
with cwd = capsule workspace and watches the stream-json events for cumulative
token usage. When usage exceeds the capsule's token budget the circuit breaker
kills the child process and records a breaker event in the run log.
In-container execution is Phase 2.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

CAPSULE_MANIFEST_NAME = "capsule.json"
TEMPLATE_DIR_REL = "templates/capsule-devcontainer"
NAMESPACE_PARENT_REL = "artifacts/memory-namespaces"
RUN_LOG_DIR_REL = ".substrateos/logs"

# Default cumulative token budget per build run (ADR-016). Counts input,
# output, and cache-creation tokens; cache reads are excluded as they would
# dominate the count without reflecting real spend.
DEFAULT_TOKEN_BUDGET = 2_000_000

GIT_AUTHOR_NAME = "M. Walker"
GIT_AUTHOR_EMAIL = "178984035+Markus-Doc@users.noreply.github.com"

MIT_LICENSE = """MIT License

Copyright (c) {year} M. Walker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

CAPSULE_CLAUDE_MD = """# Capsule: {project}

## Mission

{mission}

## Constraints

- This capsule is an isolated SubstrateOS project: work only inside this
  directory. Never read or modify sibling projects or the SubstrateOS repo.
- Memory namespace: `{namespace}`. All persistent memory for this capsule is
  scoped to that namespace; never touch another namespace.
- No secrets, keys, or credentials in any file.
- Tests must pass before any commit.
- Keep outputs as clean Markdown and plain Python; no new frameworks or
  platforms beyond what the mission states.
"""

CAPSULE_GITIGNORE = """__pycache__/
*.py[cod]
*.egg-info/
.venv/
.env
.substrateos/
"""


@dataclass
class BuildResult:
    tokens_used: int
    token_budget: int
    breaker_tripped: bool
    exit_code: int
    run_log: Path


def _run_git(cwd: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )


def scaffold_capsule(
    root: Path,
    project: str,
    mission: str = "(mission not yet defined)",
    token_budget: int = DEFAULT_TOKEN_BUDGET,
    dest_parent: Path | None = None,
) -> Path:
    """Scaffold a capsule as a sibling directory of the SubstrateOS repo.

    Copies the devcontainer template with placeholder tokens substituted,
    writes the capsule CLAUDE.md / LICENSE / manifest, and git-inits the
    directory with the standing author identity.
    """
    if not project.replace("-", "").replace("_", "").isalnum():
        raise ValueError(f"project name must be a simple slug: {project!r}")
    template_dir = root / TEMPLATE_DIR_REL
    if not template_dir.is_dir():
        raise FileNotFoundError(f"capsule template missing: {template_dir}")

    capsule_dir = (dest_parent or root.parent) / project
    if capsule_dir.exists():
        raise FileExistsError(f"capsule directory already exists: {capsule_dir}")

    namespace_dir = root / NAMESPACE_PARENT_REL / project
    namespace_dir.mkdir(parents=True, exist_ok=True)

    devcontainer_dir = capsule_dir / ".devcontainer"
    devcontainer_dir.mkdir(parents=True)
    for src in template_dir.iterdir():
        if not src.is_file():
            continue
        text = src.read_text(encoding="utf-8")
        text = text.replace("__MEMORY_NAMESPACE_DIR__", namespace_dir.resolve().as_posix())
        text = text.replace("__CAPSULE_NAMESPACE__", project)
        (devcontainer_dir / src.name).write_text(text, encoding="utf-8")

    (capsule_dir / "CLAUDE.md").write_text(
        CAPSULE_CLAUDE_MD.format(project=project, mission=mission, namespace=project),
        encoding="utf-8",
    )
    (capsule_dir / "LICENSE").write_text(
        MIT_LICENSE.format(year=datetime.now(UTC).year), encoding="utf-8"
    )
    (capsule_dir / ".gitignore").write_text(CAPSULE_GITIGNORE, encoding="utf-8")
    (capsule_dir / CAPSULE_MANIFEST_NAME).write_text(
        json.dumps(
            {
                "project": project,
                "namespace": project,
                "mission": mission,
                "token_budget": token_budget,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    _run_git(capsule_dir, "init")
    _run_git(capsule_dir, "config", "user.name", GIT_AUTHOR_NAME)
    _run_git(capsule_dir, "config", "user.email", GIT_AUTHOR_EMAIL)
    _run_git(capsule_dir, "add", "-A")
    _run_git(capsule_dir, "commit", "-m", f"chore: scaffold capsule {project}")
    return capsule_dir


def load_capsule_manifest(capsule_dir: Path) -> dict:
    path = capsule_dir / CAPSULE_MANIFEST_NAME
    if not path.is_file():
        raise FileNotFoundError(f"not a capsule (no {CAPSULE_MANIFEST_NAME}): {capsule_dir}")
    return json.loads(path.read_text(encoding="utf-8"))


def _usage_tokens(event: dict) -> int:
    """Billable tokens in one stream-json event (cache reads excluded)."""
    usage = event.get("usage")
    if usage is None:
        usage = event.get("message", {}).get("usage")
    if not isinstance(usage, dict):
        return 0
    return sum(
        int(usage.get(key) or 0)
        for key in ("input_tokens", "output_tokens", "cache_creation_input_tokens")
    )


def monitor_stream(
    lines: Iterable[str],
    token_budget: int,
    log_line: Callable[[str], None],
) -> tuple[int, bool]:
    """Accumulate token usage from stream-json lines until done or over budget.

    Every line is appended to the run log. Returns (tokens_used, tripped);
    when tripped, iteration stops immediately so the caller can kill the child.
    """
    tokens_used = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        log_line(line)
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        tokens_used += _usage_tokens(event)
        if tokens_used > token_budget:
            return tokens_used, True
    return tokens_used, False


def _spawn_claude(mission: str, cwd: Path) -> subprocess.Popen[str]:
    claude = shutil.which("claude")
    if claude is None:
        raise RuntimeError("claude CLI not found on PATH (needed for lab build)")
    # --dangerously-skip-permissions reflects the owner's standing authorisation
    # on this machine (ADR-015); end-users would run under their own permission
    # model. --verbose is required by claude for stream-json in print mode.
    # Auth is delegated to the claude CLI's own credential store: an inherited
    # ANTHROPIC_API_KEY would override it (ADR-015).
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    return subprocess.Popen(
        [
            claude,
            "-p",
            mission,
            "--dangerously-skip-permissions",
            "--output-format",
            "stream-json",
            "--verbose",
        ],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )


def run_build(
    root: Path,
    project: str,
    mission: str | None = None,
    token_budget: int | None = None,
    dest_parent: Path | None = None,
    spawn: Callable[[str, Path], subprocess.Popen[str]] | None = None,
) -> BuildResult:
    """Host-scoped headless build of one capsule with the circuit breaker armed."""
    capsule_dir = (dest_parent or root.parent) / project
    manifest = load_capsule_manifest(capsule_dir)
    mission = mission or manifest.get("mission") or "(mission not yet defined)"
    budget = token_budget or int(manifest.get("token_budget") or DEFAULT_TOKEN_BUDGET)

    log_dir = capsule_dir / RUN_LOG_DIR_REL
    log_dir.mkdir(parents=True, exist_ok=True)
    started = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_log = log_dir / f"run-{started}.jsonl"

    proc = (spawn or _spawn_claude)(mission, capsule_dir)
    assert proc.stdout is not None
    with run_log.open("a", encoding="utf-8") as log:
        tokens_used, tripped = monitor_stream(
            proc.stdout, budget, lambda line: log.write(line + "\n")
        )
        if tripped:
            proc.kill()
            proc.wait()
            log.write(
                json.dumps(
                    {
                        "type": "circuit-breaker",
                        "reason": "token budget exceeded",
                        "tokens_used": tokens_used,
                        "token_budget": budget,
                        "utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    }
                )
                + "\n"
            )
            return BuildResult(tokens_used, budget, True, 1, run_log)
    exit_code = proc.wait()
    return BuildResult(tokens_used, budget, False, exit_code, run_log)
