---
title: My Agent Brain
version: 0.1
status: locked planning snapshot
date: 2026-05-31
owner: Markus Walker
primary_host: Lab
format_goal: human and machine readable
---

# My Agent Brain

## Purpose

My Agent Brain is a local-first AI project engine running on the Ubuntu LTS machine called Lab.

Its purpose is to turn a plain English project idea into a structured, isolated, build-ready project workspace. It should collect research, process data, build project memory, prepare the environment, hand off to the best AI build tool, verify the result, then support future plain English changes.

The system must stay general and reusable. It should support websites, SaaS products, dashboards, CRMs, full-stack applications, language-specific builds, LLM workflows, AI training experiments, security tools, research systems and future project types.

## Core principle

Shared brain, isolated projects.

Lab provides reusable orchestration, ingestion, retrieval, model hosting, build support, verification and audit tooling.

Each project gets its own isolated project capsule with its own files, memory, containers, dependencies, scripts, instructions, logs, artifacts and secrets.

Project context must not bleed between capsules.

## High level workflow

1. The user describes an idea in plain English.
2. Lab creates a new project capsule.
3. Research is collected manually and with LLM help using legitimate methods.
4. Raw files are stored first and kept traceable.
5. Deterministic extraction processes raw files before any AI interpretation.
6. Local inference attempts data preparation, tagging, summarisation and structure creation.
7. Postgres stores structured project memory.
8. pgvector or a vector store enables semantic search.
9. Lab generates a small context pack for the build agent.
10. The best build method is selected based on workload.
11. Build agents implement, test and verify the project.
12. The finished project is served or hosted.
13. The user can request changes in plain English.
14. A final security and readiness audit is run before public release or cloud deployment.

## Local-first model

Lab should attempt to do as much preprocessing and setup locally as possible before using paid or frontier AI.

Local work should include:

- research processing
- text extraction
- chunking
- tagging
- summarisation
- deduplication
- schema suggestions
- Postgres memory preparation
- vector memory preparation
- context pack generation
- environment setup
- first-pass project planning
- log summarisation
- simple build support

If the local model is too slow, inaccurate or weak for a specific task, only that task should escalate to Claude or Codex.

The system is local-first, not local-only.

## Escalation rule

Use the smallest capable AI method for the job.

| Workload | Preferred method |
|---|---|
| Routine preprocessing | Local model |
| Structured extraction | Deterministic tools first |
| Simple code edits | Codex CLI or Claude Code |
| Focused implementation | Codex CLI, Codex cloud or Claude Code |
| Complex build planning | Claude or Codex |
| Large coordinated build | Claude Code or Dynamic Workflows |
| Whole-codebase audit | Dynamic Workflows |
| Cross-checked research synthesis | Dynamic Workflows |
| Security and release readiness audit | Claude, Codex or Dynamic Workflows depending on scope |

Dynamic Workflows should be treated as an escalation mode, not the default mode.

## Project capsule model

Each project should have its own capsule.

Example layout:

```text
/projects/
  book-website/
  saas-dashboard/
  csaw-workbench/
  llm-training-experiment/
```

Each capsule should contain:

```text
raw/
processed/
memory/
db/
vector/
workspace/
scripts/
skills.md
agent-instructions/
containers/
logs/
artifacts/
outputs/
deploy/
secrets/
```

Each project should have its own Docker or container environment.

Each project should have its own project-specific instructions and tooling.

Each project should have separate memory boundaries.

## Database model

Postgres is the primary structured memory system.

pgvector can provide semantic vector search inside Postgres. A dedicated vector database can be added later if needed.

The database should be designed for fast, narrow recall. The AI should not read whole tables.

Core memory areas:

- projects
- sources
- source units
- chunks
- embeddings
- tags
- claims
- decisions
- tasks
- runs
- artifacts
- build errors
- security findings
- review queue

Every chunk should link back to a source.

Every claim should link back to supporting chunks.

AI-generated summaries and interpretations are derived data, not source truth.

## Retrieval rule

The AI should query memory through strict retrieval tools.

It should not browse raw tables.

Required retrieval behaviours:

- project-scoped queries
- source-linked results
- row limits
- cursor paging
- confidence values
- support references
- previous and next chunk lookup
- keyword search
- semantic search
- metadata filters
- no broad table dumps

Example retrieval tools:

```text
get_project_state
search_sources
search_chunks
get_chunk_context
find_claims
list_open_questions
get_build_errors
get_next_task
get_recent_runs
show_sources_for_claim
```

## Accuracy rule

Raw data must not be trusted to an LLM first.

Accuracy-first flow:

```text
Raw source
↓
Hash and archive
↓
Deterministic extraction
↓
Source-linked chunking
↓
Embedding
↓
Local AI enrichment
↓
Verification gate
↓
Curated memory
```

No unsourced claim becomes project memory.

Low-confidence extraction goes to review.

AI can propose meaning, but only source-linked data becomes trusted memory.

## Research collection rule

Research collection should use legitimate methods only.

Allowed examples:

- manual notes
- uploaded files
- PDFs
- text files
- screenshots
- videos
- API exports
- approved platform APIs
- agent browser control within allowed use
- repo clones where authorised
- service documentation
- user feedback sources collected within rules

Research should be stored raw before it is summarised.

## Build phase rule

The build agent should never start from a vague prompt.

It should start from a prepared context pack.

A build context pack should include:

- project brief
- success criteria
- constraints
- current project state
- relevant sources
- key decisions
- open questions
- proposed architecture
- environment details
- test plan
- retrieval guide
- next build task

## Verification rule

Every build phase should produce evidence.

Verification outputs should include:

- build logs
- test results
- lint results
- screenshots where relevant
- browser checks where relevant
- deployment notes
- known issues
- final status

The agent should not only say that work is complete. It should show evidence.

## Security and readiness rule

Before public release or live cloud deployment, run a readiness pass.

Checks should include:

- secret scanning
- dependency review
- authentication review
- authorisation review
- input validation review
- logging review
- Docker review
- environment variable review
- deployment review
- README and documentation review
- license and public repository review

## Cloud portability rule

Lab should be local-first, but not a dead-end local system.

Tooling should be selected so a project can move to AWS or other cloud infrastructure later.

Design rules:

- use containers
- use environment variables for config
- avoid hardcoded local paths
- keep data exportable
- use Postgres-compatible designs
- keep vector memory portable
- keep artifacts and logs structured
- keep secrets separate
- document runtime assumptions

## Simplicity rule

Do not build a swarm platform first.

Do not start with a large dashboard.

Do not add complex orchestration until the core loop works.

Version 1 should stay simple:

```text
Docker Compose
Postgres
pgvector
Ollama
Docling
MarkItDown
Playwright tooling
Codex CLI
Claude Code
Tailscale SSH
project capsules
retrieval tools
context pack generator
```

## First proof target

The first proof should demonstrate the full loop without becoming too large.

Recommended first proof:

```text
Plain English project idea
↓
Research folder
↓
Postgres memory
↓
Vector search
↓
Context pack
↓
Small app build
↓
Tests and screenshots
↓
Served locally
↓
Plain English change request
↓
Verified update
```

## Machine-readable plan

```yaml
system_name: My Agent Brain
version: 0.1
status: locked_planning_snapshot
host:
  name: Lab
  os: Ubuntu LTS
  role: local_first_ai_project_engine
architecture:
  pattern: shared_brain_isolated_project_capsules
  shared_brain:
    responsibilities:
      - create_project
      - ingest_research
      - extract_text
      - build_project_memory
      - run_local_inference
      - generate_context_pack
      - launch_build_agent
      - capture_logs
      - verify_outputs
      - prepare_release_audit
  project_capsule:
    isolation_required: true
    contains:
      - raw_research
      - processed_data
      - postgres_schema_or_database
      - vector_collection
      - workspace_files
      - project_containers
      - dependencies
      - scripts
      - skills_md
      - agent_instructions
      - logs
      - artifacts
      - secrets
      - deployment_config
workflow:
  - idea_intake
  - project_capsule_creation
  - research_collection
  - raw_archive
  - deterministic_extraction
  - local_llm_preprocessing
  - database_memory_build
  - vector_memory_build
  - context_pack_generation
  - build_agent_selection
  - build_and_test
  - serve_or_host
  - plain_english_iteration
  - security_and_release_audit
local_first:
  enabled: true
  default_worker: local_model
  fallback_workers:
    - Claude
    - Codex
  quality_gate:
    checks:
      - accuracy
      - speed
      - source_linking
      - schema_quality
      - format_consistency
      - hallucination_rate
    action_if_failed: escalate_specific_task_only
memory:
  structured_store: Postgres
  vector_store_default: pgvector
  vector_store_optional: dedicated_vector_db
  source_of_truth:
    - raw_sources
    - extracted_text
    - source_linked_chunks
  derived_data:
    - summaries
    - claims
    - tags
    - recommendations
retrieval:
  direct_table_access_for_agents: false
  tools_required: true
  requirements:
    - project_scope
    - row_limits
    - cursor_paging
    - source_links
    - confidence_values
    - metadata_filters
    - keyword_search
    - semantic_search
    - previous_next_chunk_lookup
build_phase:
  starts_from_context_pack: true
  vague_prompt_allowed: false
  agent_options:
    - local_model
    - Codex_CLI
    - Codex_cloud
    - Claude_Code
    - Claude_Dynamic_Workflows
dynamic_workflows:
  default: false
  use_for:
    - large_coordinated_builds
    - whole_codebase_audits
    - cross_checked_research
    - release_readiness_reviews
    - complex_parallel_verification
security_release_gate:
  required_before_public_release: true
  checks:
    - secrets
    - dependencies
    - authentication
    - authorisation
    - input_validation
    - logging
    - docker
    - environment_variables
    - deployment
    - documentation
cloud_portability:
  required: true
  rules:
    - containerised_services
    - env_based_config
    - no_hardcoded_local_paths
    - exportable_data
    - postgres_compatible
    - portable_vector_memory
    - separated_secrets
    - documented_runtime_assumptions
simplicity:
  start_small: true
  avoid_initial_complexity:
    - swarm_framework
    - large_dashboard
    - custom_orchestration_platform
    - unnecessary_agent_bus
```

## Decision summary

The approved design direction is:

```text
My Agent Brain
= local-first reusable AI project engine
+ isolated project capsules
+ Postgres structured memory
+ vector semantic search
+ local inference first
+ Claude or Codex escalation
+ Dynamic Workflows only when justified
+ verification and security gates before release
```
