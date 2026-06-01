# ADR-003: MCP Memory Server as the Memory Interface

Date: 2026-06
Status: Accepted

## Decision

Use an MCP-compatible memory server (agentmemory) as the sole interface
for persistent knowledge storage and retrieval.

## Context

The Model Context Protocol is now the standard interface for tool-augmented agents
across major model providers. Building against MCP ensures the memory layer is
portable and replaceable regardless of which execution engine is active.

## Retrieval Design

Hybrid retrieval: BM25 keyword search plus vector similarity.
Every chunk stored with SHA256 content hash, capture timestamp, and source URL.
AI-generated summaries flagged as derived data and queued for human review before promotion to trusted memory.

## Consequences

- Memory is vendor-agnostic and stored in open formats.
- Adding or replacing a model provider does not require memory migration.
- Human review gate prevents hallucinations from becoming trusted facts.
