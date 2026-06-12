"""Remote trigger pathway: Telegram long-poll channel + RTC self-wake duty cycle (ADR-018).

The owner messages a Telegram bot; a `labctl trigger` loop drains the queue via
``getUpdates`` (outbound HTTPS only — no webhook, no inbound port), executes
allowlisted commands, replies on the same chat, then suspends the host with an
RTC alarm armed so the box wakes itself every N minutes (ADR-018). Missions run
on the established capsule machinery: mission text travels on stdin, never argv
or shell (ADR-015), metered through stream-json with the token circuit breaker
armed (ADR-016).

The bot token and the numeric user-id allowlist live in the environment or the
gitignored ``.env`` — never in tracked files, never in logs or error messages.
Run logs, the command audit trail, the getUpdates offset, and the
suspend-inhibit marker live under ``artifacts/trigger-runs/`` (gitignored).
"""

from __future__ import annotations

import getpass
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

from labctl import usage as usage_mod
from labctl.capsule import (
    DEFAULT_TOKEN_BUDGET,
    BuildResult,
    _kill_build,
    _spawn_claude,
    monitor_stream,
)
from labctl.lab import _breaker_record, _env_or_dotenv

RUN_DIR_REL = "artifacts/trigger-runs"
MAX_MISSION_CHARS = 4000
REPLY_LIMIT = 4096
API_BASE = "https://api.telegram.org"

SYSTEMD_TEMPLATE_REL = "templates/trigger-systemd/substrateos-trigger.service"
SYSTEMD_UNIT_NAME = "substrateos-trigger"
SYSTEMD_UNIT_DEST = f"/etc/systemd/system/{SYSTEMD_UNIT_NAME}.service"

UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

HELP_TEXT = (
    "commands: /status | /run <mission> | /usage | /stay [minutes] | /sleep | /help"
)


class TriggerError(RuntimeError):
    """Trigger operation cannot proceed; the message is user-actionable."""


@dataclass(frozen=True)
class TriggerConfig:
    token: str | None
    allowed_user_ids: frozenset[int]
    poll_timeout: int = 25
    wake_interval_min: int = 10
    linger_seconds: int = 90
    token_budget: int = DEFAULT_TOKEN_BUDGET


def _int_var(root: Path, var: str, default: int) -> int:
    raw = _env_or_dotenv(root, var)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise TriggerError(f"{var} must be an integer, got {raw!r}") from exc


def _allowed_user_ids(root: Path) -> frozenset[int]:
    """Numeric Telegram user ids only: usernames are spoofable/reassignable (ADR-018)."""
    raw = _env_or_dotenv(root, "TRIGGER_ALLOWED_USER_IDS") or ""
    ids: set[int] = set()
    for entry in raw.split(","):
        entry = entry.strip()
        if not entry:
            continue
        if not entry.isdigit():
            raise TriggerError(
                f"TRIGGER_ALLOWED_USER_IDS entry is not a numeric Telegram user id: {entry!r}"
            )
        ids.add(int(entry))
    return frozenset(ids)


def load_trigger_config(root: Path) -> TriggerConfig:
    return TriggerConfig(
        token=_env_or_dotenv(root, "TRIGGER_TELEGRAM_TOKEN"),
        allowed_user_ids=_allowed_user_ids(root),
        poll_timeout=_int_var(root, "TRIGGER_POLL_TIMEOUT", 25),
        wake_interval_min=_int_var(root, "TRIGGER_WAKE_INTERVAL_MIN", 10),
        linger_seconds=_int_var(root, "TRIGGER_LINGER_SECONDS", 90),
        token_budget=_int_var(root, "TRIGGER_TOKEN_BUDGET", DEFAULT_TOKEN_BUDGET),
    )


# --- transport ----------------------------------------------------------------

# (method, params) -> full Telegram envelope dict {"ok": bool, "result": ...}
HttpCall = Callable[[str, dict], dict]


def _default_http(token: str, method: str, params: dict) -> dict:
    """POST one Bot API method over stdlib urllib; returns the decoded envelope.

    The token never appears in errors: messages cite the redacted URL only,
    and exception chaining is severed (urllib errors carry the full URL).
    """
    url = f"{API_BASE}/bot{token}/{method}"
    redacted = f"{API_BASE}/bot<redacted>/{method}"
    # Poll-aware timeout: a getUpdates long poll holds the connection open for
    # params["timeout"] seconds, so allow that plus headroom.
    timeout = max(30, int(params.get("timeout") or 0) + 10)
    try:
        request = urllib.request.Request(
            url,
            data=json.dumps(params).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        # nosemgrep: python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected -- scheme is the https:// constant API_BASE; token/method only join the path
        with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec B310
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raise TriggerError(f"telegram HTTP {exc.code} from {redacted}") from None
    except ValueError:  # InvalidURL et al. quote the token-bearing URL verbatim
        raise TriggerError(f"telegram request invalid (malformed token?) at {redacted}") from None
    except OSError as exc:  # URLError, timeouts, refused connections
        reason = getattr(exc, "reason", None) or exc.__class__.__name__
        raise TriggerError(f"telegram unreachable ({reason}) at {redacted}") from None
    try:
        envelope = json.loads(body)
    except json.JSONDecodeError:
        raise TriggerError(f"telegram returned non-JSON from {redacted}") from None
    if not isinstance(envelope, dict):
        raise TriggerError(f"telegram returned a non-object envelope from {redacted}")
    return envelope


def api_call(token: str, method: str, params: dict, http: HttpCall | None = None) -> dict | list:
    """One Bot API call; returns the ``result`` payload of the envelope."""
    call: HttpCall = http or (lambda m, p: _default_http(token, m, p))
    envelope = call(method, params)
    if not isinstance(envelope, dict) or envelope.get("ok") is not True:
        description = ""
        if isinstance(envelope, dict):
            description = str(envelope.get("description") or "")
        raise TriggerError(
            f"telegram {method} failed: {description or 'ok != true'} "
            f"({API_BASE}/bot<redacted>/{method})"
        )
    return envelope.get("result")


def get_updates(token: str, offset: int, timeout: int, http: HttpCall | None = None) -> list[dict]:
    result = api_call(token, "getUpdates", {"offset": offset, "timeout": timeout}, http)
    if not isinstance(result, list):
        return []
    return [update for update in result if isinstance(update, dict)]


def send_message(token: str, chat_id: int, text: str, http: HttpCall | None = None) -> None:
    api_call(token, "sendMessage", {"chat_id": chat_id, "text": text[:REPLY_LIMIT]}, http)


# --- command grammar ------------------------------------------------------------


def parse_command(text: str) -> tuple[str, str]:
    """Split a chat message into (verb, argument).

    ``/run build X`` -> ("run", "build X"); the verb is lowercased and any
    ``@botname`` suffix is stripped (Telegram appends it in group chats).
    Anything not starting with "/" maps to ("help", "").
    """
    text = text.strip()
    if not text.startswith("/"):
        return ("help", "")
    parts = text[1:].split(maxsplit=1)
    verb = parts[0].split("@", 1)[0].lower() if parts else ""
    arg = parts[1].strip() if len(parts) > 1 else ""
    return (verb or "help", arg)


# --- run-dir state: offset, audit trail, inhibit marker --------------------------


def _run_dir(root: Path) -> Path:
    run_dir = root / RUN_DIR_REL
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def read_offset(root: Path) -> int:
    """Last processed update_id; 0 when none recorded yet."""
    try:
        return int((root / RUN_DIR_REL / "offset").read_text(encoding="utf-8").strip())
    except (FileNotFoundError, ValueError):
        return 0


def write_offset(root: Path, update_id: int) -> None:
    """Persist the high-water update_id so no update is ever replayed."""
    (_run_dir(root) / "offset").write_text(str(update_id), encoding="utf-8")


def audit(root: Path, **fields) -> None:
    """Append one JSON line to the audit trail. NEVER includes the bot token."""
    record = {"utc": datetime.now(UTC).strftime(UTC_FORMAT), **fields}
    with (_run_dir(root) / "audit.jsonl").open("a", encoding="utf-8") as log:
        log.write(json.dumps(record) + "\n")


def inhibit_until(root: Path) -> datetime | None:
    """Suspend-inhibit deadline, or None when the marker is missing or unparseable.

    Expiry is judged by `suspend_guard_reason` (which receives an injectable
    ``now``); this reader stays clock-free for deterministic tests.
    """
    try:
        stamp = (root / RUN_DIR_REL / "inhibit-until").read_text(encoding="utf-8").strip()
        deadline = datetime.fromisoformat(stamp)
    except (FileNotFoundError, ValueError):
        return None
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=UTC)
    return deadline


def set_inhibit(root: Path, minutes: int, now: datetime) -> datetime:
    """Arm the suspend-inhibit marker; returns the deadline (second precision)."""
    deadline = (now + timedelta(minutes=minutes)).replace(microsecond=0)
    (_run_dir(root) / "inhibit-until").write_text(
        deadline.strftime(UTC_FORMAT), encoding="utf-8"
    )
    return deadline


# --- mission execution -----------------------------------------------------------


def run_local_mission(
    root: Path,
    mission: str,
    token_budget: int,
    spawn: Callable[[str, Path], subprocess.Popen[str]] | None = None,
) -> BuildResult:
    """Run a metered headless claude mission in the repo with the breaker armed.

    Reuses the capsule machinery end to end: mission on stdin only — never argv
    beyond the fixed BUILD_INSTRUCTION, never shell (ADR-015) — stream-json
    metering and the token circuit breaker (ADR-016). The run log lives under
    ``artifacts/trigger-runs/`` so killed runs keep their evidence.
    """
    if len(mission) > MAX_MISSION_CHARS:
        raise TriggerError(
            f"mission too long: {len(mission)} chars (cap {MAX_MISSION_CHARS})"
        )
    started = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_log = _run_dir(root) / f"run-{started}.jsonl"

    proc = (spawn or _spawn_claude)(mission, root)
    assert proc.stdout is not None
    with run_log.open("a", encoding="utf-8") as log:
        tokens_used, tripped = monitor_stream(
            proc.stdout, token_budget, lambda line: log.write(line + "\n")
        )
        if tripped:
            _kill_build(proc)
            log.write(_breaker_record(tokens_used, token_budget) + "\n")
            return BuildResult(tokens_used, token_budget, True, 1, run_log)
    exit_code = proc.wait()
    return BuildResult(tokens_used, token_budget, False, exit_code, run_log)


# --- suspend guards and RTC alarm ------------------------------------------------


def suspend_guard_reason(root: Path, sessions: str, now: datetime) -> str | None:
    """Reason suspend must be blocked, or None when clear to suspend.

    ``sessions`` is the output of ``who``. A running mission never reaches
    this check: the duty cycle is sequential (drain -> mission -> guard).
    """
    if sessions.strip():
        return "interactive session active"
    deadline = inhibit_until(root)
    if deadline is not None and deadline > now:
        return f"inhibited until {deadline.strftime(UTC_FORMAT)}"
    return None


def suspend_with_alarm(
    seconds: int,
    runner: Callable[..., subprocess.CompletedProcess] | None = None,
) -> None:
    """Suspend to RAM (S3, never poweroff) with the RTC alarm armed.

    This call BLOCKS across the suspend: rtcwake returns only after the box
    resumes (RTC alarm or magic packet), so the caller continues exactly where
    it left off post-wake.
    """
    proc = (runner or subprocess.run)(
        ["sudo", "-n", "rtcwake", "-m", "mem", "-s", str(seconds)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or "").strip() or f"rtcwake exited {proc.returncode}"
        raise TriggerError(f"suspend failed: {detail}")


# --- command handling ------------------------------------------------------------


def _run_quiet(
    runner: Callable[..., subprocess.CompletedProcess] | None, argv: list[str]
) -> str:
    """stdout of argv via the injected runner; "unknown" on any failure."""
    try:
        proc = (runner or subprocess.run)(argv, capture_output=True, text=True)
    except OSError:
        return "unknown"
    if proc.returncode != 0:
        return "unknown"
    return (proc.stdout or "").strip() or "unknown"


def _status_reply(
    root: Path,
    config: TriggerConfig,
    runner: Callable[..., subprocess.CompletedProcess] | None,
) -> str:
    deadline = inhibit_until(root)
    inhibit = (
        f"until {deadline.strftime(UTC_FORMAT)}"
        if deadline is not None and deadline > datetime.now(UTC)
        else "none"
    )
    return "\n".join(
        [
            f"host: {_run_quiet(runner, ['hostname'])}",
            f"uptime: {_run_quiet(runner, ['uptime', '-p'])}",
            f"repo: {_run_quiet(runner, ['git', '-C', str(root), 'log', '-1', '--format=%h-%cs'])}",
            f"inhibit: {inhibit}",
            f"wake interval: {config.wake_interval_min} min",
        ]
    )


def handle_command(
    root: Path,
    config: TriggerConfig,
    verb: str,
    arg: str,
    *,
    spawn: Callable[[str, Path], subprocess.Popen[str]] | None = None,
    runner: Callable[..., subprocess.CompletedProcess] | None = None,
) -> str:
    """Execute one authorized command; always returns the reply text, never raises."""
    if verb == "status":
        return _status_reply(root, config, runner)
    if verb == "run":
        if not arg:
            return "usage: /run <mission text>"
        try:
            result = run_local_mission(root, arg, config.token_budget, spawn=spawn)
        except TriggerError as exc:
            return str(exc)
        if result.breaker_tripped:
            return (
                f"CIRCUIT BREAKER: token budget exceeded "
                f"({result.tokens_used}/{result.token_budget}), mission terminated"
            )
        return (
            f"mission complete: exit {result.exit_code}, "
            f"tokens {result.tokens_used}/{result.token_budget}, log {result.run_log.name}"
        )
    if verb == "usage":
        return usage_mod.render(usage_mod.collect_usage(root))
    if verb == "stay":
        try:
            minutes = int(arg) if arg else 60
        except ValueError:
            return "usage: /stay [minutes]"
        minutes = max(1, min(minutes, 1440))
        deadline = set_inhibit(root, minutes, datetime.now(UTC))
        return f"staying awake until {deadline.strftime(UTC_FORMAT)}"
    if verb == "sleep":
        return f"suspending now; next wake in {config.wake_interval_min} min"
    return HELP_TEXT


# --- duty cycle ------------------------------------------------------------------


def drain_updates(
    root: Path,
    config: TriggerConfig,
    *,
    http: HttpCall | None = None,
    spawn: Callable[[str, Path], subprocess.Popen[str]] | None = None,
    runner: Callable[..., subprocess.CompletedProcess] | None = None,
    send: Callable[[int, str], None] | None = None,
    poll_timeout: int = 1,
) -> dict:
    """One drain of the update queue (short poll by default; listen mode passes
    the configured long-poll timeout).

    Returns {"processed": <handled allowed updates>, "sleep_requested": bool}.
    The offset is advanced and persisted for EVERY update — denied and
    malformed included — so nothing is ever replayed. Unauthorized senders are
    audited and silently dropped (no reply: no oracle for token-guessers, and
    strangers cannot extend the listen window).
    """
    token = config.token
    if token is None:
        raise TriggerError("trigger not configured (TRIGGER_TELEGRAM_TOKEN missing)")
    send_fn = send or (lambda chat_id, text: send_message(token, chat_id, text, http))

    processed = 0
    sleep_requested = False
    for update in get_updates(token, read_offset(root) + 1, poll_timeout, http):
        update_id = update.get("update_id")
        if isinstance(update_id, int):
            write_offset(root, update_id)
        message = update.get("message") or {}
        user_id = (message.get("from") or {}).get("id")
        chat_id = (message.get("chat") or {}).get("id")
        text = message.get("text")
        well_formed = (
            isinstance(user_id, int) and isinstance(chat_id, int) and isinstance(text, str)
        )
        if not well_formed:
            audit(root, update_id=update_id, user_id=user_id, chat_id=chat_id,
                  verdict="malformed", verb=None)
            continue
        verb, arg = parse_command(text)
        if user_id not in config.allowed_user_ids:
            audit(root, update_id=update_id, user_id=user_id, chat_id=chat_id,
                  verdict="denied", verb=verb)
            continue
        audit(root, update_id=update_id, user_id=user_id, chat_id=chat_id,
              verdict="allowed", verb=verb)
        if verb == "run":
            # Missions block for minutes; acknowledge before executing.
            send_fn(chat_id, f"mission accepted (budget {config.token_budget} tokens)")
        send_fn(chat_id, handle_command(root, config, verb, arg, spawn=spawn, runner=runner))
        processed += 1
        if verb == "sleep":
            sleep_requested = True
    return {"processed": processed, "sleep_requested": sleep_requested}


def _who(runner: Callable[..., subprocess.CompletedProcess] | None) -> str:
    proc = (runner or subprocess.run)(["who"], capture_output=True, text=True)
    return proc.stdout or ""


def cycle_once(
    root: Path,
    config: TriggerConfig,
    *,
    http: HttpCall | None = None,
    spawn: Callable[[str, Path], subprocess.Popen[str]] | None = None,
    runner: Callable[..., subprocess.CompletedProcess] | None = None,
    clock: Callable[[], float] | None = None,
    sleep: Callable[[float], None] | None = None,
    suspend: Callable[[int], None] | None = None,
    sessions_fn: Callable[[], str] | None = None,
    dry_run: bool = False,
) -> dict:
    """One duty cycle: drain for the linger window, then guard-checked suspend.

    Activity (handled commands) extends the window by another linger_seconds;
    a /sleep command short-circuits it. Returns {"suspended": bool, ...} with
    the guard reason when suspend was blocked.
    """
    clock_fn = clock or time.monotonic
    sleep_fn = sleep or time.sleep
    suspend_fn = suspend or suspend_with_alarm

    deadline = clock_fn() + config.linger_seconds
    while True:
        drained = drain_updates(root, config, http=http, spawn=spawn, runner=runner)
        if drained["sleep_requested"]:
            break
        if drained["processed"]:
            deadline = clock_fn() + config.linger_seconds
        if clock_fn() >= deadline:
            break
        sleep_fn(2.0)

    sessions = sessions_fn() if sessions_fn is not None else _who(runner)
    reason = suspend_guard_reason(root, sessions, datetime.now(UTC))
    if reason:
        return {"suspended": False, "reason": reason}
    if dry_run:
        return {
            "suspended": False,
            "reason": "dry-run",
            "would_suspend_s": config.wake_interval_min * 60,
        }
    suspend_fn(config.wake_interval_min * 60)
    return {"suspended": True, "reason": None}


def run_cycle(
    root: Path,
    config: TriggerConfig,
    *,
    http: HttpCall | None = None,
    spawn: Callable[[str, Path], subprocess.Popen[str]] | None = None,
    runner: Callable[..., subprocess.CompletedProcess] | None = None,
    clock: Callable[[], float] | None = None,
    sleep: Callable[[float], None] | None = None,
    suspend: Callable[[int], None] | None = None,
    sessions_fn: Callable[[], str] | None = None,
    dry_run: bool = False,
    iterations: int | None = None,
) -> dict | None:
    """Run duty cycles forever (`iterations` bounds it for tests / --once).

    A suspended iteration resumes here after wake and rolls straight into the
    next cycle; a guard-blocked iteration sleeps 60s before retrying. Returns
    the last cycle outcome.
    """
    sleep_fn = sleep or time.sleep
    outcome: dict | None = None
    count = 0
    while iterations is None or count < iterations:
        outcome = cycle_once(
            root, config, http=http, spawn=spawn, runner=runner, clock=clock,
            sleep=sleep, suspend=suspend, sessions_fn=sessions_fn, dry_run=dry_run,
        )
        count += 1
        if not outcome["suspended"] and (iterations is None or count < iterations):
            sleep_fn(60.0)
    return outcome


def run_listen(
    root: Path,
    config: TriggerConfig,
    *,
    http: HttpCall | None = None,
    spawn: Callable[[str, Path], subprocess.Popen[str]] | None = None,
    runner: Callable[..., subprocess.CompletedProcess] | None = None,
    sleep: Callable[[float], None] | None = None,
    iterations: int | None = None,
) -> int:
    """Drain loop without ever suspending (dev / always-on mode).

    Uses the configured getUpdates long poll (TRIGGER_POLL_TIMEOUT) so the
    connection is held server-side instead of hammering short polls. Returns
    the total number of handled commands (`iterations` bounds the loop for
    tests / --once).
    """
    sleep_fn = sleep or time.sleep
    processed = 0
    count = 0
    while iterations is None or count < iterations:
        processed += drain_updates(
            root, config, http=http, spawn=spawn, runner=runner,
            poll_timeout=config.poll_timeout,
        )["processed"]
        count += 1
        if iterations is None or count < iterations:
            sleep_fn(2.0)
    return processed


# --- systemd install -------------------------------------------------------------


def install_systemd_unit(
    root: Path,
    runner: Callable[..., subprocess.CompletedProcess] | None = None,
) -> list[str]:
    """Render the unit template, install and enable it via sudo -n.

    Substitutes __TRIGGER_USER__/__TRIGGER_REPO__/__TRIGGER_VENV__, copies the
    rendered unit to /etc/systemd/system, reloads systemd, and enables the
    service. Never starts it: it runs at next boot/resume. Returns the actions
    performed, for the CLI to print.
    """
    run = runner or subprocess.run
    template = root / SYSTEMD_TEMPLATE_REL
    if not template.is_file():
        raise TriggerError(f"systemd unit template missing: {template}")
    text = template.read_text(encoding="utf-8")
    text = text.replace("__TRIGGER_USER__", getpass.getuser())
    text = text.replace("__TRIGGER_REPO__", str(root.resolve()))
    text = text.replace("__TRIGGER_VENV__", sys.prefix)
    rendered = _run_dir(root) / f"{SYSTEMD_UNIT_NAME}.service"
    rendered.write_text(text, encoding="utf-8")

    actions = [f"rendered unit: {rendered}"]
    steps = (
        (["sudo", "-n", "cp", str(rendered), SYSTEMD_UNIT_DEST],
         f"installed: {SYSTEMD_UNIT_DEST}"),
        (["sudo", "-n", "systemctl", "daemon-reload"], "systemd daemon reloaded"),
        (["sudo", "-n", "systemctl", "enable", SYSTEMD_UNIT_NAME],
         f"enabled: {SYSTEMD_UNIT_NAME} (not started; runs at next boot/resume)"),
    )
    for argv, action in steps:
        proc = run(argv, capture_output=True, text=True)
        if proc.returncode != 0:
            detail = (proc.stderr or "").strip() or f"exit {proc.returncode}"
            raise TriggerError(f"{' '.join(argv)} failed: {detail}")
        actions.append(action)
    return actions
