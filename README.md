# SubstrateOS

A thin, local-first AI orchestration harness. Not a platform.

## How to Use (Start Here — No Experience Needed)

Everything is driven by one command: **`labctl`**. Think of it as the remote
control for the whole system. You never need to touch the internals.

**One-time setup.** Open PowerShell in this folder and paste these two lines
(on Linux/WSL use `python3 -m venv` and `.venv/bin/` instead):

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e "scripts[dev]"
```

**Day-to-day.** Four buttons on the remote, in the order you'd normally press them:

```powershell
.\.venv\Scripts\labctl doctor    # "Are you healthy?"  - checks your environment
.\.venv\Scripts\labctl ingest <file.md>   # "Read this and remember it" - adds a source to memory
.\.venv\Scripts\labctl status    # "What's going on, and what should I do next?"
.\.venv\Scripts\labctl gate      # "Check my work" - secret scan, lint, tests; run before any push
```

**If you are ever lost:** run `labctl status` and do whatever it lists under
"next recommended actions". That is the whole operating manual.

First time in a fresh clone, run `.\.venv\Scripts\labctl init` once to create
the manifest and folders (safe to re-run). Any command explains itself with
`--help`.

Power-user flags: `labctl ingest <file> --namespace <ns>` indexes into a
specific memory namespace; `--source-link <url>` records where a file came
from. Ingested output lands in `artifacts/ingest/`, memory in
`artifacts/memory.sqlite` (both local-only, gitignored). Tests live in
`scripts/tests` — run them with `.\.venv\Scripts\python -m pytest scripts/tests -q`.

## What This Is

SubstrateOS (formerly Agent Brain) is a disciplined harness that glues together existing high-performance tools
(Claude Code, agentmemory MCP, Docling, Firecrawl) into a repeatable "Idea to Repo" workflow.

The core principle is **Shared Brain, Isolated Capsules**: centralised long-term knowledge,
strict per-project execution isolation.

## Current Phase

Phase 1: Core Loop — first build landed 2026-06-11 (labctl CLI, ingestion,
SQLite FTS5 memory, status dashboard, release gate, capsule template).
Tool readiness landed 2026-06-12: gitleaks, Trivy, Semgrep (WSL), Docling and
Firecrawl installed and smoke-tested; the release gate now runs six stages —
secret scan, lint, tests, SAST, vuln scan, and a promptfoo eval (ADR-012) —
with `labctl gate --strict` for pre-publish runs.
Remaining Phase 1 work: multi-source ingestion (PDF/web), capsule launch,
token budget circuit breaker. Milestone-gated, no calendar deadlines; the
remaining work is one autonomous Fable 5 build campaign (ADR-010).
See docs/planning/phase-1-plan.md.
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
