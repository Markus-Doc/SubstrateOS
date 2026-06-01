<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# You are a world-class AI research analyst, agentic software architect, prompt engineer and technical due diligence reviewer.

Your task is to deeply research whether the attached project concept, called “My Agent Brain”, is worth building, how it should be adjusted, and which existing public tools, repos, workflows, creators, communities, papers and products should be studied or reused before any implementation begins.

Assume the user is a capable technical beginner in this specific area. They are not a traditional full-stack engineer, but they can understand technical systems, run CLI tools, read code, debug issues and use AI coding agents. They want the simplest reliable path, not an overbuilt platform.

Important mindset:
Do not assume the current plan is correct.
Do not limit your research to Postgres, pgvector, local inference, Claude, Codex, Dynamic Workflows, agents or any tool already mentioned.
Actively search for better approaches, simpler approaches, existing open-source systems, commercial tools, community workflows and recent influencer discoveries.
Challenge the plan where appropriate.

Project concept summary:
The user wants to build a local-first AI project engine on an Ubuntu LTS laptop called “Lab”.
The system should let the user describe a project in plain English, such as:

* build a website
* build a SaaS product
* build a dashboard
* build a CRM
* build a full-stack application
* build a language-specific app
* build an LLM workflow
* run AI training experiments
* build security tooling
* build research systems

The desired system, currently called “My Agent Brain”, should:

* create an isolated project capsule for each project
* collect raw research and source files
* process data accurately
* build project memory
* prepare a build-ready context pack
* set up containers, scripts, dependencies and environment
* hand off to the best AI build tool
* support Claude Code, Codex CLI, Codex cloud, local models or other tools
* use Claude Dynamic Workflows only if it is genuinely useful
* let the user request changes later in plain English
* run verification, testing, screenshots and logs
* run a security and release readiness audit before public release or cloud deployment
* avoid project context bleeding between different projects

Current plan, which you must evaluate critically:

* shared Lab brain plus isolated project capsules
* local-first inference where possible, not local-only
* deterministic extraction before AI interpretation
* Postgres as structured project memory
* pgvector or another vector store for semantic search
* strict retrieval tools instead of dumping whole tables into prompts
* source-linked chunks
* no unsourced AI claims becoming trusted memory
* Docker or containers per project
* local models for preprocessing where good enough
* Claude or Codex for high-value reasoning and build tasks
* Dynamic Workflows for large coordinated work, audits, research synthesis and complex verification
* cloud portability to AWS or other cloud platforms later

Main research goal:
Find the best practical architecture, tool stack and workflow for this exact goal in mid-2026, based on the newest public information.

Research areas to cover:

1. Very recent Claude and Anthropic developments
Research Claude Opus 4.8, Claude Code Dynamic Workflows, Claude Code memory, Claude Code hooks, Claude Code MCP, Claude Remote Control, Claude Desktop, Claude mobile control and any current best practices from Anthropic docs, blogs, interviews and community examples.
Answer:

* Is Dynamic Workflows useful for this project?
* Where should it be used?
* Where should it not be used?
* What are the token and cost risks?
* Are there new Claude-native features that make part of this custom project unnecessary?
* Are there creator workflows showing better patterns?

2. Codex and OpenAI alternatives
Research OpenAI Codex CLI, Codex cloud, Codex app, Codex agent loop, OpenAI Agents SDK, OpenAI MCP support and any current 2026 best practices.
Answer:

* Can Codex already do much of this?
* Should the user build a local “brain” or mostly use Codex features?
* What are Codex’s strengths compared with Claude Code?
* What are the best ways to combine Codex and Claude?

3. Other agent platforms and coding tools
Research current tools such as:

* Cursor
* Windsurf
* Devin
* GitHub Copilot coding agent
* GitHub Agent HQ
* Google Jules
* Aider
* OpenHands
* Continue
* SuperAGI
* CrewAI
* LangGraph
* AutoGen
* OpenClaw
* Roo Code
* Cline
* Task Master AI
* agentmemory
* Open Brain
* OpenViking
* any newer or better projects discovered during research

For each relevant tool:

* what it does
* whether it is open source or paid
* whether it can run locally
* whether it supports project memory
* whether it supports MCP
* whether it supports isolated project workspaces
* whether it works well for beginner-friendly vibe coding
* whether it could replace part of the planned system
* whether it is worth using, forking, avoiding or studying

4. Public repos and templates
Search GitHub, GitLab and public code indexes for projects that already implement:

* AI second brain
* agent memory
* coding agent memory
* MCP memory server
* Postgres AI memory
* pgvector project memory
* local AI coding agent
* Claude Code workflow
* Codex workflow
* RAG for codebases
* agent project capsules
* repo indexing for LLMs
* codebase knowledge graph
* local-first AI workstation
* personal AI assistant over Telegram, Discord or mobile
* AI project factory
* plain English to full-stack app workflows

Return specific repos with:

* name
* URL
* stars or activity if available
* recent commit status
* license
* stack
* what to reuse
* what to avoid
* whether it is mature, experimental or risky

5. Creator, YouTube, Reddit, Discord and influencer research
Search very recent public material from:

* YouTube
* Reddit
* X or Twitter
* Hacker News
* Discord communities where publicly indexed
* blogs
* newsletters
* Medium
* Dev.to
* personal websites
* creator demos
* Instagram or short-form AI workflow summaries where discoverable

Look for people who have already built:

* personal AI command centres
* Claude Code Dynamic Workflow setups
* Opus 4.8 workflows
* thousands of subagents workflows
* phone-controlled Claude or Codex setups
* coding agent orchestration rigs
* local AI workstations
* local-first RAG memory for agents
* AI project factory pipelines
* vibe coding workflows that actually ship production apps

Prioritise fresh material from the last 30 to 90 days.
Separate hype from substance.
Identify repeatable patterns and practical takeaways.

6. Memory architecture comparison
Compare the current Postgres plus vector plan against alternatives:

* Postgres plus pgvector
* Supabase
* SQLite plus vector extensions
* LanceDB
* Qdrant
* Chroma
* Weaviate
* Pinecone
* Neo4j
* graph databases
* knowledge graph systems
* filesystem-based context
* Markdown or Obsidian style memory
* Claude native memory
* OpenAI memory or project context
* MCP memory servers
* codebase graph systems using Tree-sitter

Answer:

* What is simplest?
* What is fastest?
* What is most accurate?
* What is easiest to query by AI tools?
* What is easiest to move to AWS later?
* What should a beginner start with?
* What should be avoided until later?

7. Data ingestion and accuracy
Research best tools and current best practices for turning raw research into usable project memory.
Include:

* PDFs
* text files
* screenshots
* HTML
* web pages
* videos
* audio
* transcripts
* code repositories
* spreadsheets
* API exports
* Reddit data
* product reviews
* issue trackers
* documentation

Compare:

* Docling
* MarkItDown
* Unstructured
* LlamaIndex ingestion
* LangChain document loaders
* Haystack
* Apache Tika
* OCR tools
* Whisper or faster-whisper
* browser automation tools
* Firecrawl or similar crawl tools
* Playwright MCP or browser-control options

Answer:

* Which tools should be used first?
* Which tools are too complex?
* How should hallucination be prevented?
* What should be deterministic?
* What should an LLM be allowed to enrich?
* How should source provenance, hashes, citations, confidence and review queues be implemented?

8. Local inference reality check
Research current local model options for the user’s intended preprocessing tasks:

* summarisation
* tagging
* deduplication
* schema suggestions
* structured extraction
* report generation
* context pack generation
* codebase summarisation
* project planning

Consider:

* Ollama
* LM Studio
* llama.cpp
* vLLM
* local Qwen models
* local Llama models
* local DeepSeek models
* embedding models
* rerankers
* small local models for classification
* GPU and RAM constraints on a modest laptop

Answer:

* Which tasks are realistic locally?
* Which tasks should go to Claude or Codex?
* How should the quality gate work?
* How should the system benchmark whether local inference is good enough?

9. Project isolation and container strategy
Research best practices for isolated AI project capsules.
Compare:

* Docker Compose per project
* devcontainers
* Nix
* mise
* uv
* pipx
* pyenv
* pnpm workspaces
* containerised build environments
* cloud-ready project templates
* sandboxing for coding agents
* secrets isolation
* separate DB schema versus separate database per project
* separate vector collections

Answer:

* What is the simplest safe setup?
* What should each project capsule contain?
* How should switching projects work?
* How should environment bleed be prevented?
* What should be global and what should be per-project?

10. Security and deployment readiness
Research how AI-generated projects should be reviewed before release.
Include:

* secret scanning
* dependency scanning
* SAST
* container scanning
* auth and access control checks
* input validation checks
* OWASP checks
* license checks
* README and deployment docs
* cloud deployment readiness
* AWS path
* GitHub public repo readiness
* AI coding agent safety practices

Recommend simple tools that fit a local Ubuntu Lab workflow.

11. Decide whether this project is worth building
Be honest.
Evaluate whether the user should:

* build My Agent Brain
* use an existing tool
* combine existing tools
* reduce scope dramatically
* start with a smaller proof
* abandon parts of the plan
* wait for Claude or Codex features to mature

Do not flatter the idea.
Give a practical verdict.

12. Recommend the first build path
Provide a staged plan for a beginner-friendly implementation.
Keep it simple.
Do not over-engineer.
Prioritise working proof over platform design.

The output must include:

A. Executive verdict
One page max.
Say whether the project is worth building and why.

B. Best discovered existing tools and repos
Ranked table.
Include official links, repo links, activity, maturity, license, and fit.

C. “Use, study, avoid” list
Clear recommendations.

D. Best current architecture
Show the recommended architecture after research, even if it differs from the user’s current plan.

E. Simplified v1 stack
A minimal tool list.
No unnecessary complexity.

F. Local versus paid AI decision matrix
Which tasks should be local first, which should go to Claude, which should go to Codex, which should use Dynamic Workflows.

G. Research ingestion pipeline
Accuracy-first pipeline with source provenance.

H. Memory and retrieval design
Best option for structured memory and semantic recall.

I. Project capsule design
How to keep projects isolated.

J. Agent workflow design
How the user should move from idea to research to prep to build to verify.

K. Risks and failure modes
Token cost, hallucination, poisoned memory, overengineering, security, secrets, tool churn, abandoned repos.

L. Suggested first proof project
Pick the best small project to prove the whole loop.
Explain why.

M. Source appendix
Include all important sources grouped by:

* official docs
* repos
* papers
* blog posts
* YouTube or creator content
* Reddit or community discussions

Research quality requirements:

* Prioritise sources from May 2026 and the last 90 days.
* Use official docs where possible.
* Use public repos with recent activity.
* Include creator and community material, but label it as lower confidence unless verified.
* Include dates for fast-moving claims.
* Do not confuse older agent frameworks with Claude’s new Dynamic Workflows.
* Clearly identify unsupported hype.
* Include direct links.
* Include citations or source references for every major claim.
* Distinguish “proven”, “promising”, “experimental” and “hype”.
* When evidence is weak, say so.

Final instruction:
The user wants the simplest, most reliable path to a useful system.
Optimise for clarity, reuse, low token waste, project isolation, accuracy and practical shipping.

It is worth building a trimmed version of My Agent Brain, but as a thin local orchestrator that glues together existing MCP memory servers, ingestion tools, security scanners and Claude or Codex, rather than a heavy custom platform with its own complex agent framework and storage layer.[^1][^2]

***

## Executive verdict (A)

You should build My Agent Brain, but with a sharply reduced scope focused on three things

- A local "Lab" controller that
    - creates per project capsules
    - runs a deterministic ingestion and memory pipeline
    - launches Claude Code and Codex safely with the right context.[^3][^1]
- Reuse existing ecosystems instead of rolling your own agent framework or memory database
    - MCP memory servers such as agentmemory, AgentCortex, and Axiom agent memory already provide project isolated, persistent memory with hybrid search and MCP interfaces.[^4][^2][^5]
    - AI Factory and Factory already give you cross agent, project aware workflows and MCP wiring from a single CLI.[^6][^1]
- Start with simple file based and sqlite based memory, plus one MCP memory server, then layer Postgres or pgvector only if you outgrow this.[^7][^8]

Dynamic Workflows and OpenAI Agents SDK are now powerful enough that you do not need to build a general multi agent engine yourself, only a disciplined harness around them for your laptop Lab.[^9][^10]

***

## Best existing tools and repos (B)

These are the most relevant tools and repos to study or adopt before you write custom code.

### Ranked shortlist

| Rank | Tool or repo | What it is | Open source or paid | Project memory support | MCP support | Activity and maturity | Fit for My Agent Brain |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | `rohitg00/agentmemory`[^2][^11] | Persistent MCP memory server and engine for AI coding agents with hybrid search, knowledge graph extensions and observability | OSS MIT, with hosted option | Yes, central shared memory with project tags and confidence scoring | Yes, full MCP server | Active in 2026 with frequent commits and real creator usage in Cursor and Claude workflows | Use directly as your first "shared Lab brain", do not reimplement this layer |
| 2 | AgentCortex MCP[^4] | MCP native memory system with isolated memory banks per repo, automatic project detection, no context bleed | OSS (MIT like) | Yes, strict project isolated memory | Yes | Active, positioned exactly on repo isolated dev memory | Use as model for your per project capsules and isolation rules |
| 3 | Axiom `agent-memory`[^5] | Harness agnostic memory system for coding agents that works with Cursor, Codex, Claude and custom CLIs | OSS | Yes, workspace and agent scoped | Likely via MCP or client SDKs | New but part of a serious company, active in 2026 | Study and possibly adopt for a simpler memory backend if agentmemory feels heavy |
| 4 | AI Factory CLI (`lee-to/ai-factory`)[^1] | Agent native development environment that wires up agents, MCP servers and skills with one command | OSS MIT | Yes, spec driven workflows and skills, not a generic memory DB | Yes, via skills and MCP servers | Very active in 2026, used as glue between Claude Code, Codex, Cursor and others | Strong candidate to adopt instead of writing your own "project engine" CLI, or at least copy its patterns |
| 5 | Factory AI (`Factory-AI/factory`)[^6][^12] | Agent native development platform with Droid agent across CLI, web and Slack, focused on shipping software | Source available, commercial service | Yes, persistent project context and logs inside Factory | Plugs into MCP servers and tools | Active with 2026 commits and terminal benchmark focus | Study the agent loop and isolation patterns rather than rebuilding, maybe use as external orchestrator if you want SaaS help |
| 6 | OpenHands and Software Agent SDK[^13][^14][^15] | AI driven development platform and SDK for agents that work with code and either local or ephemeral workspaces | OSS for core, commercial cloud for hosting | Supports project specific workspaces and stateful agents | Can integrate MCP tools and external sandboxes | Actively releasing in 2026 with tagged releases | Study for containerised workspaces and safe sandboxes, but probably overkill for a first Lab build |
| 7 | LangGraph and langgraph agent memory example[^16][^17][^18] | Low level orchestration framework for long running stateful agents plus examples of Redis based long term memory | OSS Apache 2 style | Yes, short term and long term memory abstractions | MCP integration supported in examples | Very active, industry standard for complex agents | Study for later multi step workflows, but keep v1 of My Agent Brain lighter than a full LangGraph graph |
| 8 | Docling[^19][^20][^21] | High quality document conversion and structure extraction library with MCP server, focused on accurate layout and tables | OSS under a permissive license | Not memory itself, but front door to deterministic ingestion | Yes, Docling MCP for agents | Active releases in 2026, widely used for advanced PDF ingestion | Use as your primary ingestion engine for complex PDFs and docs in the Lab |
| 9 | Firecrawl[^22][^23][^24][^25] | AI oriented web scraping and crawling API that returns clean markdown, JSON and screenshots with MCP and CLI support | OSS with hosted SaaS | Not a memory, but ideal for deterministic web to markdown ingestion | Yes, MCP and plugins for Claude and Cursor | Very active, widely used for RAG pipelines | Use as default web ingestion step instead of writing your own crawlers |
| 10 | agent memory MCP skill (Agent Skills marketplace)[^26] | Turnkey MCP skill that wraps agentMemory as a memory tool with search, read and write | OSS inside Antigravity IDE repo | Yes, persistent searchable memory for agents | Yes | Maintained, provides an easy bridge into agentmemory | Use as ready made memory MCP server before custom wiring |
| 11 | Recall type Claude Code memory servers[^27][^28][^29] | MCP servers that hook Claude Code session lifecycle to implement persistent project memory | Mixed open source and hosted | Yes, session and project scoped | Yes, Claude focused | Real world Claude Code practice | Study for lifecycle hooks and "pre compact" patterns, do not re implement from scratch |
| 12 | Supermemory and Recallium for Cursor[^30][^31][^32] | External persistent memory systems for Cursor with MCP or plugin integration | OSS plus hosted | Yes, cross tool shared memory | Yes | Active and used by Cursor users in 2026 | Study to understand memory governance and non DB options like file based `.brain` folders |

That table gives you enough concrete code bases to read before you implement a single schema or memory layer.

***

## Use, study, avoid list (C)

### Use directly in v1 or v2

- Firecrawl API or self hosted instance for HTML and site ingestion.[^22][^24][^25]
- Docling library and MCP server for PDFs, Office files and complex layouts.[^19][^20][^21]
- Claude Code CLI with Dynamic Workflows enabled only for large repo wide audits or refactors.[^33][^34][^9]
- OpenAI Codex CLI for alternative code changes, especially where you want multi model checks or OpenAI Agents SDK integration.[^35][^36][^3]
- One MCP memory system to start, ideally agentmemory or AgentCortex, instead of your own Postgres memory.[^2][^4]
- Trivy, Semgrep CE and Gitleaks for security and release readiness checks.[^37][^38][^39]


### Study for patterns

- AI Factory CLI for one command project setup with agents and MCP servers.[^1]
- Factory AI for agent native workflow and "agent as colleague" patterns.[^6]
- OpenHands Software Agent SDK for workspace isolation and ephemeral sandboxes.[^15]
- LangGraph examples for long running stateful workflows and memory graphs.[^17][^16]
- OpenAI Agents SDK examples, especially sandbox agents and MCP integration via `openai-agents-mcp`.[^40][^10][^41]
- Recall and Claude memory servers for lifecycle hooks like session start, observe, pre compact, session end.[^27][^29]


### Avoid or defer for now

- Running your own dedicated vector database like Qdrant, Weaviate or Milvus just for your laptop Lab. They add operational overhead you do not need and pgvector or sqlite are enough until you have tens of millions of vectors.[^42][^8][^7]
- Building a full multi agent orchestrator from scratch when Dynamic Workflows and Agents SDK already handle parallel plans and subagents.[^10][^9][^40]
- Deep and custom knowledge graph systems or Neo4j until you actually hit use cases that need relationship queries, not just semantic search.[^43][^44]
- Overly complex ingestion stacks where you chain several LLM based enrichment passes before you trust the data. Keep ingest deterministic and let AI enrich views, not the source of truth.

***

## Best current architecture (D)

For mid 2026 and your constraints, the best architecture is

- A thin local Lab controller on Ubuntu
- Project capsules that are just git repos plus a `.lab` folder
- One shared "Lab brain" served via an MCP memory server
- Claude Code and Codex as the heavy reasoning engines
- Deterministic ingestion tools feeding memory, with strong provenance.


### High level components

1. **Lab controller (Python or Go CLI)**
    - Creates new project folders from templates, initialises git, sets up `.lab` and optional devcontainer.
    - Writes a small manifest with project id, description, main stack, and links to memory keys.
2. **Memory layer**
    - Uses an MCP memory server such as agentmemory or AgentCortex. This provides hybrid search, project scoped memories and MCP tools for your agents.[^4][^2]
    - Underlying storage can be Postgres or another DB, but that is hidden from your Lab logic.
3. **Ingestion pipeline**
    - Deterministic file and web ingestion via Docling and Firecrawl.
    - Ingestion jobs produce markdown plus JSON metadata and hashes, stored under `.lab/raw` and indexed into memory with provenance fields.[^20][^22]
4. **Retrieval and context packaging**
    - Simple retrieval API that fetches relevant memories and source files for a given task and builds a "context pack" for Claude or Codex, limited by token budget.
    - Packs are per project and never mix data across projects.
5. **Build harness**
    - For small tasks: use Claude Code or Codex directly in the project directory.
    - For large refactors: call Claude Code Dynamic Workflows or Codex Cloud goal tasks that operate over the repo, using your memory server and ingestion results as context where supported.[^45][^9]
6. **Security and release checks**
    - Hook Trivy, Semgrep and Gitleaks into a Lab "audit" command that runs before any public release or cloud deployment.[^38][^39][^37]

You do not need your own general graph orchestrator in v1, only clear boundaries and good use of MCP and the existing agent platforms.

***

## Simplified v1 stack (E)

For a first working version on your Ubuntu Lab laptop

- **Language and runtime**
    - Python for the Lab controller and scripts.
    - Shell scripts where convenient, but keep the orchestration in Python.
- **AI services**
    - Claude Code CLI for main coding agent and Dynamic Workflows when explicitly requested.[^46][^9]
    - OpenAI Codex CLI for cross checking and some long running `/goal` tasks.[^45][^3]
- **Memory**
    - One MCP memory server such as agentmemory, running locally with a simple Postgres or sqlite backend. You treat it as a service, not as a schema you manage.[^5][^2]
- **Storage**
    - Plain files and sqlite in each project for Lab configuration and local indexes.
    - Let the memory server handle semantics and embeddings.
- **Ingestion**
    - Docling CLI or Python library for documents.[^20]
    - Firecrawl API for web pages and site crawls, or self hosted if you want fully local.[^25][^22]
- **Security**
    - Trivy CLI for container and IaC scanning.[^47][^37]
    - Semgrep CE CLI for SAST.[^48][^38]
    - Gitleaks CLI for secrets.[^39][^49]
- **Environment isolation**
    - One Dockerfile or devcontainer template per language stack, applied per project.
    - Avoid heavy Nix or multi layer tool chains until you feel pain.

This is enough to build an idea to repo loop, with ingestion, memory, build and audit.

***

## Local versus paid AI decision matrix (F)

### Task to engine mapping

| Task | Local first | Claude best | Codex best | Dynamic Workflows |
| :-- | :-- | :-- | :-- | :-- |
| Simple tagging, classification, dedup | Local Qwen or DeepSeek small model via Ollama or LM Studio | Only if local quality is poor | Rarely needed | No |
| Light summarisation of single docs | Local 7B to 14B distilled model, maybe DeepSeek R1 Distill 14B | For higher quality summaries or mixed media | Either, but Claude often has better long context handling | No |
| Complex multi doc synthesis, architecture decisions | Use local only for pre filter, not final answer | Yes, Opus or equivalent is best | Use for cross checking designs built with Claude | Only if you want adversarial checking at scale |
| Code generation within one module | Local model if speed or privacy matter and quality is acceptable | Yes, especially with Claude Code context window | Strong, with Codex CLI TUI and subagents | No |
| Large repo refactor, migration, or security audit | Local cannot realistically handle multi hundred file refactors on a modest laptop | Yes, with Dynamic Workflows scanning and verification | Yes, with Codex Cloud tasks and Agents SDK sandbox | Yes, this is the primary use case for Dynamic Workflows |
| Long running "build a SaaS feature" tasks | Local is useful for pre filtering and logs, but not for end to end planning | Strong, especially when paired with remote control and Cowork scheduled tasks | Strong, especially `/goal` feature that runs for hours | Only for the largest, multi step codebase tasks where many subagents make sense |
| RAG over your own project memory | Use local embeddings and retrieval, possibly via agentmemory | Claude or Codex can consume retrieved chunks and reason | Same as Claude | No, plain agent calls are enough |

### Cost and token risks

- Dynamic Workflows are explicitly documented as consuming "meaningfully more usage" than normal Claude Code runs, so they should be reserved for scoped tasks and not turned on by default for every prompt.[^34][^33][^9]
- Codex `/goal` and cloud tasks can run for many hours and hold resources, so you should track those runs and limit them to clearly defined operations.[^50][^36][^45]
- Your Lab controller should add an explicit "workload type" flag so you can decide whether a task is small, medium or large and choose local versus cloud and Dynamic Workflows accordingly.

***

## Research ingestion pipeline (G)

An accuracy first pipeline for My Agent Brain should look like this

1. **Collect sources deterministically**
    - For files in the project, read directly from git working tree.
    - For web resources, use Firecrawl scrape or crawl modes to convert to markdown or JSON with boilerplate removed.[^23][^22][^25]
    - For documents (PDF, DOCX, PPTX, XLSX), run Docling CLI to export to markdown or JSON with structure preserved, not through an LLM.[^19][^20]
    - For audio and video, use Whisper or faster Whisper for transcription, and Docling for WebVTT and audio metadata where available.[^51][^52][^19]
2. **Normalize and hash**
    - Store the raw content and a normalised markdown version in `.lab/raw` with SHA256 hashes, file size and source URL or path.
    - Create a small JSON record describing each source: type, source, hash, timestamp, owner.
3. **Chunk deterministically**
    - Use deterministic chunking rules based on headings and paragraph boundaries, such as Docling components or Firecrawl sections, not LLM based chunk splits.[^24][^20]
    - Include chunk position, parent document id and hash in each chunk metadata.
4. **Index into memory**
    - For each chunk, compute embeddings using a known embedding model via the memory server, store the text, metadata and embedding together.[^2][^5]
    - Never let a model alter the stored text of the chunk. Any enrichment must write new fields.
5. **Optional enrichment**
    - Run local models for lightweight tagging and classification of chunks, storing tags and categories as metadata.
    - For summaries and higher level notes, allow Claude or Codex to write new memory entries linked to sources, but never overwrite the raw text.
6. **Provenance, citations and confidence**
    - Every derived memory item stores the ids of input chunks and an LLM confidence score if you choose to keep one, as agentmemory and similar systems already do.[^11][^43][^2]
    - When building a context pack, always include enough ids that you can reconstruct which sources were used for what answer.
7. **Review queues**
    - For risky or important derived memories, such as security conclusions or architecture decisions, mark them as "pending human review" and require you to approve them in a simple TUI before they become trusted memory.

This mirrors patterns used in Firecrawl RAG setups and Docling usage and matches how dedicated memory engines like agentmemory and Cortex handle provenance and confidence.[^53][^22][^2][^20]

***

## Memory and retrieval design (H)

### Storage choice

Given you are one user on one Lab laptop with plans for later AWS migration

- Start with the memory server default, which is typically Postgres or sqlite under the hood, without you managing it directly.[^5][^2]
- For your own code, maintain a very simple sqlite database in each project for local indexes and cross linking.

Comparing options

- **Postgres plus pgvector** is the "boring default" when you already have Postgres, and many teams report it is not the bottleneck until tens of millions of vectors.[^8][^42][^7]
- **SQLite plus vector extensions** is ideal for single user, local projects where you want one file to copy and back up and do not need concurrent writes.[^8]
- **Qdrant, Weaviate, Pinecone and LanceDB** are more useful in multi tenant or large scale setups and add maintenance you do not need yet.[^44][^42][^7][^8]

For your case, the simplest approach is

- Let agentmemory or AgentCortex handle the main semantic memory backing store as a service you call.
- Use sqlite with a thin Python wrapper for anything specific to your Lab controller that the memory server does not cover.


### Retrieval strategy

- Always retrieve by project id plus query, never across all projects. The memory server should enforce this.
- Combine keyword filters with vector similarity rather than raw kNN. That can be done through the memory server APIs or through pgvector where needed.[^42][^8]
- Keep retrievers very simple in v1: one semantic retriever, one "recent decisions" retriever. You do not need a full multi stage reranking pipeline yet.


### Native Claude or OpenAI memory

- Claude Projects memory and OpenAI workspace memory are useful, but they are tied to hosted environments and not ideal as the primary source of truth for a local Lab brain.[^54][^27]
- Use them as hints and for conversational convenience rather than as the durable memory backing your project capsules.

***

## Project capsule design (I)

Your project capsule should be simple, inspectable and portable.

### On disk structure

Within `~/lab/<project-name>`

- `src/` or language appropriate folders.
- `.lab/` with subfolders
    - `config.json` with project id, description, stack, and memory keys.
    - `raw/` with raw ingested sources and hashes.
    - `notes/` with development diary style notes that agents and you can both read, formatted as markdown.
    - `context/` with cached context packs generated for major tasks.
- Optional `.devcontainer/` or `Dockerfile` for containerised environment.

This mirrors patterns like `.brain` folders and Cursor memory bank setups that people use successfully in 2026.[^31][^32]

### Environment isolation

- Use per project virtualenv or uv for Python, plus a per project container template only when needed.
- Do not share virtualenvs between projects.
- Keep secrets in standard mechanisms such as `.env` files or OS keyrings and never store them in memory servers.


### Switching and bleed prevention

- The Lab controller always sets an explicit project id and passes it to the memory MCP server, so calls are scoped.
- When launching Claude Code or Codex you always start from the project directory, and you do not share the same terminal session between projects when agents are running.
- Do not mount multiple project folders into the same Docker container unless you have a very good reason.

This is simpler than per project Postgres databases and separate vector collections and is closer to how real world memory systems like AgentCortex solve context bleed.[^4]

***

## Agent workflow design (J)

From idea to verified project with My Agent Brain

1. **Idea capture**
    - You tell the Lab controller "new project" with a short natural language description.
    - It scaffolds a capsule, writes `config.json` and opens a README stub.
2. **Research and ingestion**
    - You paste key URLs and documents into the project or let a small script run Firecrawl and Docling to fetch and convert content.
    - The controller indexes these into the memory server with provenance.
3. **Planning**
    - You call a "plan" command that asks Claude or Codex to propose an architecture and task list based on project notes and ingested material.
    - The plan and reasoning are written back into memory and `.lab/notes`.
4. **Build**
    - For small features, you work interactively in Claude Code or Codex in the project directory.
    - For large tasks, you optionally start a Dynamic Workflow or Codex `/goal` run and let it operate for a longer period while you monitor.[^55][^9][^45]
5. **Verification and testing**
    - The Lab controller runs tests in the devcontainer or local environment.
    - Screenshots, logs and test results go into `.lab/context` and memory as detached references.
6. **Security and readiness audit**
    - A "lab audit" command runs Gitleaks, Semgrep and Trivy, plus any language specific linters or SAST, and lets Claude or Codex summarise the results while you keep the raw scan outputs.[^56][^37][^38][^39]
7. **Release or deployment plan**
    - The agent prepares README, deployment docs, IaC templates and checklists, then you review them manually.

This workflow keeps agent power high while still making every important step observable and reversible.

***

## Risks and failure modes (K)

Key risks you should account for

- **Token and cost blowouts**
    - Dynamic Workflows can consume many times the tokens of normal runs and should not be used for day to day editing.[^33][^9][^34]
    - Codex `/goal` and cloud tasks can run 14 hour sessions, so you need caps and alerts.[^50][^45]
- **Hallucination and poisoned memory**
    - If you let agents write unsourced claims into trusted memory, you will quickly accumulate errors.
    - Always separate deterministic ingested data from LLM generated notes and require a review step for the latter.
- **Overengineering**
    - There is strong temptation to add LangGraph, CrewAI, complex vector databases and knowledge graphs from day one. Many creators regret this and later move back to a simpler plus MCP setup.[^57][^58][^43]
- **Secrets and credentials**
    - Secret scanning tools must run before git push and before container build, or you risk hard coded keys leaking.[^59][^39]
    - Agents should not have access to your entire home directory. Use scoped working directories and strict MCP server configuration.
- **Tool churn and abandoned repos**
    - Several memory and agent repos have already been archived or replaced, such as LangGraph Memory being archived in 2026 which shows how fast this space moves.[^60][^43]
    - Your own Lab controller should depend only on stable surface areas: MCP spec, Claude Code CLI, Codex CLI, and simple CLIs like Firecrawl and Docling.

Given your security background this is also a chance to build the Lab with threat modeling around MCP servers and agent permissions from day one.[^61]

***

## Suggested first proof project (L)

A good first proof is

**"AI security checklist and audit harness for one small Flask or FastAPI app"**

Why this works

- The scope is small enough that Dynamic Workflows are optional.
- It exercises ingestion (docs, OWASP pages, your own notes), memory (decisions and findings), code generation, and security scanning.
- You can compare what Claude Code or Codex propose with existing OWASP and AppSec guidance, which you already understand.[^37][^38]
- You will immediately see whether your memory and context pack design helps the agent stay consistent about security requirements.

Flow

1. Use the Lab controller to create a "secure-api-demo" project.
2. Ingest OWASP cheat sheets, framework docs and your own requirements with Docling and Firecrawl.
3. Ask Claude Code to design and scaffold a small API with auth and input validation.
4. Run tests, Semgrep, Gitleaks and Trivy, then have the agent produce a security report and deployment checklist.
5. Review what it got wrong and adjust your ingestion, memory and verification steps.

If this loop feels smooth, you know the Lab design is on the right track.

***

## Source appendix (M)

Grouped by type, focusing on 2026 and late 2025 where possible.

### Official docs and product pages

- Anthropic Claude Code Dynamic Workflows docs and blog.[^62][^9][^34]
- Anthropic computer use, Dispatch and Remote Control posts.[^63][^64][^65][^66][^67]
- OpenAI Codex CLI docs and feature pages.[^68][^36][^69][^3][^35]
- OpenAI Agents SDK docs.[^10]
- Docling project docs and GitHub.[^21][^19][^20]
- Firecrawl documentation and reviews.[^70][^23][^22][^24][^25]
- Trivy, Semgrep and Gitleaks official resources.[^49][^71][^38][^39][^48][^47][^37]
- LM Studio and Ollama or local LLM coverage.[^72][^73][^74][^75][^76]


### Repos

- `rohitg00/agentmemory` persistent memory for coding agents.[^11][^2]
- AgentCortex MCP memory system.[^4]
- Axiom `agent-memory` standalone memory system.[^5]
- LangGraph agent memory example.[^18][^16][^17]
- AI Factory CLI.[^1]
- Factory AI core platform.[^77][^6]
- OpenHands main repo and Software Agent SDK.[^78][^13][^14][^15]
- Docling GitHub repo.[^21]
- Firecrawl repos and tools.[^22][^24][^25]
- OpenAI Whisper.[^79][^52][^51]


### Papers and technical comparisons

- Vector database benchmark and feature comparisons across pgvector, Qdrant, Weaviate, Milvus and LanceDB.[^44][^7][^42][^8]
- Local LLM capability and hardware requirement surveys in 2026.[^80][^75][^76][^81][^72]
- Benchmarks of text extraction tools Docling, MarkItDown, Unstructured and others.[^82][^83][^84][^85][^86]
- Analysis of AI agent frameworks Agents SDK versus MCP.[^87][^57]


### Blogs and long form posts

- AI Agent Open Source Weekly on agentmemory and MCP trends.[^61]
- Open source AI project roundups highlighting OpenClaw, LangChain, Dify and others.[^88][^89][^58][^90]
- Detailed Trivy and Semgrep reviews and recent updates.[^71][^38][^48][^47][^37]
- Firecrawl evaluations and best practice guides.[^25][^70][^22]


### YouTube and creator content

- Dynamic Workflows walkthrough and hidden usage costs.[^91][^92]
- Codex `/goal` experiments in long running tasks.[^50]
- Local LLM tutorials using Ollama on Windows and Mac.[^93][^94][^95]
- "Give Cursor infinite memory" series using agentmemory.[^11]
- "Top AI repos in 2026" style videos that highlight OpenClaw, LangChain, Dify, Firecrawl and others.[^88]


### Reddit and community discussions

- Deep dive discussion of OpenAI Codex agent loop.[^55]
- Claude Code persistent memory via MCP and lifecycle hooks.[^29][^27]
- Cursor persistent memory and `.brain` folders discussions.[^32][^31]
- r/AI_Agents threads on memory layers and agent frameworks.[^96][^43]

***

If you want, next step can be to translate this into a concrete Ubuntu setup plan for your Lab, with exact commands, configs and a first `lab` CLI skeleton that matches your tmux and zsh workflow.
<span style="display:none">[^100][^101][^102][^103][^104][^105][^106][^107][^108][^109][^110][^111][^112][^113][^114][^115][^116][^117][^118][^119][^120][^121][^122][^123][^124][^125][^126][^127][^128][^129][^130][^131][^132][^133][^134][^135][^97][^98][^99]</span>

<div align="center">⁂</div>

[^1]: https://github.com/lee-to/ai-factory/blob/2.x/README.md

[^2]: https://github.com/rohitg00/agentmemory

[^3]: https://developers.openai.com/codex/cli

[^4]: https://github.com/sage-hq/agentcortex-mcp

[^5]: https://github.com/axiomhq/agent-memory

[^6]: https://github.com/Factory-AI/factory/blob/main/README.md

[^7]: https://aidxn.com/blog/pinecone-vs-open-source-showdown/

[^8]: https://encore.dev/articles/best-vector-databases

[^9]: https://claude.com/blog/introducing-dynamic-workflows-in-claude-code

[^10]: https://developers.openai.com/api/docs/guides/agents

[^11]: https://www.youtube.com/watch?v=q-K3VRc9Vls

[^12]: https://github.com/Factory-AI

[^13]: https://github.com/openhands

[^14]: https://github.com/OpenHands/OpenHands/releases

[^15]: https://github.com/OpenHands/software-agent-sdk

[^16]: https://github.com/langchain-ai/langgraph

[^17]: https://github.com/Ofekirsh/langgraph-agent-memory

[^18]: https://github.com/langchain-ai/memory-agent

[^19]: https://docling-project.github.io/docling/

[^20]: https://www.docling.ai

[^21]: https://github.com/docling-project/docling

[^22]: https://comparateur-ia.com/en/ai-tools/firecrawl

[^23]: https://www.firecrawl.dev/glossary/web-extraction-apis/what-is-html-to-markdown-conversion-web-scraping

[^24]: https://www.firecrawl.dev/tools/website-to-markdown

[^25]: https://www.firecrawl.dev/blog/scrape-a-website-to-markdown

[^26]: https://www.agentskills.in/marketplace/@Dokhacgiakhoa/agent-memory-mcp

[^27]: https://www.reddit.com/r/ClaudeAI/comments/1rgrq09/i_built_a_persistent_memory_system_for_claude/

[^28]: https://lobehub.com/mcp/viralvoodoo-claude-code-memory

[^29]: https://github.com/doobidoo/mcp-memory-service/wiki/Memory-Hooks-Complete-Guide

[^30]: https://github.com/supermemoryai/cursor-supermemory

[^31]: https://forum.cursor.com/t/persistent-ai-memory-for-cursor/145660

[^32]: https://forum.cursor.com/t/what-are-you-using-for-ai-memory-across-tools/145359/2

[^33]: https://ecommercenews.com.au/story/anthropic-launches-dynamic-workflows-in-claude-code

[^34]: https://code.claude.com/docs/en/workflows

[^35]: https://developers.openai.com/codex/cli/features

[^36]: https://fluxio.dev/post/openai-codex-complete-guide-2026/

[^37]: https://appsecsanta.com/trivy

[^38]: https://appsecsanta.com/semgrep

[^39]: https://gitleaks.org

[^40]: https://www.youtube.com/watch?v=Bl1e69d_VJU

[^41]: https://github.com/lastmile-ai/openai-agents-mcp

[^42]: https://callsphere.ai/blog/vector-database-benchmarks-2026-pgvector-qdrant-weaviate-milvus-lancedb

[^43]: https://ossinsight.io/blog/agent-memory-race-2026

[^44]: https://www.lancedb.com/lp/vs-qdrant

[^45]: https://www.mindstudio.ai/blog/codex-goal-ralph-loop-14-hour-autonomous-task/

[^46]: https://www.jitendrazaa.com/blog/ai/claude-code-complete-guide-2026-from-basics-to-advanced-mcp-2/

[^47]: https://trivy.dev

[^48]: https://semgrep.dev/docs/release-notes/january-2026

[^49]: https://gitleaks.io

[^50]: https://www.youtube.com/watch?v=dDKRRs5ov9g

[^51]: https://openai.com/index/whisper/

[^52]: https://github.com/openai/whisper/releases

[^53]: https://forum.cursor.com/t/cortex-production-ready-memory-for-ai-agents-built-with-cursor/148436

[^54]: https://github.blog/changelog/2026-01-15-agentic-memory-for-github-copilot-is-in-public-preview/

[^55]: https://www.reddit.com/r/vibecoding/comments/1ql2m4x/openai_deep_dive_unrolling_the_codex_agent_loop/

[^56]: https://www.merito.com/resources/product-release-updates/semgrep-appsec-platform-update-april-2026-ai-detection-autofix-and-enterprise-governance

[^57]: https://www.tldl.io/blog/ai-agent-frameworks-openai-anthropic-mcp-2026

[^58]: https://www.ossphere.dev/blog/best-open-source-ai-projects-you-should-explore-in-2026

[^59]: https://www.jit.io/resources/appsec-tools/git-secrets-scanners-key-features-and-top-tools-

[^60]: https://github.com/langchain-ai/langgraph-memory

[^61]: https://zengineer.blog/blog/tech/ai-agentic-weekly-github-20260517-en/

[^62]: https://code.claude.com/docs/en/whats-new

[^63]: https://9to5google.com/2026/03/24/claude-can-now-remotely-control-your-computer-and-it-looks-absolutely-wild-video/

[^64]: https://simonwillison.net/2026/Feb/25/claude-code-remote-control/

[^65]: https://claude.com/blog/dispatch-and-computer-use

[^66]: https://code.claude.com/docs/en/remote-control

[^67]: https://claudefa.st/blog/guide/development/remote-control-guide

[^68]: https://developers.openai.com/codex/cli/reference

[^69]: https://github.com/openai/codex

[^70]: https://scribehow.com/page/Dont_Buy_Firecrawl_in_2026_Until_You_Read_This_Brutally_Honest_Review__eZi3aD6JT-CDjcJ0HDPuGQ

[^71]: https://www.aquasec.com/products/trivy/

[^72]: https://ibuidl.org/blog/local-llms-2026-ollama-guide-20260310

[^73]: https://weavai.app/blog/en/2026/04/23/lm-studio-2026-guide-run-free-local-ai-models/

[^74]: https://lmstudio.ai

[^75]: https://www.sitepoint.com/best-local-llm-models-2026/

[^76]: https://www.sitepoint.com/local-llms-are-getting-easier-the-complete-guide-2026/

[^77]: https://github.com/Factory-AI/factory

[^78]: https://github.com/OpenHands/open-operator

[^79]: https://github.com/sindresorhus/awesome-whisper

[^80]: https://aidevdayindia.org/blogs/lmsys-chatbot-arena-current-rankings/how-to-run-deepseek-r1-locally-for-developers.html

[^81]: https://zenn.dev/agdexai/articles/deepseek-local-deploy-2026

[^82]: https://github.com/microsoft/markitdown/discussions/1178

[^83]: https://www.linkedin.com/posts/sivakumar-sivaprahasam-7b97614_markitdown-docling-and-marker-are-all-tools-activity-7350183885122523137-qjEN

[^84]: https://dev.to/nhirschfeld/i-benchmarked-4-python-text-extraction-libraries-2025-4e7j

[^85]: https://themenonlab.blog/blog/best-open-source-pdf-to-markdown-tools-2026

[^86]: https://www.reddit.com/r/Python/comments/1ls6hj5/i_benchmarked_4_python_text_extraction_libraries/

[^87]: https://www.prompthub.us/blog/openais-agents-sdk-and-anthropics-model-context-protocol-mcp

[^88]: https://www.youtube.com/watch?v=nOX6WvBHvS4

[^89]: https://www.buildmvpfast.com/blog/best-open-source-ai-projects-github-2026

[^90]: https://blog.bytebytego.com/p/top-ai-github-repositories-in-2026

[^91]: https://www.reddit.com/r/ClaudeAI/comments/1tq9ofy/introducing_dynamic_workflows_in_claude_code/

[^92]: https://www.youtube.com/watch?v=-tLlZqrXpo8

[^93]: https://webscraft.org/blog/ollama-na-8-gb-ram-yaki-modeli-pratsyuyut-u-2026?lang=en

[^94]: https://www.youtube.com/watch?v=dhKNlFsL7Zo

[^95]: https://www.youtube.com/watch?v=sBPsCOfLYds

[^96]: https://www.reddit.com/r/AI_Agents/comments/1pu2tzm/5_most_popular_open_source_ai_agent_repos_from/

[^97]: https://www.linkedin.com/posts/openai_unrolling-the-codex-agent-loop-activity-7420556370015371264-n4dX

[^98]: https://www.sitepoint.com/openai-codex-cli-terminalfirst-coding-agent-tutorial-2026/

[^99]: https://github.com/Pimzino/agentic-tools-mcp

[^100]: https://github.com/rinadelph/Agent-MCP

[^101]: https://github.com/openhands-agent

[^102]: https://github.com/SHAdd0WTAka/Zen-Ai-Pentest/issues/20

[^103]: https://www.hackster.io/news/take-control-with-a-40-ai-command-center-59ab1aa281d8

[^104]: https://github.com/imlnr/ai-factory

[^105]: https://www.aibase.com/repos/topic/local-first

[^106]: https://tiffanya.gumroad.com/l/2026workflowkit?layout=profile\&recommended_by=more_like_this\&recommender_model_name=sales

[^107]: https://x.com/GithubProjects/status/2019795763191279992

[^108]: https://tiffanya.gumroad.com/l/2026workflowkit

[^109]: https://repos.ecosyste.ms/hosts/GitHub/topics/local-first

[^110]: https://www.youtube.com/watch?v=jEqV-L9NP8A

[^111]: https://thethinkingedge.com/p/build-your-personal-ai-command-center

[^112]: https://ai-automation-central.com/blog/post/github-personal-ai-trends-2026/

[^113]: https://nimbalyst.com/blog/best-claude-code-mcp-servers/

[^114]: https://www.reddit.com/r/Agent_AI/comments/1t5a284/50_best_mcp_servers_for_claude_code_2026/

[^115]: https://www.totalum.app/blog/best-mcp-servers-2026

[^116]: https://hidekazu-konishi.com/entry/claude_code_features_settings_reference_2026.html

[^117]: https://latenode.com/blog/best-claude-code-mcp-servers

[^118]: https://github.com/topics/project-memory?l=html

[^119]: https://www.youtube.com/watch?v=pYMWspLVMKw

[^120]: https://github.com/caramaschiHG/awesome-ai-agents-2026

[^121]: https://github.com/matatonic/openedai-whisper

[^122]: https://github.com/docling-project/docling/discussions/3241

[^123]: https://github.com/openai/whisper/blob/main/CHANGELOG.md

[^124]: https://github.com/Olawoyin365/docling-exploration-outreachy

[^125]: https://www.cncf.io/online-programs/trivy-open-source-scanner-for-container-images-just-download-and-run/

[^126]: https://semgrep.dev/products/semgrep-code

[^127]: https://app.daily.dev/posts/5-gitleaks-alternatives-for-better-secrets-scanning-in-2026-p7zk3jtpj

[^128]: https://www.reddit.com/r/devops/comments/1rjziax/trivy_the_container_scanning_tool_security/

[^129]: https://semgrep.dev/events/semgrep-secure-2026-virtual-keynote

[^130]: https://mcpmarket.com/tools/skills/secret-scanning-with-gitleaks

[^131]: https://www.reddit.com/r/LocalLLaMA/comments/1th7f24/whats_your_current_local_llm_setup_in_2026/

[^132]: https://workhorizon.jp/posts/deepseek-r1-tsukaikata-2026-reasoning-model-local-api-o1-hikaku

[^133]: https://www.reddit.com/r/LocalLLaMA/comments/1prjldr/whats_the_realistic_entry_point_for_a_good_local/

[^134]: https://github.com/deepseek-ai/DeepSeek-R1

[^135]: https://huggingface.co/deepseek-ai/DeepSeek-R1

