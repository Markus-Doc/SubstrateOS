# ADR-007: Devcontainers — WSL2 First, Remote Linux Later

Date: 2026-06
Status: Accepted

## Decision

Target Docker in WSL2 for local development. Remote Linux (Lab machine) is the later execution target but is not required for Phase 1.

## Context

The repo lives on Windows but the project is Linux-oriented. WSL2 is closer to the intended Linux runtime than native Windows and avoids Docker Desktop-specific behaviour. The Lab machine (dedicated LAN hardware) is the eventual production execution target, but requiring remote Linux from day one would slow early development.

## Constraints

- Devcontainer configs must work in WSL2 first.
- Paths, scripts, and docs must remain compatible with remote Linux.
- No Docker Desktop-specific behaviour unless no alternative exists.

## Consequences

- Local development is unblocked immediately on the Windows machine.
- Promotion to the Lab machine is a configuration change, not an architecture change.
- WSL2 and remote Linux share enough runtime parity that surprises at promotion time should be minimal.
