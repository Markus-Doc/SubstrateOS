# Ultracode / Dynamic-Workflow Escalation — Evaluation

Date: 2026-06-14
Author: Opus 4.8 session (Windows host; SubstrateOS read-only evaluation)
Status: Promoted to **ADR-027** (2026-06-14) once the install/distribution build
(ADR-026) landed at `4190dd8`. This doc remains the working analysis; ADR-027 is
the decision record.

> ⚠️ Multi-session note: at the time of writing another build session held
> uncommitted work in `scripts/labctl/{cli,doctor,subos}.py`, `pyproject.toml`,
> and new `scripts/labctl/data/` + `scripts/sync_spec_data.py`. This file is a
> deliberately collision-safe new doc; it touches no code and no numbered ADR
> (the active session just used ADR-026, so a number is reserved for the eventual
> decision record rather than claimed here).

## Question

Should SubstrateOS integrate Claude Code's `ultracode` (dynamic-workflow) trigger
— and the planning ergonomics around `/plan` — given that the OS already
implements its own multi-agent orchestration?

## Decision-leaning

**Do NOT integrate `ultracode` as a default or base capability. Admit it only as
an opt-in, engine-detected escalation tactic that runs *under* the OS judge.**

Rationale in one line: SubstrateOS's `orchestrate.py` (Dynamic Workflows, M5,
ADR-019) already fills the planner→workers→reviewer→judge role that `ultracode`
plays in Claude Code, so `ultracode` is not a missing capability — it is, at
most, an optional alternative *worker-execution strategy*.

## Why not as a base step (the conflicts)

1. **Not in governing research.** `ultracode` appears only in
   `docs/research/archive/master-research-v1.md`, **not** in the current
   `docs/research/master-research.md` (v2, which wins per ADR-020). Naming it as
   a SubstrateOS capability today violates the CLAUDE.md core rule "do not
   introduce tools/frameworks/platforms not already in the research doc" until
   research is updated (ADR-021 pipeline).
2. **Engine coupling.** `ultracode` exists only in Claude Code. Hardcoding it
   into the base breaks the write-once/compile-many, engine-neutral thesis
   (ADR-019, ADR-023). The OS deliberately reimplements orchestration itself
   rather than depending on one engine's feature.
3. **Audit-divergence risk.** The OS harness is fixed-shape, budget-capped, and
   fully traced (JSONL + agentic-eval metrics, P2-B). A naive `ultracode` call
   fans out to many subagents outside that gating.

Per the v2 impact assessment §3.8, Claude-specific ergonomics belong in the
**SHOULD tier** of ADR-019's capability handshake, never as base requirements.

## The design that resolves the tension: ultracode *under* the judge

```
OS orchestration (architect → workers → reviewer → JUDGE)
        │
        ▼  judge returns REJECT  ("not understood how I want")
        │
   [staged option, previously skipped]:
        "escalate this stage → branch + run as ultracode"
        │
        ▼  ultracode writes its own harness, fans out, returns evidence
        │
        ▼  the OS JUDGE re-evaluates the escalated result  ← OS stays supervisor
```

`ultracode` never gets final say; the existing `verify-before-accept` JUDGE stage
still gates acceptance. The OS supersedes `ultracode` by *supervising* it, not by
excluding it.

### Trigger
The judge's **REJECT verdict** is the natural "something isn't understood how I
want" signal. On REJECT, surface the previously-skipped "retry-as-ultracode"
option as a clean staged pane (plumbing hidden, prefilled command — consistent
with the staged-pane presentation pattern). Escalation is a ladder, not a
parallel system.

### Inheritance boundary (manage expectations here)
- **Flows IN (inheritable):** the OS `HandoffPacket` — mission, in/out-of-scope,
  grounding (BM25 retrieval over the repo namespace), verification commands, stop
  conditions. This seeds the escalated run with what the OS already understood.
- **Does NOT carry over:** the OS *stage shape*. The point of escalation is to
  let `ultracode` write its own bespoke harness and choose its own decomposition.
  Forcing architect→workers→reviewer onto it would defeat the purpose.
- **Caveat on `/plan` / "ultraplan":** `/plan` (plan mode) is a real Claude Code
  command; `/ultraplan` is **not** confirmed to exist. Planning inside the
  dynamic-workflow path is something `ultracode` does itself. So "inherit
  planning tailoring" realistically means: optionally run plan mode to seed the
  packet, then let `ultracode` plan its own fan-out. Do not design around an
  `/ultraplan` primitive.

### The one real cost: audit boundary changes
The OS token **circuit breaker is per-stage**; `ultracode` spawns subagents that
the per-stage breaker will not see. Therefore an escalated branch must be:
- capped at the **outer subprocess boundary** (a total token budget for the whole
  escalated run), and
- folded back into the OS JSONL trace as a single "escalated-stage" record.

Auditability is preserved, but granularity *inside* the escalated branch is
whatever Claude Code emits, not OS stage-level detail. State this explicitly so a
future alignment audit reads it as a decision, not a trace gap.

### Isolation
Run the escalated attempt in an isolated **capsule sibling-dir** (ADR-014) or a
git worktree so it cannot disturb the main run while it tries; it returns a
handoff packet for the OS judge to re-evaluate.

## Summary of constraints honoured
- **Out of the base, opt-in, engine-detected (Claude Code only)** → preserves
  engine-neutrality (ADR-019/ADR-023).
- **Behind the OS judge + an outer budget cap** → preserves the verify-before-
  accept and metering posture (ADR-016).
- **Research-first** → admit via the ADR-021 pipeline (update master-research to
  cite Dynamic Workflows/`ultracode`) *before* a numbered ADR, honouring the
  "research wins / nothing not in research" rule.

## Next step
When the in-flight build lands, promote this to a numbered ADR ("ultracode as a
SHOULD-tier escalation strategy under the judge") and, if accepted, schedule the
master-research v-next update through the ADR-021 pipeline.
