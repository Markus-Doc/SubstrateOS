# Install & Distribution — Build Session Prompt

Standalone handoff for a fresh `/new` session at very-high model effort. Paste the
fenced block below, then run `/plan`. Design of record: ADR-026 and
`docs/planning/install-distribution-plan.md`.

```
Operate as SubstrateOS (you are the orchestrator; drive `labctl`, never bypass the
release gate). Repo: C:\Users\marku\OneDrive\Documents\GitHub\SubstrateOS, branch main.

Read first — the design is already locked and primed on disk:
  docs/decisions/ADR-026-packaging-distribution-installers.md
  docs/planning/install-distribution-plan.md
Follow that plan; do not relitigate the locked decisions (move ADR-026 Proposed->Accepted
when implemented).

MISSION: make SubstrateOS installable and usable by a first-time, medium-to-low-skill user
— "clone or curl/wget, run one installer, then `subos claude` works from any directory in a
fresh shell" — on Windows PowerShell, Linux, and macOS, WITHOUT diminishing later
container/EKS deployment. Reach a full "ready to install and use" state today.

BUILD PROCESS (mine — use it):
- Begin with `/plan` at VERY-HIGH effort and fan the milestones out as a Dynamic Workflow:
  an architect plus parallel sub-agents (up to ~16) for the independent milestones in the
  plan doc (spec-as-package-data, version single-source, install.ps1, install.sh,
  Dockerfile, doctor checks, INSTALL.md, tests, docs).
- Drive the work as a `/loop`: build -> test -> fix -> adversarial review, like a human dev
  team in agent form, until acceptance holds.
- TEST BY ACTUALLY RUNNING IT: install into a scratch location, open a FRESH shell in an
  UNRELATED directory, run `subos claude --dry-run` and `subos --version`, and VERIFY WITH
  AI VISION — screenshot the fresh-shell run and confirm the output visually. If a live
  install/Docker build is needed, ask for confirmation to install rather than assuming.

MILESTONES (see plan doc for detail):
1. Bundle substrate/methodology.md (+ warm/skill templates) as PACKAGE DATA; subos
   resolves the spec via importlib.resources so it runs from any dir / in a container.
2. pyproject version single-sourced from labctl.__version__ (fix 0.1.0 vs 0.2.0).
3. install.ps1 + install.sh: curl-able, idempotent, pipx-first (venv fallback), Python>=3.11
   check, PATH/ensurepath, execution-policy + "open a new terminal" guidance, then VERIFY
   with `subos --version` and `labctl doctor`. Support --full-auto-default (opt-in, writes
   overlay/local config; never bake privilege into the public Base).
4. INSTALL.md for a medium-to-low-skill user, cross-platform.
5. Root Dockerfile + .dockerignore: SubstrateOS golden image (entrypoint labctl/subos,
   12-factor env config, NO secrets baked) so local container == EKS-ready.
6. Extend `labctl doctor`: subos-on-PATH, spec-resolvable-from-any-dir, engine-binary
   detection.
7. Tests for spec-as-data resolution, version consistency, new doctor checks. README + docs.

HARD CONSTRAINTS:
- Release gate (7 stages) GREEN before every commit and push; fetch-check collisions before
  each push; ONE git driver; keep history linear.
- Identity/PII: holder "M. Walker"; never write the legal surname, full legal name, or any
  personal email into any file/commit. No secrets/keys/credentials tracked. Commits end:
  Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>.
- No tools/frameworks outside the master research; no Postgres/LangGraph/AutoGen/local
  inference. subos pins NO model (uses the installed engine on PATH; no API/billing).
  Optional tools' keys/billing stay optional.

ACCEPTANCE (all must hold before "done"):
1. From a FRESH PowerShell in an arbitrary directory (not the repo), `subos claude --dry-run`
   resolves the PACKAGED spec and prints the plan; `subos --version` shows 0.2.0 — verified
   by SCREENSHOT (AI Vision).
2. install.sh passes shellcheck/lint and runs the same logical steps (dry-run ok if no Linux
   host this session — note it).
3. `docker build` of the root Dockerfile succeeds, or it is lint-clean with the live build
   stated as owner-gated.
4. Full 7-stage gate green; the new tests pass.
5. Role-play a first-time installer (app-support skill) on Windows; record a short findings
   log; fix anything that trips the novice.
Commit + push each milestone gate-green. Report done vs owner-gated (live Docker build, real
Linux/mac run, any live engine spend) without auto-consuming those resources.
```

## Notes

`/plan`, the Dynamic-Workflow sub-agent fan-out, `/loop`, and AI Vision are Claude Code
native features — the orchestration engine. SubstrateOS contributes the guardrails the
loop runs against: `labctl workflow run` (its own architect -> workers -> reviewer ->
judge), the 7-stage release gate, capsule isolation, and the `app-support` role-play
skill. The prompt composes both layers rather than duplicating either.
