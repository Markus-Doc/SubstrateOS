# Phase 2 Plan: Performance, Scale, and the Lab Execution Host

Approved 2026-06-12. Source scope: Final_Research-Agent_Brain.md §8 Phase 2
("Optimize retrieval and expand autonomous capabilities") plus the deferred
items assigned to Phase 2 by ADR-009 (vector/hybrid retrieval), ADR-015
(in-container capsule execution — Phase 2's first job), ADR-016 (per-campaign
cumulative accounting), and the Phase 1 retrospective debt list.

## Objective

Optimize retrieval and expand autonomous capabilities: local embeddings on the
RTX 3070 Lab host, hybrid retrieval behind the existing `MemoryProvider` seam,
in-container capsule execution, and Dynamic Workflows for codebase-wide audits.

## Locked decisions (owner, 2026-06-12)

1. **The Lab host (RTX 3070, OQ-001) is ready and reachable over SSH.** Goal,
   flagged by the owner: the machine becomes dedicated to operating frontier
   AI models explicitly the way SubstrateOS sets it — wake it, dispatch any
   task via the established defaults. Lab-host integration is a first-class
   milestone, not an embeddings detail.
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
by `labctl`, run by an in-container agent, using hybrid retrieval (BM25 +
vector from embeddings computed on the RTX 3070), orchestrated as a Dynamic
Workflow (architect → workers → reviewer → judge), producing a committed
findings report — with `labctl gate --strict` all-PASS and evidence in
`artifacts/evidence/`.

## Task Breakdown

### Milestone 1: Inherited Debt and Campaign Metering

- [ ] Re-ingest no longer duplicates memory rows: uniqueness guard in
      `SQLiteMemory` plus the ingest tail skips indexing when the content is
      unchanged (`skipped=True`); one-time cleanup of existing duplicate rows
- [ ] OQ-006 dashboard reads live SubstrateOS state instead of example data
      (retrospective debt item)
- [ ] Per-campaign cumulative token accounting across capsule run logs
      (`labctl usage`), closing the ADR-016 open consequence
- [ ] Tests for all of the above; suite green

### Milestone 2: Lab Host Integration

- [ ] Lab host SSH/WoL details collected from the owner (hostname/IP, user,
      key, MAC) and stored in gitignored config only — single pause point
- [ ] `labctl lab wake` sends the Wake-on-LAN magic packet (stdlib socket,
      no new dependencies)
- [ ] `labctl lab status` over SSH: reachability, uptime, `nvidia-smi`,
      Docker presence; wired into `labctl doctor`
- [ ] Lab host role recorded as an ADR (what runs there vs the Windows
      control plane; extends ADR-013)

### Milestone 3: Hybrid Retrieval

- [ ] `EmbeddingProvider` seam (mirrors the ADR-005 provider pattern):
      HTTP call to an embedding service on the Lab host; serving stack and
      model chosen during the campaign and recorded as an ADR
- [ ] Embeddings stored in SQLite next to chunks (ADR-001: no Postgres until
      SQLite measurably breaks; brute-force cosine at current scale)
- [ ] `SQLiteMemory.search_vector` implemented (replacing the Phase 1 stub)
      plus hybrid merge (reciprocal rank fusion) behind `MemoryProvider`;
      namespace isolation preserved in SQL
- [ ] CLI: `labctl search --mode keyword|vector|hybrid`
- [ ] Embeddings backfilled for existing namespaces (substrateos,
      research-dashboard)
- [ ] Retrieval evidence: recorded query set run BM25-only vs hybrid,
      side-by-side results committed to `artifacts/evidence/`

### Milestone 4: In-Container Capsule Execution (ADR-015's deferred first job)

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
      Workflow, grounded by hybrid retrieval over the repo's namespace
- [ ] Capstone (success metric): the audit run on SubstrateOS itself through
      the harness, in-container, findings report committed. Missions framed
      as engineering/code-quality audits, not pentest language (master doc:
      cyber-classifier rerouting)

### Milestone 6: Close-Out

- [ ] Plan ticked; Phase 2 retrospective; completion report with evidence
      index; all judgement calls captured as ADRs
- [ ] Memory and `~/.claude/plans/` handoff updated for Phase 3
- [ ] Pushed to main only behind `labctl gate --strict` all-PASS

## Standing Constraints

- No new tools beyond the research docs without an ADR; SQLite until it
  measurably breaks (ADR-001); no LangGraph/AutoGen (ADR-002); no local
  inference on the i7 laptop — embedding compute happens only on the Lab host.
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
