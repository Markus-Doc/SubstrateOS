# Branch-1 Build Plan: Base+Overlay seam, engine-agnostic front-end, multi-agent orchestration

Status: ✅ COMPLETE (2026-06-13) — all milestones M-A…M-F landed gate-green on
main (commits 3922bbe, 3c9b37f, 8e65876, 3e3e1e9, e97582a). New surfaces: `subos`
launcher, `/substrateos` warm activation, `labctl workflow`, `labctl conformance`,
the Overlay seam, and the 7th (supply-chain) gate stage. ADRs 019–024.
Authority: ADR-019 (architecture), ADR-020/021
(research + upkeep), master research at `docs/research/master-research.md`.
SubstrateOS-dictated: milestone-driven (ADR-010), **release gate green before
every push**, no new heavyweight frameworks (ADR-002).

This plan is handoff-ready for a fresh high-effort Opus build session. Each
milestone is independently shippable and gated. Milestones M-A/M-B are
research-safe (pure architecture plumbing the research validates) and may build
immediately; M-E/M-F should reconcile with the branch-2 impact assessment
(`docs/planning/research-impact-review-prompt.md`) before landing.

## Principles (from ADR-019)
- **Overlay → Base, one way.** Base never imports/hardcodes an Overlay.
  Discovery is by env var (`SUBSTRATEOS_OVERLAY`) only.
- **Ships blank.** Mechanism present, no-op defaults, documented scaffold.
- **Base runs naked.** Gate stays green with no Overlay present.
- **Guarantees in `labctl`, not the model** (gate, circuit breaker, isolation,
  review queue) — so engine-swap and multi-agent dispatch never weaken safety.
- **Compile target = `SKILL.md` + `AGENTS.md`** open standards (confirmed).

## Milestones

### M-A — Format + spec skeleton  ✅ DONE (2026-06-13)
Locked SKILL.md/AGENTS.md as the canonical compile target (ADR-019); canonical
engine-neutral spec checked in at `substrate/methodology.md` (MUST/SHOULD tiers,
activation contract, compile-target table) with `substrate/README.md`.

### M-B — Base extension seam  ✅ DONE (2026-06-13)
- Overlay discovery + command-plugin hook (`SUBSTRATEOS_OVERLAY` → mount extra
  `labctl` commands). No-op + safe when unset.
- Provider registry generalising the `WebProvider`/`MemoryProvider` ABC pattern
  so an Overlay can register named providers.
- Blank documented scaffold at `templates/overlay-example/`.
- DoD: tests for load/no-op/error paths; gate green **with overlay absent**.

### M-C — `subos` launcher + adapters  ✅ DONE (2026-06-13)
`subos <engine>` console script (`labctl/subos.py`): compiles the canonical spec
into the engine's instruction file (managed-marker overwrite protection,
`labctl/compile_spec.py`), assembles the launch plan, prints a confirmation
banner, and execs the engine — with `--dry-run` for inspection. Engine adapters
(`labctl/engines.py`) for claude/codex/gemini/cursor: binary, instruction file,
skills dir, full-auto flag mapping. Base default posture = platform-default;
`--full-auto` opt-in (ADR-019). 8 tests; ruff clean; proven end to end.
Remaining for later: compiling `SKILL.md` skills (not just the instruction
file).

### M-D — `/substrateos` warm activation  ✅ DONE (2026-06-13)
`labctl/handshake.py`: MUST tier (harness-enforced on any engine) + SHOULD tier
mapped to per-engine `capabilities`, with honest gap self-report.
`compile_spec.compile_warm_command` emits the per-engine `/substrateos` command
(`.claude/commands/`, `.codex/prompts/`, `.cursor/commands/`) with the
launch-time-only caveat; `subos --dry-run` now prints the cold handshake. Engine
adapters carry `capabilities` + `warm_command_file`. 6 tests; ruff clean.

### M-E — Multi-agent / sub-agent orchestration  ✅ DONE (2026-06-13)
`labctl/orchestrate.py`: architect → workers → reviewer → judge with handoff
packets and verify-before-accept (judge gates acceptance). Pure engine with an
injectable `StageRunner` (fully tested without spending tokens); default
`claude_stage_runner` wraps the headless-claude circuit-breaker machinery
(`labctl.capsule`), each stage budget-capped. JSONL run-log + agentic-eval trace
metrics (P2-B: task_completion, budget_utilisation, breaker_trips, …).
`labctl workflow run "<mission>" [--workers N] [--dry-run]`. 8 tests; ruff clean.

### M-F — Conformance + supply-chain gate  ✅ DONE (2026-06-13)
**Supply-chain audit = 7th gate stage** (ADR-024, P1-B approved):
`labctl/supplychain.py` discovers SKILL.md + `.mcp.json` servers and flags any
not on the `substrate/trusted-tools.json` allowlist (ships blank → green naked);
wired as `gate.run_supplychain`. **Cross-engine conformance**:
`labctl/conformance.py` encodes the MUST contract as scenarios + injectable
`Responder` + `check_conformance`; `labctl conformance` prints the contract.
Stage count updated to seven across docs/methodology/handshake. 9 + 3 tests;
two existing gate stage-list tests updated for the 7th stage; ruff clean.

## Sequencing vs branch-2  (branch-2 COMPLETE 2026-06-13)
Branch-2's whole-repo impact assessment
(`docs/planning/research-v2-impact-assessment.md`) cleared the base: **no
architecture rewrite, no genuine contradiction.** Backlog folded in here:
- **P1-A** default model Opus 4.8 → **ADR-022 (Accepted).**
- **P1-B** supply-chain audit gate (skills/MCP/plugins) → **M-F**. It
  **expands the locked Phase-2 scope** ("six stages / no red-team expansion"),
  but supply-chain audit ≠ red-team. **OWNER DECISION: APPROVED 2026-06-13**
  (Markus) — M-F's supply-chain stage is unblocked; phase-2-plan locked decision
  #4 amended accordingly. M-F should author its own ADR for the new stage.
- **P2-A** in-process MCP tool seam for `labctl` providers → folds into M4
  (in-container execution); uses the M-B `ProviderRegistry`.
- **P2-B** trace + agentic-eval metrics (Task Completion, Tool Correctness, …)
  → folds into **M-E** (Dynamic Workflows orchestration).
- **P3-A** log LiteLLM-not-used + thin-harness-not-framework divergences
  (ADR-013 precedent).

M-C/M-D proceed now. M-E reconciles with P2-B. M-F's supply-chain stage is
**unblocked** (P1-B approved 2026-06-13). P3-A landed as **ADR-023** (logged
divergences) by branch-2; do not re-author it.
