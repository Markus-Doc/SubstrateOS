# SubstrateOS: Claude Code Context

## Project
SubstrateOS (formerly Agent Brain). Local-first AI orchestration harness.
Phase 1 of 3. Build phase: Lab Controller CLI, ingestion, memory, status dashboard.

## Scope Right Now
Phase 1 build authorized (2026-06-11). Build target is the labctl package under
scripts/, per docs/planning/phase-1-build-prompt.md and the approved build plan.

## Core Rules
- Treat MASTER_AI_System_Research.md (repo root) as the master research document (ADR-008).
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
