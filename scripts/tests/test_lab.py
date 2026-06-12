import json
import subprocess
from pathlib import Path

import pytest

from labctl.capsule import BUILD_INSTRUCTION, DEFAULT_TOKEN_BUDGET
from labctl.lab import (
    LabError,
    RUN_LOG_DIR_REL,
    WOL_PORT,
    _dispatch_command,
    _status_probe,
    _sync_command,
    dispatch,
    load_lab_config,
    magic_packet,
    probe_status,
    send_wol,
    status_ok,
    sync,
)


def usage_line(tokens: int) -> str:
    return json.dumps(
        {"type": "assistant", "message": {"usage": {"input_tokens": tokens, "output_tokens": 0}}}
    )


def completed(stdout: str = "", returncode: int = 0, stderr: str = "") -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(args=["ssh"], returncode=returncode, stdout=stdout, stderr=stderr)


class FakeProc:
    """Stand-in for the ssh dispatch subprocess (mirrors test_capsule.FakeProc)."""

    def __init__(self, lines: list[str]):
        self.stdout = iter(lines)
        self.killed = False
        self.returncode = 0

    def kill(self):
        self.killed = True

    def wait(self):
        return self.returncode


PROBE_OK = (
    "hostname=useragent\n"
    "uptime=up 2 hours\n"
    "claude=2.0.0 (Claude Code)\n"
    "codex=codex-cli 0.133.0\n"
    "gh_auth=ok\n"
    "repo_head=b56f613-2026-06-12\n"
)


# --- config -----------------------------------------------------------------


def test_config_defaults_and_dotenv(repo: Path, monkeypatch: pytest.MonkeyPatch):
    for var in ("LAB_SSH_HOST", "LAB_WOL_MAC", "LAB_WOL_BROADCAST", "LAB_REMOTE_REPO"):
        monkeypatch.delenv(var, raising=False)
    config = load_lab_config(repo)
    assert config.ssh_host == "substrate-lab"
    assert config.wol_mac is None
    assert config.wol_broadcast == "255.255.255.255"
    assert config.remote_repo == "~/SubstrateOS"

    (repo / ".env").write_text(
        "LAB_WOL_MAC=aa:bb:cc:dd:ee:ff\nLAB_SSH_HOST=otherhost\n", encoding="utf-8"
    )
    config = load_lab_config(repo)
    assert config.wol_mac == "aa:bb:cc:dd:ee:ff"
    assert config.ssh_host == "otherhost"

    monkeypatch.setenv("LAB_SSH_HOST", "envhost")  # environment beats .env
    assert load_lab_config(repo).ssh_host == "envhost"


# --- wake -------------------------------------------------------------------


def test_magic_packet_layout():
    packet = magic_packet("08:62:66:b4:1a:d2")
    mac = bytes([0x08, 0x62, 0x66, 0xB4, 0x1A, 0xD2])
    assert len(packet) == 102
    assert packet[:6] == b"\xff" * 6
    assert packet[6:] == mac * 16
    # dash-separated and uppercase forms are equivalent
    assert magic_packet("08-62-66-B4-1A-D2") == packet


@pytest.mark.parametrize("bad", ["", "08:62:66:b4:1a", "zz:bb:cc:dd:ee:ff", "0862.66b4.1ad2"])
def test_magic_packet_rejects_bad_mac(bad: str):
    with pytest.raises(ValueError):
        magic_packet(bad)


def test_send_wol_uses_injected_sender():
    sent: list[tuple[bytes, tuple[str, int]]] = []
    send_wol("aa:bb:cc:dd:ee:ff", broadcast="192.168.50.255", sender=lambda p, a: sent.append((p, a)))
    assert sent == [(magic_packet("aa:bb:cc:dd:ee:ff"), ("192.168.50.255", WOL_PORT))]


# --- status -----------------------------------------------------------------


def test_status_probe_is_one_round_trip_and_parses(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("LAB_SSH_HOST", raising=False)
    calls: list[list[str]] = []

    def runner(argv, **kwargs):
        calls.append(argv)
        return completed(stdout=PROBE_OK)

    parsed = probe_status(load_lab_config(repo), runner=runner)
    assert len(calls) == 1
    assert calls[0][:1] == ["ssh"]
    assert "BatchMode=yes" in calls[0]
    assert parsed["hostname"] == "useragent"
    assert parsed["claude"].startswith("2.0.0")
    assert parsed["gh_auth"] == "ok"
    assert parsed["repo_head"] == "b56f613-2026-06-12"

    verdicts = status_ok(parsed)
    assert all(verdicts.values())


def test_status_flags_missing_tools():
    verdicts = status_ok(
        {
            "hostname": "useragent",
            "uptime": "up 1 minute",
            "claude": "missing",
            "codex": "codex-cli 0.133.0",
            "gh_auth": "unauthenticated",
            "repo_head": "missing",
        }
    )
    assert verdicts["hostname"] and verdicts["codex"]
    assert not verdicts["claude"]
    assert not verdicts["gh_auth"]
    assert not verdicts["repo_head"]


def test_status_unreachable_raises(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("LAB_SSH_HOST", raising=False)
    def runner(argv, **kwargs):
        return completed(returncode=255, stderr="Connection timed out")

    with pytest.raises(LabError, match="unreachable"):
        probe_status(load_lab_config(repo), runner=runner)


def test_status_probe_prefixes_local_bin():
    probe = _status_probe("~/SubstrateOS")
    assert probe.startswith('PATH="$HOME/.local/bin:$PATH"')
    assert 'git -C "$HOME/SubstrateOS" log -1' in probe


# --- sync -------------------------------------------------------------------


def test_sync_command_has_clone_and_pull_branches():
    command = _sync_command("~/SubstrateOS")
    assert "git clone https://github.com/Markus-Doc/SubstrateOS.git" in command
    assert "pull --ff-only" in command
    assert 'if [ -d "$HOME/SubstrateOS"/.git ]' in command


def test_sync_returns_resulting_head(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("LAB_SSH_HOST", raising=False)
    def runner(argv, **kwargs):
        return completed(stdout="Already up to date.\nb56f613-2026-06-12\n")

    assert sync(load_lab_config(repo), runner=runner) == "b56f613-2026-06-12"


def test_sync_failure_raises(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("LAB_SSH_HOST", raising=False)
    def runner(argv, **kwargs):
        return completed(returncode=1, stderr="fatal: not possible to fast-forward")

    with pytest.raises(LabError, match="fast-forward"):
        sync(load_lab_config(repo), runner=runner)


# --- dispatch ---------------------------------------------------------------


def test_dispatch_command_shape():
    command = _dispatch_command("~/SubstrateOS")
    assert command.startswith('cd "$HOME/SubstrateOS" && ')
    assert "--dangerously-skip-permissions" in command
    assert "--output-format stream-json --verbose" in command
    assert BUILD_INSTRUCTION in command  # instruction on argv; mission stays on stdin


def test_dispatch_within_budget_logs_stream(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("LAB_SSH_HOST", raising=False)
    proc = FakeProc([usage_line(100), json.dumps({"type": "result"})])
    missions: list[str] = []

    def spawn(mission, argv):
        missions.append(mission)
        assert argv[0] == "ssh"
        return proc

    result = dispatch(repo, "tiny mission", spawn=spawn)
    assert missions == ["tiny mission"]
    assert not result.breaker_tripped
    assert not proc.killed
    assert result.exit_code == 0
    assert result.tokens_used == 100
    assert result.token_budget == DEFAULT_TOKEN_BUDGET
    assert result.run_log.parent == repo / RUN_LOG_DIR_REL
    log = result.run_log.read_text(encoding="utf-8")
    assert usage_line(100) in log


def test_dispatch_breaker_trips_kills_and_sweeps_remote(
    repo: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.delenv("LAB_SSH_HOST", raising=False)
    proc = FakeProc([usage_line(300), usage_line(300)])
    sweeps: list[list[str]] = []

    def runner(argv, **kwargs):
        sweeps.append(argv)
        return completed()

    result = dispatch(
        repo, "runaway mission", token_budget=500, spawn=lambda m, a: proc, runner=runner
    )
    assert result.breaker_tripped
    assert proc.killed
    assert result.exit_code == 1
    assert result.tokens_used == 600
    assert len(sweeps) == 1 and 'pkill -f "claude -p"' in sweeps[0][-1]
    log = result.run_log.read_text(encoding="utf-8")
    assert "circuit-breaker" in log
    assert "token budget exceeded" in log
