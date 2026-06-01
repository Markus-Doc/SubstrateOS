# System Overview: Agent Brain Architecture

## Core Principle

Shared Brain, Isolated Capsules.
Long-term knowledge is centralised. Project execution is strictly isolated.

## Five-Layer Architecture

```
+---------------------------------------------------------------+
|  1. LAB CONTROLLER (Local)                                    |
|     Python CLI. Scaffolds projects, manages git worktrees,   |
|     launches containers, enforces budget circuit breakers.    |
+---------------------------------------------------------------+
                          |
+---------------------------------------------------------------+
|  2. INGESTION PIPELINE                                        |
|     Firecrawl (web) + Docling (PDF, Office, complex layouts) |
|     Output: token-efficient Markdown with provenance          |
+---------------------------------------------------------------+
                          |
+---------------------------------------------------------------+
|  3. MEMORY LAYER (Shared)                                     |
|     agentmemory MCP server, SQLite backend                   |
|     BM25 + vector hybrid retrieval                            |
|     SHA256 content hash + source URL per chunk                |
|     AI-derived content held in review queue until approved    |
+---------------------------------------------------------------+
        |                              |
+---------------+            +--------------------+
|  4. CAPSULE   |            |  4. CAPSULE        |
|  Project A    |            |  Project B         |
|  Devcontainer |            |  Devcontainer      |
|  Scoped mem   |            |  Scoped mem        |
+---------------+            +--------------------+
        |                              |
+---------------------------------------------------------------+
|  5. EXECUTION ENGINES (Cloud)                                 |
|     Claude Code, Codex (GPT-5.5)                             |
|     Treated as replaceable. No vendor lock-in.               |
+---------------------------------------------------------------+
```

## Security Gate (Pre-Push)

Every release runs:
- Gitleaks: secret scanning
- Semgrep: static application security testing
- Trivy: container and dependency vulnerability scanning

## Explicitly Out of Scope (All Phases)

- Postgres in Phase 1
- LangGraph, AutoGen, or heavyweight agent frameworks
- Local LLM inference on the i7 laptop
