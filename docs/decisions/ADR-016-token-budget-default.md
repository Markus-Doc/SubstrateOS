# ADR-016: Token budget circuit breaker — counting rule and default

Date: 2026-06-12
Status: Accepted

## Decision

The circuit breaker meters cumulative `input_tokens + output_tokens +
cache_creation_input_tokens` across all usage events in the build's
stream-json output. `cache_read_input_tokens` is deliberately excluded.
The default budget is **2,000,000 tokens per build run**, stored as
`token_budget` in `capsule.json` and overridable per run
(`labctl build --token-budget N`). When the running total exceeds the budget,
labctl kills the child claude process, appends a `circuit-breaker` record to
the run log, and exits non-zero.

## Context

Cache reads dominate raw token counts in any multi-turn agent session (the
same context is re-read every turn at ~10% of base price) — counting them
would make the budget fire on conversation length rather than real spend.
The included fields track what actually costs money and what an out-of-control
loop inflates. 2M tokens comfortably covers a small-project build (the Phase 1
capstone class of task) while capping a runaway loop at roughly single-digit
dollars of API-equivalent spend.

## Consequences

- The breaker is enforced in `labctl.capsule.monitor_stream`, unit-tested on
  synthetic streams, and demonstrated live with a tiny `--token-budget` run
  (M3 checklist evidence).
- Budgets are per run, not per capsule lifetime; cumulative campaign
  accounting is a Phase 2 concern.
- If Anthropic changes the stream-json usage schema, `_usage_tokens` is the
  single point to update.
