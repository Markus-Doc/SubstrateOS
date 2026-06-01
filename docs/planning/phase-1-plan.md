# Phase 1 Plan: The Core Loop (Weeks 1-4)

## Objective

Establish the Idea to Repo workflow end to end using existing tools.

## Success Metric

Successfully build and audit a personal research dashboard from raw sources to GitHub,
with all security gates passing.

## Stack

- Lab Controller: Python CLI (scaffolding, worktree management, container launch)
- Memory: agentmemory MCP, SQLite backend
- Ingestion: Docling (docs), Firecrawl (web)
- Build Agent: Claude Code

## Task Breakdown

### Week 1: Skeleton and Tooling

- [ ] Repo foundation committed (this scaffold)
- [ ] Open questions resolved (see docs/planning/open-questions.md)
- [ ] agentmemory MCP server installed and smoke-tested
- [ ] Docling and Firecrawl confirmed working on the Lab machine
- [ ] .devcontainer base config created for a test capsule

### Week 2: Ingestion Pipeline

- [ ] Ingest at least three research sources (PDF, web page, plain text)
- [ ] All outputs normalised to Markdown with provenance metadata
- [ ] Memory chunks stored with SHA256 hash and source URL
- [ ] Review queue working: AI summaries held until manually approved

### Week 3: Lab Controller CLI (Minimal)

- [ ] `lab new <project-name>` scaffolds a capsule directory and Devcontainer
- [ ] `lab ingest <source>` runs the ingestion pipeline for a source
- [ ] `lab build <project-name>` launches Claude Code in the capsule context
- [ ] Token budget circuit breaker fires correctly on a test run

### Week 4: First Full Build and Audit

- [ ] Personal research dashboard built end to end inside a capsule
- [ ] Gitleaks, Semgrep, and Trivy all pass on the output
- [ ] Build log and evidence committed to artifacts/
- [ ] Phase 1 retrospective written and committed to docs/planning/

## Out of Scope for Phase 1

- Postgres migration
- Local embeddings or reranker models
- Multi-agent swarm tasks
- Cloud deployment of any component
