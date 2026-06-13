# ADR-025: In-container capsule execution and capsule memory access

Date: 2026-06-13
Status: Accepted

## Decision

Capsule builds may run inside a Docker container (`labctl build --container`),
the deferred first job of ADR-015. The dispatching `labctl` keeps full control:
mission on stdin, stream-json metering, and the token circuit breaker — but the
breaker now **kills the whole container** (`docker kill`), not just a host
process tree.

### Auth (Phase-2 locked decision 2)

The Claude OAuth token is injected at launch as the `CLAUDE_CODE_OAUTH_TOKEN`
environment variable, passed to `docker run` by **name only** (`-e
CLAUDE_CODE_OAUTH_TOKEN`) so the value never appears in argv, the image layers,
or any mount. Never an API key (ADR-017). The capsule image (`templates/
capsule-devcontainer/Dockerfile`) installs the Claude Code CLI but bakes in no
credentials.

### Capsule memory access

The capsule's namespace directory is bind-mounted read-write at `/memory` — the
same single namespace the host build already mounts, preserving the isolation
guarantee (no other namespace, no credential mounts). **MCP exposure of memory
is deliberately NOT added**: the file mount is sufficient for a single in-
container agent. MCP memory access is reconsidered only if multi-agent
in-container access genuinely needs it (ADR-009), and would be its own ADR.

## Implementation

- `capsule.build_docker_argv` / `_spawn_claude_container` / `kill_container` /
  `run_container_build`; `run_build` gained a `kill` hook so the breaker
  termination strategy is pluggable (host tree vs container).
- `labctl build --container` reads `CLAUDE_CODE_OAUTH_TOKEN` from the env and
  errors clearly if absent.
- Run path staged per OQ-005: devcontainer/Docker in WSL2 first, then the
  identical flow on the Lab box over SSH.

## Consequences

- The container-execution plumbing is built and unit-tested (argv, token-not-in-
  argv, container-kill on breaker trip) without requiring Docker in CI.
- The **live in-container breaker demonstration with committed evidence**
  (M4 final bullet) and the M5 capstone run require Docker on the target and real
  Agent-SDK token spend; they are owner-triggered, not auto-run.
