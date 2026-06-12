# ADR-012: Evaluation layer — promptfoo in the release gate now; Garak/PyRIT in Phase 2

Date: 2026-06-12
Status: Accepted

## Decision

The master research document's evaluation layer gets an owner today rather
than staying unassigned:

- **promptfoo** — the master doc's consensus primary regression gate
  [S01-C029] [S02-C026] [S03-C020] — is wired into `labctl gate` as an
  `evals` stage now, invoked via `npx promptfoo eval` against a committed
  config (`evals/promptfooconfig.yaml`). The starter config is a zero-cost
  smoke eval (echo provider, no API keys) proving the harness runs in CI.
- **Garak** (per release) and **PyRIT** (quarterly) are explicitly assigned
  to **Phase 2**, matching the master doc's recommended cadence "promptfoo
  per PR, Garak per release, PyRIT quarterly" [S01-C034].
- The **OWASP injection preset** [S01-C030] is activated in the promptfoo
  config once capsule agents carry real system prompts; until then there is
  nothing to probe, so the slot is kept as a documented placeholder in the
  config.

## Context

The alignment audit (2026-06-12) found the master doc's eval-loop layer —
"nothing merges until gates pass" [S01-C060] — assigned to no phase: no ADR
owned it, no plan milestone referenced it. promptfoo is local-first, MIT,
YAML-config, and runs with zero API cost against the echo provider, so the
cost of wiring it in now is one gate stage and one config file. Garak and
PyRIT, by contrast, generate harmful prompts by design and need dedicated
non-production endpoints with strict egress controls [S03-C024] — operational
surface Phase 1 does not have and does not need before capsule agents exist.

## Consequences

- `labctl gate` gains an `evals` stage (skipped gracefully when node/npx is
  absent; `--strict` turns skips into failures before any public push).
- A failing promptfoo eval blocks release, satisfying the master doc's "a
  delegated patch is not accepted until promptfoo passes" rule [S01-C062].
- Phase 2 planning inherits two concrete items: Garak per release and PyRIT
  quarterly, plus activation of the OWASP preset against real capsule system
  prompts with a regression test for every injection fixed.
