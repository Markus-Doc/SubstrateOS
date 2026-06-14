# ADR-027: ultracode as a SHOULD-tier escalation strategy under the judge

Date: 2026-06-14
Status: Accepted

## Decision

Claude Code's `ultracode` (dynamic-workflow) trigger is **not integrated as a
base or default SubstrateOS capability**. The OS already implements its own
multi-agent orchestration — `scripts/labctl/orchestrate.py` (Dynamic Workflows,
M5, ADR-019: architect → workers → reviewer → judge, with handoff packets,
verify-before-accept, per-stage token circuit breaker, and JSONL + agentic-eval
traces) — which fills the same planner/judge role that `ultracode` plays inside
Claude Code. `ultracode` is therefore not a missing capability.

It is admitted **only** as a conditional, opt-in escalation tactic that runs
*under* the OS judge, never as a peer to it:

1. **Out of the base; SHOULD-tier, engine-detected.** Available only when the
   active engine is Claude Code (per the ADR-019 capability handshake; see the
   v2 impact assessment §3.8 placing Claude-specific ergonomics in the SHOULD
   tier). Other engines never see it. The Base stays engine-neutral.
2. **Triggered on a judge REJECT.** The existing verify-before-accept JUDGE
   verdict is the "not understood how I want" signal. On REJECT, a previously
   skipped "retry-as-ultracode" option is surfaced as a clean staged pane
   (plumbing hidden, prefilled command — consistent with the staged-pane
   presentation pattern). Escalation is a ladder, not a parallel system.
3. **The OS stays supervisor.** The escalated `ultracode` run writes its own
   harness and returns evidence; the **OS judge re-evaluates** that result.
   `ultracode` never gets final say.
4. **Inheritance boundary.** The OS `HandoffPacket` (mission, in/out-of-scope,
   grounding via BM25 retrieval, verification commands, stop conditions) flows
   *in* to seed the escalated run. The OS **stage shape does not** carry over —
   the point of escalation is to let `ultracode` choose its own decomposition.
   Note: `/plan` (plan mode) is a real Claude Code command; `/ultraplan` is not
   confirmed to exist, so no design depends on it — planning inside the
   dynamic-workflow path is something `ultracode` does itself.
5. **Audit cap.** The OS circuit breaker is per-stage and will not see the
   subagents `ultracode` fans out. An escalated branch must be capped at the
   **outer subprocess boundary** (a total token budget for the whole escalated
   run) and folded back into the OS JSONL trace as a single "escalated-stage"
   record. Granularity inside that branch is whatever Claude Code emits, by
   design — recorded here so a future audit reads it as a decision, not a trace
   gap.
6. **Isolation.** An escalated attempt runs in an isolated capsule sibling-dir
   (ADR-014) or git worktree so it cannot disturb the main run.

## Context

This promotes `docs/planning/ultracode-escalation-eval.md` (committed `dd374b4`),
written read-only while a concurrent session held the install/distribution build
(ADR-026, landed at `4190dd8`). The owner's lean was explicit: do not integrate
`ultracode`/`/ultraplan`, because the OS is tuned to supersede them — but keep an
optional escalation hatch for the case where the native workflow's understanding
falls short.

The negative half of this decision (no base integration) is firmly **Accepted**
and is fully research-aligned: it requires no new tool and follows ADR-002 (no
heavyweight framework), ADR-019/ADR-023 (engine-neutral, write-once/compile-many,
logged divergences). The OS-as-orchestrator pattern is independently validated by
the master research (`## Ai Orchestration`, `## Agents`) and mapped to M5 in the
v2 impact assessment §3.1 (CONFIRMS).

## Consequences

- **Implementation is deferred / conditional**, not accepted by this ADR. Before
  any escalation path is built, `ultracode` must first be admitted into the
  governing research (`docs/research/master-research.md`, v2) via the ADR-021
  pipeline — it currently appears only in `archive/master-research-v1.md`, so
  building it now would violate the "nothing not in research" core rule. This ADR
  records the *shape* the feature must take if and when it is admitted.
- The ADR-021 research/review pipeline can diff against this record: the watch
  item is the Claude Code Dynamic Workflows / `ultracode` feature surface.
- If built, it extends ADR-019 (capability handshake / SHOULD tier), ADR-016
  (budget metering — adds the outer-boundary cap), and the M5 orchestrator
  (REJECT-path escalation hook); it does not reverse any existing ADR.
- If the premise changes (the OS orchestrator proves insufficient such that
  `ultracode` should become a first-class worker path rather than a REJECT-only
  escalation), this ADR is the amendment point.
