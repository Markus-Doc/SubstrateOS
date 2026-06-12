# ADR-015: `lab build` is host-scoped headless claude in Phase 1

Date: 2026-06-12
Status: Accepted

## Decision

`labctl build <project>` runs the build agent on the Windows host as
`claude -p "<mission>" --dangerously-skip-permissions --output-format
stream-json --verbose` with `cwd` set to the capsule workspace. In-container
execution (launching claude inside the capsule devcontainer) is deferred to
Phase 2 on the Lab machine.

Two invocation policies travel with this:

1. **`--dangerously-skip-permissions` is owner policy, not product policy.**
   It reflects Markus's standing authorisation for full automation on his own
   machine. If SubstrateOS ships publicly, end-users run plain `claude` under
   their own permission model; the flag must become configurable before any
   public release.
2. **Headless children get no inherited `ANTHROPIC_API_KEY`.** labctl strips
   that variable from the child environment for every headless claude
   invocation (summaries and builds), delegating auth entirely to the claude
   CLI's own credential store. Discovered empirically: a stale
   `ANTHROPIC_API_KEY` in the user environment silently overrides the CLI's
   subscription login and fails every `claude -p` call with "Invalid API key".

## Context

Phase 1's control plane is the Windows host + WSL2 (ADR-013); Docker-in-WSL2
capsule execution is validated for the devcontainer template but wiring claude
into it adds no Phase 1 evidence beyond what host-scoped execution proves
(mission in, stream-json out, budget enforced). The capsule directory itself
still provides workspace isolation: the child process starts in the capsule
workspace, and the capsule CLAUDE.md states the boundary.

## Consequences

- Phase 1 isolation is by convention (cwd + CLAUDE.md constraints), not by
  container boundary; Phase 2 moves execution inside the devcontainer.
- stream-json events are the contract for usage metering (ADR-016) and run
  logs (`.substrateos/logs/run-<ts>.jsonl` in the capsule, gitignored there).
