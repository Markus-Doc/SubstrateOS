# ADR-030: supply-chain audit excludes first-party generated skills

Date: 2026-06-14
Status: Accepted

## Decision

The supply-chain gate stage (`scripts/labctl/supplychain.py`) now treats a skill
as a third-party supply-chain risk only when it is **not** a SubstrateOS-generated
file. Skills whose `SKILL.md` carries the generated-by marker (`is_managed`, the
same marker `subos` stamps on every compiled engine file) are first-party: they
are the OS itself, compiled from the canonical spec, not an introduced tool. They
are skipped by `_discover_skills`, so they are neither scanned nor flagged.

Third-party skills (no marker) and MCP servers are scanned exactly as before and
still fail the gate when unvetted.

## Context

ADR-024 added the supply-chain stage to vet skills, MCP servers, and plugins as
executable, prompt-injectable risk. Its docstring promises the naked Base stays
green: blank allowlist, no third-party tools, nothing to flag.

That promise was not actually kept. Booting through `subos` compiles the OS's own
kernel skill to `.claude/skills/substrateos/SKILL.md` (the skill form of the same
first-party content as `CLAUDE.md`). The audit then discovered that generated
skill, found `substrateos` absent from the empty allowlist, and failed the gate
against the OS itself. So any real `subos` boot turned the supply-chain stage red.

Two fixes were possible:

1. Add `substrateos` to `substrate/trusted-tools.json`. Rejected: the allowlist is
   documented to ship blank, and is meant for audited third-party tools. Putting a
   first-party generated artifact in it muddies what "trusted" means and changes
   the shipped Base posture.
2. Recognise first-party generated skills and exclude them from the third-party
   scan. Chosen: it is the OS not flagging itself, it keeps the allowlist blank and
   meaningful, and it makes the naked-Base-stays-green promise true.

This narrows the audit to its real target (third-party, unvetted tools). It does
not weaken the stage: an unvetted scraper skill or sketchy MCP server still fails,
as the tests assert. The generated marker is a reliable first-party signal because
only `subos`/the compiler writes it, and the same marker already guards instruction
files from hand-edits (ADR-019).

## Consequences

- `subos` boots no longer self-trip the supply-chain stage; the naked Base is green
  end to end.
- The exclusion is marker-based, so it covers every engine's generated skill
  (`.claude`, `.agents`, `.gemini`, `.cursor`), not just Claude.
- Tests in `tests/test_supplychain.py` assert the generated skill is treated as
  first-party while a co-located third-party skill is still flagged.
- This extends ADR-024; it reverses none of it. If a future generated-skill format
  drops the marker, this exclusion stops applying to it (fail-closed).
