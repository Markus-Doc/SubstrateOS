# ADR-024: Supply-chain audit as the 7th release-gate stage

Date: 2026-06-13
Status: Accepted

## Decision

The release gate gains a **seventh stage, `supply-chain`**, that audits every
third-party skill / MCP server / plugin declared in the repo against an audited
allowlist (`substrate/trusted-tools.json`). Any discovered tool not on the
allowlist fails the stage. The Base ships the allowlist **blank**, so the stage
passes when SubstrateOS runs naked.

## Context

This implements branch-2 backlog item **P1-B**, owner-approved 2026-06-13 (see
`docs/planning/phase-2-plan.md` locked-decision #4 amendment). The master
research (`docs/research/master-research.md`, `## Red Teaming`, `## Gh Skill`)
is emphatic that every skill/MCP/plugin is executable, prompt-injectable
supply-chain risk and must be audited and sandboxed before it touches real data.
The engine-agnostic front-end (ADR-019) actively *pulls in* third-party skills,
so this guardrail is close to load-bearing.

Supply-chain audit is **distinct from red-teaming**: Garak/PyRIT generate
harmful prompts to probe a model; this audits *tool provenance* (licence,
maintainers, scripts, network, permissions) before a tool runs. So it does not
reopen Phase 2's deferral of red-team expansion.

## Implementation

- `scripts/labctl/supplychain.py` — `audit(root)` discovers `SKILL.md` under the
  per-engine skills dirs and MCP servers in `.mcp.json`, flagging any not in the
  allowlist.
- `scripts/labctl/gate.py` — `run_supplychain(root)` appended to `run_gate` as
  the final stage.
- `substrate/trusted-tools.json` — the blank, documented allowlist; add a name
  only after auditing the tool. Overlays may extend it in their own repo.

## Consequences

- The gate is now seven stages; docs and the methodology MUST tier updated.
- A new skill/MCP only passes the gate once a human has audited it and added it
  to the allowlist — least-privilege by default.
- Future hardening (parsing licences/permissions, sandbox enforcement) extends
  `supplychain.audit` without changing the gate wiring.
