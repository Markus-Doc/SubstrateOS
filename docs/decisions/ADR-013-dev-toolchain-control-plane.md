# ADR-013: Dev toolchain in the gate; Windows + WSL2 is the control plane

Date: 2026-06-12
Status: Accepted

## Decision

Two undocumented deviations from the research documents are legitimised:

1. **ruff and pytest are gate tooling, not stack additions.** The release
   gate's `lint` and `tests` stages (ruff, pytest) are ordinary Python dev
   hygiene for the labctl package itself. They are not new tools, frameworks,
   or platforms in the sense of the CLAUDE.md core rule — that rule governs
   the orchestration stack (memory, ingestion, agents, evaluation), not the
   linter and test runner of the controller's own codebase.
2. **The "Lab" control plane is the Windows host plus WSL2.** Where
   Final_Research §2 says "the local Ubuntu machine ('Lab') serves as the
   orchestration and storage hub", the implemented control plane is the
   Windows 11 host running labctl natively, with WSL2 (Ubuntu) supplying the
   Linux-only tooling (devcontainer validation per ADR-007, Semgrep). The
   research's intent — a single local machine as orchestration and storage
   hub, heavy reasoning offloaded to frontier APIs — is preserved; only the
   literal OS phrasing differs.

## Context

The alignment audit (2026-06-12) flagged both as silent deviations: ruff and
pytest appear in no research document yet sit in the release gate, and the
research's "local Ubuntu machine" phrasing never matched the actual Windows
laptop + WSL2 setup that ADR-007 already built on. Neither deviation changes
architecture; both needed a paper trail so the next audit scores them as
decisions, not drift.

## Consequences

- Gate stages may use standard dev-hygiene tooling for labctl's own code
  without a research-doc citation; orchestration-stack tools still require
  one.
- "Lab machine" in plans and checklists (e.g. "Docling and Firecrawl
  confirmed working on the Lab machine") means the Windows host + WSL2 pair.
  Linux-only tools run inside WSL2 and are invoked from labctl via `wsl`
  when absent from the Windows PATH.
