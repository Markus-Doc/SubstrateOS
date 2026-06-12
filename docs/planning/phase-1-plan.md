# Phase 1 Plan: The Core Loop

## Progress: autonomous build run 2026-06-11

Executed per docs/planning/phase-1-build-prompt.md (commits 8198ec3..HEAD).
Delivered: labctl Typer CLI (init, status, ingest, doctor, gate per ADR-006);
deterministic ingestion with SHA256/timestamp/source frontmatter and review-queue
convention; SQLite FTS5 memory provider with BM25 and namespace isolation
(agentmemory MCP integration deferred, ADR-009); OQ-006 status dashboard
rendering from live repo state; release gate (secret scan, ruff, pytest);
WSL2-validated capsule devcontainer template. Master research doc ingested as
first source (25 chunks, searchable). Evidence in artifacts/evidence/; full
summary in artifacts/phase-1-completion-report.md.

Not yet done from the original checklist: Docling install, Firecrawl setup,
multi-source ingestion (PDF/web), `lab build` capsule launch, token budget
circuit breaker, Semgrep/Trivy, the Milestone 4 end-to-end dashboard-project build.
Checklist below updated to reflect actual state.

## Progress: alignment + tool readiness run 2026-06-12

Closed the ~90% alignment audit gaps and provisioned the machine. Installed and
smoke-tested: gitleaks 8.30.1, Trivy 0.71.0, Docling (PDF→Markdown verified),
Firecrawl (key in local .env, single-page scrape verified), Semgrep 1.166.0 in
WSL. Release gate extended with sast (Semgrep), vuln-scan (Trivy), and evals
(promptfoo, ADR-012) stages plus `--strict`; doctor gained tool-presence
checks. ADR-012/ADR-013 recorded; CLAUDE.md memory section corrected to match
ADR-009 reality. Remaining work below is the ADR-010 autonomous campaign,
starting from a fully provisioned machine.

## Objective

Establish the Idea to Repo workflow end to end using existing tools.

## Execution Model (ADR-010)

No calendar deadlines. Milestones are gated by their checklists being done and
verified, never by dates or "weeks". The remaining Phase 1 work is executed by
Claude (Fable 5) as an autonomous build run — loop-driven (/loop, dynamic
pacing), using agents and subagents where they genuinely help — carrying the
checklist through to completion rather than stopping at a time box.

## Success Metric

Successfully build and audit a personal research dashboard from raw sources to GitHub,
with all security gates passing.

## Stack

- Lab Controller: Python CLI (scaffolding, worktree management, container launch)
- Memory: agentmemory MCP, SQLite backend
- Ingestion: Docling (docs), Firecrawl (web)
- Build Agent: Claude Code

## Task Breakdown

### Milestone 1: Skeleton and Tooling

- [x] Repo foundation committed (this scaffold)
- [x] Open questions resolved (see docs/planning/open-questions.md)
- [ ] agentmemory MCP server installed and smoke-tested (deferred — built-in SQLite provider instead, ADR-009)
- [x] Docling and Firecrawl confirmed working on the Lab machine (2026-06-12: PDF→Markdown and single-page scrape smoke tests passed; "Lab machine" = Windows host + WSL2 per ADR-013)
- [x] .devcontainer base config created for a test capsule (templates/capsule-devcontainer/, build-validated in WSL2)

### Milestone 2: Ingestion Pipeline

- [x] Ingest at least three research sources (PDF, web page, plain text) — master doc (text), arXiv 1706.03762 (PDF via Docling), anthropic.com/engineering/building-effective-agents (web via one metered Firecrawl scrape); all searchable (artifacts/evidence/m2-*)
- [x] All outputs normalised to Markdown with provenance metadata
- [x] Memory chunks stored with SHA256 hash and source URL
- [x] Review queue working: AI summaries held until manually approved (real claude -p summary generated 2026-06-12, human-approved, then indexed; labctl review list/generate/approve)

### Milestone 3: Lab Controller CLI (Minimal)

- [x] `lab new <project-name>` scaffolds a capsule directory and Devcontainer (sibling dir per ADR-014: devcontainer tokens substituted, capsule CLAUDE.md, MIT LICENSE, git init)
- [x] `lab ingest <source>` runs the ingestion pipeline for a source (text + PDF + URL dispatch)
- [x] `lab build <project-name>` launches Claude Code in the capsule context (host-scoped headless per ADR-015)
- [x] Token budget circuit breaker fires correctly on a test run (live demo 2026-06-12: 7120 tokens vs 50 budget, child tree killed, breaker record logged; artifacts/evidence/m3-breaker-demo-transcript.txt)

### Milestone 4: First Full Build and Audit

- [ ] Personal research dashboard built end to end inside a capsule
- [ ] Gitleaks, Semgrep, and Trivy all pass on the output
- [ ] Build log and evidence committed to artifacts/
- [ ] Phase 1 retrospective written and committed to docs/planning/

## Out of Scope for Phase 1

- Postgres migration
- Local embeddings or reranker models
- Multi-agent swarm tasks
- Cloud deployment of any component
