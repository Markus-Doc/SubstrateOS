# ADR-018: Remote trigger pathway — Telegram bot + RTC self-wake duty cycle + Tailscale (resolves OQ-007)

Date: 2026-06-12
Status: Accepted

## Decision

The owner chose the remote trigger pathway (2026-06-12), closing OQ-007.
Three coupled choices:

1. **Channel: Telegram bot, long-polling.** A `labctl trigger` loop polls the
   Telegram Bot API (`getUpdates`, outbound HTTPS only) and replies on the
   same chat. No webhook, no inbound port, no public endpoint. Commands are
   accepted only from an allowlisted Telegram user id; everything else is
   logged and ignored. The bot token and allowlist live in the gitignored
   `.env` (`TRIGGER_TELEGRAM_TOKEN`, `TRIGGER_ALLOWED_USER_IDS`), never in
   tracked files.
2. **Wake: RTC self-wake duty cycle.** A magic packet must originate on the
   LAN, and no always-on relay device exists. Instead of a relay, the box
   wakes itself: the trigger loop suspends the host with an RTC alarm armed
   (`rtcwake -m mem -s <interval>`), wakes every N minutes (default 10),
   drains the Telegram queue, executes any mission, then re-suspends.
   Wake-on-demand becomes bounded-latency polling (worst case = one
   interval). True WoL from the control plane (`labctl lab wake`) is
   unchanged and composes: any resume — RTC or magic packet — returns
   control to the same loop.
3. **Tunnel: Tailscale.** Already enrolled on the box (`useragent`) and the
   owner's iPhone; Tailscale SSH is enabled on the box as the direct command
   and emergency path. WireGuard-based, no exposed public ports. Funnel
   stays off unless a future channel needs public HTTPS ingress.

## Context

OQ-007 asked how the owner triggers the Lab operator (ADR-017) when away
from the control plane, flow: message arrives → box wakes → mission
dispatched → result reported back on the same channel. Candidates were
iMessage (hardware-blocked: no always-on Mac), WhatsApp (requires Meta
Business webhook ingress), Telegram, and Claude routines (cloud agents
cannot reach the LAN or wake the box).

Telegram long-polling is the only candidate that is simultaneously: free,
reachable from any device, zero-inbound-exposure (outbound HTTPS only, works
behind NAT with no tunnel in the data path), and implementable with the
standard library. The RTC duty cycle is the only wake design that needs no
new hardware, no router configuration, and no inbound exposure; the NIC
keeps magic-packet wake armed (`Wake-on: g`) so the existing control-plane
WoL path still gives instant wake at home.

Constraints honoured: subscription auth only — the Telegram bot token is a
channel secret, not an LLM credential; mission execution stays on the
established capsule machinery (mission on stdin per ADR-015, stream-json
metering and the token circuit breaker per ADR-016); the `labctl` surface
remains the execution path (new `trigger` command group); no secrets in
tracked files.

## Consequences

- New `labctl trigger` command group (`cycle`, `listen`, `status`) in
  `scripts/labctl/trigger.py`; stdlib `urllib` transport, injectable for
  deterministic tests (no network, no AI runtime in the suite).
- Missions from the channel run as metered local headless claude runs
  (ADR-015/016 machinery), run logs and a command audit trail (every
  received update with its allow/deny verdict) under
  `artifacts/trigger-runs/` (gitignored).
- Suspend guards: the loop never suspends while a mission is running, an
  interactive login session is active, or a suspend-inhibit marker is set
  (`/run` command `/stay`). Suspend remains S3, never poweroff (ADR-017
  amendment).
- A systemd unit template runs the cycle at boot/resume; phase-2-plan gains
  Milestone 7 with the checklist; OQ-007 is closed; CLAUDE.md scope updated.
- Threat model expands (SECURITY.md): bot-token theft, sender spoofing,
  hostile mission text. Mitigations: token outside the repo, numeric-id
  allowlist (not usernames, which are spoofable/reassignable), mission text
  travels stdin-only (never shell-interpolated), per-run token budget,
  single mission at a time, length cap, full audit log.
- Worst-case command latency equals the wake interval; the owner can keep
  the box awake with `/stay` or wake it instantly at home via `labctl lab
  wake`.
