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

**Phase 2 — performance, scale, and the Lab operator host — is in progress.**
Phase 1 (Core Loop) is complete; the history below records how we got here.

Phase 1: Core Loop — first build landed 2026-06-11 (labctl CLI, ingestion,
SQLite FTS5 memory, status dashboard, release gate, capsule template).
Tool readiness landed 2026-06-12: gitleaks, Trivy, Semgrep (WSL), Docling and
Firecrawl installed and smoke-tested; the release gate now runs seven stages —
secret scan, lint, tests, SAST, vuln scan, a promptfoo eval (ADR-012), and a
supply-chain audit of skills/MCP/plugins (ADR-024) — with `labctl gate --strict`
for pre-publish runs.
Phase 1 completed 2026-06-12 (autonomous campaign per ADR-010): multi-source
ingestion (text/PDF/web via Docling and Firecrawl), review queue with human
promotion, capsule lifecycle (`labctl new` / `labctl build`) with a live-fired
token budget circuit breaker, and the Milestone 4 capstone — the OQ-006
research dashboard built end to end through the harness and pushed to a
private repo with gitleaks/Semgrep/Trivy green.
See docs/planning/phase-1-plan.md and docs/planning/phase-1-retrospective.md.
Phase 2 in progress (docs/planning/phase-2-plan.md, realigned 2026-06-12 per
ADR-017): the Lab host as a remote agent operator — `labctl lab` wake / status
/ sync / dispatch landed 2026-06-12 with the box provisioned and
subscription-authed — plus in-container capsule execution and Dynamic
Workflows, capstoned by a codebase-wide audit of SubstrateOS itself through
the harness. Hybrid retrieval is deferred behind `MemoryProvider` (ADR-017).
Stack: Python (Typer) Lab CLI, SQLite FTS5 memory (ADR-009), Claude Code.

## Remote trigger (ADR-018)

Message the Lab box from anywhere: a Telegram message arrives → the box wakes
on its RTC duty cycle → the mission executes through the standard capsule
machinery → the result is reported back on the same chat. Six chat commands:
`/status`, `/run <mission>`, `/usage`, `/sleep`, `/stay <minutes>`, `/help`.
Configuration lives in the gitignored `.env`: `TRIGGER_TELEGRAM_TOKEN` (bot
token) and `TRIGGER_ALLOWED_USER_IDS` (numeric-id allowlist). The box wakes,
drains the queue, and re-suspends on a fixed interval, so worst-case command
latency equals the wake interval (default 10 minutes); `/stay` keeps it
awake. Install on the box with `labctl trigger install` (unit template in
`templates/trigger-systemd/`); threat model in SECURITY.md.

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
