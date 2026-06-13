# SubstrateOS: Claude Code Context

## Project
SubstrateOS (formerly Agent Brain). Local-first AI orchestration harness.
Phase 2 of 3: performance, scale, and the Lab operator host (ADR-017).

## Scope Right Now
Phase 1 complete (2026-06-12; see docs/planning/phase-1-retrospective.md).
Phase 2 realigned 2026-06-12 per ADR-017: the Lab host is a remote agent
operator, not a compute node — `labctl lab` (wake/status/sync/dispatch)
landed and the box is provisioned with subscription auth only. Remaining
campaign tail per docs/planning/phase-2-plan.md: M1 inherited debt,
in-container capsule execution (needs Docker on the box), Dynamic Workflows
+ SubstrateOS-audit capstone, M7 remote trigger pathway (OQ-007 resolved by
ADR-018: Telegram long-poll + RTC self-wake duty cycle + Tailscale SSH),
close-out. Hybrid retrieval is deferred behind MemoryProvider (ADR-017).
Build target remains the labctl package under scripts/.

## Core Rules
- Treat docs/research/master-research.md as the master research document (ADR-008, superseded-input per ADR-020).
- docs/research/Final_Research-Agent_Brain.md is the project-specific research; the master document wins on conflict.
- Do not introduce new tools, frameworks, or platforms not already in the research doc.
- Code lives in scripts/ (labctl package) only; tests must pass before commit.
- Keep all files clean Markdown, readable by both humans and LLM agents.
- Record every significant decision as an ADR in docs/decisions/.
- Do not allow secrets, keys, or credentials in any file.

## Confirmed Rejected Approaches
- Postgres in Phase 1 (ADR-001)
- LangGraph, AutoGen, or any heavyweight agent framework (ADR-002)
- Local inference on the i7 laptop

## Architecture Reference
See docs/architecture/system-overview.md for the five-layer architecture.

## Memory Layer
Built-in SQLite FTS5 provider (`SQLiteMemory` in scripts/labctl/memory.py):
BM25 keyword retrieval via native bm25() ranking, namespace isolation enforced
in SQL, every chunk stored with SHA256 hash and source URL. agentmemory MCP
integration is optional and deferred behind the MemoryProvider interface
(ADR-009). Vector/hybrid retrieval is deferred to Phase 2 (local embeddings on
the RTX 3070).
