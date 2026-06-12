# ADR-010: Milestone-driven plans, agent-executed builds; no calendar deadlines

Date: 2026-06-12
Status: Accepted

## Decision

Phase plans are structured as milestones gated only by completion of their
checklists, never by dates, weeks, or any calendar framing. Build runs are
executed by the frontier execution engine (currently Claude Fable 5) as
autonomous, loop-driven campaigns — dynamic pacing, agents and subagents where
they add real leverage — driving a phase through to its success metric in one
campaign rather than stopping at a time box.

## Context

The original Phase 1 plan was framed as "Weeks 1-4", a human-paced schedule
inherited from the research template. In practice the 2026-06-11 build run
delivered roughly half the phase in a single autonomous session, demonstrating
that calendar framing both under-asks the execution engine and creates false
"behind/ahead of schedule" signals. The owner's direction (2026-06-12) is that
plans must never be held back or dictated by dates; progress is driven by
/loop-style autonomous workflows with agent/subagent delegation.

## Consequences

- phase-1-plan.md retitled and restructured: "Week N" sections become
  "Milestone N"; an Execution Model section records the loop-driven approach.
- Future phase plans are written milestone-first from the start.
- The remaining Phase 1 work (multi-source ingestion, capsule launch via
  `lab build`, token budget circuit breaker, Semgrep/Trivy, the end-to-end
  Milestone 4 build) is one Fable 5 autonomous build campaign, not scheduled
  work.
- Time estimates may still appear in commentary but carry no gating power.
