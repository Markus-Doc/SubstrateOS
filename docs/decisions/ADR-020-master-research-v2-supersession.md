# ADR-020: master-research.md (v2) supersedes the v1 master research; research docs relocated out of repo root

Date: 2026-06-13
Status: Accepted

## Decision

- The reprocessed RESYNTH consolidation (internal title "Master Document:
  ai_os", 66 sources S01–S66) becomes the **master research document**, stored
  at `docs/research/master-research.md`.
- The previous master (RESYNTH of S01–S03, promoted in ADR-008) is **archived**
  at `docs/research/archive/master-research-v1.md` — superseded, kept for
  provenance, removed from the repo root.
- Research documents no longer live in the repo root. The root keeps only
  `README.md`, `CLAUDE.md`, `LICENSE`, and `SECURITY.md` — clean for public
  deploy.
- `docs/research/Final_Research-Agent_Brain.md` remains the project-specific
  research; the master document wins on conflict (unchanged from ADR-008).

## Context

The owner reprocessed the research into a substantially larger v2. Two large
`MASTER_*.md` files sitting in the repo root were "too messy for public deploy."
ADR-008's promotion of the v1 master at the root is therefore superseded by this
ADR on both the *which document* and *where it lives* questions.

## Pointer updates

- `substrateos.json` `source_of_truth` → `docs/research/master-research.md`
- `scripts/labctl/config.py` `Manifest.source_of_truth` default → same
- `CLAUDE.md` master-research pointer → same
- `scripts/tests/test_status.py` fixture writes/ingests the new path
- `status.py` presence check is path-relative, so the dashboard resolves the new
  location with no logic change.

## Notable findings carried forward (operational influence is tracked separately)

- The **Agent Skills / `SKILL.md`** format is now a multi-platform open standard
  (Claude, Codex, Cursor, Gemini CLI, Copilot; agentskills.io) — adopt as the
  ADR-019 compile target rather than a bespoke format.
- **`AGENTS.md`** is the cross-tool instruction standard (Linux Foundation AAIF);
  CLAUDE.md ↔ AGENTS.md is the Claude adapter pairing.
- **Model-neutral orchestration** (frontier model as planner/judge; cheaper
  agents for bulk) and "model-neutral skills + instruction files + MCP + an
  eval/safety gate lets any new frontier model drop in with a one-line change"
  directly validate ADR-019.
- **Instruction budget** (~150–200 instructions; every token loads every
  request) reinforces lean CLAUDE.md + progressive-disclosure skills.
- **Supply-chain risk**: every skill/MCP/plugin is executable and
  prompt-injectable — audit + sandbox before it touches real data.
- **Claude Fable 5** is the new top model but mandates 30-day retention and
  reroutes cyber/bio/chem to Opus 4.8 (relevant to security-engineering use);
  access was suspended as of 2026-06-12. Model-choice implications are a
  discussion item, not yet an ADR.
