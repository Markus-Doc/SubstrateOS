# Branch-1 Build Plan: Base+Overlay seam, engine-agnostic front-end, multi-agent orchestration

Status: active (2026-06-13). Authority: ADR-019 (architecture), ADR-020/021
(research + upkeep), master research at `docs/research/master-research.md`.
SubstrateOS-dictated: milestone-driven (ADR-010), **release gate green before
every push**, no new heavyweight frameworks (ADR-002).

This plan is handoff-ready for a fresh high-effort Opus build session. Each
milestone is independently shippable and gated. Milestones M-A/M-B are
research-safe (pure architecture plumbing the research validates) and may build
immediately; M-E/M-F should reconcile with the branch-2 impact assessment
(`docs/planning/research-impact-review-prompt.md`) before landing.

## Principles (from ADR-019)
- **Overlay → Base, one way.** Base never imports/hardcodes an Overlay.
  Discovery is by env var (`SUBSTRATEOS_OVERLAY`) only.
- **Ships blank.** Mechanism present, no-op defaults, documented scaffold.
- **Base runs naked.** Gate stays green with no Overlay present.
- **Guarantees in `labctl`, not the model** (gate, circuit breaker, isolation,
  review queue) — so engine-swap and multi-agent dispatch never weaken safety.
- **Compile target = `SKILL.md` + `AGENTS.md`** open standards (confirmed).

## Milestones

### M-A — Format + spec skeleton  ✅ DONE (2026-06-13)
Locked SKILL.md/AGENTS.md as the canonical compile target (ADR-019); canonical
engine-neutral spec checked in at `substrate/methodology.md` (MUST/SHOULD tiers,
activation contract, compile-target table) with `substrate/README.md`.

### M-B — Base extension seam  ✅ DONE (2026-06-13)
- Overlay discovery + command-plugin hook (`SUBSTRATEOS_OVERLAY` → mount extra
  `labctl` commands). No-op + safe when unset.
- Provider registry generalising the `WebProvider`/`MemoryProvider` ABC pattern
  so an Overlay can register named providers.
- Blank documented scaffold at `templates/overlay-example/`.
- DoD: tests for load/no-op/error paths; gate green **with overlay absent**.

### M-C — `subos` launcher + adapters
`subos <engine>` thin wrapper; Claude adapter (CLAUDE.md + `.claude/skills/`),
then Codex (`AGENTS.md`); engine-neutral permission posture mapping. DoD: launch
+ confirmation banner; adapter unit tests.

### M-D — `/substrateos` warm activation
In-session activation command compiled per engine; capability handshake (MUST vs
SHOULD tiers); live hydration via `labctl`. DoD: command artifact + handshake
report; honest launch-time-only caveat surfaced.

### M-E — Multi-agent / sub-agent orchestration  (reconcile w/ branch-2)
Frontier-as-planner/judge + sub-agent workers (architect → workers → reviewer →
judge; handoff packets; verify-before-accept — per master research). Dispatch
through `labctl`; each sub-agent budget-capped by the existing token circuit
breaker; isolated per capsule. This is the Phase-2 "Dynamic Workflows" milestone.
DoD: orchestrated run with per-agent budgets + run-log evidence; gate green.

### M-F — Conformance + supply-chain gate  (reconcile w/ branch-2)
Cross-engine conformance eval (promptfoo, per engine: "given SubstrateOS context,
refuses to bypass the gate, drives labctl correctly"). Supply-chain audit stage
for any skill/MCP/plugin loaded (licence/maintainer/scripts/network/permissions;
sandbox before real data). DoD: new gate stage(s); evidence; gate green.

## Sequencing vs branch-2  (branch-2 COMPLETE 2026-06-13)
Branch-2's whole-repo impact assessment
(`docs/planning/research-v2-impact-assessment.md`) cleared the base: **no
architecture rewrite, no genuine contradiction.** Backlog folded in here:
- **P1-A** default model Opus 4.8 → **ADR-022 (Accepted).**
- **P1-B** supply-chain audit gate (skills/MCP/plugins) → **M-F**, but it
  **expands the locked Phase-2 scope** ("six stages / no red-team expansion").
  Supply-chain audit ≠ red-team, but this needs an **owner decision** before
  M-F lands.
- **P2-A** in-process MCP tool seam for `labctl` providers → folds into M4
  (in-container execution); uses the M-B `ProviderRegistry`.
- **P2-B** trace + agentic-eval metrics (Task Completion, Tool Correctness, …)
  → folds into **M-E** (Dynamic Workflows orchestration).
- **P3-A** log LiteLLM-not-used + thin-harness-not-framework divergences
  (ADR-013 precedent).

M-C/M-D proceed now. M-E reconciles with P2-B. M-F's supply-chain stage is
gated on the P1-B owner decision.
