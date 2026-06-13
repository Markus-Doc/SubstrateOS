# ADR-008: MASTER_AI_System_Research.md promoted to master research document

Date: 2026-06-11
Status: Accepted (superseded in part by ADR-020, 2026-06-13 — the master research
is now docs/research/master-research.md (v2); the v1 doc named below is archived
at docs/research/archive/master-research-v1.md)

## Decision

`MASTER_AI_System_Research.md` (repo root) is the master research document for
Agent Brain. Where it conflicts with `docs/research/Final_Research-Agent_Brain.md`,
the master document wins. Conflicts are logged here, not silently resolved.

## Context

The master document is a RESYNTH five-stage consolidation of three frontier-AI
orchestration sources (S01–S03), with per-paragraph provenance markers and an
explicit conflicts/gaps register. It covers Claude Fable 5 specifics, the
frontier-as-judge orchestration pattern, Agent Skills, MCP supply-chain risk,
context engineering, evaluation tooling, and a converged layered architecture.
It supersedes the earlier project research as the strategic reference.

`Final_Research-Agent_Brain.md` remains the project-specific research for
Agent Brain's concrete Phase 1 scope (Lab Controller, ingestion, memory,
capsules) and stays in place.

## Known divergences (logged, not resolved)

- The master document is Claude-centric strategy and tooling research; it does
  not redefine Agent Brain's five-layer architecture or Phase 1 scope. No
  direct contradiction with ADR-001…007 was found on promotion.
- The master document's own conflicts (G007 umbrella terminology, G029 NeMo
  Guardrails maturity) are inherited as-is.

## Consequences

- Project `CLAUDE.md` points to the master document first.
- The first ingestion target for the Phase 1 pipeline is the master document
  itself, hashed and provenance-stamped.
- Orchestration patterns used in builds (architect → workers → reviewer →
  judge, handoff packets, verify-before-accept) follow the master document.
