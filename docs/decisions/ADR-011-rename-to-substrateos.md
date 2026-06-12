# ADR-011: Project renamed from Agent Brain to SubstrateOS

Date: 2026-06-12
Status: Accepted

## Decision

The project is renamed **SubstrateOS** (owner's choice, 2026-06-12). The GitHub
repo is renamed accordingly; the manifest file becomes `substrateos.json` and
the default memory namespace becomes `substrateos`.

## Context

"Agent Brain" was the working title inherited from the research phase. The
owner wants a more professional name for the persistent architecture that
frontier execution engines (currently Claude Fable 5) bolt onto. "Substrate"
captures the role precisely: the durable layer — memory, ingestion, capsules,
gates — underneath replaceable models (ADR/no-vendor-lock-in principle in the
system overview).

## Consequences

- Branding surfaces updated: README, CLAUDE.md, system-overview title, capsule
  template comments, labctl docstrings, manifest defaults, tests.
- Manifest renamed `agentbrain.json` -> `substrateos.json`; `labctl` reads only
  the new name. Default namespace `agent-brain` -> `substrateos`; local memory
  was re-ingested under the new namespace (artifacts are local-only and
  regenerable).
- Historical documents keep their original titles: research docs in
  `docs/research/` and `raw/research/` ("My Agent Brain"), prior ADRs, and the
  phase-1 build prompt are records, not branding.
- Local folder rename (`Agent-Brain` -> `SubstrateOS`) is done by the owner
  outside a session, since the agent's working directory lives inside it.
