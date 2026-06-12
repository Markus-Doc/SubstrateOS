# Security Policy

## Reporting a Vulnerability

Please report vulnerabilities privately via **GitHub's private vulnerability
reporting** on this repository (Security tab → "Report a vulnerability").
Do not open public issues for security findings.

Alternatively, use the contact form at https://www.markuswalker.com.

You should receive an acknowledgement within a few days. Please include
reproduction steps and the affected component (`labctl` command, module, or
configuration).

## Scope

SubstrateOS is a local-first orchestration harness. The security-relevant
surfaces are:

- the release gate (`labctl gate`): secret scan, SAST, dependency/vuln scan
- capsule isolation guarantees (`templates/capsule-devcontainer/README.md`)
- the Lab host operator channel (ssh, ADR-017) — key-based, BatchMode only
- the remote trigger channel (`labctl trigger`, ADR-018) — Telegram
  long-poll, numeric-id allowlist only

No secrets, keys, or credentials are ever committed to this repository; all
machine-specific configuration lives in the gitignored `.env`.

## Remote trigger pathway (ADR-018)

The remote trigger lets the owner message the Lab box from anywhere and have
missions executed and answered on the same chat.

**Assets.** The Telegram bot token, and the authority to execute missions on
the Lab box.

**Attack surface.** The Telegram channel only: the trigger loop makes
outbound HTTPS long-poll requests to the Bot API. No webhook, no inbound
port, no public endpoint.

**Threats and mitigations.**

- **Bot-token theft.** The token lives only in the gitignored `.env`
  (`TRIGGER_TELEGRAM_TOKEN`), never in tracked files; it is never logged or
  echoed, and is redacted from error messages.
- **Sender spoofing.** Commands are accepted only from numeric Telegram user
  ids on the allowlist (`TRIGGER_ALLOWED_USER_IDS`) — never usernames, which
  are spoofable and reassignable. Updates from unlisted ids are silently
  dropped (no reply that would confirm the bot exists) and recorded in the
  audit log.
- **Hostile mission text.** Mission text is delivered to the claude run on
  stdin only and is never shell-interpolated; it is capped at 4000
  characters; every run is metered against the per-run token budget circuit
  breaker (ADR-016); only a single mission runs at a time, sequentially; and
  every received update with its allow/deny verdict plus every run log lands
  in the audit trail under `artifacts/trigger-runs/` (gitignored).
- **Replay.** The long-poll update offset is persisted, so already-processed
  updates are never fetched or executed again after a restart or wake.
- **Availability.** Suspend guards keep the duty cycle from sleeping under a
  running mission or an active interactive session, and suspend is S3 only —
  never poweroff — so the box always comes back on the next RTC alarm or
  Wake-on-LAN packet.
