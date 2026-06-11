# Agent Brain

A thin, local-first AI orchestration harness. Not a platform.

## How to Use (Quick Start)

One-time setup from the repo root (Windows PowerShell; on Linux/WSL use `python3 -m venv` and `.venv/bin/`):

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e "scripts[dev]"
```

Then drive everything through the `labctl` CLI:

```powershell
.\.venv\Scripts\labctl init      # create the project manifest + required dirs (idempotent)
.\.venv\Scripts\labctl doctor    # check your environment (python, git, sqlite FTS5, dirs)
.\.venv\Scripts\labctl status    # the dashboard: phase, decisions, providers, next actions
.\.venv\Scripts\labctl ingest <file.md>   # hash + provenance-stamp a source, index it into memory
.\.venv\Scripts\labctl gate      # release gate: secret scan -> lint -> tests (run before any push)
```

Typical session: `doctor` to confirm the environment is healthy, `ingest` your research
sources, `status` to see project state and the next recommended actions, `gate` before
pushing anything.

Useful flags: `labctl ingest <file> --namespace <ns>` to index into a specific memory
namespace, `--source-link <url>` to record where a file originally came from. Run any
command with `--help` for details.

Ingested output lands in `artifacts/ingest/`, memory in `artifacts/memory.sqlite`
(both local-only, gitignored). Tests live in `scripts/tests` — run them directly with
`.\.venv\Scripts\python -m pytest scripts/tests -q`.

## What This Is

Agent Brain is a disciplined harness that glues together existing high-performance tools
(Claude Code, agentmemory MCP, Docling, Firecrawl) into a repeatable "Idea to Repo" workflow.

The core principle is **Shared Brain, Isolated Capsules**: centralised long-term knowledge,
strict per-project execution isolation.

## Current Phase

Phase 1: Core Loop — first build landed 2026-06-11 (labctl CLI, ingestion,
SQLite FTS5 memory, status dashboard, release gate, capsule template).
Remaining Phase 1 work: multi-source ingestion (PDF/web), capsule launch,
token budget circuit breaker. See docs/planning/phase-1-plan.md.
Stack: Python (Typer) Lab CLI, SQLite FTS5 memory (ADR-009), Claude Code.

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
