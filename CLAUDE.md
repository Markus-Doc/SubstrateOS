# Agent Brain: Claude Code Context

## Project
Agent Brain. Local-first AI orchestration harness.
Phase 1 of 3. Documentation and skeleton phase only.

## Scope Right Now
You are helping build the repo foundation: docs, ADRs, planning files, and config.
No application code is in scope until the architecture and phase plan are signed off.

## Core Rules
- Treat docs/research/Final_Research-Agent_Brain.md as the source of truth.
- Do not introduce new tools, frameworks, or platforms not already in the research doc.
- Do not write code in scripts/ until explicitly instructed.
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
agentmemory MCP server, SQLite backend, scoped per capsule namespace.
BM25 plus vector hybrid retrieval. Every chunk stored with SHA256 hash and source URL.
