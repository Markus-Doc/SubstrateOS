# Phase 1 Full Build Prompt (for /plan → /goal)

> This is the canonical prompt for the Phase 1 AFK build run. Pass it to /plan;
> execute the resulting plan to completion as /goal. Saved here so the running
> session can re-read its own mission at any point.

---

## Mission

Plan and then fully execute the **Phase 1 build of Agent Brain** end-to-end as a `/goal`, running unattended while the owner is AFK. Produce working, tested, committed code — not further planning documents. Make judgement calls yourself; never stop to ask the owner. Record every significant judgement call as an ADR in `docs/decisions/`.

## Source of truth

- `MASTER_AI_System_Research.md` (repo root) is now the **master research document** for this project. First build action: record an ADR promoting it, git-add it (it is currently untracked), and update the source-of-truth pointer in the project `CLAUDE.md`.
- `docs/research/Final_Research-Agent_Brain.md` remains the project-specific research. Where the two conflict, the master document wins; log the conflict in the ADR rather than silently resolving it.
- All confirmed decisions in `docs/decisions/` (ADR-001 … ADR-007) and the closed answers in `docs/planning/open-questions.md` are binding. Do not relitigate them.

## Hard constraints

1. **5-hour total runtime cap.** At session start, write the start timestamp to `artifacts/run-meta.json`. Every loop iteration first checks elapsed time against that file. At T-minus-30-minutes enter wind-down: no new workstreams, finish in-flight verification, commit everything, write the completion report. Never let a loop schedule work that cannot finish inside the cap.
2. **Loops are dynamically paced, never on timers.** Use `/loop` in dynamic mode (self-scheduled wakeups). A loop re-runs only when it has a reason: a delegated task finished, a gate failed and produced a fix target, or the next milestone became unblocked. If a wait is needed (e.g. an install or test run in the background), schedule the wakeup to match the actual signal, not a fixed interval.
3. **Dynamic Workflows for coding agent orchestration, explicitly.** The orchestrator acts as architect and judge: it decomposes milestones into bounded subtasks and dispatches them to parallel subagents using self-contained handoff packets — repo path, exact objective, in/out of scope, expected evidence, verification commands, stop conditions. Workers implement; the orchestrator reviews diffs and test output and **verifies delegated claims before accepting them**. Nothing is committed until its tests pass. This is the architect → workers → reviewer → judge pattern from the master research. Skip delegation for tiny fixes and tightly coupled edits — do those inline.
4. **Respect existing ADRs:** SQLite only (ADR-001); no LangChain/LangGraph/AutoGen or any heavyweight framework (ADR-002); all memory access behind an interface, repo files remain source of truth (ADR-003/004); Firecrawl is cloud-API, optional, metered, behind a provider interface — do **not** wire a key or call it in this run (ADR-005); Lab Controller is a Python Typer CLI with minimal commands (ADR-006); Devcontainer configs WSL2-compatible first (ADR-007).
5. **Security:** no secrets, keys, or credentials in any file. Run a secret scan (gitleaks if installable, else a scripted regex/entropy fallback) before any push; a failed scan blocks the push, full stop. New tooling installs go into a project-local `.venv` only.
6. **Environment:** Windows 11 host, PowerShell, Python 3.11+. Pure-Python, cross-platform code; no Windows-only or Docker-Desktop-specific behaviour.

## Build scope, in strict priority order

Complete each milestone (code + tests + evidence + commit) before starting the next. If the time budget forces cuts, cut from the bottom.

1. **Lab Controller CLI.** Python package under `scripts/` using Typer. Commands per ADR-006: `init`, `status`, `ingest`, `doctor`. `doctor` checks environment health (Python version, venv, git state, required dirs, config presence).
2. **Ingestion pipeline (deterministic core).** `ingest <path-or-url>` normalises a raw source into Markdown with SHA256 content hash, capture timestamp, and source link, stored under a project-scoped location. Include the review-queue convention: AI-derived summaries are flagged and unpromoted by default. **First real ingestion target: `MASTER_AI_System_Research.md` itself.**
3. **Memory provider interface.** A storage-agnostic interface with an SQLite implementation: scoped namespaces per project, BM25 keyword retrieval (vector retrieval stubbed behind the interface, not implemented). Integration with an external agentmemory MCP server is optional — attempt it only if trivial; never block on it (ADR-004).
4. **Status dashboard — the Phase 1 success metric.** `status` renders the full OQ-006 display list from real repo state: project name/phase, source-of-truth doc, confirmed decisions, open questions, next recommended actions, configured providers, missing configuration, last ingestion run, environment warnings.
5. **Release gate.** A `gate` command (or script) chaining: secret scan, lint, pytest. Wire it so the final push of this session only happens if the gate passes.
6. **Capsule Devcontainer template.** WSL2-compatible `devcontainer.json` + Dockerfile template with scoped mounts per the architecture doc. Config only; validate with Docker if reachable from this host, otherwise record "deferred — no Docker runtime available" with evidence and move on.

## Definition of done

- `pytest` fully green; `doctor` passes; `status` renders all OQ-006 fields from live repo state; the master research doc has been ingested with hash + provenance; `gate` passes.
- Evidence for every milestone (test output, command transcripts) saved under `artifacts/` and the pointers committed.
- Docs updated: phase-1-plan progress noted, new ADRs recorded, project `CLAUDE.md` source-of-truth pointer updated.
- A final completion report at `artifacts/phase-1-completion-report.md` summarising what was built, what was cut, every judgement call, and exact runtime used.
- Incremental commits on `main` throughout with clear messages; push to `origin/main` at the end **only if the secret scan passes**.

## If blocked

Never wait on the owner. Time-box any external dependency (network install, flaky tool) to 10 minutes, then take the simplest in-scope fallback, stub behind an interface, record the decision, and continue. A degraded-but-honest milestone beats a stalled run.
