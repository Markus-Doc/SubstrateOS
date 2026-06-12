# Capsule Devcontainer Template

## What a capsule is

A capsule is the isolated execution environment for a single SubstrateOS project: a
devcontainer that sees only its own project workspace and its own scoped slice of the
shared memory layer (Zero Context Bleed). The Lab Controller scaffolds one capsule per
project from this template, substitutes the placeholder tokens, and launches it. Targets
Docker in WSL2 first, remote Linux later (ADR-007); no Docker Desktop-specific behaviour.

## Placeholder tokens (substituted by the Lab Controller)

| Token | Replaced with |
|---|---|
| `__MEMORY_NAMESPACE_DIR__` | Absolute host path of this capsule's memory namespace directory (bind-mounted at `/memory`) |
| `__CAPSULE_NAMESPACE__` | The capsule's memory namespace identifier (exported as `CAPSULE_NAMESPACE`) |

`${localWorkspaceFolderBasename}` is resolved by the devcontainer tooling itself and is
not a Lab Controller token.

## Validation

- Image only: `docker build -t capsule-template-test .` from this directory.
- Full config: substitute the tokens into a copy, then run
  `devcontainer up --workspace-folder <project>` with the
  [devcontainer CLI](https://github.com/devcontainers/cli).
  The raw template will not start as-is because `__MEMORY_NAMESPACE_DIR__` is not a real path.

## Isolation guarantees

- Only two mounts exist: the project workspace folder (devcontainer default) and the
  capsule's memory namespace directory at `/memory`. Nothing else.
- No host credential mounts. Never mount `~/.ssh`, `~/.aws`, `~/.gnupg`, or any other
  credential or token store into a capsule.
- Never mount the repo root of another project, or any shared parent directory that
  would expose sibling projects.
- No privileged flags, no host Docker socket, no host network namespace.
- The container runs as the non-root `capsule` user with no sudo.
