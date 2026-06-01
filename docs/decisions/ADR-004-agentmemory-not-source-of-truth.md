# ADR-004: agentmemory as Optional Provider, Not Source of Truth

Date: 2026-06
Status: Accepted

## Decision

Use rohitg00/agentmemory as the reference MCP memory package, but do not make it a hard Phase 1 dependency. Memory must sit behind a provider interface.

## Context

Agent memory is useful for cross-session recall but must not replace repo documentation, structured state files, decision records, or explicit instructions. Phase 1 source of truth is always the repo. rohitg00/agentmemory was chosen because it supports MCP, hooks, and REST-style usage, keeping it more flexible than a Claude-only memory setup.

## Constraints

- agentmemory must never replace repo documentation or decision records.
- All persistent project state lives in files, not in the memory store.
- The memory provider interface must allow swapping or disabling the backend without redesigning the system.

## Consequences

- Phase 1 can proceed without agentmemory running.
- Memory integration is an enhancement, not a prerequisite.
- Provider abstraction enables future migration to a different MCP server.
