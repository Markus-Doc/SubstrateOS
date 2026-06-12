# ADR-017: The Lab host is a remote agent operator, not a compute node

Date: 2026-06-12
Status: Accepted

## Decision

The Lab host's role is **remote agent operation**: it runs the same claude CLI
as the control plane (`claude --dangerously-skip-permissions`, default Fable 5
at high effort; Codex CLI as backup), permanently authenticated **via device
code on the owner's Claude Max subscription — never API keys** — against a
current checkout of this repo. Nothing in SubstrateOS depends on the Lab box's
processing power.

Concretely:

1. `labctl lab` (wake, status, sync, dispatch) is the operator interface from
   the Windows control plane (ADR-013). Wake is a stdlib Wake-on-LAN magic
   packet; status is one ssh round trip; sync clones or fast-forwards the
   GitHub checkout (GitHub remains the CI/CD source of truth); dispatch runs a
   metered headless claude mission on the box, reusing the capsule machinery
   unchanged — mission on stdin (ADR-015), stream-json metering and the token
   circuit breaker (ADR-016), run log kept on the control plane under the
   gitignored `artifacts/lab-runs/`.
2. Connection details (ssh host alias, WoL MAC, remote repo path) live only in
   the environment or the gitignored `.env` (`LAB_SSH_HOST`, `LAB_WOL_MAC`,
   `LAB_WOL_BROADCAST`, `LAB_REMOTE_REPO`). No host, MAC, or IP in tracked
   files.
3. Provisioning is **sudo-free into `~/.local/bin`** (the operator account has
   no sudo): claude via the native installer, gh via release tarball. All ssh
   from labctl is `BatchMode=yes` — never interactive, never password.
4. The wake-into-current-OS guarantee is a user crontab entry,
   `@reboot sleep 30 && git -C ~/SubstrateOS pull --ff-only`, plus
   `labctl lab sync` for on-demand refresh.
5. Remote git identity matches the standing convention: "M. Walker" with the
   GitHub noreply email, configured in the remote clone.

## Context

The original Phase 2 plan assumed the Lab host carried an RTX 3070 and would
serve local embeddings for hybrid retrieval. The actual machine (`useragent`,
Ubuntu 24.04) carries a GTX 950M — no useful inference capacity — and the
owner's locked vision (2026-06-12) is explicitly that the box is operated for
its *agency*, not its compute: wake it from anywhere, land in a current
SubstrateOS checkout with full Markus-Doc write access, and pick up any
project as if at the main PC.

## Consequences

- **Hybrid retrieval / local GPU embeddings are descoped from the Phase 2
  critical path.** Vector search remains a deferred seam behind
  `MemoryProvider` (the ADR-009 `search_vector` stub) until hardware or need
  justifies it. The phase-2 plan's old Milestone 3 moves to a deferred
  section.
- Subscription-only auth: from 15 June 2026 headless `claude -p` on
  subscription plans draws from a separate monthly Agent SDK credit bucket;
  every dispatch is metered and an exhausted bucket means stop-and-report,
  never an API-key fallback.
- In-container capsule execution on the box still needs Docker there (not
  installed; requires sudo) — it stays a remaining Phase 2 item, not part of
  the operator bring-up.
- Remote *trigger* pathways (messaging-initiated wake/dispatch) are an open
  question, recorded as OQ-007; nothing is built for them yet.
