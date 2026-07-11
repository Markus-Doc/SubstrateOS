# SubstrateOS

## Ownership and third-party rights

SubstrateOS is an original project by M. Walker. The repository-level MIT License covers the original code, documentation, architecture, and methodology. AI engines, dependencies, external tools, and standards retain their own rights and terms. The related `research-dashboard` repository is part of the same project family. See [NOTICE.md](NOTICE.md).

A thin, local-first AI orchestration harness. Not a platform.

## Install (Start Here, No Experience Needed)

One installer, then `subos claude` works from any directory in a fresh shell.
Full step-by-step for all three platforms, plus troubleshooting:
**[INSTALL.md](INSTALL.md)**.

**First, get the code:** `git clone` this repository (or download the ZIP from
GitHub and unzip it), then open a terminal in that folder and run the installer
for your OS.

**Windows (PowerShell)**, inside your clone of this repo:

```powershell
.\install.ps1
```

**Linux / macOS**, inside your clone of this repo:

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

## Going further, from first run to power user

A natural progression once `subos`/`labctl` are installed. Each step builds on the
last; every command explains itself with `--help`.

1. **Talk to your OS.** `subos claude` launches Claude as a SubstrateOS kernel, an
   interactive session that drives the harness for you. Start here for any task.
   Swap engines any time: `subos codex` / `subos gemini` / `subos cursor`.
2. **Preview, then choose your posture.** `subos claude --dry-run` shows exactly what
   will happen without launching. The default posture is safe; `--full-auto` opts
   into the engine's full-auto mode and `--platform-default` forces safe. Make
   full-auto your personal default with the `SUBSTRATEOS_FULL_AUTO` setting.
3. **Feed the brain.** `labctl ingest <file|url>` adds a source to local memory.
   AI-derived summaries enter a **review queue** (`labctl review list`, then
   `labctl review approve`), so nothing is trusted until you promote it.
4. **Check your work.** `labctl gate` runs the seven-stage release gate (secret scan,
   lint, tests, SAST, vuln scan, evals, supply-chain). Run it before every push, and
   `labctl gate --strict` before publishing.
5. **Orchestrate.** `labctl workflow run "<mission>"` runs a multi-agent build
   (architect -> workers -> reviewer -> judge); `labctl audit <repo>` audits a
   codebase the same way; `labctl new` / `labctl build` scaffold and run isolated
   **capsules**.
6. **Stay current.** `labctl research` keeps the OS aligned with AI best practices:
   it drives RESYNTH, diffs the result against your ADRs/tooling, and surfaces a
   review report. Guide: [docs/planning/research-pipeline.md](docs/planning/research-pipeline.md).
7. **Go remote / always-on.** `labctl lab` operates a wake-on-demand box; `labctl
   trigger` lets you message it (Telegram) and have it work while you're away.
8. **Make it yours.** Layer private settings via an **Overlay** (`SUBSTRATEOS_OVERLAY`,
   scaffold at `templates/overlay-example/`); the public Base ships blank.

**Billing note (interactive vs headless).** Talking to `subos claude` runs on your
normal subscription, including all the autonomous work it does for you in that
session. Only commands that spawn their *own* background agents (`labctl audit`,
`labctl build`, `labctl workflow run`, and `labctl research --headless`) use the
unattended "Agent SDK" lane. Everything is interactive (subscription) by default;
the headless lane is always opt-in.

## Current Phase

**The build is essentially complete and ready for UAT.** Phases 1 and 2 are
landed. Every architecture decision (ADR-001 through ADR-027) is Accepted, so no
open proposals remain. What's left is owner-triggered live verification plus an
optional Phase 3 that's deferred on purpose.

Phase 1, the Core Loop, landed 2026-06-11 and completed 2026-06-12: the `labctl`
CLI, multi-source ingestion (text, PDF, and web via Docling and Firecrawl), SQLite
FTS5 memory, a status dashboard, the seven-stage release gate (secret scan, lint,
tests, SAST, vuln scan, a promptfoo eval, and a supply-chain audit of
skills/MCP/plugins), and the capsule lifecycle (`labctl new` / `labctl build`) with
a live-fired token-budget circuit breaker. The Milestone 4 capstone, the OQ-006
research dashboard, was built end to end through the harness. See
docs/planning/phase-1-plan.md and docs/planning/phase-1-retrospective.md.

Phase 2 (docs/planning/phase-2-plan.md, realigned per ADR-017) added the Lab host
as a remote agent operator (`labctl lab` wake / status / sync / dispatch),
in-container capsule execution, and Dynamic Workflows (`labctl workflow run`,
`labctl audit`). Two further efforts landed on top. Cross-platform install and
distribution (ADR-026) lets a first-time user clone, run one installer, and get
`subos` working from any directory. The research-and-review pipeline (ADR-021,
`labctl research`) keeps the OS current with AI best practices. Hybrid retrieval
stays deferred behind `MemoryProvider` (ADR-017).

Nothing significant is left to build. The remaining items are live verification
runs that need hardware or credits you supply: the in-container circuit-breaker
demo (Docker), the self-audit capstone (Docker plus token spend), and the phone
trigger round-trip (your phone plus the lab box). A short close-out retrospective
is the only doc still pending.

Phase 3 is optional future scope, deferred on purpose: vector/hybrid retrieval when
hardware justifies it, cloud and EKS deployment (the Dockerfile already makes the
local container the deploy unit), and swarm orchestration.

Stack: Python (Typer) Lab CLI, SQLite FTS5 memory (ADR-009), and the AI engine of
your choice (Claude Code by default).

## Remote trigger (ADR-018)

Message the Lab box from anywhere. A Telegram message arrives, the box wakes on its
RTC duty cycle, the mission executes through the standard capsule machinery, and the
result is reported back on the same chat. Six chat commands: `/status`,
`/run <mission>`, `/usage`, `/sleep`, `/stay <minutes>`, `/help`. Configuration
lives in the gitignored `.env`: `TRIGGER_TELEGRAM_TOKEN` (bot token) and
`TRIGGER_ALLOWED_USER_IDS` (numeric-id allowlist). The box wakes, drains the queue,
and re-suspends on a fixed interval, so worst-case command latency equals the wake
interval (default 10 minutes); `/stay` keeps it awake. Install on the box with
`labctl trigger install` (unit template in `templates/trigger-systemd/`); threat
model in SECURITY.md.

## Engine-agnostic front-end & dynamic workflows (Phase 2)

SubstrateOS is the substrate; the AI engine is a swappable kernel (ADR-019). One
canonical spec (`substrate/methodology.md`) compiles to each engine's native files
(`CLAUDE.md`, `AGENTS.md`, and so on), so you write once and run on any engine.

- `subos <engine>`: launch Claude/Codex/Gemini/Cursor as a SubstrateOS kernel
  (compiles the instruction file, applies the permission posture; `--full-auto`
  is opt-in, `--dry-run` inspects). The deterministic guarantees live in
  `labctl`, not the model, so swapping engines never weakens safety.
- `/substrateos`: in-session warm activation, compiled per engine.
- `labctl workflow run "<mission>"`: multi-agent orchestration (architect ->
  workers -> reviewer -> judge; per-agent budget caps; verify-before-accept).
- `labctl audit <repo>`: codebase-quality audit as that workflow, BM25-grounded
  over the repo's memory namespace, producing a findings report (ADR-025).
- `labctl build --container`: run a capsule build in Docker; the circuit breaker
  kills the whole container; OAuth token injected by name only (ADR-025).
- `labctl research`: keep the OS current with AI best practices (ADR-021).
  `brief`/`sync` drive RESYNTH to re-synthesise a candidate, `review` diffs it
  against the ADRs/tooling/watch-list into a human-promoted report. Operated by your
  interactive `subos` session, with **no headless spend** unless you pass `--auto`.
- `labctl conformance`: the cross-engine MUST contract.

Private customisation layers on via an **Overlay** (`SUBSTRATEOS_OVERLAY`, scaffold
at `templates/overlay-example/`); the Base ships blank and runs naked.

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
- Dockerfile          Golden image; the same unit runs locally and on EKS (ADR-026)
- INSTALL.md          Full cross-platform install guide

## Do Not

- Do not start build work without reading docs/architecture/system-overview.md
- Do not add Postgres, LangGraph, AutoGen, or local inference models
- Do not allow context bleed between project capsules
