# ADR-021: Scheduled "Current AI Best Practices" research & review pipeline

Date: 2026-06-13
Status: Accepted
Implemented: 2026-06-14 — `labctl research` (status/brief/sync/review) in
`scripts/labctl/research.py`; watch-list `substrate/research-watch.json` (bundled as
package data, Overlay-tunable); review reports flow through the existing review queue.

## Decision

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

## Resolved decisions (owner, 2026-06-14)

- **AI execution = interactive-operator by default.** `labctl research` is
  deterministic, file-backed tooling; the interactive `subos <engine>` session
  operates it and does the thinking — **no headless model call, no Agent-SDK credit
  spend** by default. A `--auto` mode (headless, metered by the ADR-016 circuit
  breaker) is opt-in and explicitly labelled. This mirrors RESYNTH's own design
  (synthesis intelligence supplied by the operating agent session; zero runtime AI
  dependency).
- **Output gating = report-only.** Each run writes an AI-derived review report into
  the **existing review queue** (`origin: derived, promoted: false`); the owner
  promotes it (`labctl review approve`) and authors any ADRs. The pipeline never
  auto-creates ADR files.
- **Cadence / trigger = manual on the control plane** (`labctl research ...`).
  Lab-box scheduling (ADR-018 RTC duty cycle / `@reboot`) is documented as opt-in
  Overlay wiring, not baked into the public Base.
- **Scope = targeted watch-list** at `substrate/research-watch.json` (Base default,
  Overlay-tunable): the tools/standards/formats already named in ADR-019/022/025/027.
- **RESYNTH = optional external tool** (`labctl doctor` reports it, graceful skip when
  absent); pipeline state is repo-resident under `artifacts/research/<topic>/`.
- **Relationship to ADR-010 + the review queue:** the report is AI-derived content,
  unpromoted until a human approves — same discipline as `labctl review`.

## Consequences

- A new `labctl` surface and a scheduled job; the Base ships the mechanism, the
  watch-list/cadence can be Overlay-tunable.
- Contingency plans (OpenHands as an execution-engine adapter, alternative
  instruction formats) become *actionable on a signal* rather than aspirational.
