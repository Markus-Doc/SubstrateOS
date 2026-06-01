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

Status: OPEN
Resolved:
Date:

---

## OQ-002: agentmemory MCP Implementation

Question: Which specific agentmemory MCP fork or package will be used?
Several exist with different feature sets and maintenance status.

Status: OPEN
Resolved:
Date:

---

## OQ-003: Firecrawl Deployment

Question: Self-hosted Firecrawl instance or cloud API with key?
This affects secrets management and whether network access is needed from inside capsules.

Status: OPEN
Resolved:
Date:

---

## OQ-004: Lab Controller Shell Target

Question: Is the Lab Controller a Python CLI (Click/Typer) from the start,
or a shell script wrapper first?

Status: OPEN
Resolved:
Date:

---

## OQ-005: Devcontainer Runtime

Question: Where do Devcontainers run?
Docker Desktop on Windows, Docker inside WSL2, or a separate Linux machine?

Status: OPEN
Resolved:
Date:

---

## OQ-006: Phase 1 Dashboard Scope

Question: What exactly is the personal research dashboard?
Needs a defined input (raw sources) and output (what the dashboard shows)
before it can be built.

Status: OPEN
Resolved:
Date:
