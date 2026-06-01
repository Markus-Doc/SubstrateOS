# ADR-001: SQLite over Postgres for Phase 1 Memory Backend

Date: 2026-06
Status: Accepted

## Decision

Use SQLite as the memory backend for the agentmemory MCP server in Phase 1.

## Context

A full Postgres deployment would require managing a running server process,
connection pooling, and schema migrations from day one. The Phase 1 goal is
velocity: establish the core Idea to Repo loop, not build infrastructure.

## Consequences

- Minimal operational overhead in Phase 1.
- agentmemory MCP provides a vendor-agnostic interface.
- All memory stored in open format. Migration to Postgres + pgvector is a
  well-defined Phase 2 task with no architecture changes required above the memory layer.

## Rejected Alternative

Custom Postgres platform in v1. Rejected as premature over-engineering.
