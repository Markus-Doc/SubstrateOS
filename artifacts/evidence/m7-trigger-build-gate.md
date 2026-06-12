# M7 Remote Trigger Pathway — build evidence (2026-06-12)

Built on the Lab box itself (`useragent`) per ADR-018, orchestrated as a
Dynamic Workflow (architect → module worker ∥ docs worker → spec-driven test
worker → adversarial reviewer → judge). Reviewer verdict: pass, zero blocking
findings; five advisories, two fixed by the judge (poll_timeout wired into
listen mode; ValueError/InvalidURL token-redaction edge in `_default_http`).

## Suite

147 passed (105 baseline + 42 new trigger tests), ruff clean.

## `labctl gate --strict` (all scanners native on the box)

```
[PASS] secret-scan: gitleaks: no leaks found
[PASS] lint: ruff: clean
[PASS] tests: pytest: 147 passed in 10.33s
[PASS] sast: semgrep: no findings
[PASS] vuln-scan: trivy: no HIGH/CRITICAL findings
[PASS] evals: promptfoo: all assertions passed
gate: all stages passed
```

Tool versions installed for the strict run: gitleaks 8.30.1 (`~/.local/bin`),
trivy 0.71.0 (`~/.local/bin`), semgrep 1.166.0 (project venv).

## Box state

- Tailscale SSH enabled (`tailscale set --ssh`, v1.98.4); owner verified a
  Termius session from the iPhone over the tailnet (ACL ssh rule switched
  from `check` to `accept`, root dropped from `users`).
- NIC magic-packet wake remains armed (`Wake-on: g`); control-plane
  `labctl lab wake` path unchanged.
- `substrateos-trigger.service` installed and enabled, inactive by design:
  `ConditionPathExists=.env` holds it until the owner provides
  `TRIGGER_TELEGRAM_TOKEN`.

## Pending live verification (owner-gated)

`/status` + small `/run` from the owner's phone via Telegram, and one full
suspend → RTC wake → drain → reply cycle. Will be recorded as
`m7-trigger-live-cycle.md` when the bot token lands.
