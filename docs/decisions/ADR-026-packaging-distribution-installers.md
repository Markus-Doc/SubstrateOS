# ADR-026: Packaging, distribution, and cross-platform installers

- Status: Accepted
- Date: 2026-06-14
- Implemented: 2026-06-14 — spec bundled as `labctl/data` package data with an
  `importlib.resources` fallback in `subos._default_spec_path()`; `pyproject`
  version single-sourced from `labctl.__version__`; `install.ps1` + `install.sh`;
  root `Dockerfile` + `.dockerignore`; `labctl doctor` install-health checks;
  `INSTALL.md`. Live `docker build` and a real Linux/macOS run remain owner-gated.
- Supersedes: none
- Related: ADR-002 (no heavyweight frameworks), ADR-019 (Base/Overlay, engine-agnostic
  front-end), ADR-025 (in-container capsule execution)

## Context

SubstrateOS is currently installed developer-style: clone the repo, create a venv,
`pip install -e scripts[dev]`, then invoke `.\.venv\Scripts\subos`. That is fine for
contributors but fails the goal of a first-time, medium-to-low-skill user who wants to
"clone or curl, run an installer, then `subos claude` works from any directory in a
fresh shell" — on Windows PowerShell, Linux, and macOS alike.

Two further constraints shape the decision:

1. **Container-first / golden-image friendliness.** The owner packages projects so a
   golden image could later deploy on EKS (or run fully locally). Nothing in the local
   polish may diminish later container/cloud deployment.
2. **`subos` must run from any directory.** Today `subos` locates its canonical spec
   (`substrate/methodology.md`) by finding the SubstrateOS repo root, so a globally
   installed `subos` launched elsewhere cannot find the spec.

## Decision

1. **Keep the core a pip-installable Python package** (`labctl` + `subos` console
   scripts). This is the one primitive that works identically in a venv, under pipx,
   inside an OCI image, and on EKS — honouring ADR-002 (no new heavyweight tooling).

2. **Ship the canonical spec as package data.** Bundle `substrate/methodology.md` (and
   the warm-command / skill templates) into the installed package and resolve it via
   `importlib.resources`. `subos._default_spec_path()` falls back to the packaged
   resource when not inside a repo, so `subos <engine>` works from any directory and
   inside a container. The repo copy remains the editable source of truth.

3. **Global install via pipx**, user-scope, with `pipx ensurepath`; fall back to a
   managed venv + PATH shim when pipx is absent. Inside containers, install with plain
   system `pip` (no venv).

4. **Two curl/wget-able, idempotent installers** performing the same logical steps:
   - `install.ps1` (Windows PowerShell)
   - `install.sh` (Linux / macOS)
   Steps: verify Python >= 3.11, ensure pipx, install the package, then verify with
   `subos --version` and `labctl doctor`. Friendly step-by-step output; handle the
   PowerShell execution-policy note and the "open a new terminal for PATH" caveat.
   A packaged `.exe` is deferred (script first).

5. **Root `Dockerfile` + `.dockerignore`** building a SubstrateOS golden image
   (entrypoint `labctl` / `subos`; 12-factor env-var config; no secrets baked). Local
   container == EKS-ready base. No Helm now; nothing here blocks it later.

6. **Base ships safe (platform-default).** Personal full-auto stays opt-in via an
   installer flag (`--full-auto-default`) that writes to overlay/local config — never
   baked into the public Base (ADR-019).

7. **Single-source the version.** `pyproject` reads `labctl.__version__`, fixing the
   0.1.0 / 0.2.0 split that an installer would otherwise surface.

8. **`labctl doctor` gains install-health checks**: `subos` on PATH, spec resolvable
   from any directory, and engine-binary detection — so a first-run user sees a clear
   green.

## Consequences

- A novice can install on any of the three platforms and run `subos claude` from a
  fresh shell anywhere; the same image is the container/EKS deployment unit.
- `subos` no longer depends on being run from inside the clone.
- New surface to maintain: two installer scripts and a Dockerfile, all exercised by the
  release gate and a role-played first-install acceptance pass.
- `subos` still pins no model and adds no API/billing — it launches the installed engine
  on PATH as-is; optional tools' keys/billing remain optional.

## Acceptance

Recorded in `docs/planning/install-distribution-plan.md`. Live Docker build and a real
Linux/macOS run are owner-gated; the Dockerfile and `install.sh` must at minimum be
lint-clean and dry-run-validated when a host is unavailable.
