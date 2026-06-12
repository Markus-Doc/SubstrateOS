# ADR-014: Capsules scaffold as sibling directories of the SubstrateOS repo

Date: 2026-06-12
Status: Accepted

## Decision

`labctl new <project>` scaffolds a capsule at `<parent-of-SubstrateOS>/<project>`
(e.g. `C:\Users\marku\OneDrive\Documents\GitHub\<project>`), not inside the
SubstrateOS repo. The capsule's memory namespace directory stays under
SubstrateOS at `artifacts/memory-namespaces/<project>/` and is the only
SubstrateOS path the capsule ever sees (bind-mounted at `/memory` per the
devcontainer template).

## Context

Every capsule becomes its own GitHub repository (the Phase 1 capstone pushes
`research-dashboard` as a private repo). Nesting a git repo inside the
SubstrateOS working tree would create submodule-like confusion, leak capsule
history into SubstrateOS scans, and violate the template's isolation guarantee
against mounting a shared parent directory. Sibling placement matches how all
other repos live on this machine (one directory per repo under `GitHub/`).

## Consequences

- The capsule workspace and the SubstrateOS repo share no ancestor that is
  itself a repo; gitleaks/semgrep/trivy runs on either tree see only that tree.
- Scaffolding writes: devcontainer (tokens substituted), capsule `CLAUDE.md`
  (mission, constraints, namespace), MIT `LICENSE` (holder "M. Walker"),
  `capsule.json` manifest, `.gitignore`, and a git init + initial commit with
  the standing author identity (M. Walker + GitHub noreply email).
- Tests scaffold into pytest tmp dirs via the `dest_parent` parameter; the
  CLI always uses the real sibling layout.
