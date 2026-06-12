# Phase 1 Completion Report 2 — M2-M4 Campaign

Campaign: phase-1-completion-m2-m4 (ADR-010 autonomous run, /loop dynamic)
Start: 2026-06-12T03:42:33Z
Report written: 2026-06-12T04:37Z — **runtime ~55 minutes** of the 5-hour cap
(final gate + push followed immediately after; total stayed under 1.5 hours).
Baseline: c01ec79 (clean main).

## Definition of done — status

1. **Test suite green:** 77 passed (55 baseline + 22 new). ✔
2. **`labctl gate --strict`:** six stages PASS, zero skips (run at close-out,
   transcript in artifacts/evidence/final-gate-strict.txt). ✔
3. **Ingest handles text + PDF + URL:** three real sources searchable with
   provenance in the `substrateos` namespace — master research doc (text),
   arXiv 1706.03762 "Attention Is All You Need" (PDF via Docling, 31 chunks),
   anthropic.com/engineering/building-effective-agents (one metered Firecrawl
   scrape, 13 chunks). Evidence: m2-* transcripts. ✔
4. **Review queue end to end:** real `claude -p` summary generated,
   human-approved (the campaign's single flagged step), promoted and indexed.
   Evidence: m2-review-generate-transcript.txt. ✔
5. **`labctl new` + `labctl build` + breaker:** capsule scaffold per ADR-014;
   host-scoped build per ADR-015; breaker fired live (7,120 tokens vs 50
   budget, tree-kill, breaker record). Evidence: m3-breaker-demo-transcript.txt. ✔
6. **Private repo `Markus-Doc/research-dashboard`:** built through the
   harness (23 turns, 154,685 metered tokens, $2.45 API-equivalent), 39 own
   tests passing, gitleaks/Semgrep/Trivy clean, MIT (M. Walker), `main`
   branch, no PII in tree or history. Evidence: m4-*. ✔
7. **Plan ticked, retrospective + this report committed, pushed to main.** ✔

## New ADRs

- ADR-014 capsule sibling directory layout
- ADR-015 host-scoped lab build, skip-permissions policy, cleaned child env,
  stdin mission delivery
- ADR-016 token budget counting rule + 2M default

## Defects found and fixed (real-run discoveries)

1. Stale `ANTHROPIC_API_KEY` overriding the claude CLI credential store.
2. Inherited `CLAUDECODE`/`CLAUDE_CODE_*` restricting nested headless claude
   to read-only.
3. Windows `claude.CMD` shim mangling multiline argv (flags silently lost) —
   missions now travel via stdin.
4. `proc.kill()` orphaning node on Windows; breaker now kills the process
   tree.
5. `review approve/generate` crashed on relative paths (fixed + regression
   test).

## Commits (this campaign)

- 2bcf830 feat: ingest source-type dispatch (PDF/URL) + review queue (M2)
- 1553b57 feat: capsule lifecycle - labctl new/build + token circuit breaker (M3)
- dee87f1 fix: circuit breaker kills the full process tree on Windows (M3)
- 19495a7 fix: headless claude children get fully cleaned env (ADR-015)
- 6bdcf22 fix: deliver build mission via stdin, not argv (ADR-015)
- (close-out commit: plan ticks, README, retrospective, this report, evidence)

## Out of scope, untouched (Phase 2+)

Postgres/pgvector, local embeddings, vector retrieval, in-container agent
execution, Garak/PyRIT, OWASP presets, web dashboard UI, cloud deployment,
swarm orchestration.
