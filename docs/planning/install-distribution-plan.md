# Install & Distribution Build Plan

Status: primed 2026-06-14 — ready for a build session. Decision of record: ADR-026.

## Goal

A first-time, medium-to-low-skill user can **clone or `curl`/`wget` the repo, run one
installer, and then run `subos claude` from any directory in a fresh shell** — on
Windows PowerShell, Linux, and macOS — without diminishing later container/EKS
deployment. End state: a full "ready to install and use" SubstrateOS.

## Locked design (ADR-026)

- Core stays a pip-installable package (`labctl` + `subos`).
- Canonical spec shipped as **package data** (`importlib.resources`); `subos` resolves
  it from the installed package, so it runs from any directory and inside a container.
- Global install via **pipx** (user-scope, ensurepath); venv+PATH fallback; system
  `pip` inside containers.
- `install.ps1` (Windows) + `install.sh` (Linux/macOS), curl-able, idempotent, with a
  verify step (`subos --version`, `labctl doctor`).
- Root `Dockerfile` + `.dockerignore` = SubstrateOS golden image (12-factor, no secrets).
- Base ships safe; personal full-auto is opt-in (`--full-auto-default`).
- `pyproject` version single-sourced from `__version__` (fix 0.1.0/0.2.0).
- `labctl doctor` gains: subos-on-PATH, spec-resolvable-from-any-dir, engine-binary
  detection.
- `INSTALL.md` written for a medium-to-low-skill user, cross-platform.

## Build scope (milestones)

1. Spec-as-package-data + `_default_spec_path()` packaged-resource fallback.
2. `pyproject` dynamic version aligned to 0.2.0.
3. `install.ps1` + `install.sh` (pipx-first, venv fallback, Python check, PATH, verify).
4. `INSTALL.md` (novice, cross-platform).
5. Root `Dockerfile` + `.dockerignore` (golden image).
6. `labctl doctor` install-health checks.
7. ADR-026 moved Proposed -> Accepted by the implementing session.
8. Tests: spec-as-data resolution, version consistency, new doctor checks.
9. README + docs update.

## Build process (owner's pipeline)

- Start with **`/plan` at very-high model effort** so it fans out into the Dynamic
  Workflow (architect + parallel sub-agents, up to ~16) per the milestones above.
- Drive the work with **`/loop`** as a build -> test -> fix -> adversarial cycle, like a
  human dev team in agent form.
- **Test by actually running the tool**: execute the installer in a scratch location,
  launch `subos claude --dry-run` from an unrelated directory, and **verify with AI
  Vision** (screenshot the fresh-shell run) or request confirmation to install live.
- Operate as SubstrateOS: drive `labctl`; release gate (7 stages) green before every
  commit and push; fetch-check collisions before each push; one git driver; linear
  history.

## Acceptance (all must hold)

1. From a FRESH PowerShell in an arbitrary directory (not the repo), `subos claude
   --dry-run` resolves the packaged spec and prints the plan; `subos --version` = 0.2.0.
2. `install.sh` passes shellcheck/lint and runs the same logical steps (dry-run ok if no
   Linux host this session — note explicitly).
3. `docker build` of the root Dockerfile succeeds, or it is lint-clean with the live
   build stated as owner-gated.
4. Full 7-stage gate green; tests added for spec-as-data, version consistency, doctor.
5. A role-played first-time install (app-support skill) on Windows, with a short
   findings log; novice trip-ups fixed.

## Owner-gated (do not auto-consume)

Live Docker build, real Linux/macOS run, any live engine spend. Plumbing + dry-run
validation are in scope; live runs await the owner.
