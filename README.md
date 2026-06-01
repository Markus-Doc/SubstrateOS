# Agent Brain

A thin, local-first AI orchestration harness. Not a platform.

## What This Is

Agent Brain is a disciplined harness that glues together existing high-performance tools
(Claude Code, agentmemory MCP, Docling, Firecrawl) into a repeatable "Idea to Repo" workflow.

The core principle is **Shared Brain, Isolated Capsules**: centralised long-term knowledge,
strict per-project execution isolation.

## Current Phase

Phase 1: Core Loop (Weeks 1-4)
Objective: Establish the Idea to Repo workflow using existing tools.
Stack: Python Lab CLI, agentmemory MCP (SQLite), Docling, Claude Code.

## Repo Structure

- docs/research/      Source of truth research documents
- docs/architecture/  System design and layer diagrams
- docs/decisions/     Architecture Decision Records (ADRs)
- docs/planning/      Phase plans and open questions
- scripts/            Lab Controller CLI (Phase 1 build target)
- artifacts/          Build outputs, context packs, logs

## Do Not

- Do not start build work without reading docs/architecture/system-overview.md
- Do not add Postgres, LangGraph, AutoGen, or local inference models
- Do not allow context bleed between project capsules
