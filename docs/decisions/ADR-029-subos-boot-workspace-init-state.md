# ADR-029: subos boot surfaces workspace init state; prompt over auto-init

Date: 2026-06-14
Status: Accepted

## Decision

The `subos` launcher now distinguishes two facts on boot that were previously
conflated:

- **Kernel hydrated** - the methodology compiled into the engine instruction file
  (this already happened).
- **Workspace initialized** - a `substrateos.json` manifest exists in the target,
  so labctl treats the directory as a real workspace.

`subos` reads the manifest (`labctl.config.load_manifest`) for the target and
reports the workspace state on both the `--dry-run` plan and the real pre-launch
banner. When the workspace is uninitialized, it says so plainly and recommends
`labctl init`.

On the auto-init question we chose **prompt, not silent auto-init**:

- Default behaviour: `subos` does not create anything. It reports the
  uninitialized state and points at `labctl init`.
- Opt-in: a new `--init` flag makes `subos` run `init_project(target)` itself
  before launch (creating the target dir if needed), printing the actions taken.

The engine-side boot contract in `substrate/methodology.md` is updated to match:
the boot confirmation is two-part (kernel hydrated, then workspace state read from
`labctl status` / the manifest), and if uninitialized the engine surfaces it and
offers `labctl init` before project work. The generated `CLAUDE.md` (and other
engine files) are recompiled from the spec; they are not hand-edited (ADR-019).

## Context

After the OneDrive -> D: migration, `subos claude` could hydrate the methodology
and land in a directory labctl treated as uninitialized, with no signal to the
user. The boot banner only spoke to kernel hydration, so "knows subos but never
inited inside" looked identical to a healthy boot.

Why prompt over auto-init: the Base must stay deterministic and side-effect-free.
A launcher that silently writes a manifest and scaffolds directories on every boot
is surprising, fights `--dry-run`/CI use, and sits awkwardly next to the
"no silent mutation / honour the review queue" posture. Making init an explicit
one-flag action keeps the safe default while still being a single keystroke away
when the user wants it. `subos` also hands off to the engine immediately, so a
blocking y/n prompt would not compose well with non-interactive use; a visible
recommendation plus `--init` is the clean seam.

## Consequences

- `subos --dry-run` gains a `workspace:` line; the real launch banner states both
  kernel hydration and workspace state. New user-facing strings avoid em and en
  dashes per the house writing rule.
- `subos --init` is the supported path to initialize-then-launch; without it the
  user (or the engine, per the spec) runs `labctl init`.
- `substrate/methodology.md` changed, so the package-data spec copy and the
  generated engine files were resynced/recompiled (`scripts/sync_spec_data.py`
  plus a compile pass). The drift-guard test enforces the package-data copy.
- Tests in `tests/test_subos.py` cover the uninitialized message, the initialized
  message, and that `--init` writes the manifest before launch.
