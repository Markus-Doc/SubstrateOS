"""Deterministic tests for the remote trigger pathway (ADR-018).

Everything is injected — http transport, subprocess runner, claude spawn,
clock, sleep, suspend — so no test can touch the network, spawn claude, or
suspend the machine.
"""

import getpass
import json
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from typer.testing import CliRunner

from labctl.capsule import DEFAULT_TOKEN_BUDGET
from labctl.cli import app
from labctl.trigger import (
    MAX_MISSION_CHARS,
    REPLY_LIMIT,
    RUN_DIR_REL,
    UTC_FORMAT,
    TriggerConfig,
    TriggerError,
    api_call,
    cycle_once,
    drain_updates,
    get_updates,
    handle_command,
    inhibit_until,
    install_systemd_unit,
    load_trigger_config,
    parse_command,
    read_offset,
    run_local_mission,
    send_message,
    set_inhibit,
    suspend_guard_reason,
    suspend_with_alarm,
    write_offset,
)

TRIGGER_VARS = (
    "TRIGGER_TELEGRAM_TOKEN",
    "TRIGGER_ALLOWED_USER_IDS",
    "TRIGGER_POLL_TIMEOUT",
    "TRIGGER_WAKE_INTERVAL_MIN",
    "TRIGGER_LINGER_SECONDS",
    "TRIGGER_TOKEN_BUDGET",
)

SECRET_TOKEN = "123456:SECRET-bot-token"  # fake credential, exists to prove redaction
ALLOWED_ID = 777


@pytest.fixture(autouse=True)
def _clean_trigger_env(monkeypatch: pytest.MonkeyPatch):
    """No real trigger configuration may leak into any test."""
    for var in TRIGGER_VARS:
        monkeypatch.delenv(var, raising=False)


def config_for(**overrides) -> TriggerConfig:
    fields = {"token": SECRET_TOKEN, "allowed_user_ids": frozenset({ALLOWED_ID})}
    fields.update(overrides)
    return TriggerConfig(**fields)


def completed(
    stdout: str = "", returncode: int = 0, stderr: str = ""
) -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(
        args=["fake"], returncode=returncode, stdout=stdout, stderr=stderr
    )


def usage_line(tokens: int) -> str:
    return json.dumps(
        {"type": "assistant", "message": {"usage": {"input_tokens": tokens, "output_tokens": 0}}}
    )


def tg_update(update_id: int, user_id: int = ALLOWED_ID, chat_id: int = 4242,
              text: str = "/help") -> dict:
    return {
        "update_id": update_id,
        "message": {"from": {"id": user_id}, "chat": {"id": chat_id}, "text": text},
    }


class FakeProc:
    """Stand-in for a claude subprocess (mirrors test_capsule.FakeProc)."""

    def __init__(self, lines: list[str]):
        self.stdout = iter(lines)
        self.killed = False
        self.returncode = 0

    def kill(self):
        self.killed = True

    def wait(self):
        return self.returncode


class FakeHttp:
    """Telegram transport double: queued getUpdates batches, captured sends."""

    def __init__(self, batches: list[list[dict]] | None = None):
        self.batches = list(batches or [])
        self.calls: list[tuple[str, dict]] = []
        self.sent: list[tuple[int, str]] = []

    def __call__(self, method: str, params: dict) -> dict:
        self.calls.append((method, params))
        if method == "getUpdates":
            return {"ok": True, "result": self.batches.pop(0) if self.batches else []}
        if method == "sendMessage":
            self.sent.append((params["chat_id"], params["text"]))
        return {"ok": True, "result": {}}


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def read_audit(root: Path) -> list[dict]:
    path = root / RUN_DIR_REL / "audit.jsonl"
    if not path.is_file():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


# --- config -----------------------------------------------------------------


def test_config_defaults(repo: Path):
    config = load_trigger_config(repo)
    assert config.token is None  # missing token -> None, never an empty string
    assert config.allowed_user_ids == frozenset()
    assert config.poll_timeout == 25
    assert config.wake_interval_min == 10
    assert config.linger_seconds == 90
    assert config.token_budget == DEFAULT_TOKEN_BUDGET


def test_config_dotenv_and_env_precedence(repo: Path, monkeypatch: pytest.MonkeyPatch):
    (repo / ".env").write_text(
        f"TRIGGER_TELEGRAM_TOKEN={SECRET_TOKEN}\n"
        "TRIGGER_ALLOWED_USER_IDS=111, 222\n"
        "TRIGGER_POLL_TIMEOUT=20\n"
        "TRIGGER_WAKE_INTERVAL_MIN=5\n"
        "TRIGGER_LINGER_SECONDS=30\n"
        "TRIGGER_TOKEN_BUDGET=1000\n",
        encoding="utf-8",
    )
    config = load_trigger_config(repo)
    assert config.token == SECRET_TOKEN
    assert config.allowed_user_ids == frozenset({111, 222})
    assert config.poll_timeout == 20
    assert config.wake_interval_min == 5
    assert config.linger_seconds == 30
    assert config.token_budget == 1000

    monkeypatch.setenv("TRIGGER_WAKE_INTERVAL_MIN", "15")  # environment beats .env
    assert load_trigger_config(repo).wake_interval_min == 15


def test_config_rejects_non_numeric_allowlist_entry(repo: Path):
    # usernames are spoofable/reassignable (ADR-018): numeric ids only
    (repo / ".env").write_text("TRIGGER_ALLOWED_USER_IDS=111,@markus\n", encoding="utf-8")
    with pytest.raises(TriggerError, match="numeric"):
        load_trigger_config(repo)


# --- command grammar ----------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("hello there", ("help", "")),
        ("/run build X", ("run", "build X")),
        ("/STATUS", ("status", "")),
        ("/status@MyBot", ("status", "")),
        ("/run@MyBot build X", ("run", "build X")),
        ("  /sleep  ", ("sleep", "")),
    ],
)
def test_parse_command(text: str, expected: tuple[str, str]):
    assert parse_command(text) == expected


# --- transport ------------------------------------------------------------------


def test_api_call_returns_result_payload():
    def http(method, params):
        assert method == "getMe"
        return {"ok": True, "result": {"username": "SubstrateBot"}}

    assert api_call(SECRET_TOKEN, "getMe", {}, http) == {"username": "SubstrateBot"}


def test_api_call_failure_never_leaks_token():
    def http(method, params):
        return {"ok": False, "description": "Unauthorized"}

    with pytest.raises(TriggerError) as excinfo:
        api_call(SECRET_TOKEN, "getUpdates", {"offset": 1}, http)
    message = str(excinfo.value)
    assert "Unauthorized" in message
    assert SECRET_TOKEN not in message
    assert "SECRET" not in message
    assert "<redacted>" in message


def test_get_updates_drops_non_dict_entries():
    def http(method, params):
        return {"ok": True, "result": [{"update_id": 1}, "garbage", 7]}

    assert get_updates(SECRET_TOKEN, 1, 1, http) == [{"update_id": 1}]


def test_send_message_truncates_to_reply_limit():
    http = FakeHttp()
    send_message(SECRET_TOKEN, 42, "x" * (REPLY_LIMIT + 500), http)
    assert http.calls[0][0] == "sendMessage"
    (chat_id, text) = http.sent[0]
    assert chat_id == 42
    assert len(text) == REPLY_LIMIT


# --- offset persistence (replay protection) ----------------------------------------


def test_offset_roundtrip_and_missing_file(repo: Path):
    assert read_offset(repo) == 0  # nothing recorded yet
    write_offset(repo, 1234)
    assert read_offset(repo) == 1234
    assert (repo / RUN_DIR_REL / "offset").read_text(encoding="utf-8") == "1234"


def test_run_dir_is_gitignored():
    gitignore = Path(__file__).resolve().parents[2] / ".gitignore"
    assert f"{RUN_DIR_REL}/" in gitignore.read_text(encoding="utf-8")


# --- drain_updates ----------------------------------------------------------------


def test_drain_polls_from_last_offset_plus_one(repo: Path):
    write_offset(repo, 41)
    http = FakeHttp([[]])
    drain_updates(repo, config_for(), http=http)
    method, params = http.calls[0]
    assert method == "getUpdates"
    assert params["offset"] == 42
    assert params["timeout"] == 1  # short poll inside the listen window


def test_drain_denies_unknown_sender_silently(repo: Path):
    sent: list[tuple[int, str]] = []
    http = FakeHttp([[tg_update(7, user_id=666, text="/run rm everything")]])
    outcome = drain_updates(
        repo, config_for(), http=http, send=lambda chat_id, text: sent.append((chat_id, text))
    )
    assert outcome == {"processed": 0, "sleep_requested": False}
    assert sent == []  # silent drop: no oracle for strangers
    assert read_offset(repo) == 7  # offset persisted even when denied: no replay
    records = read_audit(repo)
    assert len(records) == 1
    assert records[0]["verdict"] == "denied"
    assert records[0]["user_id"] == 666
    assert records[0]["verb"] == "run"
    assert "utc" in records[0]
    audit_text = (repo / RUN_DIR_REL / "audit.jsonl").read_text(encoding="utf-8")
    assert SECRET_TOKEN not in audit_text  # the token is never audited


def test_drain_audits_malformed_update_and_advances_offset(repo: Path):
    sent: list[tuple[int, str]] = []
    http = FakeHttp([[{"update_id": 9, "message": {"chat": {"id": 1}}}]])  # no from/text
    outcome = drain_updates(
        repo, config_for(), http=http, send=lambda chat_id, text: sent.append((chat_id, text))
    )
    assert outcome == {"processed": 0, "sleep_requested": False}
    assert sent == []
    assert read_offset(repo) == 9
    assert read_audit(repo)[0]["verdict"] == "malformed"


def test_drain_authorized_status_audits_and_replies(repo: Path):
    http = FakeHttp([[tg_update(3, text="/status")]])

    def runner(argv, **kwargs):
        if argv == ["hostname"]:
            return completed(stdout="useragent\n")
        if argv[:2] == ["git", "-C"]:
            assert argv[2] == str(repo)
            return completed(stdout="b56f613-2026-06-12\n")
        return completed(stdout="up 2 hours\n")

    outcome = drain_updates(repo, config_for(), http=http, runner=runner)
    assert outcome == {"processed": 1, "sleep_requested": False}
    assert read_offset(repo) == 3
    [(chat_id, reply)] = http.sent  # default send path goes through the injected http
    assert chat_id == 4242
    assert "useragent" in reply
    assert "b56f613-2026-06-12" in reply
    assert read_audit(repo)[0]["verdict"] == "allowed"


# --- handle_command ----------------------------------------------------------------


def test_status_runner_failure_degrades_to_unknown(repo: Path):
    def runner(argv, **kwargs):
        return completed(returncode=1, stderr="boom")

    reply = handle_command(repo, config_for(), "status", "", runner=runner)  # never raises
    assert "unknown" in reply
    assert "wake interval: 10 min" in reply


def test_help_for_unknown_verb_lists_all_six_commands(repo: Path):
    reply = handle_command(repo, config_for(), "bogus", "")
    for command in ("/status", "/run", "/usage", "/stay", "/sleep", "/help"):
        assert command in reply


def test_usage_command_renders_usage_report(repo: Path):
    reply = handle_command(repo, config_for(), "usage", "")
    assert "no run logs found" in reply


def test_run_empty_arg_gives_usage_hint(repo: Path):
    reply = handle_command(
        repo, config_for(), "run", "",
        spawn=lambda mission, cwd: pytest.fail("spawn must not be called"),
    )
    assert reply.startswith("usage:")


# --- mission execution ---------------------------------------------------------------


def test_drain_run_acks_first_then_reports_completion(repo: Path):
    proc = FakeProc([usage_line(100), json.dumps({"type": "result"})])
    missions: list[tuple[str, Path]] = []

    def spawn(mission, cwd):
        missions.append((mission, cwd))
        return proc

    http = FakeHttp([[tg_update(5, text="/run build the thing")]])
    outcome = drain_updates(repo, config_for(token_budget=1000), http=http, spawn=spawn)
    assert outcome == {"processed": 1, "sleep_requested": False}
    assert missions == [("build the thing", repo)]  # mission via spawn stdin, cwd = repo root

    assert len(http.sent) == 2
    assert http.sent[0][1] == "mission accepted (budget 1000 tokens)"  # ack before execution
    reply = http.sent[1][1]
    assert "mission complete: exit 0, tokens 100/1000" in reply

    logs = list((repo / RUN_DIR_REL).glob("run-*.jsonl"))
    assert len(logs) == 1
    assert usage_line(100) in logs[0].read_text(encoding="utf-8")
    assert reply.endswith(f"log {logs[0].name}")

    records = read_audit(repo)
    assert records[0]["verdict"] == "allowed"
    assert records[0]["verb"] == "run"


def test_run_breaker_trips_kills_and_reports(repo: Path):
    proc = FakeProc([usage_line(300), usage_line(300)])
    reply = handle_command(
        repo, config_for(token_budget=500), "run", "runaway", spawn=lambda mission, cwd: proc
    )
    assert "CIRCUIT BREAKER" in reply
    assert "(600/500)" in reply
    assert proc.killed
    log = next((repo / RUN_DIR_REL).glob("run-*.jsonl")).read_text(encoding="utf-8")
    assert "circuit-breaker" in log
    assert "token budget exceeded" in log


def test_run_local_mission_rejects_long_mission_before_spawn(repo: Path):
    with pytest.raises(TriggerError, match="too long"):
        run_local_mission(
            repo, "x" * (MAX_MISSION_CHARS + 1), 1000,
            spawn=lambda mission, cwd: pytest.fail("spawn must not be called"),
        )
    assert not list((repo / RUN_DIR_REL).glob("run-*.jsonl"))


def test_run_command_over_cap_replies_error_without_spawn(repo: Path):
    reply = handle_command(
        repo, config_for(), "run", "x" * (MAX_MISSION_CHARS + 1),
        spawn=lambda mission, cwd: pytest.fail("spawn must not be called"),
    )
    assert "mission too long" in reply


# --- inhibit marker and suspend guards -------------------------------------------


def test_set_inhibit_roundtrip_deterministic(repo: Path):
    now = datetime(2026, 6, 12, 12, 0, tzinfo=UTC)
    deadline = set_inhibit(repo, 60, now)
    assert deadline == datetime(2026, 6, 12, 13, 0, tzinfo=UTC)
    assert inhibit_until(repo) == deadline


def test_inhibit_until_missing_or_garbage_is_none(repo: Path):
    assert inhibit_until(repo) is None
    (repo / RUN_DIR_REL).mkdir(parents=True)
    (repo / RUN_DIR_REL / "inhibit-until").write_text("not-a-timestamp", encoding="utf-8")
    assert inhibit_until(repo) is None


def test_stay_writes_inhibit_and_guard_blocks_until_deadline(repo: Path):
    reply = handle_command(repo, config_for(), "stay", "30")
    assert reply.startswith("staying awake until ")
    deadline = inhibit_until(repo)
    assert deadline is not None
    assert reply.endswith(deadline.strftime(UTC_FORMAT))

    before = deadline - timedelta(minutes=1)
    after = deadline + timedelta(seconds=1)
    reason = suspend_guard_reason(repo, "", before)
    assert reason == f"inhibited until {deadline.strftime(UTC_FORMAT)}"
    assert suspend_guard_reason(repo, "", after) is None  # expired marker clears the guard


def test_stay_caps_at_1440_minutes(repo: Path):
    handle_command(repo, config_for(), "stay", "999999")
    deadline = inhibit_until(repo)
    assert deadline is not None
    delta = deadline - datetime.now(UTC)
    assert timedelta(minutes=1439) < delta <= timedelta(minutes=1440)


def test_guard_blocks_on_interactive_session(repo: Path):
    now = datetime(2026, 6, 12, tzinfo=UTC)
    sessions = "markus   tty7         2026-06-12 09:00\n"
    assert suspend_guard_reason(repo, sessions, now) == "interactive session active"
    assert suspend_guard_reason(repo, "", now) is None
    assert suspend_guard_reason(repo, "   \n", now) is None  # whitespace is not a session


# --- suspend_with_alarm ---------------------------------------------------------


def test_suspend_with_alarm_exact_argv():
    calls: list[list[str]] = []

    def runner(argv, **kwargs):
        calls.append(argv)
        assert kwargs.get("capture_output") is True
        assert kwargs.get("text") is True
        return completed()

    suspend_with_alarm(600, runner=runner)
    assert calls == [["sudo", "-n", "rtcwake", "-m", "mem", "-s", "600"]]


def test_suspend_with_alarm_failure_raises_with_stderr():
    def runner(argv, **kwargs):
        return completed(returncode=1, stderr="rtcwake: permission denied")

    with pytest.raises(TriggerError, match="permission denied"):
        suspend_with_alarm(600, runner=runner)


# --- cycle_once ------------------------------------------------------------------


def test_cycle_dry_run_drains_window_then_reports(repo: Path):
    http = FakeHttp()  # every getUpdates returns an empty batch
    clock = FakeClock()
    sleeps: list[float] = []

    def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)
        clock.now += seconds

    outcome = cycle_once(
        repo,
        config_for(linger_seconds=4, wake_interval_min=10),
        http=http,
        clock=clock,
        sleep=fake_sleep,
        sessions_fn=lambda: "",
        suspend=lambda seconds: pytest.fail("dry-run must not suspend"),
        dry_run=True,
    )
    assert outcome == {"suspended": False, "reason": "dry-run", "would_suspend_s": 600}
    polls = [call for call in http.calls if call[0] == "getUpdates"]
    assert len(polls) >= 2  # kept draining across the listen window
    assert sleeps and all(gap == pytest.approx(2.0) for gap in sleeps)  # ~2s poll gap


def test_cycle_guard_blocked_returns_reason_without_suspend(repo: Path):
    suspends: list[int] = []
    outcome = cycle_once(
        repo,
        config_for(linger_seconds=0),
        http=FakeHttp(),
        clock=FakeClock(),
        sleep=lambda seconds: None,
        sessions_fn=lambda: "markus tty7 2026-06-12 09:00\n",
        suspend=suspends.append,
    )
    assert outcome == {"suspended": False, "reason": "interactive session active"}
    assert suspends == []


def test_cycle_sleep_command_short_circuits_window_and_suspends(repo: Path):
    http = FakeHttp([[tg_update(11, text="/sleep")]])
    suspends: list[int] = []
    outcome = cycle_once(
        repo,
        config_for(linger_seconds=3600, wake_interval_min=10),
        http=http,
        clock=FakeClock(),
        sleep=lambda seconds: pytest.fail("/sleep must short-circuit the window"),
        sessions_fn=lambda: "",
        suspend=suspends.append,
    )
    assert outcome["suspended"] is True
    assert suspends == [600]  # wake_interval_min * 60
    assert any("suspending now; next wake in 10 min" == text for _, text in http.sent)
    assert read_offset(repo) == 11


# --- CLI -------------------------------------------------------------------------


cli_runner = CliRunner()


def test_cli_listen_and_cycle_exit_zero_when_unconfigured(repo: Path, monkeypatch):
    monkeypatch.chdir(repo)
    for args in (["trigger", "listen", "--once"], ["trigger", "cycle", "--once"]):
        result = cli_runner.invoke(app, args)
        assert result.exit_code == 0  # systemd-friendly idle exit
        assert "trigger not configured (TRIGGER_TELEGRAM_TOKEN missing)" in result.output


def test_cli_trigger_status_reports_config(repo: Path, monkeypatch):
    monkeypatch.chdir(repo)
    (repo / ".env").write_text("TRIGGER_ALLOWED_USER_IDS=777\n", encoding="utf-8")
    result = cli_runner.invoke(app, ["trigger", "status"])
    assert result.exit_code == 0
    assert "token: MISSING" in result.output
    assert "allowlist: 1 user id(s)" in result.output
    assert "offset: 0" in result.output
    assert "inhibit: none" in result.output
    # --probe without a token fails fast: no network call possible
    result = cli_runner.invoke(app, ["trigger", "status", "--probe"])
    assert result.exit_code == 1


# --- systemd install ---------------------------------------------------------------


TEMPLATE_UNIT = (
    "[Service]\n"
    "User=__TRIGGER_USER__\n"
    "WorkingDirectory=__TRIGGER_REPO__\n"
    "ExecStart=__TRIGGER_VENV__/bin/labctl trigger cycle\n"
)


def write_template(repo: Path) -> None:
    template_dir = repo / "templates" / "trigger-systemd"
    template_dir.mkdir(parents=True)
    (template_dir / "substrateos-trigger.service").write_text(TEMPLATE_UNIT, encoding="utf-8")


def test_install_substitutes_placeholders_and_enables(repo: Path):
    write_template(repo)
    calls: list[list[str]] = []

    def runner(argv, **kwargs):
        calls.append(argv)
        return completed()

    actions = install_systemd_unit(repo, runner=runner)

    rendered = repo / RUN_DIR_REL / "substrateos-trigger.service"
    text = rendered.read_text(encoding="utf-8")
    assert "__TRIGGER_" not in text  # no placeholder survives substitution
    assert f"User={getpass.getuser()}" in text
    assert f"WorkingDirectory={repo.resolve()}" in text
    assert f"ExecStart={sys.prefix}/bin/labctl trigger cycle" in text

    assert calls == [
        ["sudo", "-n", "cp", str(rendered), "/etc/systemd/system/substrateos-trigger.service"],
        ["sudo", "-n", "systemctl", "daemon-reload"],
        ["sudo", "-n", "systemctl", "enable", "substrateos-trigger"],
    ]  # exactly install + reload + enable: the service is never started
    assert len(actions) == 4  # rendered, installed, reloaded, enabled — for the CLI to print


def test_install_missing_template_raises(repo: Path):
    with pytest.raises(TriggerError, match="template missing"):
        install_systemd_unit(repo, runner=lambda argv, **kwargs: completed())


def test_install_sudo_failure_raises(repo: Path):
    write_template(repo)

    def runner(argv, **kwargs):
        return completed(returncode=1, stderr="sudo: a password is required")

    with pytest.raises(TriggerError, match="password is required"):
        install_systemd_unit(repo, runner=runner)
