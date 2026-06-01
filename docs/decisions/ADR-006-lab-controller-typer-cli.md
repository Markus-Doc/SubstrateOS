# ADR-006: Lab Controller as Python Typer CLI

Date: 2026-06
Status: Accepted

## Decision

Build the Lab Controller as a Python CLI using Typer from the start.

## Context

A shell script can handle one-off setup, but the Lab Controller needs commands, config, validation, logs, structured state files, and safe error handling from early on. Typer provides clean command definitions without becoming heavy. Click was considered but Typer's type-annotation approach reduces boilerplate.

## Phase 1 Scope

Implement only: init, status, ingest, doctor.
Do not build a daemon, web app, scheduler, or multi-agent orchestration layer in Phase 1.

## Consequences

- Shell scripts remain acceptable for one-off environment setup, not for Lab Controller logic.
- The CLI is the single entry point for all lab operations.
- Extending commands in Phase 2 is additive and does not require restructuring.
