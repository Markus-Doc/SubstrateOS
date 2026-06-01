# My Agent Brain: Technical Due Diligence and Build Decision (May 2026)

## A. Executive Verdict

**Build a thin, file-first orchestration layer, not a platform. Do not build the Postgres plus pgvector "brain" as your v1.** The single most important finding is that the AI coding ecosystem moved hard toward built-in memory, subagents, hooks, skills and orchestration between late 2025 and May 2026, so most of what "My Agent Brain" proposes now exists as features inside Claude Code and Codex CLI, or as small open-source repos you can reuse. Building a custom database-backed memory engine first would duplicate work that is now free, and it is the single highest risk of wasted effort for a technical beginner.

The plan's instincts are mostly correct: project isolation, deterministic extraction before AI interpretation, source-linked chunks, no unsourced AI claims becoming trusted memory, containers per project, and local-first where possible. Those are genuinely good principles and align with 2026 best practice. The error is sequencing and scope. The user wants the simplest reliable path, and the simplest reliable path in 2026 is to assemble existing tools (Claude Code or Codex CLI plus a small memory MCP server plus devcontainers plus a few security scanners) rather than to build a bespoke engine.

The Lab laptop (i7-4720HQ, 12GB DDR3L, GTX 960M 2GB) is correctly assessed as not viable for meaningful local inference. Treat it as orchestration and storage only. The 2GB VRAM cannot even hold a small 4-bit 7B model, and CPU-only inference at 12GB RAM will be painfully slow for anything beyond tiny classification. Push all real inference to paid APIs, and use the RTX 3070 desktop only if you later want a local embedding or small preprocessing model.

Verdict in one line: reduce scope dramatically, start with a small proof using existing tools, and only build custom memory if and when you hit a concrete limit you can name.

## B. Best Discovered Existing Tools and Repos

Confidence labels: Proven (mature, widely used, official), Promising (active, real traction, some risk), Experimental (early, thin track record), Hype (loud claims, weak evidence).

| Tool / Repo | What it does | OSS / Paid | Local? | Memory | MCP | Isolation | Fit | Maturity |
|---|---|---|---|---|---|---|---|---|
| Claude Code (code.claude.com) | Terminal coding agent, subagents, hooks, skills, CLAUDE.md memory, Dynamic Workflows, Remote Control, Cowork | Paid (Pro/Max/Team/Ent or API) | No (cloud model) | Yes (CLAUDE.md + auto memory + subagent memory) | Yes (client and host) | Worktrees, subagent context isolation | Core build/reasoning engine | Proven |
| OpenAI Codex CLI (github.com/openai/codex) | Open-source Rust terminal agent, Goal Mode, subagents, MCP, permission profiles, remote control | OSS CLI, paid models | No | Versioned memory summaries | Yes | Sandbox, permission profiles | Second build engine, cross-check | Proven |
| Archon (github.com/coleam00/Archon) | "Harness builder": YAML workflows for AI coding, isolated worktrees, idea-to-PR, web dashboard, MCP | OSS | Orchestrates cloud agents | Project/knowledge base | Yes | Per-task worktrees | Closest existing match to user's vision | Promising |
| agentmemory (github.com/rohitg00/agentmemory) | Persistent memory for coding agents, local SQLite, MCP, plugins for Claude Code/Codex | OSS (MIT) | Yes (local SQLite + local embeddings) | Yes | Yes (53 MCP tools, 12+ lifecycle hooks, REST API on port 3111) | Per-session capture | Drop-in memory layer | Promising |
| Engram (github.com/Gentleman-Programming/engram) | Single Go binary, SQLite+FTS5, MCP, CLI, TUI, no Python/Docker | OSS | Yes | Yes | Yes | Per-project DB file | Simplest local memory | Promising |
| Task Master AI (github.com/eyaltoledano/claude-task-master) | Turns a PRD into dependency-aware tasks, drops into Cursor/Claude/Codex/Roo/Cline | OSS | Partial | Task state | Yes (selectable tool loading) | Per-project tasks | Planning/PRD decomposition | Proven |
| Open Brain (github.com/srnichols/OpenBrain) | Postgres+pgvector semantic memory, Docker, MCP, one-prompt install | OSS | Yes (Docker) | Yes (provenance, hashes) | Yes | Per-deployment | Reference if you must go Postgres later | Experimental |
| Docling (IBM) | PDF/doc to structured Markdown, strong on tables/layouts | OSS | Yes (CPU ok) | No | No | n/a | Accuracy-first ingestion | Proven |
| MarkItDown (Microsoft) | Fast doc-to-Markdown, thin wrapper, no models/GPU | OSS (MIT) | Yes | No | No | n/a | First-pass clean digital docs | Proven |
| Firecrawl (firecrawl.dev) | URL to clean Markdown, crawl/map/extract, MCP, automatic provenance/source URLs | Freemium | API | No | Yes | n/a | Web research ingestion with citations | Proven |
| Playwright MCP | Full browser control, forms, auth, JS-heavy pages | OSS | Yes | No | Yes | n/a | When you must drive a real browser | Proven |
| gitleaks / TruffleHog / Semgrep / Trivy | Secret scanning, SAST, container/dependency scanning | OSS | Yes | No | No | n/a | Release-readiness audit | Proven |
| Qwen3-Embedding (0.6B/4B/8B, Apache 2.0) | SOTA open embedding+reranker, runs on Ollama | OSS | Yes (3070, not Lab) | n/a | n/a | n/a | Local embeddings if needed | Proven |
| Cursor / Windsurf / Devin / Jules / Antigravity | IDE and cloud coding agents | Paid/Freemium | No | Varies | Varies | Varies | Optional, not core | Proven |
| Cline / Roo Code / OpenHands / Aider / Continue | OSS coding agents, bring-your-own-model | OSS | Yes (with local or API models) | Memory Bank patterns | Yes | Varies | Optional alternatives | Proven |
| supermemory / membot / agent-memory-mcp / hindsight | Memory MCP servers with varying designs | OSS/Freemium | Mostly yes | Yes | Yes | Varies | Study for patterns | Promising/Experimental |

## C. Use, Study, Avoid

**Use now (v1):**
- Claude Code as primary build and reasoning engine. Opus 4.8 is priced at $5 per million input tokens and $25 per million output tokens (unchanged from 4.7), with a fast mode at $10/$50 per million at roughly 2.5x output speed (down from $30/$150 on 4.7). Use Opus 4.8 for hard tasks and cheaper tiers for routine work.
- One small local memory MCP server: agentmemory or Engram. These give persistent cross-session memory with near-zero setup and no Postgres.
- Devcontainers (one per project) for isolation and safe autonomous runs.
- Docling plus MarkItDown for document ingestion, Firecrawl for web research with built-in provenance.
- gitleaks, Semgrep, Trivy for the pre-release audit.
- Task Master AI for turning a plain-English brief into dependency-aware tasks.

**Study (borrow patterns, do not necessarily run):**
- Archon (coleam00): the closest existing implementation of "describe a project, get isolated workflows, idea-to-PR". Study its YAML workflow model and worktree isolation before building anything custom.
- Cole Medin's PIV loop (Plan, Implement, Validate) and "context engineering" repos, and his "Dark Factory" autonomous experiment (label as experimental, not proven production).
- Open Brain for a clean Postgres+pgvector provenance schema if you later outgrow file/SQLite memory.
- Anthropic's official Claude Code docs on subagents, hooks, skills, memory and Dynamic Workflows.

**Avoid (for now):**
- Building a custom Postgres+pgvector memory engine as v1. Premature.
- Heavyweight agent frameworks (LangGraph, AutoGen, CrewAI, SuperAGI) for this use case. They add orchestration complexity you do not need when Claude Code and Codex already orchestrate.
- Any meaningful local LLM inference on the Lab laptop.
- Chasing every new memory MCP repo. The space is crowded and many are weeks old with thin track records (tool churn risk is real).

## D. Best Current Architecture

The recommended architecture differs from the user's plan in sequencing and weight. It is a "shared brain plus isolated capsules" design, but the shared brain starts as files plus a small SQLite-backed memory MCP server, not Postgres.

Layers:
1. **Orchestration and storage (Lab laptop, Ubuntu).** Holds the repos, the memory MCP server, devcontainer definitions, scripts, and the ingestion outputs. No inference here.
2. **Inference (paid APIs).** Claude Code (Opus 4.8 and cheaper tiers) as the primary engine. Codex CLI (GPT-5.5) as a second engine for cross-checking and review. Optionally AWS Bedrock later for portability (Opus 4.8 is available on Bedrock and Vertex).
3. **Shared brain (global).** A small set of Markdown files (preferences, conventions, cross-project lessons) plus one local memory MCP server (agentmemory or Engram) for semantic recall. Source-linked, with provenance and content hashes.
4. **Project capsules (per project).** A devcontainer, a project-scoped CLAUDE.md and .claude/rules, a project memory scope, an isolated git worktree or repo, and project-scoped secrets. No context bleed because memory is namespaced per project and the container only mounts that project directory.
5. **Ingestion pipeline (deterministic first).** Docling/MarkItDown/Firecrawl produce clean Markdown with source URLs and hashes before any LLM touches the content. LLM only enriches (summaries, tags) and never invents trusted facts. A review queue holds low-confidence items.
6. **Verification and release gate.** Tests, screenshots, logs, then gitleaks plus Semgrep plus Trivy plus a dependency and license check before any public push or cloud deploy.

This keeps the "deterministic extraction before AI interpretation" and "no unsourced AI claims become trusted memory" principles, which are correct, while removing the database build burden from v1.

## E. Simplified v1 Stack

Minimal, no unnecessary complexity:

- **Engine:** Claude Code (start here). Add Codex CLI later for cross-checking.
- **Memory:** agentmemory or Engram (pick one). Local, SQLite, MCP, free.
- **Planning:** Task Master AI (optional, when projects get complex).
- **Isolation:** Devcontainers, one per project, mounting only the project folder.
- **Ingestion:** MarkItDown (fast, clean docs) plus Docling (complex PDFs/tables) plus Firecrawl (web, with provenance).
- **Security gate:** gitleaks (pre-commit), Semgrep (SAST), Trivy (deps/containers).
- **Memory files:** CLAUDE.md per project (kept short, under ~60 lines), .claude/rules/*.md path-scoped, .claude/skills for repeated workflows.

Free tier: agentmemory/Engram, Docling, MarkItDown, Playwright, gitleaks, Semgrep, Trivy, devcontainers, Qwen3 embeddings on the 3070. Budget tier: Claude Pro or Codex via ChatGPT plan, Firecrawl paid pages, pay-as-you-go API within the spend cap. Expensive tier: Claude Max, heavy Dynamic Workflows runs, Devin-style cloud agents.

## F. Local vs Paid AI Decision Matrix

| Task | Lab laptop | RTX 3070 desktop | Claude | Codex | Dynamic Workflows |
|---|---|---|---|---|---|
| Deterministic extraction (PDF/HTML to Markdown) | Yes (Docling/MarkItDown, CPU) | Yes | No | No | No |
| Embeddings for semantic search | No | Yes (Qwen3-Embedding) | Optional (API) | Optional | No |
| Summarisation/tagging/dedup | No (too slow) | Maybe (small model) | Yes (cheap tier) | Yes | No |
| Schema/structured extraction | No | Maybe | Yes | Yes | No |
| Codebase summarisation | No | No | Yes | Yes | Only if very large |
| Project planning/PRD | No | No | Yes | Yes | No |
| High-value reasoning, build tasks | No | No | Yes (Opus 4.8) | Yes (GPT-5.5) | No (single pass is enough) |
| Large coordinated work (codebase-wide audit, big migration) | No | No | Yes | Yes | Yes (this is its purpose) |
| Security/release audit across whole repo | No | No | Yes | Yes | Yes if repo is large |
| Verification, adversarial cross-check | No | No | Yes | Yes | Yes for high-stakes |

Model-strength note for routing decisions: GPT-5.5 scores around 82.7% on Terminal-Bench 2.0 and leads on terminal and CLI workflows, while Opus 4.8 scores around 88.6% on SWE-bench Verified and 69.2% on SWE-bench Pro. In practice, lean on Opus 4.8 for multi-file agentic builds and reasoning, and consider Codex/GPT-5.5 for terminal-heavy work and as an independent reviewer.

Quality gate rule: route a task locally only if a quick benchmark shows the local model matches the API on a held-out sample of your real data. On the Lab laptop the honest answer is almost nothing runs locally. On the 3070, embeddings and light classification are realistic, generation of useful code or reports is not at the quality you want.

## G. Research Ingestion Pipeline (accuracy-first with provenance)

Order matters. Deterministic first, AI second.

1. **Capture with provenance.** Web via Firecrawl (returns source URL metadata automatically). Files via Docling (complex layouts, tables, formulas) or MarkItDown (clean digital docs, fast). Audio/video via Whisper or faster-whisper to transcript. Record source URL or path, capture timestamp, and a content hash (sha256) for every item.
2. **Normalise to Markdown.** Markdown is token-efficient and improves retrieval. Keep the source reference attached to each chunk.
3. **Chunk and store with metadata.** Each chunk keeps source, hash, capture date, and a confidence field. Store in the memory MCP server.
4. **LLM enrichment only.** The model may add summaries, tags, and suggested links, but enrichment is labelled as derived, never as a source fact. No unsourced AI claim is promoted to trusted memory.
5. **Review queue.** Low-confidence extractions, conflicting facts, or anything the model flagged go to a queue for human approval before becoming trusted. Per Anthropic's own launch material, Opus 4.8 is "around four times less likely than its predecessor to allow flaws in code it has written to pass unremarked," and is "more likely to flag uncertainties about its work and less likely to make unsupported claims," which helps here, but you still gate it.
6. **Hallucination defences.** Prefer extractive over generative for facts, keep citations on every chunk, and never let the model overwrite a hashed source. Use a reranker (Qwen3-Reranker on the 3070, or an API reranker) when retrieval precision matters.

## H. Memory and Retrieval Design

The research is clear that for a beginner who wants the simplest reliable path, you should start with files plus a small SQLite-backed vector/keyword memory, not Postgres.

- **Start with:** CLAUDE.md and .claude/rules for stable rules, plus one local memory MCP server (Engram uses SQLite+FTS5 in a single Go binary, agentmemory uses local SQLite with local embeddings). agentmemory's own COMPARISON.md reports 95.2% Recall@5 (also 98.6% R@10, MRR 88.2) on LongMemEval-S (ICLR 2025, 500 questions) using a BM25+vector hybrid with all-MiniLM-L6-v2, claiming to beat mem0 (68.5%) and Letta/MemGPT (83.2%). These figures are vendor self-reported, so treat them as Promising rather than independently Proven. Both tools are free, local, MCP-native, and require no database administration.
- **Why not Postgres+pgvector first:** pgvector is excellent and the right destination if you outgrow SQLite, but it adds operational burden (tuning, index choice, maintenance) that a beginner does not need at the start. The consensus across multiple 2026 comparisons is that pgvector is the simplest path only if you already run Postgres, and that embedded options like SQLite vector extensions, Chroma or LanceDB are better for local-first prototyping.
- **Hybrid retrieval:** keyword plus vector beats either alone. Engram and the second-brain starter patterns both use hybrid search.
- **Move to AWS later:** the cleanest migration path is Postgres+pgvector on RDS (or Supabase), because your structured memory and vectors live in one SQL system that maps directly to managed cloud. Keep your memory schema simple now so this migration is mechanical later.
- **Avoid until later:** graph databases (Neo4j), Weaviate, Milvus, Pinecone. These solve scale and relationship problems you do not have yet.

Beginner recommendation: Engram if you want the absolute simplest single-binary local memory, agentmemory if you want the richest MCP toolset and benchmarked retrieval. Either is a fine v1.

## I. Project Capsule Design (isolation)

The strongest, simplest isolation primitive in 2026 is the devcontainer. Official Anthropic and community guidance both recommend running coding agents inside a devcontainer that mounts only the project directory, so a misbehaving agent's blast radius is the container.

Each capsule contains:
- A .devcontainer (Dockerfile plus devcontainer.json) mounting only that project folder. Bind-mount ~/.claude or ~/.codex read-only if you want shared skills, nothing else from home.
- A project-scoped CLAUDE.md (short) and .claude/rules.
- A project memory scope (per-project SQLite file for Engram, or per-project namespace/collection in agentmemory). Separate collection per project prevents context bleed.
- An isolated git worktree or separate repo.
- Project-scoped secrets in the container env or a per-project .env that is never committed (and is gitleaks-scanned).

Global vs per-project: global holds your preferences, conventions, cross-project lessons, and shared skills. Per-project holds everything else. Switching projects means opening that project's devcontainer, which loads only that project's memory and rules. This is how you prevent environment and context bleed without building anything custom.

Tooling inside the capsule: uv for Python, pnpm for Node, pinned versions. Devcontainers handle reproducibility so you do not need Nix unless you want it. Keep it simple.

## J. Agent Workflow Design (idea to research to prep to build to verify)

A staged loop that maps onto existing Claude Code and Codex features rather than custom code:

1. **Describe (plain English).** You state the project. The agent asks clarifying questions and writes a short brief.
2. **Research.** Firecrawl plus Docling gather sources with provenance into the project memory. For big multi-source synthesis, Claude Code's built-in /deep-research workflow runs many subagents and returns one cited report.
3. **Plan.** Task Master AI or Claude plan mode turns the brief into dependency-aware tasks. Human approves the plan.
4. **Prep capsule.** Create the devcontainer, project CLAUDE.md, rules, memory scope, and a build-ready context pack (the curated, source-linked subset the build agent needs).
5. **Build.** Claude Code (or Codex) implements task by task inside the capsule. Subagents handle bounded side quests (research, review) without bloating the main context.
6. **Verify.** Run tests, capture screenshots and logs. Use a separate review agent (Codex reviewing Claude's output, or a Claude review subagent) and hooks (PreToolUse to block dangerous commands, PostToolUse to run linters).
7. **Audit and release gate.** gitleaks, Semgrep, Trivy, dependency and license checks, README and deploy docs check, before any public push or cloud deploy.
8. **Iterate in plain English.** You request changes, the loop re-enters at the relevant stage.

Where Dynamic Workflows fits: only at stages 2, 6 and 7 when the work is genuinely large (codebase-wide audit, hundreds-of-files migration, cross-checked research synthesis). For everyday single-feature builds, a normal Claude Code session or a few subagents is cheaper and sufficient. Use the keyword "workflow" or /effort ultracode to trigger it, and start scoped because it consumes meaningfully more tokens (see Risks).

## K. Risks and Failure Modes

- **Token cost blowout.** Dynamic Workflows and high "effort" settings consume meaningfully more tokens. Anthropic's exact warning is that "Dynamic workflows can consume substantially more tokens than a typical Claude Code session," and community guidance quantifies it further, with one estimate that "a codebase-wide audit could use 10 to 100 times more tokens than a single-pass approach" (Blink, blink.new). The hard ceilings are up to 16 agents running concurrently and 1,000 agents total per run (Claude Code docs). Opus 4.8 also defaults to high effort. Mitigation: keep a hard spend cap (the user's few-hundred-dollar cap), start workflows scoped, route cheap stages to cheaper models, and monitor usage.
- **Hallucination and poisoned memory.** If AI guesses become trusted memory, every downstream build inherits the error. Mitigation: deterministic extraction first, provenance and hashes on every chunk, review queue, never promote unsourced claims. This is the single most important discipline in the whole system.
- **Overengineering.** The biggest risk for this user is building a platform instead of shipping. Mitigation: file-first memory, reuse over build, prove the loop on one small project first.
- **Security and secrets.** AI agents can leak secrets or run dangerous commands. Mitigation: devcontainers with minimal mounts, project-scoped secrets, gitleaks pre-commit, hooks blocking destructive commands, never grant production credentials to a capsule.
- **Context bleed between projects.** Mitigation: per-project memory scopes/collections and per-project containers.
- **Tool churn and abandoned repos.** The memory-MCP space is crowded and young (many repos are weeks old). Mitigation: prefer tools with real traction and permissive licences (agentmemory MIT, Engram, Archon), keep your memory data in an open format (Markdown plus SQLite) so you can switch tools without lock-in.
- **Single-vendor dependence.** Claude Code ties you to Anthropic. Mitigation: keep Codex CLI (open-source, model-swappable) as a parallel engine and keep memory portable.
- **Lab hardware over-reach.** Mitigation: accept Lab is orchestration only, do not waste time trying to run models on 2GB VRAM.

## L. Suggested First Proof Project

**Build a small, real, full-stack app end-to-end through the whole loop: a personal "research-to-dashboard" web app.** Concretely: ingest a handful of sources on a topic you care about (Firecrawl plus Docling), store them in the local memory MCP server with provenance, then have Claude Code build a small dashboard (a single-page web app plus a tiny API) that displays the synthesised, source-linked findings, all inside a devcontainer, ending with the security audit before a GitHub push.

Why this project: it exercises every part of the loop (plain-English brief, sourced research, deterministic ingestion, project memory, capsule isolation, build handoff, verification with screenshots, and the release gate) on something small enough to finish in days. It proves the architecture without the database build, surfaces real token costs within your cap, and produces a shippable artefact. If this loop works smoothly, you have validated the whole "My Agent Brain" concept cheaply. If it does not, you have learned exactly where the friction is before investing in custom infrastructure.

A simpler alternative if even that feels large: a CLI tool that ingests one folder of PDFs and answers questions with citations, built and audited through the same loop. Same lessons, smaller surface.

## M. Source Appendix

**Official docs and primary sources**
- Anthropic, Introducing Claude Opus 4.8 (anthropic.com/news/claude-opus-4-8)
- Claude API Docs, What's new in Claude Opus 4.8 (platform.claude.com)
- Claude Code Docs, Orchestrate subagents at scale with dynamic workflows (code.claude.com/docs/en/workflows), confirms v2.1.154 minimum, 16 concurrent / 1,000-agent cap, availability on all paid plans plus Anthropic API, Amazon Bedrock, Vertex AI and Microsoft Foundry
- Claude blog, Introducing dynamic workflows in Claude Code (claude.com/blog)
- Claude Code Docs, Create custom subagents (code.claude.com/docs/en/sub-agents)
- OpenAI Developers, Codex CLI and changelog (developers.openai.com/codex)
- OpenAI, Introducing upgrades to Codex (openai.com)
- Qwen, Qwen3-Embedding and Qwen3-VL-Embedding/Reranker (qwenlm.github.io, arXiv 2506.05176, arXiv 2601.04720)

**Repos**
- coleam00/Archon, rohitg00/agentmemory, Gentleman-Programming/engram, eyaltoledano/claude-task-master, srnichols/OpenBrain, supermemoryai/supermemory, openai/codex

**Comparisons and technical blogs**
- Vector DB comparisons 2026 (callsphere.ai, 4xxi.com, encore.dev, firecrawl.dev, tigerdata.com)
- PDF/ingestion comparisons (firecrawl.dev best PDF parsers, danilchenko.dev MarkItDown vs Docling vs Marker, tigerdata.com)
- Security tooling (appsecsanta.com, devsecops.ae, devopstales.com, oneuptime.com)
- Coding agent comparisons (artificialanalysis.ai, morphllm.com, toolradar.com, lushbinary.com), plus GPT-5.5 vs Opus 4.8 benchmark coverage (VentureBeat, MarkTechPost, May 2026)
- Devcontainer isolation (codewithandrea.com, markphelps.me, zenvanriel.nl, dev.to)
- Claude Code architecture and best practices (penligent.ai, tembo.io, mcp.directory, medium data-science-collective)
- Dynamic Workflows token-cost commentary (blink.new)

**Creator and community (lower confidence unless verified)**
- Cole Medin (YouTube @ColeMedin, github.com/coleam00, PIV loop, Archon, Dark Factory) - verified channel and repos, "10x/100x" and Dark Factory claims are creator demos, treat as experimental
- Claude Cowork Dispatch and Remote Control guides (datacamp.com, claudefa.st, therundown.ai, aimaker.substack.com) - feature existence verified against Anthropic, specific workflow claims lower confidence
- Ken Huang on Claude Code orchestration primitives (kenhuangus.substack.com)

**Notes on confidence**
- Claude Opus 4.8, Dynamic Workflows, Codex GPT-5.5, Cursor 3.0, Windsurf 2.0 plus Cognition/Devin acquisition: confirmed by multiple May 2026 sources including official ones (Proven).
- Bun Zig-to-Rust port via Dynamic Workflows: roughly 750,000 lines of Rust and 6,755 commits, 99.8% of the existing test suite passing, 11 days first-commit-to-merge, hundreds of parallel agents with two reviewers per file. Anthropic's blog states it is "not yet in production," and Bun creator Jarred Sumner said "we haven't been typing code ourselves for many months now" (The Register, May 14, 2026). Treat as Promising, not independently verified production evidence.
- Dynamic Workflows availability: official docs say all paid plans including Pro (via /config toggle) plus Anthropic API, Amazon Bedrock, Vertex AI and Microsoft Foundry, with Max/Team/API on by default and Enterprise off by default at launch. The launch blog and secondary press list only Max/Team/Enterprise plus API, so treat "Pro via /config toggle" as docs-confirmed only. Hard limits are 16 concurrent agents and 1,000 agents total per run. No quantified token-cost figures are published officially, only "substantially more tokens" warnings (the 10x-100x figure is community estimate).
- Memory MCP benchmark numbers (for example agentmemory's 95.2% R@5 on LongMemEval-S): vendor/self-reported, treat as Promising not independently Proven.