# Open Questions

These must be resolved before Phase 1 build work begins.
Record the answer and the date when each is closed.

---

## OQ-001: Lab Host Environment

Question: What is the actual execution environment for the Lab Controller?
The repo path is Windows (C:\Users\marku) but the architecture specifies Ubuntu.

Options:
- WSL2 on the same Windows machine
- Separate Linux machine on the local network
- Dual boot

Status: CLOSED
Resolved: Dedicated physical machine on LAN, connected to home router, woken via Wake-on-LAN command. This is the Lab host — all Lab Controller execution, memory storage, and Devcontainer runtime runs here.
Date: 2026-06-01

---

## OQ-002: agentmemory MCP Implementation

Question: Which specific agentmemory MCP fork or package will be used?
Several exist with different feature sets and maintenance status.

Status: CLOSED
Resolved: Use rohitg00/agentmemory as the reference package. It is not a hard Phase 1 dependency. Memory must sit behind a provider interface. agentmemory must never replace repo documentation, structured state files, decision records, or explicit instructions. Phase 1 source of truth is always repo files.
Date: 2026-06-01

---

## OQ-003: Firecrawl Deployment

Question: Self-hosted Firecrawl instance or cloud API with key?
This affects secrets management and whether network access is needed from inside capsules.

Status: CLOSED
Resolved: Use Firecrawl cloud API. Start on the free or lowest practical tier. Firecrawl must be optional and metered, sitting behind a provider interface so it can later be replaced, self-hosted, rate-limited, or disabled. Use cheaper retrieval methods first; invoke Firecrawl only when higher-quality extraction, crawling, or browser handling is required.
Date: 2026-06-01

---

## OQ-004: Lab Controller Shell Target

Question: Is the Lab Controller a Python CLI (Click/Typer) from the start,
or a shell script wrapper first?

Status: CLOSED
Resolved: Python CLI using Typer from the start. Phase 1 scope: minimal commands only — init, status, ingest, doctor. No daemon, web app, or complex orchestration. Shell scripts are acceptable for one-off setup tasks but not for the Lab Controller itself.
Date: 2026-06-01

---

## OQ-005: Devcontainer Runtime

Question: Where do Devcontainers run?
Docker Desktop on Windows, Docker inside WSL2, or a separate Linux machine?

Status: CLOSED
Resolved: Docker in WSL2 for the Windows development machine. Remote Linux (Lab) is the later execution target but is not required in early development. Devcontainer configs must be WSL2-compatible first and remote-Linux-compatible later. No Docker Desktop-specific behaviour unless unavoidable.
Date: 2026-06-01

---

## OQ-006: Phase 1 Dashboard Scope

Question: What exactly is the personal research dashboard?
Needs a defined input (raw sources) and output (what the dashboard shows)
before it can be built.

Status: CLOSED
Resolved: A local project status dashboard, CLI-rendered from local files. Not a product UI.

Inputs:
- project manifest
- research source list
- decision records
- open questions
- task list
- ingestion status
- provider configuration status
- local environment health checks
- recent run logs

Displays:
- project name and current phase
- source-of-truth research document
- confirmed decisions
- open questions
- next recommended actions
- configured providers
- missing required configuration
- last successful ingestion or processing run
- warnings from environment checks

A web dashboard may follow only after the state model proves useful.
Date: 2026-06-01

---

## OQ-007: Remote Trigger Pathways for the Lab Operator

Question: How does Markus trigger the Lab operator (ADR-017) when away from
the control plane? Candidate channels: iMessage, Telegram, WhatsApp, Claude
"Dispatch". The flow to design: message arrives -> box wakes (WoL relay or
always-on listener) -> mission dispatched -> result reported back on the same
channel.

Constraints already locked: subscription auth only (no API keys), no secrets
in tracked files, the existing `labctl lab` surface stays the execution path.

Status: CLOSED
Resolved: Telegram bot via outbound long-polling (no inbound exposure) as the
channel; RTC self-wake duty cycle (`rtcwake -m mem`, default 10-minute
interval) instead of a WoL relay — no always-on relay device exists, so the
box wakes itself, drains the queue, executes, re-suspends; Tailscale (already
enrolled on box + iPhone) with Tailscale SSH as the direct command tunnel.
Control-plane WoL unchanged. Full rationale and threat-model delta: ADR-018.
Date: 2026-06-12
