# `labctl research` — best-practices research/review pipeline (ADR-021)

Keeps SubstrateOS current with AI best practices. It re-synthesises current
research with **RESYNTH** and diffs the result against the OS design, surfacing a
human-promoted review report proposing ADRs / tooling swaps / deprecations. It
**detects when a current choice ages out** instead of discovering staleness by
accident (ADR-019's promise of a Base that is reviewed regularly).

## How it runs (read this first)

By default the pipeline is **operated by the interactive session you launched with
`subos <engine>`** — `labctl research` gives you deterministic, file-backed
commands and *you/the session* do the thinking. **No headless model call, no
Agent-SDK credit spend.** Every command that can spend credits requires the
explicit, clearly-labelled `--auto` flag.

> **Billing note.** Interactive `subos claude` runs on your normal Claude
> subscription. `--auto` runs `claude -p` unattended, which from 15 June 2026 draws
> from the separate metered **Agent SDK** credit bucket. Default flows never touch it.

## Prerequisite

Install **RESYNTH** (separate optional tool, zero runtime AI dependency):
`labctl doctor` reports whether `resynth` is on PATH (a `[WARN]` if absent — the
pipeline simply can't run a live sweep until it's installed). See the RESYNTH repo
for its installer.

## The interactive flow

```
labctl research status --show-watch        # see the watch-list and any sweeps
labctl research brief --topic "current AI agent best practices"
# -> scaffolds a RESYNTH project under artifacts/research/<slug>/ and emits one
#    research prompt per deep-research platform. Run those prompts, save each
#    report as a file in a folder.
labctl research sync "current AI agent best practices" --reports <folder>
# -> intakes the reports and drives RESYNTH's gated stages. When a stage needs
#    thinking, it prints the exact instruction; do it in your subos session, then
#    re-run `sync` to continue. Resumable. Ends with a sealed candidate MASTER.json.
labctl research review "current AI agent best practices" --candidate <MASTER.json>
# -> writes an AI-derived, UNPROMOTED review report (per-watch-item verdict +
#    proposed changes) into the review queue.
labctl review list                          # shows the report as PENDING
# ... you author any resulting ADRs by hand ...
labctl review approve <report-path>          # promote the record
```

`research review` also works with **no candidate** — a self-audit of the
watch-list against the current ADRs — useful between full RESYNTH sweeps.

## Opt-in headless (`--headless`)

`sync --headless` and `review --headless` perform the thinking steps with headless
claude, metered by the ADR-016 token circuit breaker. They print a credit-spend
warning. Use only for fire-and-forget sweeps. (`--auto` is retained as an alias.)

A personal/Overlay preference can flip the default: when
`SUBSTRATEOS_RESEARCH_HEADLESS` is truthy (`1`/`true`/`yes`/`on`) the commands
default to headless without the flag. The public Base ships it **unset** — default
off, i.e. interactive. The per-command flag still wins (you can always pass
`--headless` explicitly), and the credit-spend warning prints whenever headless is
active however it was selected.

## The watch-list

`substrate/research-watch.json` (Base default, **Overlay-tunable**) names the
tools/standards/formats to watch — instruction compile formats (SKILL.md/AGENTS.md),
supported engines, in-container execution (bespoke vs OpenHands), the
ultracode/Dynamic-Workflows surface (ADR-027), the default model, retrieval, and the
governing research itself. Each item records its current choice and the ADRs it
backs, so `review` can give a per-item verdict. It is bundled as package data, so it
resolves from any directory.

## Optional: scheduling on the lab box (not enabled by default)

The Base ships the pipeline as a manual control-plane command. To run it on a
cadence, wire it into the lab-box duty cycle in an **Overlay** (never the public
Base): a `@reboot` / RTC-self-wake job (ADR-018) that runs `labctl research review`
(report-only) and reports the pending report back over the Telegram trigger. Keep
`--headless` (and `SUBSTRATEOS_RESEARCH_HEADLESS`) off unless you accept the
Agent-SDK spend.
