# My Agent Brain: 2026 Technical Strategy and Final Master Plan

## 1. Executive Verdict: The Disciplined Harness
The strategic objective for "My Agent Brain" is to build a **thin, local-first orchestration layer**, not a monolithic platform. As of mid-2026, the AI coding ecosystem has matured around built-in memory, subagents, and the Model Context Protocol (MCP). Consequently, the most viable path is a **disciplined harness** that glues together existing, high-performance tools (Claude Code, Codex, agentmemory, and Docling) rather than a bespoke, database-backed engine. 

This approach prioritizes **execution speed and simplicity** while preserving a long-term path toward cloud-scale migration.

---

## 2. Core Philosophy and Architectural Principles
The foundational principle is **"Shared Brain, Isolated Capsules."** The system centralizes long-term knowledge ("The Brain") while strictly isolating the execution and environment of individual projects ("The Capsule").

### Key Principles
*   **Deterministic First, AI Second:** Raw research must be processed via deterministic tools (Docling/Firecrawl) before AI interpretation to prevent hallucinations from becoming "facts".
*   **The Lab as Control Plane:** The local Ubuntu machine ("Lab") serves as the orchestration and storage hub. Reasoning and heavy build tasks are offloaded to frontier APIs.
*   **Harness Agnosticism:** Model vendors and coding agents are treated as replaceable execution engines within a governed framework.
*   **Zero Context Bleed:** Mandatory project-level isolation ensures secrets, dependencies, and memory do not leak between capsules.

---

## 3. System Architecture
The architecture is structured into five distinct functional layers:

1.  **Lab Controller (Local):** A Python-based CLI that scaffolds projects, manages git worktrees, and launches containers.
2.  **Ingestion Pipeline:** A deterministic workflow that normalizes diverse data sources into structured Markdown with provenance.
3.  **Memory Layer (Shared):** A local **MCP memory server** (e.g., `agentmemory`) providing persistent semantic recall and cross-session knowledge via a SQLite backend.
4.  **Project Capsules (Isolated):** Individual **Devcontainers** mounting only project-specific directories and scoped memory namespaces.
5.  **Execution Engines (Cloud):** High-reasoning frontier models (e.g., Claude Opus 4.8, Codex GPT-5.5) invoked for implementation and review.

---

## 4. Memory Architecture and Knowledge Governance
For Phase 1, the system utilizes **SQLite-backed MCP memory** instead of a full Postgres deployment. This minimizes operational overhead while providing a high-performance, vendor-agnostic interface for agents.

### Retrieval and Accuracy Rules
*   **Hybrid Retrieval:** The system utilizes BM25 (keyword) plus vector similarity search to ensure precision.
*   **Cryptographic Provenance:** Every memory chunk is stored with a SHA256 content hash, capture timestamp, and a direct link to the original source.
*   **Review Queue:** AI-generated summaries and interpretations are flagged as "derived data" and held in a review queue for human approval before becoming "trusted memory".

---

## 5. Ingestion and Context Engineering Workflow
The ingestion pipeline converts raw research into a **Build Context Pack**, ensuring build agents never start from a vague prompt.

1.  **Capture:** Firecrawl for web scraping; Docling for PDFs, Office docs, and complex layouts.
2.  **Normalization:** All inputs are converted to token-efficient Markdown with metadata preserved.
3.  **Context Packaging:** The Lab Controller generates a curated, task-specific subset of memory and environment rules (`CLAUDE.md`) to keep agent focus high and costs low.

---

## 6. Build and Verification Workflow
The build process is an iterative staged loop:
1.  **Research & Plan:** Ingest sources and decompose the project brief into dependency-aware tasks.
2.  **Prep Capsule:** Initialize the Devcontainer, project-scoped rules, and context pack.
3.  **Implementation:** Build agents (Claude Code or Codex) implement tasks within the isolated capsule.
4.  **Evidence-Based Verification:** Every build phase must produce observable evidence, including logs, test results, and screenshots.

---

## 7. Security and Governance
As a professional Secure AI portfolio piece, the harness includes a mandatory **Release Gate**:
*   **Secret Scanning:** `Gitleaks` runs on every pre-commit and pre-release task.
*   **Vulnerability Scanning:** `Semgrep` (SAST) and `Trivy` (Container/SCA) audit the codebase and environment before any public push or cloud deployment.
*   **Circuit Breakers:** The Lab Controller monitors token usage and session length, freezing the capsule if hard budget caps are exceeded.

---

## 8. Implementation Roadmap

### Phase 1: The Core Loop (Weeks 1-4)
*   **Objective:** Establish the "Idea to Repo" workflow using existing tools.
*   **Stack:** Python Lab CLI, `agentmemory` MCP (SQLite), Docling, and Claude Code.
*   **Success Metric:** Successfully build and audit a "personal research dashboard" from raw sources to GitHub.

### Phase 2: Performance and Scale (Months 2-6)
*   **Objective:** Optimize retrieval and expand autonomous capabilities.
*   **Evolution:** Introduce local embeddings/rerankers on the RTX 3070; migrate to **Postgres + pgvector** if SQLite limits are reached; implement **Dynamic Workflows** for codebase-wide audits.

### Phase 3: Long-term Platform Evolution
*   **Cloud Parity:** Move the Lab Controller and Memory to AWS (RDS/pgvector).
*   **Swarm Orchestration:** Graduate to managed multi-agent factories for large-scale SaaS builds.

---

## 9. Model Portability and Risk Mitigation
To avoid vendor lock-in, the architecture adheres to the **Model Context Protocol (MCP)** standard. All memory is stored in open formats (Markdown, SQLite/Postgres), ensuring the system remains resilient as dominance shifts between model providers.

### Explicitly Rejected Approaches
*   **Custom Postgres Platform in v1:** Rejected as premature over-engineering. SQLite-backed MCP is sufficient for initial velocity.
*   **Heavyweight Agent Frameworks:** Frameworks like LangGraph or AutoGen are deferred; Claude Code’s native orchestration is more efficient for this use case.
*   **Local Reasoning on Lab Laptop:** Rejected due to hardware constraints. The i7-4720HQ is better utilized for orchestration than slow, low-quality inference.