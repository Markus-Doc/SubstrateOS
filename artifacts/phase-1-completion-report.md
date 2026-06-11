# Phase 1 Build — Completion Report

Run: phase-1-full-build, 2026-06-11. Mission spec: docs/planning/phase-1-build-prompt.md.
Start 10:40:41Z; active build complete by ~10:53Z. Runtime ~13 minutes of a
5-hour cap. Nothing was cut for time.

## Built (all milestones complete)

| Milestone | Commit | Delivered |
|---|---|---|
| M0 source-of-truth handoff | 8198ec3 | ADR-008 promoting MASTER_AI_System_Research.md; CLAUDE.md updated |
| M1 package skeleton | d23ba1e | labctl Typer package (scripts/), init + doctor, config/timebox modules, 9 tests |
| M2+M3 ingestion + memory | b8af326 | Deterministic ingest (SHA256/timestamp/source frontmatter, review-queue convention, ingest log) + SQLiteMemory (FTS5 BM25, SQL-enforced namespaces, vector stub), wired as `labctl ingest` |
| M6 capsule template | c91c01f | templates/capsule-devcontainer/ — non-root, no sudo, scoped mounts, Lab Controller placeholder tokens; `docker build` validated in WSL2 (twice: agent + orchestrator) |
| M4 status dashboard | 870b951 | `labctl status` rendering every OQ-006 field from live repo state |
| M5 release gate | 4dfb9c5 | `labctl gate`: secret scan (gitleaks or built-in fallback), ruff, pytest |

Final state: 36/36 tests green, ruff clean, gate all-PASS, doctor all-ok.
Master research doc ingested as first source: sha256 8a059e27679a…, 25 chunks,
BM25-retrievable in namespace `agent-brain`, isolation verified.

## Orchestration actually used

Dynamic Workflows as specified: orchestrator as architect/judge; three parallel
background subagents (M3 memory, M6 devcontainer, M5 gate) on self-contained
handoff packets; every delegated claim re-verified by the orchestrator (tests
re-run, code reviewed, docker build re-executed) before acceptance. Loops were
signal-driven (subagent completion notifications), zero timer-based waits.

## Judgement calls

1. **ADR-009**: external agentmemory MCP server deferred; built-in SQLite FTS5
   provider behind the MemoryProvider interface serves Phase 1.
2. M6 agent validated via Docker **inside WSL2** rather than reporting
   "deferred" when PowerShell-side docker was absent — correct per ADR-007.
3. Capsule base image is python:3.11-slim with a hand-built non-root user
   instead of the devcontainers image (which ships passwordless sudo).
4. Dashboard output is ASCII-only (Windows legacy codepage rendering).

## Process notes (honest record)

- **Slip**: `git add scripts` during the M4 commit (870b951) swept in the M5
  subagent's in-progress gate.py before verification. gate.py was subsequently
  verified unmodified and its tests landed in 4dfb9c5. History not rewritten.
- **False alarm**: an ad-hoc PowerShell elapsed-time check mixed DateTime
  Kinds and reported 9h48m (sign-less negative timespan); commit timestamps
  disproved it and the corrected check showed 12m41s. labctl/timebox.py uses
  timezone-aware parsing and is not affected.

## Evidence

artifacts/evidence/: m2-m3-retrieval.txt, m2-m3-pytest.txt,
m6-docker-build.txt, m4-status-live.txt, m5-gate-live.txt. Local-only
(gitignored): artifacts/ingest/, artifacts/memory.sqlite, run-meta.json.

## Recommended next steps (not done — out of this run's scope)

- Ingest two more source types (PDF, web) toward the Week 2 checklist;
  Docling/Firecrawl onboarding per ADR-005.
- `lab build` capsule launch + token budget circuit breaker (Week 3 items).
- Exercise the review queue with a real AI-derived summary.
- Optional: expose SQLiteMemory over MCP when multi-agent access is needed.
