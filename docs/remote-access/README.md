# Lab Remote Access — Telegram control + Tailscale SSH (bolt-on)

> **This is NOT SubstrateOS-base.** It is a separable bolt-on feature: how the
> owner remotely connects, from anywhere, straight to the lab's `subos`/Claude
> session running on the host `useragent`. It sits *beside* SubstrateOS, reuses
> the `labctl` surface, and is a candidate to be **extracted into its own
> "homelab AI" project** later (see [Extraction](#extraction--future-home)).
>
> Decision records: [ADR-017](../decisions/ADR-017-lab-host-remote-agent-operator.md)
> (lab host as remote agent operator) and
> [ADR-018](../decisions/ADR-018-remote-trigger-telegram-rtc-duty-cycle.md)
> (Telegram + RTC + Tailscale). Build evidence:
> [m7-trigger-build-gate](../../artifacts/evidence/m7-trigger-build-gate.md).

## Goal

Be in the office (or anywhere), pull out a phone, and either:
- **drive the lab interactively** — SSH into `useragent` and land in the
  `subos`/Claude session, or
- **fire a lightweight control/status message** — over Telegram, even when not
  ready to open a shell.

No port-forwarding, no public endpoint, no separately-billed API: the lab runs
Claude under the owner's **Max subscription**, not a metered API key.

## Architecture — control plane vs data plane

The two channels are complementary, not competing. This split is the core mental
model:

| Plane | Channel | Job | Works when box is asleep? |
|-------|---------|-----|---------------------------|
| **Control** | Telegram bot (long-poll) | wake / check status / queue a task | **Yes** — message queues until the box next polls |
| **Data** | Tailscale SSH (Termius) | the real interactive `subos`/Claude session | **No** — box must be awake and on the tailnet |

- **Telegram = control plane.** Outbound HTTPS long-poll only (`getUpdates`),
  no inbound port, no public URL. Tiny messages. Use it to confirm the box is
  up and, if needed, to keep it awake before you SSH.
- **Tailscale SSH = data plane.** WireGuard mesh; the phone and the box share a
  tailnet regardless of physical network. This is where real work happens.

Typical flow from outside the LAN: **(optional) Telegram `/status` to confirm
reachable → SSH in via Termius → land in `subos`/Claude → work (incl. iPhone
native voice-to-text typed straight into the session).**

## Established & verified

Confirmed working as of 2026-06-13:

- **External SSH from anywhere** — verified over **LTE (cellular, off home
  Wi-Fi)** via Termius using the **hostname `useragent`** (Tailscale MagicDNS).
  Tailscale makes "same network" irrelevant. *Tip: connect by hostname, not by
  raw tailnet IP — the hostname survives any future IP change.*
- **Telegram control channel** — `/status` round-trips; the trigger audit log
  shows allowlisted `help`, `status`, and `run` verdicts from the owner's
  account. (This satisfies the "pending live verification" note in the M7
  build-gate evidence.)
- **Tailscale SSH** — enabled on the box (`tailscale set --ssh`); tailnet ACL
  tightened from `check` to `accept`, root dropped from SSH users.

### Components

- Host **`useragent`** — `safari@192.168.50.171` (LAN), tailnet **100.88.24.45**,
  SSH alias `substrate-lab` from the Windows control plane.
- NIC magic-packet wake armed (`Wake-on: g`, MAC `08:62:66:b4:1a:d2`);
  control-plane `labctl lab wake` sends it (LAN-only path).
- `substrateos-trigger.service` — the Telegram duty-cycle loop
  (`labctl trigger cycle`). Token + allowlist in gitignored `.env`
  (`TRIGGER_TELEGRAM_TOKEN`, `TRIGGER_ALLOWED_USER_IDS`).
- `substrateos-agent.service` — boot-time `git pull --ff-only` then launches
  the `substrateos` tmux session running Claude (today `claude`; the
  `subos --claude` switch is **backlog**, see below).

### Telegram commands

`/status` · `/run <mission>` · `/usage` · `/stay [minutes]` · `/sleep` · `/help`

## Operating modes

- **Always-on (current owner preference).** The box is kept online, so SSH is
  simply always available and `/status` confirms it. The wake-latency concerns
  below do not apply in this mode.
- **WoL / RTC duty-cycle (patient default, snappy on demand).** The designed
  mode: the box suspends and RTC-wakes (~10 min interval) to drain Telegram,
  giving bounded-latency control. `/stay [minutes]` overrides to snappy
  (stays awake, instant); `/sleep` returns to patient. The
  always-on vs duty-cycle choice is a power-vs-latency trade (see backlog:
  power metering).

## Security posture

- Zero inbound exposure: Telegram is outbound-poll only; Tailscale is
  WireGuard, no public ports; magic-packet wake is LAN-only.
- Telegram: numeric-id allowlist (not spoofable usernames), mission text
  travels **stdin-only** (never shell-interpolated), per-run token budget,
  one mission at a time, length cap, full audit trail under
  `artifacts/trigger-runs/` (gitignored).
- Auth is **subscription only** (Claude Max / gh / Codex) — never API keys.
  The Telegram bot token is a *channel* secret, not an LLM credential, and
  lives outside the repo.
- Lifecycle: suspend (S3) only, never poweroff (ADR-017).

## Backlog — needs build planning (NOT yet built)

Held until the new SubstrateOS (`subos`) build lands; revisit then.

1. **`subos --claude` as the auto-launch target.** Make the agent service
   prefer `subos --claude` with fallback to `claude` until `subos` ships.
2. **Checkout freshness on a suspend-only box.** Auto-pull fires only at boot
   today; a rarely-rebooted box goes stale. Plan: pull `--ff-only` at the top
   of each trigger wake (or a resume hook).
3. **Session recycle policy.** Pulling ≠ adopting — the long-lived session must
   restart to run new code. Proposed: a guarded Telegram `/update` (pull +
   recycle, refuses while a mission or live SSH session is active);
   optionally auto-recycle on wake when idle.
4. **`/run` completion summary.** Today `/run` is fire-and-forget; improve it to
   reply on the same chat with a tight summary when the mission finishes.
   ✅ Feasible — reuses existing reply path; mostly formatting.
5. **Wake + ETA report over Telegram.** If SSH is unavailable, queue a wake and
   report likeliest time-to-SSH. ⚠️ Caveat: a *sleeping* box only sees the
   Telegram message on its next RTC wake, so Telegram cannot wake it faster
   than the duty interval; true instant wake needs the LAN magic packet
   (`labctl lab wake`). Mainly relevant if returning to WoL mode.
6. **AC power-usage estimate (always-on vs WoL decision aid).** ⚠️ Software can
   *estimate* via battery energy counters (`/sys/class/power_supply/.../energy_uj`,
   `upower`), but a laptop cannot measure true wall draw on AC; the power-pack
   label gives only the adapter's max rating (an upper bound). An accurate kWh
   figure needs a smart plug. Decide required accuracy before building.

## Extraction — future home

This bolt-on is intentionally decoupled from SubstrateOS-base and may be lifted
into a standalone **"homelab AI" remote-access** project. Conceptually it
replaces the role of tools like OpenClaw (and possibly Hermes) for reaching a
home lab, with the key benefit that execution runs on a **Max subscription**
with no separately-billed API surface. When extracted, carry: the control/data
plane split, the `labctl trigger` loop, the systemd units, the security model,
and this document.
