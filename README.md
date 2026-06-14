# SubstrateOS

A thin, local-first AI orchestration harness. Not a platform.

## Install (Start Here — No Experience Needed)

One installer, then `subos claude` works from any directory in a fresh shell.
Full step-by-step for all three platforms, plus troubleshooting:
**[INSTALL.md](INSTALL.md)**.

**Windows (PowerShell)** — in a clone of this repo:

```powershell
.\install.ps1
```

**Linux / macOS** — in a clone of this repo:

```sh
./install.sh
```

The installer checks Python (>= 3.11), installs the `labctl` + `subos` commands
with `pipx` (isolated, user-scope), and verifies with `subos --version` and
`labctl doctor`. **Open a new terminal afterwards** so PATH picks up the new
commands. Personal full-auto is opt-in: add `-FullAutoDefault` (Windows) or
`--full-auto-default` (Linux/macOS).

## How to Use

Everything is driven by **`labctl`** (the harness) and **`subos`** (launch an AI
engine as a SubstrateOS kernel). After installing, run them from anywhere:

```powershell
subos claude --dry-run   # preview launching Claude as a SubstrateOS kernel
subos claude             # launch it for real (Codex / Gemini / Cursor also work)
labctl doctor            # "Are you healthy?" - checks your environment + install
labctl status            # "What's going on, and what should I do next?"
labctl ingest <file.md>  # "Read this and remember it" - adds a source to memory
labctl gate              # "Check my work" - secret scan, lint, tests; before any push
```

**If you are ever lost:** run `labctl status` and do whatever it lists under
"next recommended actions". First time in a fresh clone, run `labctl init` once
to create the manifest and folders (safe to re-run). Any command explains itself
with `--help`.

Power-user flags: `labctl ingest <file> --namespace <ns>` indexes into a specific
memory namespace; `--source-link <url>` records where a file came from. Ingested
output lands in `artifacts/ingest/`, memory in `artifacts/memory.sqlite` (both
local-only, gitignored).

**Contributors / development install.** To hack on SubstrateOS itself, use an
editable install instead of the global one:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e "scripts[dev]"
.\.venv\Scripts\python -m pytest scripts/tests -q   # run the tests
```

After editing `substrate/methodology.md`, run `python scripts/sync_spec_data.py`
to refresh the copy bundled with the installed package (a drift-guard test
enforces they match).

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

## Engine-agnostic front-end & dynamic workflows (Phase 2)

SubstrateOS is the substrate; the AI engine is a swappable kernel (ADR-019). One
canonical spec (`substrate/methodology.md`) compiles to each engine's native
files (`CLAUDE.md`, `AGENTS.md`, …) — write once, run on any engine.

- `subos <engine>` — launch Claude/Codex/Gemini/Cursor as a SubstrateOS kernel
  (compiles the instruction file, applies the permission posture; `--full-auto`
  is opt-in, `--dry-run` inspects). The deterministic guarantees live in
  `labctl`, not the model, so swapping engines never weakens safety.
- `/substrateos` — in-session warm activation, compiled per engine.
- `labctl workflow run "<mission>"` — multi-agent orchestration (architect →
  workers → reviewer → judge; per-agent budget caps; verify-before-accept).
- `labctl audit <repo>` — codebase-quality audit as that workflow, BM25-grounded
  over the repo's memory namespace, producing a findings report (ADR-025).
- `labctl build --container` — run a capsule build in Docker; the circuit breaker
  kills the whole container; OAuth token injected by name only (ADR-025).
- `labctl research` — keep the OS current with AI best practices (ADR-021):
  `brief`/`sync` drive RESYNTH to re-synthesise a candidate, `review` diffs it against
  the ADRs/tooling/watch-list into a human-promoted report. Operated by your
  interactive `subos` session — **no headless spend** unless you pass `--auto`.
- `labctl conformance` — the cross-engine MUST contract.

Private customisation layers on via an **Overlay** (`SUBSTRATEOS_OVERLAY`,
scaffold at `templates/overlay-example/`); the Base ships blank and runs naked.

## Repo Structure

- substrate/          Canonical engine-neutral spec (compile source)
- docs/research/      Source of truth research documents
- docs/architecture/  System design and layer diagrams
- docs/decisions/     Architecture Decision Records (ADRs)
- docs/planning/      Phase plans and open questions
- scripts/            Lab Controller CLI (labctl + subos)
- templates/          Capsule + overlay scaffolds
- artifacts/          Build outputs, context packs, logs
- install.ps1 / install.sh   One-command installers (Windows / Linux-macOS)
- Dockerfile          Golden image — the same unit runs locally and on EKS (ADR-026)
- INSTALL.md          Full cross-platform install guide

## Do Not

- Do not start build work without reading docs/architecture/system-overview.md
- Do not add Postgres, LangGraph, AutoGen, or local inference models
- Do not allow context bleed between project capsules
