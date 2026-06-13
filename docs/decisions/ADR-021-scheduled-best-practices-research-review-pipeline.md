# ADR-021: Scheduled "Current AI Best Practices" research & review pipeline

Date: 2026-06-13
Status: Proposed (future upgrade — decision to be finalised when scoped)

## Decision (proposed)

SubstrateOS will run a **scheduled research-and-review pipeline** that keeps the
OS current with AI best practices and tooling, built on the **RESYNTH** tool
already used to produce the master research (docs/research/master-research.md).

On a cadence, the pipeline:
1. **Re-synthesises** current best-practice / frontier-tooling research into an
   updated candidate master-research document (RESYNTH).
2. **Diffs** the candidate against the current SubstrateOS design, ADRs, and
   tooling choices.
3. **Surfaces a review report** proposing ADRs, tooling swaps, and deprecations
   — promoted by a human via the existing review-queue discipline (never
   auto-merged).

This pipeline is the **mechanism that detects when current choices age out**
(e.g. the `SKILL.md`/`AGENTS.md` compile formats, the supported conversational
engines, bespoke-vs-OpenHands for in-container execution) and **triggers
migration to the documented contingency** rather than discovering staleness by
accident. It operationalises ADR-019's promise of a Base that is "maintained and
reviewed regularly."

## Context

The AI space changes rapidly. ADR-019/020 chose `SKILL.md`/`AGENTS.md` as the
primary compile target and named OpenHands/others as contingencies *precisely
because* a review pipeline would tell us when to switch. RESYNTH already produced
master-research v2 (ADR-020), so the synthesis half exists; this ADR adds the
scheduled cadence + diff + review-and-propose half.

## Open questions (to resolve before Accepting)

- **Cadence / trigger**: fixed schedule vs manual vs event-driven; likely a
  `labctl research`-style command (e.g. `labctl research sync` / `review`).
- **Where it runs**: tie into existing scheduled infra — the lab box duty cycle,
  `@reboot` auto-sync, RTC self-wake, Telegram trigger (ADR-018).
- **Scope**: whole-ecosystem sweep vs targeted watch-list of tools/standards.
- **Output gating**: report-only vs auto-drafted ADR proposals (PRs), always
  human-promoted.
- **Relationship** to ADR-010 (milestone discipline) and the review queue
  (AI-derived content unpromoted until approved).

## Consequences

- A new `labctl` surface and a scheduled job; the Base ships the mechanism, the
  watch-list/cadence can be Overlay-tunable.
- Contingency plans (OpenHands as an execution-engine adapter, alternative
  instruction formats) become *actionable on a signal* rather than aspirational.
