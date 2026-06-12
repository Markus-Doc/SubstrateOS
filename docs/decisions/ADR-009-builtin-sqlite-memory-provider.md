# ADR-009: Built-in SQLite FTS5 memory provider; agentmemory MCP deferred

Date: 2026-06-11
Status: Accepted

## Decision

Phase 1 memory is served by labctl's own `SQLiteMemory` provider (stdlib
sqlite3, FTS5 virtual table, native bm25() ranking, namespace filtering
enforced in SQL). Integration with an external agentmemory MCP server is
deferred; it remains a drop-in alternative behind the `MemoryProvider`
interface.

## Context

ADR-003 fixed MCP as the memory interface standard and ADR-004 already
demoted agentmemory to an optional provider that must never be a hard
dependency. During the 2026-06-11 autonomous build, standing up the external
server added operational surface (install, process lifecycle, smoke testing)
without adding Phase 1 capability: SQLite FTS5 gives BM25 keyword retrieval —
the only retrieval mode Phase 1 requires — with zero dependencies. Vector
retrieval is stubbed (`NotImplementedError`) at the interface, exactly where
a hybrid backend would slot in.

## Consequences

- `labctl ingest` indexes chunks directly via `SQLiteMemory`; no daemon runs.
- Exposing the same store to agents over MCP (or swapping in agentmemory) is
  a provider change, not an architecture change.
- The Milestone 1 checklist item "agentmemory MCP server installed and
  smoke-tested" is superseded by this provider until multi-agent access is
  actually needed.
- Vector/hybrid retrieval is assigned to Phase 2 (local embeddings and
  rerankers on the RTX 3070, per Final_Research Phase 2), filling the
  `NotImplementedError` stub behind the same interface. (Addendum 2026-06-12.)
