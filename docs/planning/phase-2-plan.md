# Phase 2 Plan: Performance, Scale, and the Lab Operator Host

Approved 2026-06-12. Source scope: Final_Research-Agent_Brain.md §8 Phase 2
("Optimize retrieval and expand autonomous capabilities") plus the deferred
items assigned to Phase 2 by ADR-009 (vector/hybrid retrieval), ADR-015
(in-container capsule execution — Phase 2's first job), ADR-016 (per-campaign
cumulative accounting), and the Phase 1 retrospective debt list.

**Realigned 2026-06-12 per ADR-017**: the Lab host is a remote agent operator,
not a compute node (actual hardware is a GTX 950M, not the RTX 3070 the
original plan assumed). Hybrid retrieval / local embeddings move off the
critical path to the Deferred section below.

## Objective

Expand autonomous capabilities: the Lab host as a wake-on-demand remote agent
operator (`labctl lab`), in-container capsule execution, and Dynamic Workflows
for codebase-wide audits. Retrieval optimisation (vector/hybrid) is deferred
behind the `MemoryProvider` seam per ADR-017.

## Locked decisions (owner, 2026-06-12)

1. **The Lab host is a remote agent operator, not a compute node (ADR-017).**
   The machine is dedicated to operating frontier AI models explicitly the way
   SubstrateOS sets it — wake it, dispatch any task via the established
   defaults, pick up any Markus-Doc project as if at the main PC. Subscription
   auth only (device-code login on Claude Max; Codex Plus as backup), never
   API keys. Nothing depends on its processing power.
2. **Capsule auth preference order:** subscription login (headless OAuth via
   `claude setup-token`, token injected as an env var at container launch) →
   API key in a secure gitignored env file → anything else. Owner is on
   Claude Max; API-key billing is to be avoided.
3. **Capstone target: SubstrateOS itself** (codebase-wide audit through the
   harness).
4. **No red-team expansion in Phase 2.** Garak / OWASP presets / PyRIT stay
   deferred; the release gate keeps its six stages. Phase 2 instead delivers
   the orchestration capability layer (Dynamic Workflows, agents and skills as
   repo-resident packages, frontier-as-judge delegation per the master
   research doc).

## Execution Model (ADR-010)

No calendar deadlines. Milestones are gated by their checklists being done and
verified. The work is executed by Claude (Fable 5) as one autonomous
loop-driven campaign (/loop, dynamic pacing), delegating bounded subtasks
where they add leverage and verifying every delegated claim. Pause points
(the only ones): Lab host SSH/WoL connection details at Milestone 2 start,
and any review-queue approvals (human-gated by design).

## Success Metric

A codebase-wide audit of SubstrateOS executed through the harness: dispatched
by `labctl`, run by an in-container agent, grounded by BM25 retrieval over the
repo's namespace (hybrid retrieval deferred per ADR-017), orchestrated as a
Dynamic Workflow (architect → workers → reviewer → judge), producing a
committed findings report — with `labctl gate --strict` all-PASS and evidence
in `artifacts/evidence/`. Plus, already delivered by the realigned M2: the Lab
operator is user-ready — wake, status, sync, and a metered dispatch all
verified from the control plane.

## Task Breakdown

### Milestone 1: Inherited Debt and Campaign Metering

- [x] Re-ingest no longer duplicates memory rows: uniqueness guard in
      `SQLiteMemory` plus the ingest tail skips indexing when the content is
      unchanged (`skipped=True`); one-time cleanup of existing duplicate rows
      (run 2026-06-12: 0 duplicates found in the live db)
- [ ] OQ-006 dashboard reads live SubstrateOS state instead of example data
      (retrospective debt item — lives in the research-dashboard repo)
- [x] Per-campaign cumulative token accounting across capsule run logs
      (`labctl usage`), closing the ADR-016 open consequence
- [x] Tests for all of the above; suite green (103 passing)

### Milestone 2: Lab Operator Bring-Up (realigned per ADR-017)

- [x] Lab host SSH/WoL details collected from the owner and stored in
      gitignored config only (`LAB_SSH_HOST`, `LAB_WOL_MAC`,
      `LAB_WOL_BROADCAST`, `LAB_REMOTE_REPO` in `.env`)
- [x] `labctl lab wake` sends the Wake-on-LAN magic packet (stdlib socket,
      no new dependencies), with `--wait` ssh polling
- [x] `labctl lab status` over SSH: one round trip — hostname, uptime,
      claude/codex versions, gh auth state, repo HEAD; soft check wired into
      `labctl doctor`
- [x] `labctl lab sync`: clone-or-fast-forward the GitHub checkout on the
      box; on-boot auto-sync via user crontab (`@reboot ... pull --ff-only`)
- [x] `labctl lab dispatch`: metered headless claude mission on the box —
      mission on stdin (ADR-015), stream-json metering and token circuit
      breaker (ADR-016), run logs on the control plane
      (`artifacts/lab-runs/`, gitignored)
- [x] Box provisioned sudo-free into `~/.local/bin`: claude (native
      installer), gh (release tarball); codex preinstalled; remote git
      identity set to the standing convention
- [x] Subscription auth on the box: claude (Max, device code), gh
      (Markus-Doc write, device code), codex (Plus, device code) — never
      API keys
- [x] Lab host role recorded as ADR-017 (extends ADR-013)

### Milestone 4: In-Container Capsule Execution (ADR-015's deferred first job)

Prerequisite cleared 2026-06-12: Docker 29.1.3 installed and verified on the
Lab box during the dial-in (ADR-017 amendment).

- [ ] Capsule image gets the claude CLI; auth per locked decision 2 — OAuth
      token injected as an env var at container launch, never written to a
      file, image layer, or mount (template isolation guarantees intact:
      still no credential mounts)
- [ ] Run path staged per OQ-005: devcontainer CLI in WSL2 first, then the
      identical flow on the Lab host over SSH as the standard target
- [ ] Mission still travels on stdin; stream-json metering and the token
      circuit breaker (ADR-016) enforced from the dispatching `labctl`,
      which kills the container, not just a process tree
- [ ] Capsule memory access design (what `/memory` carries; MCP exposure only
      if multi-agent access truly needs it, per ADR-009) — recorded as an ADR
- [ ] Breaker demonstrated live in-container; evidence committed

### Milestone 5: Dynamic Workflows — Orchestration Capability Layer + Capstone

- [ ] Repo-resident capability package encoding the master research doc's
      delegation patterns: frontier-as-judge; self-contained handoff packets
      (repo path, exact objective, in/out of scope, expected evidence,
      verification commands, stop conditions); architect → bounded workers →
      reviewer → judge. Claude Code native orchestration only (ADR-002)
- [ ] `labctl audit <repo>` runs a codebase-wide audit as that Dynamic
      Workflow, grounded by BM25 retrieval over the repo's namespace
      (hybrid deferred per ADR-017)
- [ ] Capstone (success metric): the audit run on SubstrateOS itself through
      the harness, in-container, findings report committed. Missions framed
      as engineering/code-quality audits, not pentest language (master doc:
      cyber-classifier rerouting)

### Milestone 7: Remote Trigger Pathway (OQ-007 → ADR-018; owner-directed 2026-06-12)

Inserted by owner direction: message the box from anywhere → it wakes →
SubstrateOS executes → result reported back on the same channel. Channel,
wake design, and tunnel locked by the owner; see ADR-018.

- [x] `labctl trigger` command group (`cycle`, `listen`, `status`) in
      `scripts/labctl/trigger.py`: Telegram long-poll transport (stdlib
      urllib, injectable for tests), numeric-user-id allowlist, command
      grammar (`/status`, `/run <mission>`, `/usage`, `/sleep`,
      `/stay <minutes>`, `/help`), audit log of every update with its
      allow/deny verdict under `artifacts/trigger-runs/` (gitignored)
- [x] Missions execute via the established ADR-015/016 machinery: mission on
      stdin, stream-json metering, circuit breaker, run logs in
      `artifacts/trigger-runs/`
- [x] RTC self-wake duty cycle: listen window → suspend guards (no active
      mission, no interactive login session, no inhibit marker) →
      `rtcwake -m mem -s <interval>`; any resume (RTC or WoL) returns to the
      same loop. S3 only, never poweroff
- [x] systemd unit template + documented install; survives reboot and resume
- [x] Tailscale SSH enabled on the box as the direct command/emergency path
- [x] Secrets only in gitignored `.env` (`TRIGGER_TELEGRAM_TOKEN`,
      `TRIGGER_ALLOWED_USER_IDS`); SECURITY.md threat-model delta recorded
- [x] Deterministic tests (fake transport/clock/suspend; no network, no AI
      runtime); suite green; `labctl gate --strict` all-PASS
- [ ] Live verification: owner sends `/status` and a small `/run` from his
      phone; one full suspend → RTC wake → drain → reply cycle evidenced in
      `artifacts/evidence/`

### Milestone 6: Close-Out

- [ ] Plan ticked; Phase 2 retrospective; completion report with evidence
      index; all judgement calls captured as ADRs
- [ ] Memory and `~/.claude/plans/` handoff updated for Phase 3
- [ ] Pushed to main only behind `labctl gate --strict` all-PASS

## Deferred from the critical path (ADR-017): Hybrid Retrieval (was Milestone 3)

The Lab box has no useful inference hardware (GTX 950M) and the operator role
does not need it. Vector/hybrid retrieval stays a deferred seam behind
`MemoryProvider` (the ADR-009 `search_vector` stub) until hardware or a
demonstrated retrieval-quality need justifies it. Preserved checklist for
when it returns:

- [ ] `EmbeddingProvider` seam (mirrors the ADR-005 provider pattern);
      serving stack and model chosen then and recorded as an ADR
- [ ] Embeddings stored in SQLite next to chunks (ADR-001; brute-force
      cosine at current scale)
- [ ] `SQLiteMemory.search_vector` plus hybrid merge (reciprocal rank
      fusion) behind `MemoryProvider`; namespace isolation preserved in SQL
- [ ] CLI: `labctl search --mode keyword|vector|hybrid`; backfill;
      BM25-vs-hybrid evidence in `artifacts/evidence/`

The M5 capstone audit grounds itself in BM25 retrieval (ADR-009) instead.

## Standing Constraints

- No new tools beyond the research docs without an ADR; SQLite until it
  measurably breaks (ADR-001); no LangGraph/AutoGen (ADR-002); no local
  inference on the i7 laptop, and none on the Lab box either (GTX 950M;
  ADR-017 — embedding compute waits for real hardware).
- Never bypass `labctl.capsule.clean_claude_env` / `_spawn_claude`; missions
  via stdin; `--dangerously-skip-permissions` is owner policy (ADR-015).
- Capsule isolation guarantees (`templates/capsule-devcontainer/README.md`)
  are non-negotiable.
- No secrets in tracked files; commits as "M. Walker" + GitHub noreply email,
  including on the Lab host.
- From 15 June 2026 headless `claude -p` on subscription plans draws from a
  separate monthly Agent SDK credit bucket; the campaign records metered usage
  per run and stops-and-reports if the bucket is exhausted — never a silent
  API-key fallback.

## Out of Scope for Phase 2

- Postgres/pgvector migration (only if SQLite measurably breaks — it has not)
- Garak, PyRIT, OWASP preset expansion of the gate
- Web dashboard UI
- Cloud deployment of any component; swarm orchestration (Phase 3)
