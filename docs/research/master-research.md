# Master Document: ai_os

> [!abstract] Methodology
> This master document was produced with the RESYNTH five stage pipeline.
> Sources consolidated: S01 (Frontier AI Orchestration Toolkit: Systems, Skills, MCP Ecosystem, and Claude Fable 5 Workflows (2024–2026), unknown, authored unknown), S02 (Frontier AI Capability Engineering for Claude Fable 5 and Beyond, unknown, authored unknown), S03 (Frontier AI Orchestration: A Practical, Security-Audited Toolkit for Building Your Own Workflow, unknown, authored unknown), S04 (GitHub - anthropics/claude-agent-sdk-python, unknown, authored unknown), S05 (GitHub - anthropics/claude-agent-sdk-typescript, unknown, authored unknown), S06 (Model Context Protocol, unknown, authored unknown), S07 (Manage agent skills with GitHub CLI - GitHub Changelog, unknown, authored unknown), S08 (GitHub - OpenHands/OpenHands: 🙌 OpenHands: AI-Driven Development, unknown, authored unknown), S09 (GitHub - browser-use/browser-use: 🌐 Make websites accessible for AI agents. Automate tasks online with ease., unknown, authored unknown), S10 (GitHub - promptfoo/promptfoo: Test your prompts, agents, and RAGs. Red teaming/pentesting/vulnerability scanning for AI. Compare performance of GPT, Claude, Gemini, DeepSeek, and more. Simple declarative configs with command line and CI/CD integration. Used by OpenAI and Anthropic., unknown, authored unknown), S11 (GitHub - confident-ai/deepeval: The LLM Evaluation Framework, unknown, authored unknown), S12 (RAG Evaluation Using Ragas - Zilliz blog, unknown, authored unknown), S13 (Announcing Microsoft’s open automation framework to red team generative AI Systems | Microsoft Security Blog, unknown, authored unknown), S14 (LLM Guard | Secure Your LLM Applications, unknown, authored unknown), S15 (GitHub - Aider-AI/aider: aider is AI pair programming in your terminal, unknown, authored unknown), S16 (Cline - AI Coding, Open Source and Uncompromised, unknown, authored unknown), S17 (GitHub - browser-use/web-ui: 🖥️ Run AI Agent in your browser., unknown, authored unknown), S18 (Agent-MCP by rinadelph | Multi-Agent Dev Orchestration, unknown, authored unknown), S19 (Anthropic Releases Claude Fable 5 and Claude Mythos 5: Same Underlying Model, Different Safeguards, New Mythos-Class Tier, unknown, authored unknown), S20 (Open-Source AI Agent Stack in 2026, unknown, authored unknown), S21 (AI Agent Frameworks (2026 Update): 8 SDKs Compared + the Claude Agent SDK Primitive Reference, unknown, authored unknown), S22 (Introducing the Model Context Protocol, unknown, authored unknown), S23 (Agent Skills Guide 2026: Build, Share & Secure, unknown, authored unknown), S24 (Anthropic’s Claude Fable 5, Mythos 5: What you need to know | Constellation Research, unknown, authored unknown), S25 (Claude Fable, unknown, authored unknown), S26 (Anthropic releases Claude Fable, a version of Mythos, days after warning AI is becoming too dangerous, unknown, authored unknown), S27 (Claude Fable 5: Mythos-Class AI Guide | Lushbinary, unknown, authored unknown), S28 (Use Agent Skills in VS Code, unknown, authored unknown), S29 (GitHub - heilcheng/awesome-agent-skills: Tutorials, Guides and Agent Skills Directories, unknown, authored unknown), S30 (How to write a great agents.md: Lessons from over 2,500 repositories, unknown, authored unknown), S31 (A Complete Guide To AGENTS.md, unknown, authored unknown), S32 (Model Context Protocol Changes AI Integration, unknown, authored unknown), S33 (OpenHands | The Open Platform for Cloud Coding Agents, unknown, authored unknown), S34 (Windsurf Review: Agentic AI IDE Redefining Developer Productivity, unknown, authored unknown), S35 (Open-Source Coding Agents: A Survey, unknown, authored unknown), S36 (G-Eval | DeepEval - The LLM Evaluation Framework, unknown, authored unknown), S37 (Garak: Open-source LLM vulnerability scanner - Help Net Security, unknown, authored unknown), S38 (NeMo Guardrails 2026: NVIDIA's LLM Safety Toolkit, unknown, authored unknown), S39 (What is an AI Agent?, unknown, authored unknown), S40 (A developer's guide to prompt engineering and LLMs, unknown, authored unknown), S41 (A practical guide to the Python Claude Code SDK (now agent SDK) in 2025, unknown, authored unknown), S42 (Introducing advanced tool use on the Claude Developer Platform, unknown, authored unknown), S43 (Claude Agent SDK with LiteLLM | liteLLM, unknown, authored unknown), S44 (Claude MCP Tools Server | Awesome MCP Servers, unknown, authored unknown), S45 (GitHub - softaworks/agent-toolkit: A curated collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities across development, documentation, planning, and professional workflows., unknown, authored unknown), S46 (The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents, unknown, authored unknown), S47 (OpenHands CodeAct 2.1: An Open, State-of-the-Art Software Development Agent, unknown, authored unknown), S48 (Build Secure AI Applications | Promptfoo, unknown, authored unknown), S49 (CI/CD Integration for LLM Eval and Security | Promptfoo, unknown, authored unknown), S50 (Ragas: Automated Evaluation of Retrieval Augmented Generation, unknown, authored unknown), S51 (Claude Fable 5 and Claude Mythos 5, unknown, authored unknown), S52 (Claude Fable 5: What It Is and What It Means for Developers, unknown, authored unknown), S53 (10 Killer AI Agent Skills That Are Dominating GitHub Now, unknown, authored unknown), S54 (Claude AI + Cursor IDE: The Fastest Way to Build Apps, unknown, authored unknown), S55 (Aider Review: A Developer's Month With This Terminal-Based Code Assistant [2025] | Blott, unknown, authored unknown), S56 (9 Best Promptfoo Alternatives: Which Frameworks are Better to Ship AI Agents - ZenML Blog, unknown, authored unknown), S57 (Comparison with Claude Agent SDK - Docs by LangChain, unknown, authored unknown), S58 (agents/docs/agent-skills.md at main · wshobson/agents, unknown, authored unknown), S59 (Run Claude Code as an MCP Server (Control It with GPT-5), unknown, authored unknown), S60 (Best Promptfoo alternatives in 2026: Open-source tools and SaaS - Articles - Braintrust, unknown, authored unknown), S61 (Builder | Agent skills, unknown, authored unknown), S62 (Introduction to Model Context Protocol, unknown, authored unknown), S63 (Copilot coding agent is now generally available! 🚀 · community · Discussion #159068, unknown, authored unknown), S64 (GitHub - openai/evals: Evals is a framework for evaluating LLMs and LLM systems, and an open-source registry of benchmarks., unknown, authored unknown), S65 (Best Agents SDK in 2026, unknown, authored unknown), S66 (GitHub - microsoft/playwright: Playwright is a framework for Web Testing and Automation. It allows testing Chromium, Firefox and WebKit with a single API., unknown, authored unknown).
> Merge rules applied: newer_beats_older, primary_beats_secondary, explicit_beats_implied, conflicts_are_logged_not_resolved.
> Every paragraph carries provenance markers naming the claims it rests on.
> The full decision record lives in index/reconciliation.jsonl.

## A2a

The protocol layer consolidated in 2026: ACP merged into A2A under the Linux Foundation, and MCP crossed 200 server implementations. [S21-C005]

## Aaif

The Linux Foundation announced the Agentic AI Foundation (AAIF) on 9 December 2025 with Anthropic, OpenAI and Block as founding members, contributing MCP, AGENTS.md and Goose, reaching 146 member organisations by February 2026. [S03-C008]

## Accessibility

Developers can build with LLMs without a machine-learning PhD, using basic HTTP requests and natural-language prompts. [S40-C002]

## Acquisition

promptfoo agreed to be acquired by OpenAI on 9 March 2026 to be integrated into OpenAI Frontier, reportedly remaining open source, with over 350k developers having used it and 130k active each month. [S03-C010]

## Activation

Each skill provides Claude deep domain expertise without loading everything into context upfront, including YAML frontmatter (name and activation criteria), progressive disclosure (metadata to instructions to resources), and clear 'Use when' activation triggers for automatic invocation. [S58-C002]

## Administration

Copilot Business or Copilot Enterprise subscribers require an administrator to enable the Copilot coding agent from the Policies page before it can be used. [S63-C004]

## Adoption

LLM Guard has been downloaded over 2.5 million times and is a permissively licensed open-source project, with a commercial version within the Protect AI platform coming soon. Early MCP adopters included Block and Apollo, while development tools companies Zed, Replit, Codeium, and Sourcegraph worked with MCP to enhance their platforms. The SKILL.md format originated at Anthropic, was released as an open standard, and has been adopted by OpenAI (Codex CLI), Microsoft (GitHub Copilot), and the broader ecosystem. [S14-C004] [S22-C004] [S23-C003]

## Advanced Tool Use

On Nov 24, 2025, Anthropic released three beta advanced tool use features: the Tool Search Tool, Programmatic Tool Calling, and Tool Use Examples, that let Claude discover, learn, and execute tools dynamically. [S42-C001]

## Agent Frameworks

The Claude Agent SDK (Python and TypeScript) is ranked the top system for building agents with Claude Code capabilities (file ops, shell, MCP tools) and is ideal for orchestrating Fable 5 as planner with sub-agents. Claude Code plus the Agent SDK is ranked the top system as the official Anthropic path for Claude-style agent workflows, with the same tools and context management that power Claude Code. Recommended OSS agent frameworks include LangGraph, CrewAI, AutoGen, OpenAI Agents SDK, Microsoft Agent Framework, Mastra, and Pydantic AI. Microsoft Agent Framework 1.0 went GA on April 3, 2026, merging AutoGen and Semantic Kernel into one .NET and Python SDK with MCP and A2A support. [S01-C009] [S02-C008] [S20-C005] [S21-C001]

The agent framework landscape splits into provider-native SDKs (Claude, OpenAI, Google) optimized for one model family and independent frameworks (LangGraph, CrewAI, Smolagents, Pydantic AI, AutoGen) that work across providers, with the right choice depending on whether you prioritize integration depth or model flexibility. [S21-C003]

## Agent Hosts

Supported agent hosts for gh skill install include GitHub Copilot, Claude Code, Cursor, Codex, Gemini CLI, and Antigravity, each selected via an --agent flag. [S07-C006]

## Agent Mcp

Agent-MCP (by rinadelph) is a Multi-Agent Collaboration Protocol framework that provides an MCP server exposing multi-agent orchestration (agent lifecycle, task assignment, shared knowledge graph/RAG, messaging) plus an optional real-time web dashboard. Agent-MCP uses a shared SQLite backend to store embeddings, task metadata, architectural decisions, and coding patterns as queryable records outside model context windows, letting agents query external state rather than maintaining full conversation history. Agent-MCP is licensed under GNU AGPL-3.0 and has been on a maintenance pause since September 2025, posing risks of legal compliance (network-deployment disclosure), unpatched vulnerabilities, and no official support. [S18-C001] [S18-C002] [S18-C003]

## Agent Sdks

The article compares the three most-used provider agent SDKs in 2026, the Claude Agent SDK, OpenAI Agents SDK, and Google ADK, by actually building with each rather than relying on specs. The author found the SDKs all promise minimal code but behave very differently once you go beyond demos, evaluating them on time-to-working, control under complexity, and handling of real-world workflows like multi-agent coordination, tool usage, and state management. [S65-C001] [S65-C002]

## Agent Skills

SKILL.md-based agent skills have become a multi-platform standard across Claude, Copilot, Cursor, Codex, and Gemini CLI, packaging reusable capabilities and activation criteria in portable folders. Anthropic published Agent Skills as an open standard on 18 December 2025; a skill is a folder with a SKILL.md (YAML frontmatter plus markdown body) and optional scripts, references, and assets directories. By March 2026, 32 tools from competing companies (including Gemini CLI, JetBrains Junie, AWS Kiro and Block Goose) read the same SKILL.md files, with a package manager (npx skills) and registry (skills.sh), described as the npm moment for agent context. GitHub launched gh skill, a GitHub CLI command to discover, install, manage, and publish agent skills from GitHub repositories, in public preview. [S01-C005] [S03-C006] [S03-C007] [S07-C001]

Agent skills are portable sets of instructions, scripts, and resources following the open Agent Skills specification (agentskills.io) that work across multiple agent hosts including GitHub Copilot, Claude Code, Cursor, Codex, and Gemini CLI. An Agent Skill is a folder containing a SKILL.md file plus optional scripts, reference materials, and examples, which the agent loads on demand when a task matches the skill's description, with no compilation, runtime, or dependency graph. Skills are described as the npm of AI agents: where npm packages give applications reusable code, skills give an AI agent reusable knowledge by exporting procedures, constraints, and domain expertise. As of March 2026, over 490,000 skills exist across three major marketplaces (SkillsMP, Skills.sh, ClawHub), with the trajectory from interesting idea to standard infrastructure taking less than six months. [S07-C002] [S23-C001] [S23-C002] [S23-C004]

Agent Skills are folders of instructions, scripts, and resources that GitHub Copilot loads when relevant, following an open standard (agentskills.io) that works across GitHub Copilot in VS Code, Copilot CLI, and Copilot cloud agent. Agent Skills differ from custom instructions: skills teach specialized capabilities/workflows, are portable across tools, can include scripts and resources, and load on-demand, whereas custom instructions define coding standards, are VS Code/GitHub-specific, are instructions-only, and are always applied. In VS Code, project skills are stored in .github/skills/, .claude/skills/, or .agents/skills/, and personal skills in ~/.copilot/skills/, ~/.claude/skills/, or ~/.agents/skills/. Creating a skill in VS Code involves making a directory with a SKILL.md file, filling in YAML frontmatter (name and description) plus body instructions, and optionally adding scripts, examples, or other resources. [S28-C001] [S28-C002] [S28-C003] [S28-C004]

Agent Skills are simple SKILL.md text files that teach an AI how to do specific tasks; they are instructions, not code, that the AI reads like a human reads a guide and then follows. Skills load in three stages: Browse (the AI sees a list of skill names and short descriptions), Load (it reads the full instructions when a skill is needed), and Use (it follows the instructions and accesses helper files). Skills are faster and lighter because the AI only loads what it needs when it needs it, work everywhere across compatible AI tools, and are easy to share as plain files on GitHub. Recommended ways to find skills include the SkillsMP Marketplace (which indexes Skill projects on GitHub by category, update time, and star count), Vercel's skills.sh leaderboard, and the npx skills CLI tool. [S29-C001] [S29-C002] [S29-C003] [S29-C004]

softaworks/agent-toolkit is a curated collection of skills for AI coding agents, packaging instructions and scripts that extend agent capabilities across development, documentation, planning, and professional workflows. AI agent Skills are reusable capability packages (complete folder structures of instructions, scripts, and resources) that teach an AI agent to perform specialized work consistently and autonomously without constant instruction. Skills follow an open standard (opened by Anthropic in December 2025) that works across OpenClaw, Claude.ai and Claude Code, Cursor, VS Code, GitHub Copilot, and OpenAI Codex, enabling build-once deploy-everywhere with no vendor lock-in. AI agents read skill metadata at startup (about ~100 tokens per skill) and load full instructions on-demand when a prompt matches a skill's description, a progressive-disclosure approach that keeps context windows efficient. [S45-C001] [S53-C001] [S53-C002] [S53-C003]

Best practice for skill descriptions is to use third-person voice ('Use this skill when...'), include specific trigger keywords, and keep them under 2-3 sentences, since descriptions get injected into system prompts where first-person perspective is inappropriate. In the wshobson/agents repository, Agent Skills are modular packages that extend Claude's capabilities with specialized domain knowledge following Anthropic's Agent Skills Specification, comprising 156 local specialized skills across 41 plugins. The skill collection is organized by plugin across domains such as Kubernetes Operations, LLM Application Development, Blockchain & Web3, CI/CD Automation, and Cloud Infrastructure, each grouping multiple specialized skills. In Builder, skills are specialized knowledge and workflows that a user or the AI agent can invoke during code generation sessions, with each skill defining specialized instructions for a domain such as processing PDFs, analyzing data, or reviewing code. [S53-C004] [S58-C001] [S58-C003] [S61-C001]

Builder recommends using skills for recurring tasks that benefit from consistent, specialized behavior so the AI agent follows preferred patterns every time. Builder discovers skills from .builder/skills/ (primary location) and .claude/skills/ (alternative). [S61-C002] [S61-C004]

## Agent Stack

The 2026 open-source AI agent stack is a six-layer reference architecture: model serving, the model, agent framework, retrieval and memory, tooling and integration, and trace and evaluation. The trace and evaluation layer is the layer most 2025-era stacks miss and is considered non-optional in 2026, with FutureAGI traceAI and ai-evaluation (both Apache 2.0) recommended regardless of framework. [S20-C001] [S20-C002]

## Agent Toolkit

The agent-toolkit installation method works with multiple AI coding agents including Claude Code, Codex, Cursor, and AdaL, and can be registered as a Claude Code plugin marketplace via /plugin marketplace add softaworks/agent-toolkit. Each skill, agent, and command in agent-toolkit is an individual plugin installable separately (e.g., /plugin install codex@agent-toolkit), with agents installed as agent-<name>@agent-toolkit and commands as command-<name>@agent-toolkit. agent-toolkit skills can be installed manually for Claude Code by copying a skill directory into ~/.claude/skills/, or for claude.ai by adding skills to project knowledge or pasting SKILL.md contents into the conversation. [S45-C002] [S45-C003] [S45-C004]

## Agentic

Fable 5 is the model powering Claude Code's strongest agentic results and represents a qualitative shift for agentic workloads, with its lead over previous models growing the longer and more complex the task. [S52-C004]

## Agentic Ide

Windsurf is an AI-native agentic IDE built around the VS Code ecosystem but redesigned to center AI workflows through Cascade, Supercomplete, and terminal integration, functioning as a standalone development environment rather than a plugin. [S34-C001]

## Agentic Metrics

DeepEval provides agentic metrics including Task Completion, Tool Correctness, Goal Accuracy, Step Efficiency, Plan Adherence, and Plan Quality for evaluating agents. [S11-C003]

## Agentic Workflows

Cascade is Windsurf's central agentic engine combining full-repo awareness, real-time editor awareness, and access to terminals, previews, and web search, using iterative plan-and-diff flows where the AI proposes a plan and shows diffs before the developer approves edits. [S34-C003]

## Agents

The Claude Agent SDK enables developers to programmatically build AI agents with Claude Code's capabilities, creating autonomous agents that understand codebases, edit files, run commands, and execute complex workflows. Browser Use makes websites accessible for AI agents, automating online tasks by giving the model a real browser/computer action space with persistent tools and recovery loops. In an agent harness like Claude Code or Claude Managed Agents, Claude Fable 5 can work for days at a time, planning across stages, delegating to sub-agents, and checking its own work. The Claude Agent SDK (available in Python and TypeScript) gives Claude access to a local computer, letting an agent read and write files, search a codebase, and run terminal commands to gather its own context and take action rather than just emitting text. [S05-C001] [S09-C001] [S25-C003] [S41-C002]

CodeAct is a single agent that solves a wide variety of tasks by executing Python and bash commands, powered by a language model base. [S47-C002]

## Agents Md

Building the workflow around model-neutral skills, AGENTS.md/CLAUDE.md instruction files, MCP tools and an eval-and-safety gate lets any new frontier model drop in with a one-line change. GitHub Copilot introduced custom agents defined in agents.md files, where each file acts as an agent persona (defined with frontmatter and custom instructions) enabling a team of specialists such as a @docs-agent, @test-agent, and @security-agent. Most agent files fail because they are too vague; a specific persona with exact commands, well-defined boundaries, and clear examples of good output works far better than a generic 'helpful coding assistant'. Analysis of over 2,500 agents.md files found successful ones put executable commands early, favour real code examples over explanations, set clear boundaries on what not to touch, are specific about the stack with versions, and cover six core areas. [S03-C002] [S30-C001] [S30-C002] [S30-C003]

The six core areas a great agents.md should cover are commands, testing, project structure, code style, git workflow, and boundaries. The most common helpful constraint found in successful agents.md files was 'Never commit secrets'. An AGENTS.md file is a markdown file checked into Git that customizes how AI coding agents behave in a repository, sitting at the top of the conversation history right below the system prompt as a configuration layer between the agent's base instructions and the codebase. AGENTS.md is an open standard supported by many but not all tools; notably Claude Code uses CLAUDE.md instead, and a symlink can be created between them to keep tools consistent. [S30-C004] [S30-C005] [S31-C001] [S31-C002]

Massive AGENTS.md files become an unmaintainable 'ball of mud' through a feedback loop of repeatedly adding rules, and auto-generating AGENTS.md via init scripts is discouraged because it floods the file with broadly-useful content better left progressively disclosed. Per the 'instruction budget' concept, frontier thinking LLMs can follow roughly 150-200 instructions with reasonable consistency, with smaller and non-thinking models attending to fewer, and every token in AGENTS.md loads on every request. [S31-C003] [S31-C004]

## Ai Agents

AI agents are software systems designed to work with minimal human intervention by sensing a changing environment they also affect, thinking about it, acting autonomously on their best decision, and running in a loop with memory of what they have seen and done. AI agents have existed for decades, but LLMs have recently removed a major barrier by making sophisticated reasoning available via an API call instead of requiring custom algorithms and models trained from scratch. AI agents address four problems humans cannot handle at scale: fragmented systems, endless repetitive decisions, exponential complexity with more variables than humans can track, and real-time adaptation between events. Since around 2020 LLMs have enabled building agents without hardcoding every rule or curating narrow training data, marking an evolution from brittle rulebooks to fluid reasoners. [S39-C001] [S39-C002] [S39-C003] [S39-C004]

## Ai Capability Engineering

The report recommends 'AI Capability Engineering' as the umbrella term for the field, with 'Frontier AI Orchestration' and 'Context Engineering' as subordinate sub-disciplines. The best umbrella term for the discipline is Frontier AI Capability Engineering, broader than context engineering and more durable than agentic workflow engineering or model orchestration. [S01-C007] [S02-C006]

## Ai Orchestration

Frontier AI usage in 2026 is defined more by how well teams orchestrate models, tools, and evaluations than by which single model they pick. The recommended architecture is model-neutral orchestration in which a frontier model like Fable 5 acts as planner/architect/judge while cheaper models and specialised agents handle scanning, code edits, browser automation, and bulk processing. The strongest current pattern is a layered system where the frontier model does planning, review, synthesis, and hard judgement while cheaper or specialised components handle scanning, coding, testing, browser interaction, document lookup, and log reduction. Layering work this way preserves expensive frontier tokens for high-value reasoning while keeping the whole workflow inspectable and auditable. [S01-C001] [S01-C008] [S02-C001] [S02-C002]

The strongest pattern today is to use the frontier model (Claude Fable 5) as orchestrator, architect, synthesiser and final judge while delegating token-heavy scanning, coding, testing and log reduction to cheaper agents. [S03-C001]

## Aider

Aider is AI pair programming in the terminal that maps the entire codebase to work well in larger projects and supports 100+ programming languages including python, javascript, rust, ruby, go, cpp, php, html, and css. Aider automatically commits changes with sensible commit messages, letting users diff, manage, and undo AI changes with familiar git tools. Aider can automatically lint and test code each time it makes changes and fix problems detected by linters and test suites. Aider is model-agnostic and can connect to many LLMs, including DeepSeek, Anthropic Claude (sonnet), and OpenAI (o3-mini), with the model and API key specified at launch. [S15-C001] [S15-C002] [S15-C003] [S15-C004]

In a month-long review, the author reports Aider, a terminal-based open-source code assistant, deserves its buzz, citing that developers using it have quadrupled their coding productivity. Aider works with nine popular programming languages including Python, JavaScript, and Rust, processes files for just $0.007 each, handles automatic code testing and voice-commanded feature requests, and integrates with Git for version control. The reviewer tested Aider extensively with Claude 3.7 Sonnet and GPT-4o on complex projects and daily coding tasks. Aider is installed via pip (recommended within a dedicated virtual environment) using either aider-chat or the aider-install helper, and supports Python 3.8-3.13. [S55-C001] [S55-C002] [S55-C003] [S55-C004]

## Alignment

In an automated alignment assessment, Mythos 5's level of misaligned behavior was low and similar to Opus 4.8, and since Fable 5 is the same underlying model its alignment is expected to be similar. [S51-C005]

## Alternatives

The article compares 9 leading Promptfoo alternatives ranging from dedicated evaluation frameworks like DeepEval and RAGAS to full-stack MLOps platforms like ZenML and LangSmith. [S56-C003]

## Analogy

MCP is analogized to internet standards (HTML, DNS, JSON, HTTP) that standardized plumbing to connect disparate data and applications, providing a common protocol for AI model-tool integration. [S32-C002]

## Anthropic

Anthropic open-sourced the Model Context Protocol (MCP) as a new standard for connecting AI assistants to systems where data lives, including content repositories, business tools, and development environments. MCP was created at Anthropic by David Soria Parra and Justin Spahr-Summers and is committed to as a collaborative open-source project and ecosystem. Anthropic confidentially filed its IPO prospectus days before the Fable 5 launch, after reporting a revenue run rate of roughly $47 billion and closing a funding round at a $965 billion valuation. The 'Introduction to Model Context Protocol' course is hosted on Skilljar, a learning management system Anthropic uses to deliver interactive course materials and track progress. [S22-C001] [S22-C005] [S27-C004] [S62-C001]

## Api

The query() function is an async function for querying Claude Code that returns an AsyncIterator of response messages. [S04-C002]

## Application Design

Any application that uses an LLM is effectively mapping between two domains, the user domain and the document domain, and the key engineering task is converting from user domain into document domain (e.g., by establishing what type of document the context represents). [S40-C004]

## Architecture

The recommended buildable stack starts with a model router, a local coding agent, repo-resident instruction packs, a browser tool, an eval harness, and a security gate, adding cloud agents and remote MCP servers only after every permission boundary can be audited. Browser Use 0.13 introduces a beta agent powered by a Rust core and a browser harness built for current frontier models, with the flow Python API -> Rust core -> Browser harness -> Web task done. MCP provides a universal, open standard for secure two-way connections between data sources and AI tools, replacing fragmented per-source custom integrations with a single protocol, where developers expose data via MCP servers or build AI applications as MCP clients. MCP uses a client-server architecture where MCP Hosts (such as Claude Desktop) contain MCP Clients maintaining 1-to-1 connections to MCP Servers, and the servers respond to client requests with context, tools, and prompts. [S02-C007] [S09-C002] [S22-C002] [S32-C003]

The OpenHands Software Agent SDK is a toolkit for building production software development agents that is a complete architectural redesign of the agent components of the OpenHands framework, which has 64k+ GitHub stars. OpenHands V1 is grounded in four design principles: optional isolation (local by default, sandboxable), stateless-by-default with one source of truth for state, strict separation of the agent core from applications, and two-layer composability. [S46-C001] [S46-C003]

## Archived

The Claude MCP Tools repository has been archived as of 2026-02-14, with its functionality superseded by OpenClaw's native skill ecosystem, Desktop Commander, and community MCP connectors after 14 MCP servers were evaluated as offering no unique value beyond existing tooling. [S44-C003]

## Attacks

Promptfoo creates thousands of context-aware attacks tailored to an application, drawing on real-time threat intel from a 300k+ user community and deep automation that scales beyond human-curated tests. [S48-C002]

## Auto Wait

Playwright key capabilities include auto-wait and web-first assertions that retry until conditions are met (no artificial timeouts), resilient locators that mirror how users see the page (getByRole, getByLabel, getByPlaceholder, getByTestId), and reusable saved authentication state. [S66-C004]

## Automation

PyRIT augments rather than replaces manual red teaming: in one Copilot exercise the team generated several thousand malicious prompts and scored the outputs in hours rather than weeks, with the security professional remaining in control of strategy and execution. Microsoft notes automation is needed for scaling red teaming but is not a replacement for manual probing, which is often needed to identify blind spots. OpenHands targets automating the outer loop of software development: speeding code reviews, expanding test coverage, automating docs and release notes, refactoring legacy code, and eliminating security debt across large multi-repo changes. Key capabilities of the Claude MCP Tools ecosystem include hybrid AI development across Claude Desktop and Claude Code, multi-provider AI routing with cost optimization, persistent memory with entity-relation graphs, desktop GUI automation, and development workflow enhancements like security scanning. [S13-C003] [S13-C004] [S33-C004] [S44-C002]

## Autonomy

A key design choice when building a domain-specific coding tool is whether to use an interactive assistant that keeps a human in the loop or a more autonomous agent that drives the toolchain itself. [S35-C003]

## Availability

Fable 5 is distributed on AWS Bedrock, Google Cloud, and Microsoft Azure, is available on Cursor, and will be the lead model on Claude Code. Using Fable requires 30-day data retention for safety monitoring, and as of June 12, 2026 Anthropic reported Claude Fable 5 access was unavailable. As of June 12, 2026, Anthropic suspended access to both Claude Fable 5 and Claude Mythos 5, apologizing and working to restore access. [S24-C005] [S25-C005] [S51-C006]

## Benchmark

During early access Stripe reported Fable 5 performed a codebase-wide migration in a 50-million-line Ruby codebase in one day, work a team would have needed over two months to do by hand. In third-party testing, analytics company Hex said Fable was the first model to score 90% on its core analytics benchmark of complex, long-running analytical tasks. Claude Fable 5, released June 9, 2026, scores more than 10% higher than Opus 4.8 on some benchmarks but costs double at $10/$50 per million tokens, blocks high-risk queries with a fallback to Opus 4.8, and requires 30-day data retention. The OpenHands Software Agent SDK achieves strong, state-of-the-art results on the SWE-Bench Verified and GAIA benchmarks across multiple LLM backends, and is fully open-sourced under the MIT License. [S19-C004] [S26-C005] [S27-C001] [S46-C005]

OpenHands CodeAct 2.1 (powered by the new Claude Sonnet 3.5) achieved a 53% resolve rate on SWE-Bench Verified and 41.7% on SWE-Bench Lite, which OpenHands presented as the strongest open-source AI software developer to date. SWE-Bench is a benchmark of issues and corresponding pull requests from 12 popular Python GitHub repositories, used as a gold-standard for measuring AI software developers by tasking models with generating code patches to resolve specified issues. [S47-C001] [S47-C004]

## Benchmarks

DeepEval supports both end-to-end and component-level evaluation, custom metrics, synthetic dataset generation, and benchmarking any LLM on popular benchmarks (MMLU, HellaSwag, DROP, BIG-Bench Hard, TruthfulQA, HumanEval, GSM8K) in under 10 lines of code. Anthropic launched Claude Fable 5 as a Mythos-class model made safe for general use, stating its capabilities exceed any model Anthropic has previously made generally available and that it is state-of-the-art on nearly all tested benchmarks. OpenAI Evals is a framework for evaluating LLMs and LLM systems and an open-source registry of benchmarks, installable via pip install evals. [S11-C004] [S51-C001] [S64-C001]

## Best Practices

Context engineering is becoming more important than raw context size: best systems use selective loading, repo maps, doc fetchers, progressive-disclosure skills, packers like Repomix, and live documentation tools rather than dumping everything into the prompt. Best practice for managing multiple MCP servers is to isolate each instance with dedicated ports to prevent transport collisions, use unified authentication tokens post-v1.3.0, and verify transport compatibility since Python SSE and Node.js HTTP/JSON-RPC transports are not interchangeable. [S02-C005] [S18-C004]

## Billing

Starting June 15, 2026, Claude Agent SDK usage and non-interactive claude -p runs on subscription plans draw from a separate monthly Agent SDK credit ($20 on Pro, $100 on Max 5x, $200 on Max 20x) that does not roll over, after which usage flows to standard API rates or stops. [S21-C002]

## Braintrust

Braintrust is presented as the best Promptfoo alternative for teams that have moved past local testing and need to measure AI agents in production, offering detailed per-step traces, evaluations against live traffic that plug into CI/CD, and a shared PM/engineer collaboration interface. [S60-C001]

## Browser Automation

Playwright is a framework for web testing and automation that allows testing Chromium, Firefox, and WebKit with a single API. [S66-C001]

## Browser Use

Browser Use is model-agnostic, supporting its own optimized model (bu-2-0), OpenAI (ChatOpenAI), and Anthropic Claude (ChatAnthropic, e.g. claude-opus-4-8) as the agent LLM. Browser Use is installed with the native core runtime via uv add 'browser-use[core]' and requires Python 3.11 or later. Browser Use offers both a self-hostable open-source agent (for custom tools and code-level integration) and a recommended fully-hosted cloud agent with stealth, proxy rotation, captcha solving, 1000+ integrations, and persistent filesystem and memory. Browser Use web-ui builds on the browser-use project and provides a Gradio-based web UI to run an AI browser agent interactively, supporting most browser-use functionality. [S09-C003] [S09-C004] [S09-C005] [S17-C001]

Browser Use web-ui integrates support for various LLMs including Google, OpenAI, Azure OpenAI, Anthropic, DeepSeek, and Ollama. Browser Use web-ui supports using your own browser (avoiding re-login/authentication issues), HD screen recording, and persistent browser sessions that keep the window open between AI tasks. Browser Use web-ui is run locally by cloning the repo, installing dependencies with uv (Python 3.11) and Playwright browsers, and launching python webui.py to access the UI at http://127.0.0.1:7788. [S17-C002] [S17-C003] [S17-C004]

## Builder

A Builder skill is created by making a skill directory (whose name reflects the skill, e.g. .builder/skills/pdf-processor/) containing a SKILL.md file with YAML frontmatter (name and description) plus instructions. [S61-C003]

## Built In

The SDK ships built-in tools familiar to developers: Read/Write for file operations, Bash for shell commands, Grep/Glob for searching and finding files, and WebFetch/WebSearch for internet access. [S41-C003]

## Capabilities

The Copilot coding agent can implement new features, fix bugs, address technical debt, improve test coverage, and update documentation, with tasks handed off by assigning an issue, using the agents panel, or the Delegate to coding agent button in VS Code. [S63-C003]

## Ci Cd

promptfoo can test prompts and models with automated evaluations, secure LLM apps via red teaming and vulnerability scanning, compare models side-by-side (OpenAI, Anthropic, Azure, Bedrock, Ollama), automate checks in CI/CD, and review pull requests for LLM security issues via code scanning. DeepEval integrates with any LLM framework including OpenAI Agents, LangChain, LangGraph, Pydantic AI, CrewAI, Anthropic (Claude), AWS AgentCore, and LlamaIndex, and integrates with any CI/CD environment. Promptfoo builds AI security testing into the development workflow across a connect-attack-fix loop, integrating with CI/CD pipelines, GitHub, GitLab, Jenkins, MCP and agent frameworks, on-premise or cloud. Integrating promptfoo into CI/CD pipelines lets teams automatically evaluate prompts, test for security vulnerabilities, and enforce quality before deployment. [S10-C003] [S11-C005] [S48-C001] [S49-C001]

CI/CD for LLM apps catches regressions early, performs automated red teaming and vulnerability detection, enforces quality gates with minimum performance thresholds, generates compliance reports for OWASP/NIST, and tracks token usage and costs. Prerequisites for promptfoo CI/CD include Node.js ^20.20.0 or >=22.22.0, LLM provider API keys stored as secure environment variables, and a promptfooconfig.yaml configuration file. [S49-C002] [S49-C004]

## Claude

In Anthropic's June 2026 capability hierarchy, Fable 5 and Mythos 5 sit above Opus 4.8, which sits above Sonnet 4.6, which sits above Haiku. The video 'Claude AI + Cursor IDE: The Fastest Way to Build Apps' (by The Codeholic) presents combining Claude AI with the Cursor IDE as a fast way to build applications. [S52-C002] [S54-C001]

## Claude Agent Sdk

The Claude Agent SDK for Python is installed via pip install claude-agent-sdk and requires Python 3.10+, automatically bundling the Claude Code CLI so no separate installation is required. By default Claude has access to the full Claude Code toolset (Read, Write, Edit, Bash, and others); allowed_tools is a permission allowlist that auto-approves listed tools rather than removing tools, and disallowed_tools blocks specific tools. ClaudeSDKClient supports bidirectional, interactive conversations and additionally enables custom tools and hooks defined as Python functions, which query() does not. Custom tools are implemented as in-process MCP servers that run directly within the Python application, eliminating the separate processes that regular MCP servers require. [S04-C001] [S04-C003] [S04-C004] [S04-C005]

In-process SDK MCP servers offer benefits over external MCP servers including no subprocess management, no IPC overhead, simpler single-process deployment, easier debugging, and type safety via direct Python function calls. The TypeScript Claude Agent SDK is installed via npm install @anthropic-ai/claude-agent-sdk. The Claude Code SDK has been renamed to the Claude Agent SDK, with a migration guide covering breaking changes. Anthropic states it has implemented privacy safeguards for the SDK including limited retention periods for sensitive information, restricted access to user session data, and policies against using feedback for model training. [S04-C006] [S05-C002] [S05-C003] [S05-C004]

The Claude Agent SDK has the deepest MCP integration of any framework (200+ servers, single-line config), built-in file system and shell access, extended thinking, and a hooks system for lifecycle control, centering its architecture on hooks and subagents. The original claude-code-sdk PyPI package is deprecated and has been replaced by claude-agent-sdk, after Anthropic realized the coding tools could be used for far more than coding. The SDK supports the Model Context Protocol, letting developers turn their own Python functions into new tools for Claude, such as a custom lookup_order(order_id) tool hooked into a store's API. Pointing Anthropic's Claude Agent SDK to a LiteLLM Proxy lets the same agent code use any LLM provider including OpenAI, Bedrock, Azure, and Vertex AI. [S21-C004] [S41-C001] [S41-C004] [S43-C001]

To use the Claude Agent SDK with LiteLLM, set ANTHROPIC_BASE_URL to the LiteLLM proxy (e.g. http://localhost:4000) and ANTHROPIC_API_KEY to your LiteLLM key, then specify any model from the LiteLLM config in ClaudeAgentOptions. LangChain's Deep Agents can run inside a sandbox or outside one executing commands remotely, with a pluggable execution backend (local, virtual filesystem, remote sandbox, or custom), whereas the Claude Agent SDK runs the agent inside a sandbox on its local filesystem. Deep Agents support any model provider (Anthropic, OpenAI, Google, 100+ others), while the Claude Agent SDK is limited to Claude (via Anthropic, Bedrock, Vertex, Azure). Deep Agents offer built-in multi-tenancy (scoped threads, per-user sandboxes, RBAC) and managed or self-hosted deployment via LangSmith, whereas with the Claude Agent SDK you build multi-tenancy, server, auth, and streaming yourself. [S43-C002] [S57-C001] [S57-C002] [S57-C003]

Both Deep Agents and the Claude Agent SDK are MIT licensed, though Claude Code itself is proprietary. [S57-C004]

## Claude Code

Claude MCP Tools is a Model Context Protocol server ecosystem for integrating with Anthropic's Claude Desktop and Claude Code CLI, providing a production-ready ecosystem of 21 operational MCP servers (consolidated from 25). The video 'Run Claude Code as an MCP Server (Control It with GPT-5)' (by Leon van Zyl) demonstrates running Claude Code as an MCP server so it can be controlled by another model such as GPT-5. [S44-C001] [S59-C001]

## Claude Fable 5

Claude Fable 5 is Anthropic's first generally available Mythos-class model, with a 1M token context window, up to 128k output tokens, and pricing of 10 USD per million input tokens and 50 USD per million output tokens. Claude Fable 5 retains hard safety limits that fall back to Claude Opus 4.8 for high-risk content such as offensive cyber operations and detailed exploit guidance. Mythos-class traffic is subject to mandatory 30-day data retention, with direct implications for security models, data residency, and sensitive client work. Anthropic launched Claude Fable 5 on 9 June 2026 with a 1M context window, up to 128k output tokens per request, adaptive thinking always on, and pricing of US$10 per million input and US$50 per million output tokens. [S01-C002] [S01-C003] [S01-C004] [S02-C003]

Claude Fable 5 requires 30-day data retention on Anthropic's first-party API, is not available under zero data retention arrangements, and conservatively routes some cyber and biology requests to Claude Opus 4.8, with safeguard triggers occurring in under 5 percent of sessions on average. Claude Fable 5 (model id claude-fable-5, released 9 June 2026) is a Mythos-class model with a 1M-token context window, priced at $10/$50 per million tokens, with safety classifiers that reroute cyber/bio/chem/distillation queries to Opus 4.8 and a mandatory 30-day data retention requirement. Anthropic released two models on June 9, 2026: Claude Fable 5 and Claude Mythos 5, both in a Mythos-class tier that sits above the Opus class in capability. Fable 5 and Mythos 5 share the same underlying model; the difference is safeguards, with Fable 5 shipping safety classifiers for general use and Mythos 5 having some classifiers removed and kept in limited release. [S02-C004] [S03-C003] [S19-C001] [S19-C002]

Both Mythos-class models support a 1M token context window by default, allow up to 128k output tokens per request, and are priced at $10 per million input and $50 per million output tokens, less than half the price of Claude Mythos Preview. When Fable 5's classifiers flag a request in cybersecurity, biology and chemistry, or distillation, the response is handled by Claude Opus 4.8 instead, and users are informed whenever a fallback occurs. Claude Fable 5 and Mythos 5 cost $10 per million input tokens and $50 per million output tokens, which Anthropic frames as less than half the price of Claude Mythos Preview but is roughly twice the cost of Claude Opus 4.8. After backlash over silent downgrades, Anthropic stated it will visibly show when a blocked Fable 5 request is re-run on Opus 4.8 in the same conversation, with a notice and the response labeled by the answering model, and the picker staying on Opus afterward until manually switched back. [S19-C003] [S19-C005] [S24-C001] [S24-C002]

Fable 5 was included on Pro, Max, Team and enterprise plans at no extra cost through June 22, 2026, after which (June 23) Anthropic will require usage credits due to capacity constraints. Anthropic requires a 30-day data retention policy for all traffic on Mythos-class models on first-party and third-party surfaces, will not use the data to train new Claude models, and logs all human access and ensures deletion after 30 days. Claude Fable 5 is a Mythos-level model built for the most ambitious, long-running projects, described as thorough, proactive, and able to test its own work, accessed via claude-fable-5 on the Claude API. Claude Fable 5 is priced at $10 per million input tokens and $50 per million output tokens, with an existing 90% input token discount for prompt caching, and US-only inference available at 1.1x pricing. [S24-C003] [S24-C004] [S25-C001] [S25-C002]

Claude Fable 5 includes safeguards for cybersecurity and biology, automatically routing flagged queries in those domains to Opus 4.8, and users are not charged Fable prices for rerouted requests. Claude Fable 5 is the first publicly available version of Anthropic's Mythos model, excelling at software engineering, knowledge work, and vision but blocking responses and falling back to Claude Opus 4.8 in high-risk areas like cybersecurity, biology, chemistry, and distillation. Anthropic stress-tested Fable 5's classifiers via an external bug bounty that produced no universal jailbreaks in over 1,000 hours of testing, and external red-teaming organizations also failed to find universal jailbreaks. Anthropic requires a 30-day retention on all Fable 5 / Mythos 5 traffic (even for prior zero-retention enterprises), stating the data is used only to defend against novel attacks and jailbreaks and to reduce false positives, not for training, which could set an industry precedent. [S25-C004] [S26-C001] [S26-C002] [S26-C003]

Anthropic says cases where Fable defers to Opus 4.8 are rare, with early data showing at least 95% of Fable sessions running entirely on the model's own responses. The guide characterizes Fable 5 as 'Mythos on a leash': the same underlying model wrapped in classifiers that block dangerous queries and route them to the safer Opus 4.8, providing the intelligence without unrestricted capabilities. The guide presents a practical framework for deciding when Fable 5's premium price is worth it relative to Opus 4.8, since the doubled cost changes the math on when reaching for the most capable model pays off. Anthropic tuned Fable 5's safeguards conservatively so they sometimes catch harmless requests, routing those queries to Claude Opus 4.8, triggering on average in less than 5% of sessions. [S26-C004] [S27-C003] [S27-C005] [S51-C002]

Anthropic launched Claude Fable 5 on June 9, 2026 as the most capable model it has ever made generally available, at a price point below half of what Claude Mythos Preview costs. Fable 5 and Mythos 5 share the same underlying model, with the difference being a set of safety classifiers that govern which kinds of requests Fable 5 can fulfill. [S52-C001] [S52-C003]

## Claude For Excel

In internal testing, Claude for Excel uses Programmatic Tool Calling to read and modify spreadsheets with thousands of rows without overloading the model's context window. [S42-C005]

## Claude Mythos 5

Anthropic says Mythos 5 is its first model to consistently produce novel scientific hypotheses, with scientists preferring its molecular biology hypotheses around 80% of the time in blinded comparisons. Claude Mythos 5 is the same underlying model as Fable 5 with safeguards lifted in some areas, deployed initially through Project Glasswing in collaboration with the US government, and described as having the strongest cybersecurity capabilities of any model in the world. Using Mythos 5, Anthropic's internal protein design experts accelerated aspects of drug design by around 10 times, with the model matching or beating skilled human operators on 9 of 14 protein targets using design and bioinformatics tools without human assistance. [S19-C006] [S51-C003] [S51-C004]

## Cli

The OpenHands CLI experience is familiar to users of Claude Code or Codex and can be powered with Claude, GPT, or any other LLM. [S08-C003]

## Cline

Cline is an open-source AI coding agent positioned as open source and uncompromised. Cline published a Thunderdome experiment running three Cline agents in a tmux session, each pointed at a different backend, all running OpenAI's gpt-oss 120-billion-parameter model, to reveal differences in inference speed across hardware and inference stacks. [S16-C001] [S16-C002]

## Code Execution

Programmatic Tool Calling lets Claude invoke tools from within a code execution environment, reducing context-window impact since natural-language tool calling requires a full inference pass per invocation and piles intermediate results into context. [S42-C003]

## Codeact

CodeAct 2.1 improvements included switching to function calling, adopting Anthropic's new claude-3.5 model, and fixes to make directory traversal easier for agents. [S47-C003]

## Codeium

Windsurf was developed by Cognition as the successor to Codeium, shifting from pure autocomplete to an agentic platform that can manage multi-file changes, terminal commands, and project-wide refactors. [S34-C002]

## Coding Agent

GitHub's Copilot coding agent, an asynchronous autonomous developer agent, became generally available for all paid Copilot subscribers (announced via a community discussion updated September 2025). When delegated a task, the Copilot coding agent opens a draft pull request and works in the background in its own development environment powered by GitHub Actions, then requests a review, and accepts further changes via PR comments. [S63-C001] [S63-C002]

## Coding Agents

OpenHands is a community-driven platform for AI-driven development offering multiple ways to work: a Software Agent SDK, a CLI, a Local GUI, OpenHands Cloud, and OpenHands Enterprise. OpenHands is an open-source, customizable platform for building with coding agents that can run locally or at scale, offered as an SDK, Cloud, and CLI. Open-source AI coding agents have matured enough to serve as foundations for new domain-specific tools instead of building from scratch; the survey covers OpenHands, Aider, Continue, OpenDevin, SWE-agent, and Cody. Open-source coding tools fall into three overlapping buckets: terminal-first agents (Aider, OpenHands CLI), IDE-native assistants (Continue, Cody), and autonomous software engineers (OpenDevin, SWE-agent, OpenHands cloud/ACI). [S08-C001] [S33-C001] [S35-C001] [S35-C002]

Playwright offers multiple entry points for different workflows: Playwright Test for end-to-end testing, the Playwright CLI for coding agents (Claude Code, Copilot), and Playwright MCP for AI agents and LLM-driven automation. [S66-C002]

## Colang

NeMo Guardrails uses Colang, a domain-specific language for declaratively defining conversation flows, allowed topics, and responses to user intents, which uniquely enables multi-turn dialog management beyond filtering individual inputs and outputs. [S38-C003]

## Comparison

Compared with existing SDKs from OpenAI, Claude, and Google, the OpenHands SDK uniquely integrates native sandboxed execution, lifecycle control, model-agnostic multi-LLM routing, and built-in security analysis. The alternatives were evaluated against four criteria: supported tech stack and integrations (native Python SDKs), evaluation capabilities and metrics, dataset and test management, and prompt and experiment versioning. [S46-C002] [S56-C004]

## Completion Functions

For advanced use cases like prompt chains or tool-using agents, OpenAI Evals provides a Completion Function Protocol, and results can optionally be logged to a Snowflake database. [S64-C003]

## Context Engineering

The term context engineering was coined by Shopify CEO Tobi Lutke on 19 June 2025 and endorsed by Andrej Karpathy on 25 June 2025, describing the art of providing all the context for a task to be plausibly solvable by the LLM. Chroma's Context Rot report (Hong et al., 2025) tested 18 frontier models and concluded that models do not use their context uniformly and performance grows increasingly unreliable as input length grows. The Tool Search Tool lets Claude discover tools on-demand and only see the tools needed for the current task, instead of loading all tool definitions upfront (which can consume 50K-134K+ tokens before the conversation starts). [S03-C005] [S03-C009] [S42-C002]

## Contributions

OpenAI Evals currently does not accept eval submissions with custom code, only model-graded evals with custom YAML files, and OpenAI staff actively review contributed evals when considering improvements to upcoming models. [S64-C004]

## Cost Optimization

LLM Guard is engineered for cost-effective CPU inference, offering 5x lower inference expenses on CPU compared to GPU. [S14-C003]

## Cybersecurity

Mythos was first unveiled as a preview in April 2026 and kept deliberately limited because it excels at identifying software security flaws, expanding to hundreds of organizations across 15 countries through a cybersecurity initiative called Project Glasswing focused on critical infrastructure. [S27-C002]

## Data

A Ragas RAG pipeline evaluation requires four key data points: the question, the retrieved contexts, the generated answer, and the ground truth answer. [S12-C003]

## Deepeval

DeepEval is an open-source LLM evaluation framework offering a broad metric library spanning agentic, RAG, conversational, MCP, multimodal, and safety metrics. G-Eval is DeepEval's research-backed LLM-as-a-judge metric for evaluating on any custom criteria with human-like accuracy, and DAG is its graph-based deterministic LLM-as-a-judge metric builder. G-Eval is a framework that uses LLM-as-a-judge with chain-of-thought to evaluate LLM outputs against any custom criteria, described as DeepEval's most versatile metric capable of evaluating almost any use case with human-like accuracy. G-Eval is best for subjective, use-case-specific evaluation and is usually used alongside more system-specific metrics such as ContextualRelevancyMetric for RAG and TaskCompletionMetric for agents. [S11-C001] [S11-C002] [S36-C001] [S36-C002]

A GEval metric is created by defining an evaluation criteria in everyday language, with required parameters name, criteria (or evaluation_steps), and evaluation_params, plus optional rubric and threshold (default 0.5). Providing explicit evaluation_steps tells GEval to follow those steps rather than generating them from the criteria, which allows for more controllable metric scores. For solo developers wanting local evals, the recommended open-source alternatives are DeepEval for Python-native pytest metrics and RAGAS for RAG-specific retrieval and generation scoring. DeepEval is a Python-native LLM evaluation framework built on pytest (Apache 2.0, 13.9k stars) shipping 50+ built-in metrics including G-Eval, hallucination detection, answer relevancy, contextual recall, and faithfulness, each returning a 0-1 score with a natural-language explanation. [S36-C003] [S36-C004] [S60-C002] [S60-C004]

## Deepseek

Open-weight models in 2026 (Llama 4.x, Mistral/Mixtral, Qwen 3, DeepSeek-V3/R1) are competitive with frontier closed models on most tasks. [S20-C004]

## Developer Workflow

Promptfoo closes the loop by delivering remediation guidance and security findings directly in pull requests and developer workflows. [S48-C003]

## Dimensions

Evaluating RAG architectures is challenging across several dimensions: the retrieval system's ability to identify relevant focused context, the LLM's faithful use of those passages, and the quality of the generation itself. [S50-C003]

## Ecosystem

The MCP servers repository of maintained servers has roughly 87.1k stars, and the MCP Inspector is a visual testing tool for MCP servers. [S06-C005]

## Enterprise

OpenHands Enterprise is source-available and can be self-hosted in a customer's own VPC via Kubernetes, but requires a purchased license to run for more than one month. [S08-C005]

## Eval

Promptfoo supports two main CI/CD workflows: eval (testing prompt quality and performance via promptfoo eval) and red teaming (security scanning via promptfoo redteam run). [S49-C003]

## Eval Templates

OpenAI Evals lets users build basic or model-graded evals without writing evaluation code by following an existing eval template, providing data in JSON and specifying eval parameters in YAML. [S64-C002]

## Evaluation

Evaluation and safety frameworks including Promptfoo, DeepEval, Ragas, Garak, PyRIT, NeMo Guardrails, and LLM Guard together form a toolbox for prompt/agent evaluation, red teaming, guardrails, and policy-driven runtime checks. promptfoo is a CLI and library for evaluating and red-teaming LLM apps, aimed at replacing a trial-and-error approach with shipping secure, reliable AI apps. Research indicates GPT-4 used as an evaluator aligns with human evaluations about 80% of the time, matching the Bayesian limit of human agreement, supporting the use of LLMs as judges. The authors posit that a reference-free framework like Ragas can crucially contribute to faster evaluation cycles of RAG architectures, which is especially important given the fast adoption of LLMs. [S01-C010] [S10-C001] [S12-C002] [S50-C004]

Promptfoo is a popular open-source toolkit for testing and evaluating LLM prompts via simple CLI/YAML definitions, but its command-line interface and offline nature hit a ceiling as teams move to building complex production AI agents. [S56-C001]

## Fallback

Using LiteLLM with the Agent SDK enables automatically retrying with different models if one fails and switching between models dynamically. [S43-C003]

## Feature Comparison

A systematic comparison of 31 SDK features found OpenHands shares 15 with at least one of OpenAI/Claude/Google SDKs but uniquely combines 16 additional features, including native remote execution, a production server with sandboxing, and model-agnostic multi-LLM routing across 100+ providers. [S46-C004]

## Format

In a SKILL.md file, YAML frontmatter provides machine-readable metadata (such as name and description) which the agent parses, while the Markdown body provides human-readable instructions the agent follows. [S23-C005]

## Function Calling

Prior AI-tool integration relied on closed OpenAI solutions (code interpreter, function-calling, structured outputs, introduced in 2023) and open but bespoke frameworks like LangChain, whereas MCP's client-server approach makes connectors easier to scale. [S32-C004]

## Garak

Garak is a free, open-source LLM vulnerability scanner that tests for problems like hallucinations, prompt injections, jailbreaks, and toxic outputs to help developers find where a model might fail and make it safer. Garak works with a wide range of models and platforms including Hugging Face Hub generative models, Replicate text models, OpenAI API chat and continuation models, LiteLLM, GGUF models (llama.cpp), and most systems accessible through REST. Garak produces several logs per run: a persistent garak.log debug file, a per-run JSONL report detailing every probing attempt with a status attribute, and a hit log tracking attempts that revealed a vulnerability. Garak is available for free on GitHub under NVIDIA's repository. [S37-C001] [S37-C002] [S37-C003] [S37-C004]

## Gartner

Cognition highlights Windsurf's selection as a Leader in the 2025 Gartner Magic Quadrant for AI Coding Assistants, emphasizing its agentic workflows, deep context engine, and enterprise-grade security and deployment options. [S34-C005]

## Generative Ai

Red teaming generative AI differs from traditional red teaming in three ways: it must probe both security and responsible AI risks simultaneously, it is more probabilistic (same input can yield different outputs), and the architectures vary widely across modalities. [S13-C002]

## Gh Skill

Using gh skill requires GitHub CLI version v2.90.0 or later, and skills can be pinned to a specific release tag or commit SHA with --pin so pinned skills are skipped during updates. gh skill treats agent skills as executable instructions and a supply chain risk, using content-addressed change detection via git tree SHAs, immutable releases, and portable provenance metadata written into SKILL.md frontmatter. GitHub warns that skills are installed at the user's discretion, are not verified by GitHub, and may contain prompt injections, hidden instructions, or malicious scripts, recommending inspection via gh skill preview before installation. [S07-C003] [S07-C004] [S07-C005]

## Github Integration

OpenHands offers a GitHub-native workflow where labeling an issue with 'openhands' or mentioning @openhands prompts the agent to comment, attempt a fix, and open a PR, with configuration stored in ~/.openhands/. [S35-C004]

## Governance

The Model Context Protocol is an open source project hosted by The Linux Foundation and open to community contributions. [S06-C003]

## Guardrails

LLM Guard is a suite of tools to protect LLM applications by detecting, redacting, and sanitizing LLM prompts and responses for real-time safety, security, and compliance. NVIDIA NeMo Guardrails is an open-source (Apache 2.0) toolkit for adding programmable guardrails to LLM conversational applications, with the latest release v0.20.0 (January 2026) requiring Python 3.10-3.13. NeMo Guardrails provides five rail types covering different interaction stages: input rails (user messages), dialog rails (conversation flow), retrieval rails (knowledge-base results), execution rails (tool/action calls), and output rails (response validation). [S14-C001] [S38-C001] [S38-C002]

## Hallucinations

LLMs can confidently produce information that is not real or true (hallucinations or fabulations) and can appear to perform tasks they were never explicitly trained to do. RAG systems combine a retrieval module and an LLM-based generation module, giving LLMs knowledge from a reference textual database and reducing the risk of hallucinations by acting as a natural language layer between users and textual databases. [S40-C003] [S50-C002]

## Handoffs

The OpenAI Agents SDK's core primitives are Agents (LLMs with instructions, tools, guardrails, and handoffs), Handoffs (delegating tasks to other agents), and Tools (functions, MCP, and hosted tools). [S65-C004]

## Installation

promptfoo is installed via npm install -g promptfoo (requiring Node.js ^20.20.0 or >=22.22.0) and is also available via brew, pip, or npx. [S10-C004]

## Integration

The Model Context Protocol (MCP) is an open protocol that enables seamless integration between LLM applications and external data sources and tools, providing a standardized way to connect LLMs with the context they need. MCP's novelty is standardization: it provides a single standard protocol to connect AI models to diverse data sources, replacing the fragmented, per-source custom integrations that previously made connected systems hard to scale. [S06-C001] [S32-C001]

## Integrations

NeMo Guardrails supports OpenAI, Azure, Anthropic, HuggingFace, and NVIDIA NIM models, integrates with LangChain and LangGraph, and includes jailbreak detection, prompt injection protection, fact-checking, and hallucination detection with OpenTelemetry tracing. [S38-C004]

## Languages

MCP provides official SDKs in ten languages: TypeScript, Python, Java, Kotlin, C#, Go, PHP, Ruby, Rust, and Swift. [S06-C002]

## Least Privilege

ToolHive (Stacklok) is an MCP runtime/gateway that runs MCP servers in containers with named permission profiles (none/network/custom), turning MCP tool access into an enforced least-privilege boundary. [S03-C011]

## License

All OpenHands work is available under the MIT license except the enterprise/ directory, and the core openhands and agent-server Docker images are fully MIT-licensed. promptfoo is now part of OpenAI and remains open source and MIT licensed. [S08-C004] [S10-C002]

## Limitations

Reasons teams seek Promptfoo alternatives include its CLI/YAML-heavy workflow that alienates non-engineers, its Node.js foundation conflicting with Python-first stacks, and its lack of built-in dashboards, observability, and version control for prompts and datasets. Promptfoo (10.8k GitHub stars) is a CLI-first prompt testing and red-teaming tool that runs locally with YAML configs and scans for 50+ vulnerability types, but its results stay local with no production monitoring, and its free tier allows 10k red-team probes per month. [S56-C002] [S60-C003]

## Litellm

LiteLLM is the best current neutral control plane for mixing frontier and cheap models, but its supply-chain history means it needs stricter auditing and sandboxing. [S02-C009]

## Llm As Judge

Ragas is a specialized evaluation framework for assessing Retrieval Augmented Generation (RAG) systems, leveraging advanced LLMs as judges to provide scalable, cost-effective, continuous, explainable scores for AI-generated responses. [S12-C001]

## Llm Guard

LLM Guard includes advanced input and output scanners that anonymize PII, redact secrets, and counter threats such as prompt injections and jailbreaks, and is model-agnostic across GPT, Llama, Mistral, Falcon and frameworks like Azure OpenAI, Bedrock, and LangChain. [S14-C002]

## Llms

An LLM works by predicting the next best group of letters (tokens), completing a document by repeatedly predicting the next token until it reaches a maximum token threshold or a special stop token. [S40-C001]

## Mcp

The Model Context Protocol, originating at Anthropic and now under the Linux Foundation, has become the de facto standard for model-neutral tool connectivity, with official multi-language SDKs and a growing registry of servers. Several MCP SDKs are maintained in collaboration with major companies: the C# SDK with Microsoft, the Kotlin SDK with JetBrains, and the Go SDK with Google. At launch Anthropic introduced three MCP components: the specification and SDKs, local MCP server support in Claude Desktop apps, and an open-source repository of MCP servers, with pre-built servers for Google Drive, Slack, GitHub, Git, Postgres, and Puppeteer. The ecosystem reported comprehensive testing with a 94/100 overall score, sub-second response times across all tools, and 100% success rate on Claude Code integration. [S01-C006] [S06-C004] [S22-C003] [S44-C004]

## Memories

Windsurf supports persistent customization through 'Memories' and rules stored in simple project-scoped files, letting teams encode coding standards, documentation requirements, and architectural patterns that Cascade and Supercomplete follow across generations and refactors. [S34-C004]

## Metrics

Ragas provides evaluation metrics including Faithfulness, Answer Relevancy, Context Recall, Context Precision, Context Relevancy, and Context Entity Recall, each scored from 0 to 1. [S12-C004]

## Microsoft

Microsoft released PyRIT (Python Risk Identification Toolkit for generative AI) on 22 February 2024 as an open automation framework to help security professionals and ML engineers proactively find risks in generative AI systems. [S13-C001]

## Model Agnostic

OpenHands is model-agnostic, runs in a secure sandboxed runtime the user controls (isolated Docker or Kubernetes, self-hosted or cloud, with access control and auditability), and lets users delegate tasks from GitHub, GitLab, Slack, or the API/SDK. [S33-C003]

## Model Serving

For model serving, the article recommends vLLM for scale (PagedAttention, continuous batching), Ollama for local development, and SGLang when tool-call latency matters most (RadixAttention). [S20-C003]

## Multi Agent

The OpenAI Agents SDK is an open-source, Python- and TS-first framework and a significant upgrade over Swarm, designed to simplify orchestrating multi-agent workflows using built-in language features rather than new abstractions. [S65-C003]

## Openhands

The OpenHands Software Agent SDK is a composable Python library containing all of OpenHands' agentic tech, letting users define agents in code and run them locally or scale to thousands of agents in the cloud. OpenHands ships proven workflows including scanning repos to fix vulnerabilities and open PRs, reviewing PRs for quality and security, migrating legacy COBOL to Java, and triaging incidents. [S08-C002] [S33-C002]

## Parallelism

Playwright tests run in parallel across all configured browsers in headless mode by default, with each test getting a fresh browser context for full isolation at near-zero overhead. [S66-C003]

## Rag Evaluation

Ragas (Retrieval Augmented Generation Assessment) is a framework for reference-free evaluation of RAG pipelines, providing metrics that do not rely on ground truth human annotations. [S50-C001]

## Red Teaming

Every skill, MCP server and plugin should be treated as executable, prompt-injectable supply-chain risk: audit licence, maintainers, activity, scripts, network calls and permissions, sandbox in Docker/devcontainer, and run injection tests before any tool touches real data. [S03-C004]

## Schemas

Tool Use Examples provide a universal standard for demonstrating effective tool usage, since JSON schemas define what is structurally valid but cannot express usage patterns like when to include optional parameters or which combinations make sense. [S42-C004]

## Conflicts

No conflicts were recorded during reconciliation.

## Gaps

No substantive coverage gaps were identified across the topic areas synthesised here; every winning claim from reconciliation is carried into a section above. The only known limitations are source-level: two video sources (S54 and S59) returned no public transcript and one course page (S62) exposed only a login/landing screen, so those items were marked out of scope during reconciliation and contribute no domain claims.

## Appendix: Source Register

| Source | Title | Type | Authority | Authored | Link | Content hash |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | Frontier AI Orchestration Toolkit: Systems, Skills, MCP Ecosystem, and Claude Fable 5 Workflows (2024–2026) | report | unknown | unknown | - | ff16e31eb6c0 |
| S02 | Frontier AI Capability Engineering for Claude Fable 5 and Beyond | report | unknown | unknown | - | 4e23a8418870 |
| S03 | Frontier AI Orchestration: A Practical, Security-Audited Toolkit for Building Your Own Workflow | report | unknown | unknown | - | 7ba9474ce8b8 |
| S04 | GitHub - anthropics/claude-agent-sdk-python | html-article | unknown | unknown | https://github.com/anthropics/claude-agent-sdk-python | e47fff7f4769 |
| S05 | GitHub - anthropics/claude-agent-sdk-typescript | html-article | unknown | unknown | https://github.com/anthropics/claude-agent-sdk-typescript | 80ff222d7859 |
| S06 | Model Context Protocol | html-article | unknown | unknown | https://github.com/modelcontextprotocol | 271b8eb4969b |
| S07 | Manage agent skills with GitHub CLI - GitHub Changelog | html-article | unknown | unknown | https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/ | a015a17e76ef |
| S08 | GitHub - OpenHands/OpenHands: 🙌 OpenHands: AI-Driven Development | html-article | unknown | unknown | https://github.com/OpenHands/openhands | 296fce5118ea |
| S09 | GitHub - browser-use/browser-use: 🌐 Make websites accessible for AI agents. Automate tasks online with ease. | html-article | unknown | unknown | https://github.com/browser-use/browser-use | 01daa530bf70 |
| S10 | GitHub - promptfoo/promptfoo: Test your prompts, agents, and RAGs. Red teaming/pentesting/vulnerability scanning for AI. Compare performance of GPT, Claude, Gemini, DeepSeek, and more. Simple declarative configs with command line and CI/CD integration. Used by OpenAI and Anthropic. | html-article | unknown | unknown | https://github.com/promptfoo/promptfoo | b5d4fb0e90ff |
| S11 | GitHub - confident-ai/deepeval: The LLM Evaluation Framework | html-article | unknown | unknown | https://github.com/confident-ai/deepeval | 22f45775f46a |
| S12 | RAG Evaluation Using Ragas - Zilliz blog | html-article | unknown | unknown | https://zilliz.com/blog/rag-evaluation-using-ragas | 79428478742f |
| S13 | Announcing Microsoft’s open automation framework to red team generative AI Systems | Microsoft Security Blog | html-article | unknown | unknown | https://www.microsoft.com/en-us/security/blog/2024/02/22/announcing-microsofts-open-automation-framework-to-red-team-generative- | 68c85ec46216 |
| S14 | LLM Guard | Secure Your LLM Applications | html-article | unknown | unknown | https://protectai.com/llm-guard | 628efab9111c |
| S15 | GitHub - Aider-AI/aider: aider is AI pair programming in your terminal | html-article | unknown | unknown | https://github.com/aider-ai/aider | 62390fff6a6a |
| S16 | Cline - AI Coding, Open Source and Uncompromised | html-article | unknown | unknown | https://cline.bot | 2bc85f68e4f3 |
| S17 | GitHub - browser-use/web-ui: 🖥️ Run AI Agent in your browser. | html-article | unknown | unknown | https://github.com/browser-use/web-ui | 25a4adcd785b |
| S18 | Agent-MCP by rinadelph | Multi-Agent Dev Orchestration | html-article | unknown | unknown | https://www.augmentcode.com/mcp/agent-mcp | 38d2d34a48f6 |
| S19 | Anthropic Releases Claude Fable 5 and Claude Mythos 5: Same Underlying Model, Different Safeguards, New Mythos-Class Tier | html-article | unknown | unknown | https://www.marktechpost.com/2026/06/10/anthropic-releases-claude-fable-5-and-claude-mythos-5-same-underlying-model-different-safeguards-new-mythos-class-tier/ | 7f89f8041b27 |
| S20 | Open-Source AI Agent Stack in 2026 | html-article | unknown | unknown | https://futureagi.com/blog/open-source-stack-ai-agents-2025/ | f6a03eac27ad |
| S21 | AI Agent Frameworks (2026 Update): 8 SDKs Compared + the Claude Agent SDK Primitive Reference | html-article | unknown | unknown | https://www.morphllm.com/ai-agent-framework | 117a9f05130f |
| S22 | Introducing the Model Context Protocol | html-article | unknown | unknown | https://www.anthropic.com/news/model-context-protocol | d0ac00941db0 |
| S23 | Agent Skills Guide 2026: Build, Share & Secure | html-article | unknown | unknown | https://www.termdock.com/en/blog/agent-skills-guide | ccbb160ff203 |
| S24 | Anthropic’s Claude Fable 5, Mythos 5: What you need to know | Constellation Research | html-article | unknown | unknown | https://www.constellationr.com/insights/news/anthropics-claude-fable-5-mythos-5-what-you-need-know | 677a247deb78 |
| S25 | Claude Fable | html-article | unknown | unknown | https://www.anthropic.com/claude/fable | ecd628fb0f30 |
| S26 | Anthropic releases Claude Fable, a version of Mythos, days after warning AI is becoming too dangerous | html-article | unknown | unknown | https://techcrunch.com/2026/06/09/anthropic-released-claude-fable-5-its-most-powerful-model-publicly-days-after-warning-ai-is-getting-too-dangerous/ | e62304ccff86 |
| S27 | Claude Fable 5: Mythos-Class AI Guide | Lushbinary | html-article | unknown | unknown | https://lushbinary.com/blog/claude-fable-5-developer-guide/ | 0be1234ec2e1 |
| S28 | Use Agent Skills in VS Code | html-article | unknown | unknown | https://code.visualstudio.com/docs/copilot/customization/agent-skills | dff12d8f9472 |
| S29 | GitHub - heilcheng/awesome-agent-skills: Tutorials, Guides and Agent Skills Directories | html-article | unknown | unknown | https://github.com/heilcheng/awesome-agent-skills | 382c3c25ae86 |
| S30 | How to write a great agents.md: Lessons from over 2,500 repositories | html-article | unknown | unknown | https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/ | 50197928f2f7 |
| S31 | A Complete Guide To AGENTS.md | html-article | unknown | unknown | https://www.aihero.dev/a-complete-guide-to-agents-md | 701559b094f9 |
| S32 | Model Context Protocol Changes AI Integration | html-article | unknown | unknown | https://patmcguinness.substack.com/p/model-context-protocol-changes-ai | 7995c5d85cd2 |
| S33 | OpenHands | The Open Platform for Cloud Coding Agents | html-article | unknown | unknown | https://openhands.dev | 6476e77aaf1b |
| S34 | Windsurf Review: Agentic AI IDE Redefining Developer Productivity | html-article | unknown | unknown | https://talent500.com/blog/windsurf-agentic-ai-ide-review/ | b568ac7cebff |
| S35 | Open-Source Coding Agents: A Survey | html-article | unknown | unknown | https://airesponsibly.substack.com/p/open-source-ai-coding-agents-a-survey | 5b7a7cb248c2 |
| S36 | G-Eval | DeepEval - The LLM Evaluation Framework | html-article | unknown | unknown | https://deepeval.com/docs/metrics-llm-evals | 27cc28af651f |
| S37 | Garak: Open-source LLM vulnerability scanner - Help Net Security | html-article | unknown | unknown | https://www.helpnetsecurity.com/2025/09/10/garak-open-source-llm-vulnerability-scanner/ | c17ba97f74eb |
| S38 | NeMo Guardrails 2026: NVIDIA's LLM Safety Toolkit | html-article | unknown | unknown | https://appsecsanta.com/nemo-guardrails | 946657370e97 |
| S39 | What is an AI Agent? | html-article | unknown | unknown | https://www.builder.io/blog/ai-agent | d21f853ac277 |
| S40 | A developer's guide to prompt engineering and LLMs | html-article | unknown | unknown | https://github.blog/ai-and-ml/generative-ai/prompt-engineering-guide-generative-ai-llms/ | 2f6c30a640c5 |
| S41 | A practical guide to the Python Claude Code SDK (now agent SDK) in 2025 | html-article | unknown | unknown | https://www.eesel.ai/blog/python-claude-code-sdk | 40949ca902ab |
| S42 | Introducing advanced tool use on the Claude Developer Platform | html-article | unknown | unknown | https://www.anthropic.com/engineering/advanced-tool-use | bd2b23b0496e |
| S43 | Claude Agent SDK with LiteLLM | liteLLM | html-article | unknown | unknown | https://docs.litellm.ai/docs/tutorials/claude_agent_sdk | dd643a474856 |
| S44 | Claude MCP Tools Server | Awesome MCP Servers | html-article | unknown | unknown | https://mcpservers.org/servers/GrimFandango42/Claude-MCP-tools | 9d7617e9b7a8 |
| S45 | GitHub - softaworks/agent-toolkit: A curated collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities across development, documentation, planning, and professional workflows. | html-article | unknown | unknown | https://github.com/softaworks/agent-toolkit | e8764787571a |
| S46 | The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents | html-article | unknown | unknown | https://arxiv.org/html/2511.03690v1 | faf8fecbdac7 |
| S47 | OpenHands CodeAct 2.1: An Open, State-of-the-Art Software Development Agent | html-article | unknown | unknown | https://www.openhands.dev/blog/openhands-codeact-21-an-open-state-of-the-art-software-development-agent | 7fb1d029166e |
| S48 | Build Secure AI Applications | Promptfoo | html-article | unknown | unknown | https://www.promptfoo.dev | 2ec514a41c62 |
| S49 | CI/CD Integration for LLM Eval and Security | Promptfoo | html-article | unknown | unknown | https://www.promptfoo.dev/docs/integrations/ci-cd/ | 2e4749d75376 |
| S50 | Ragas: Automated Evaluation of Retrieval Augmented Generation | html-article | unknown | unknown | https://arxiv.org/abs/2309.15217 | c7be2d6a9d08 |
| S51 | Claude Fable 5 and Claude Mythos 5 | html-article | unknown | unknown | https://www.anthropic.com/news/claude-fable-5-mythos-5 | ea9bc073d9d5 |
| S52 | Claude Fable 5: What It Is and What It Means for Developers | html-article | unknown | unknown | https://www.cosmicjs.com/blog/claude-fable-5-what-it-is-what-it-means-for-developers | 6a3de04390aa |
| S53 | 10 Killer AI Agent Skills That Are Dominating GitHub Now | html-article | unknown | unknown | https://www.browseract.com/blog/10-killer-ai-agent-skills-that-are-dominating-github-now | a11053faeeba |
| S54 | Claude AI + Cursor IDE: The Fastest Way to Build Apps | video-transcript | unknown | unknown | https://www.youtube.com/watch?v=d2a6CquJlXM | 6644daa185b8 |
| S55 | Aider Review: A Developer's Month With This Terminal-Based Code Assistant [2025] | Blott | html-article | unknown | unknown | https://www.blott.com/blog/post/aider-review-a-developers-month-with-this-terminal-based-code-assistant | 2b84a1c557a8 |
| S56 | 9 Best Promptfoo Alternatives: Which Frameworks are Better to Ship AI Agents - ZenML Blog | html-article | unknown | unknown | https://www.zenml.io/blog/promptfoo-alternatives | c26069b554e8 |
| S57 | Comparison with Claude Agent SDK - Docs by LangChain | html-article | unknown | unknown | https://docs.langchain.com/oss/python/deepagents/comparison | 395ae5f8079b |
| S58 | agents/docs/agent-skills.md at main · wshobson/agents | html-article | unknown | unknown | https://github.com/wshobson/agents/blob/main/docs/agent-skills.md | ed26b4a25960 |
| S59 | Run Claude Code as an MCP Server (Control It with GPT-5) | video-transcript | unknown | unknown | https://www.youtube.com/watch?v=a8A46gUvnXw&vl=en | 0913b1801cf9 |
| S60 | Best Promptfoo alternatives in 2026: Open-source tools and SaaS - Articles - Braintrust | html-article | unknown | unknown | https://www.braintrust.dev/articles/best-promptfoo-alternatives-2026 | 80440c59f002 |
| S61 | Builder | Agent skills | html-article | unknown | unknown | https://www.builder.io/c/docs/skills | 997a23f24b1b |
| S62 | Introduction to Model Context Protocol | html-article | unknown | unknown | https://anthropic.skilljar.com/introduction-to-model-context-protocol | dbae02ac9d85 |
| S63 | Copilot coding agent is now generally available! 🚀 · community · Discussion #159068 | html-article | unknown | unknown | https://github.com/orgs/community/discussions/159068 | 9c10a31e4034 |
| S64 | GitHub - openai/evals: Evals is a framework for evaluating LLMs and LLM systems, and an open-source registry of benchmarks. | html-article | unknown | unknown | https://github.com/openai/evals | 3517d5a2dc15 |
| S65 | Best Agents SDK in 2026 | html-article | unknown | unknown | https://dev.to/composiodev/best-agents-sdk-in-2026-7gg | 1812d49c5c2f |
| S66 | GitHub - microsoft/playwright: Playwright is a framework for Web Testing and Automation. It allows testing Chromium, Firefox and WebKit with a single API. | html-article | unknown | unknown | https://github.com/microsoft/playwright | 524828b03f6c |
