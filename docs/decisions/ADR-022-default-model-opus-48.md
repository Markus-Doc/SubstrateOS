# ADR-022: Default model is Opus 4.8, not Fable 5

Date: 2026-06-13
Status: Accepted

## Decision

SubstrateOS's default model is **Claude Opus 4.8**. Claude Fable 5 is opt-in for
heavy non-cyber reasoning, not the default.

## Context

Per the master research (docs/research/master-research.md) and the branch-2
impact assessment (P1-A):

- Fable 5 **mandates 30-day data retention** with no zero-retention option.
- Fable 5 **reroutes cybersecurity/biology/chemistry queries to Opus 4.8**
  anyway — so for SubstrateOS's security-engineering workloads it adds friction
  without delivering its headline capability.
- Fable 5 access was **suspended as of 2026-06-12**.
- The owner's environment already runs `opus-4-8`.

Engine-agnosticism (ADR-019) is unchanged: this fixes the *default model* within
the Claude engine; other engines/models remain hot-swappable, and the choice is
Overlay-tunable.

## Consequences

- `subos` and the build path default to Opus 4.8; Fable 5 is an explicit
  override.
- Note (operational, not this ADR): from 2026-06-15 subscription `claude -p` /
  Agent SDK usage draws from a separate non-rolling monthly credit, which raises
  the importance of the token circuit breaker + usage accounting (ADR-016) for
  `labctl build` and lab dispatch.
- Revisit when Fable 5 access is restored and its retention/rerouting terms
  change — a natural trigger for the ADR-021 research/review pipeline.
