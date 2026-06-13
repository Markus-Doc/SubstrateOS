# Branch-2 handoff: master-research v2 → whole-repo impact review

**Purpose.** A standalone, deep-consideration session that answers one question:
*does the new master research (v2) mandate any changes to the overall SubstrateOS
repo?* This de-risks the branch-1 multi-agent build-out by confirming the base
before we build on it. Paste this whole file into a fresh high-effort session
(Opus 4.8 — Fable 5 reroutes cyber content and was suspended 2026-06-12).

---

## Context (everything you need; do not assume prior chat)

SubstrateOS is a local-first AI orchestration harness. Source of truth:
`docs/research/master-research.md` (RESYNTH v2, 66 sources). Project rules in
`CLAUDE.md`. Architecture in `docs/architecture/system-overview.md`. Decisions in
`docs/decisions/ADR-001..ADR-021`. The harness CLI (`labctl`) lives in
`scripts/labctl/`; the release gate has six stages (secret-scan, lint, tests,
SAST, vuln-scan, promptfoo evals).

Already-agreed direction (do not relitigate, only check for *impact*):
- ADR-019: Base + Overlay (one-way dep, ships blank); engine-agnostic
  conversational front-end (`subos` launcher, `/substrateos` warm activation,
  write-once-compile-many to `SKILL.md`/`AGENTS.md`, engine-neutral permission
  posture); guarantees enforced in `labctl`, not the model.
- ADR-020: v2 promoted as master research; root decluttered.
- ADR-021 (Proposed): scheduled RESYNTH best-practices research/review pipeline.
- Hard constraints: ADR-002 rejects heavyweight agent frameworks (LangGraph,
  AutoGen, etc.); no Postgres (ADR-001); no local inference on the laptop.
  SKILL.md/AGENTS.md are the primary compile target; OpenHands/others are
  contingencies triggered only by ADR-021's pipeline.

## Your task (analyse + propose, do NOT implement code)

1. Read `docs/research/master-research.md` in full, then read every ADR and
   `docs/architecture/system-overview.md`.
2. For each of the five architecture layers and each ADR, decide: **CONFIRMS /
   REFINES / CONTRADICTS / GAP**. Cite the research section (e.g. the
   `## Agent Skills` or `## Ai Orchestration` heading) for every finding.
3. Pay special attention to: multi-agent & sub-agent orchestration (frontier as
   planner/judge + workers); the trace-and-evaluation layer ("non-optional in
   2026"); MCP as the tool seam vs CLI-driving; supply-chain risk of
   skills/MCP/plugins; model choice (Fable 5 retention + cyber rerouting vs Opus
   4.8); the June-15 headless-build billing change; in-container execution.
4. Output a written **impact assessment** + a prioritised list of **proposed new
   ADRs / ADR amendments** (titles + one-line rationale each). Propose only;
   respect the hard constraints above. Flag anything that would change Phase 2
   scope.

## Definition of done

A markdown report (suggest `docs/planning/research-v2-impact-assessment.md`) with
the layer/ADR matrix, cited findings, and the proposed-ADR backlog. No code
changes; if you write the report file, the gate must stay green.
