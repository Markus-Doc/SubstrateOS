"""Lab host operator: wake, status, sync, and remote mission dispatch (ADR-017).

The Lab box is a remote agent operator, not a compute node: it runs the same
claude CLI as the control plane (subscription auth, never API keys) against a
current checkout of this repo. labctl talks to it over ssh (always BatchMode,
never interactive) and wakes it with a stdlib Wake-on-LAN magic packet.

Connection details (host alias, MAC, repo path) live in the environment or the
gitignored ``.env`` — never in tracked files. Dispatch reuses the capsule
machinery end to end: mission on stdin (ADR-015), stream-json metering and the
token circuit breaker (ADR-016), run logs on the control plane under
``artifacts/lab-runs/`` (gitignored).
"""

from __future__ import annotations

import json
import os
import re
import shlex
import socket
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from labctl.capsule import (
    BUILD_INSTRUCTION,
    DEFAULT_TOKEN_BUDGET,
    BuildResult,
    _kill_build,
    monitor_stream,
)

LAB_REPO_URL = "https://github.com/Markus-Doc/SubstrateOS.git"
RUN_LOG_DIR_REL = "artifacts/lab-runs"
WOL_PORT = 9
SSH_OPTS = ["-o", "BatchMode=yes", "-o", "ConnectTimeout=10"]

# Keys checked by `labctl lab status`; value of "missing" means absent.
STATUS_KEYS = ("hostname", "uptime", "claude", "codex", "gh_auth", "repo_head")


class LabError(RuntimeError):
    """Lab operation cannot proceed; the message is user-actionable."""


@dataclass
class LabConfig:
    ssh_host: str
    wol_mac: str | None
    wol_broadcast: str
    remote_repo: str


def _env_or_dotenv(root: Path, var: str, default: str | None = None) -> str | None:
    """Value from the environment first, then the gitignored .env at repo root."""
    value = os.environ.get(var)
    if value:
        return value
    env_file = root / ".env"
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith(f"{var}="):
                value = line.split("=", 1)[1].strip()
                if value:
                    return value
    return default


def load_lab_config(root: Path) -> LabConfig:
    return LabConfig(
        ssh_host=_env_or_dotenv(root, "LAB_SSH_HOST", "substrate-lab"),
        wol_mac=_env_or_dotenv(root, "LAB_WOL_MAC"),
        wol_broadcast=_env_or_dotenv(root, "LAB_WOL_BROADCAST", "255.255.255.255"),
        remote_repo=_env_or_dotenv(root, "LAB_REMOTE_REPO", "~/SubstrateOS"),
    )


# --- wake -------------------------------------------------------------------


def magic_packet(mac: str) -> bytes:
    """Wake-on-LAN payload: 6x 0xFF followed by the MAC repeated 16 times."""
    parts = re.split(r"[:\-]", mac.strip())
    if len(parts) != 6 or not all(re.fullmatch(r"[0-9A-Fa-f]{2}", p) for p in parts):
        raise ValueError(f"invalid MAC address: {mac!r} (expected aa:bb:cc:dd:ee:ff)")
    raw = bytes(int(p, 16) for p in parts)
    return b"\xff" * 6 + raw * 16


def _udp_broadcast(payload: bytes, addr: tuple[str, int]) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(payload, addr)


def send_wol(
    mac: str,
    broadcast: str = "255.255.255.255",
    sender: Callable[[bytes, tuple[str, int]], None] | None = None,
) -> None:
    (sender or _udp_broadcast)(magic_packet(mac), (broadcast, WOL_PORT))


# --- ssh plumbing -----------------------------------------------------------


def _ssh_argv(host: str, remote_command: str) -> list[str]:
    return ["ssh", *SSH_OPTS, host, remote_command]


def _remote_path(path: str) -> str:
    """Shell-quote a remote path while preserving ~ home expansion."""
    if path == "~" or path.startswith("~/"):
        return '"$HOME' + path[1:].replace('"', "") + '"'
    return shlex.quote(path)


def _run_ssh(
    argv: list[str], runner: Callable[..., subprocess.CompletedProcess] | None = None
) -> subprocess.CompletedProcess:
    return (runner or subprocess.run)(
        argv,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


# --- status -----------------------------------------------------------------


def _status_probe(remote_repo: str) -> str:
    """One compound remote command emitting key=value lines for STATUS_KEYS.

    PATH is prefixed with ~/.local/bin (the native claude installer location)
    because non-interactive ssh shells do not source the login profile.
    """
    repo = _remote_path(remote_repo)
    return (
        'PATH="$HOME/.local/bin:$PATH"; '
        "echo hostname=$(hostname); "
        'echo uptime="$(uptime -p 2>/dev/null || echo unknown)"; '
        'echo claude="$(claude --version 2>/dev/null || echo missing)"; '
        'echo codex="$(codex --version 2>/dev/null || echo missing)"; '
        "if command -v gh >/dev/null 2>&1; then "
        "gh auth status >/dev/null 2>&1 && echo gh_auth=ok || echo gh_auth=unauthenticated; "
        "else echo gh_auth=missing; fi; "
        f'echo repo_head="$(git -C {repo} log -1 --format=%h-%cs 2>/dev/null || echo missing)"'
    )


def probe_status(
    config: LabConfig,
    runner: Callable[..., subprocess.CompletedProcess] | None = None,
) -> dict[str, str]:
    """One ssh round trip; raises LabError when the host is unreachable."""
    proc = _run_ssh(_ssh_argv(config.ssh_host, _status_probe(config.remote_repo)), runner)
    parsed: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if key in STATUS_KEYS:
                parsed[key] = value.strip()
    if proc.returncode != 0 and "hostname" not in parsed:
        detail = (proc.stderr or "").strip() or f"ssh exited {proc.returncode}"
        raise LabError(
            f"lab host {config.ssh_host!r} unreachable: {detail} "
            "(is it awake? try `labctl lab wake --wait`)"
        )
    return parsed


def status_ok(parsed: dict[str, str]) -> dict[str, bool]:
    """Per-check verdicts for the status checklist."""
    return {
        "hostname": bool(parsed.get("hostname")),
        "uptime": parsed.get("uptime", "unknown") != "unknown",
        "claude": parsed.get("claude", "missing") != "missing",
        "codex": parsed.get("codex", "missing") != "missing",
        "gh_auth": parsed.get("gh_auth") == "ok",
        "repo_head": parsed.get("repo_head", "missing") != "missing",
    }


def wait_for_ssh(
    config: LabConfig,
    timeout: float = 120.0,
    interval: float = 5.0,
    runner: Callable[..., subprocess.CompletedProcess] | None = None,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> bool:
    deadline = clock() + timeout
    while True:
        if _run_ssh(_ssh_argv(config.ssh_host, "true"), runner).returncode == 0:
            return True
        if clock() >= deadline:
            return False
        sleep(interval)


# --- sync -------------------------------------------------------------------


def _sync_command(remote_repo: str) -> str:
    """Clone the repo if missing, else fast-forward pull; print resulting HEAD."""
    repo = _remote_path(remote_repo)
    return (
        f"if [ -d {repo}/.git ]; then git -C {repo} pull --ff-only; "
        f"else git clone {LAB_REPO_URL} {repo}; fi "
        f"&& git -C {repo} log -1 --format=%h-%cs"
    )


def sync(
    config: LabConfig,
    runner: Callable[..., subprocess.CompletedProcess] | None = None,
) -> str:
    """Bring the remote checkout current; returns the resulting HEAD."""
    proc = _run_ssh(_ssh_argv(config.ssh_host, _sync_command(config.remote_repo)), runner)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip() or f"exit {proc.returncode}"
        raise LabError(f"lab sync failed on {config.ssh_host!r}: {detail}")
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    if not lines:
        raise LabError(f"lab sync on {config.ssh_host!r} produced no HEAD output")
    return lines[-1].strip()


# --- dispatch ---------------------------------------------------------------


def _unexpand_local_home(path: str) -> str:
    """Undo click's Windows argv expansion for remote paths.

    On Windows, click pre-expands ``~`` in command-line arguments
    (click.utils._expand_args), so a remote path given as ``~/x`` arrives as
    ``<local home>/x``. Map it back to the remote home; the local home is
    never a meaningful remote workdir.
    """
    home = str(Path.home())
    for prefix in (home, home.replace("\\", "/")):
        if path == prefix or path.startswith((prefix + "/", prefix + "\\")):
            return "~" + path[len(prefix):].replace("\\", "/")
    return path


def _dispatch_command(workdir: str) -> str:
    return (
        f"cd {_remote_path(workdir)} && "
        'PATH="$HOME/.local/bin:$PATH" '
        f"claude -p {shlex.quote(BUILD_INSTRUCTION)} "
        "--dangerously-skip-permissions --output-format stream-json --verbose"
    )


def _spawn_ssh(mission: str, argv: list[str]) -> subprocess.Popen[str]:
    # ssh does not forward the local environment, so remote dispatch is
    # naturally clean of the ADR-015 env hazards; the mission still travels
    # on stdin (ssh forwards it to the remote claude), never argv.
    # nosemgrep: python.lang.compatibility.python36.python36-compatibility-Popen1, python.lang.compatibility.python36.python36-compatibility-Popen2 -- project requires Python >= 3.11
    proc = subprocess.Popen(
        argv,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.stdin is not None
    proc.stdin.write(mission)
    proc.stdin.close()
    return proc


def dispatch(
    root: Path,
    mission: str,
    token_budget: int | None = None,
    workdir: str | None = None,
    spawn: Callable[[str, list[str]], subprocess.Popen[str]] | None = None,
    runner: Callable[..., subprocess.CompletedProcess] | None = None,
) -> BuildResult:
    """Run a metered claude mission on the lab host with the breaker armed.

    The run log lives on the control plane (this machine), so a tripped or
    killed remote run can never take its own evidence with it.
    """
    config = load_lab_config(root)
    budget = token_budget or DEFAULT_TOKEN_BUDGET
    workdir = _unexpand_local_home(workdir) if workdir else config.remote_repo
    argv = _ssh_argv(config.ssh_host, _dispatch_command(workdir))

    log_dir = root / RUN_LOG_DIR_REL
    log_dir.mkdir(parents=True, exist_ok=True)
    started = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_log = log_dir / f"run-{started}.jsonl"

    proc = (spawn or _spawn_ssh)(mission, argv)
    assert proc.stdout is not None
    with run_log.open("a", encoding="utf-8") as log:
        tokens_used, tripped = monitor_stream(
            proc.stdout, budget, lambda line: log.write(line + "\n")
        )
        if tripped:
            _kill_build(proc)
            # Killing the local ssh closes the channel, but the remote claude
            # may linger; best-effort sweep, never fatal.
            _run_ssh(_ssh_argv(config.ssh_host, 'pkill -f "claude -p"'), runner)
            log.write(
                _breaker_record(tokens_used, budget) + "\n"
            )
            return BuildResult(tokens_used, budget, True, 1, run_log)
    exit_code = proc.wait()
    return BuildResult(tokens_used, budget, False, exit_code, run_log)


def _breaker_record(tokens_used: int, budget: int) -> str:
    return json.dumps(
        {
            "type": "circuit-breaker",
            "reason": "token budget exceeded",
            "tokens_used": tokens_used,
            "token_budget": budget,
            "utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    )
