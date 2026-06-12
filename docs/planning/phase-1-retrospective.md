# Phase 1 Retrospective

Written 2026-06-12 at the close of the completion campaign (ADR-010), which
finished Milestones 2-4 in one autonomous run on top of the 2026-06-11 build
and the 2026-06-12 alignment/tool-readiness run.

## What was built

- **Lab Controller (`labctl`, Typer per ADR-006):** init, status, ingest
  (text/PDF/URL dispatch), review (generate/list/approve), new, build,
  doctor, gate (six stages, `--strict`).
- **Ingestion:** deterministic normalisation to Markdown with provenance
  frontmatter (SHA256, capture time, source, namespace) before any model
  touches content. Docling is the deterministic PDF normaliser; Firecrawl is
  optional/metered behind `WebProvider` (ADR-005) with an actionable error
  when unconfigured. Dedupe by content hash; every run appended to the JSONL
  ingest log.
- **Review queue:** AI-derived summaries (`claude -p`) land under
  `derived/` with `origin: derived, promoted: false` and are not indexed
  until a human approves them. Exercised for real: one summary of the
  ingested "Building Effective Agents" post was generated, human-approved,
  and only then indexed.
- **Memory:** built-in SQLite FTS5 provider (ADR-009), BM25 ranking,
  namespace isolation in SQL. Three real source types searchable with
  provenance (master doc text, arXiv PDF, scraped web page).
- **Capsules:** `labctl new` scaffolds a sibling-directory capsule
  (ADR-014) from the WSL2-validated devcontainer template with isolation
  guarantees intact; `labctl build` runs host-scoped headless claude with
  stream-json metering (ADR-015) and a token budget circuit breaker
  (ADR-016) that was demonstrated live (7,120 tokens vs a 50-token budget;
  process tree killed; breaker record logged).
- **Capstone (success metric):** the OQ-006 research dashboard was built
  end to end *through the harness* — scaffolded by `labctl new`, its 21 raw
  sources ingested into its own namespace, built by `labctl build` in 23
  turns / 154,685 metered tokens, verified (39 stdlib unittest tests,
  gitleaks/Semgrep/Trivy all clean), and pushed to the private repo
  `Markus-Doc/research-dashboard` (MIT, M. Walker, no PII).

## Judgement calls (all recorded as ADRs)

- Capsules are siblings of the SubstrateOS repo, never nested (ADR-014).
- Phase 1 `lab build` is host-scoped; in-container execution is Phase 2
  (ADR-015). `--dangerously-skip-permissions` is owner policy on this
  machine, not product policy.
- Token budget counts input + output + cache-creation tokens, excludes
  cache reads; default 2M per run (ADR-016).
- Headless claude children run with a cleaned environment (ADR-015).

## What the capstone failures taught us

The first two capstone build attempts produced zero files, and the failures
were the most valuable part of the campaign — each exposed a real harness
defect that unit tests with mocked subprocesses could never catch:

1. **Stale `ANTHROPIC_API_KEY` in the user environment** silently overrides
   the claude CLI's subscription login; every headless call failed with
   "Invalid API key".
2. **Inherited `CLAUDECODE`/`CLAUDE_CODE_*` variables** (present whenever
   labctl is driven from inside a Claude Code session) made the child treat
   itself as a restricted nested session that auto-denies file writes even
   with permissions skipped.
3. **The Windows npm `claude.CMD` shim mangles multiline argv**, silently
   dropping every flag after the first newline in the mission text —
   including the permissions flag. Missions now travel on stdin.
4. **`proc.kill()` orphans the real node process on Windows** (it kills only
   the cmd shim); the orphan held the capsule directory open. The breaker
   now kills the full process tree (`taskkill /T /F`).

Pattern: every defect lived at the host/child process boundary on Windows.
Phase 2's in-container execution dissolves most of this class.

## What Phase 2 inherits

- A working Idea-to-Repo loop with evidence, and a clean provider seam for
  swapping Firecrawl, adding vector retrieval (local embeddings on the RTX
  3070), or moving memory behind agentmemory MCP if it earns its place.
- The capsule template, validated but not yet wired to in-container claude
  execution — that is Phase 2's first job (ADR-015).
- The run-log/stream-json metering contract for budgets; per-campaign
  cumulative accounting is still open.
- Known limitation: re-ingesting unchanged content skips the output file
  but still re-indexes chunks into memory (duplicate rows). Harmless for
  Phase 1 scale; fix when memory grows a dedupe constraint in Phase 2.
- The OQ-006 dashboard reads its own example data; pointing it at live
  SubstrateOS state files (the original input list) is a small follow-up.

## Verdict

Phase 1 success metric met: a personal research dashboard built and audited
from raw sources to GitHub with all security gates passing, driven through
the harness rather than hand-built.
