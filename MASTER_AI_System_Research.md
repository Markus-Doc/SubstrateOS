# Master Document: my_ai_system

> [!abstract] Methodology
> This master document was produced with the RESYNTH five stage pipeline.
> Sources consolidated: S01 (Frontier AI Orchestration: A Practical, Security-Audited Toolkit for Building Your Own Workflow, unknown, authored unknown), S02 (Frontier AI Capability Engineering for Claude Fable 5 and Beyond, unknown, authored unknown), S03 (Frontier AI Orchestration Toolkit: Systems, Skills, MCP Ecosystem, and Claude Fable 5 Workflows (2024–2026), unknown, authored unknown).
> Merge rules applied: newer_beats_older, primary_beats_secondary, explicit_beats_implied, conflicts_are_logged_not_resolved.
> Every paragraph carries provenance markers naming the claims it rests on.
> The full decision record lives in index/reconciliation.jsonl.

## Executive Summary

All three sources independently converge on the same headline finding: the strongest current pattern for frontier AI work is a layered, frontier-as-judge orchestration system in which the frontier model handles planning, architecture, synthesis, risk and final review while cheaper or specialised agents handle scanning, coding, testing, browser interaction, document lookup and log reduction [S01-C001] [S02-C001] [S03-C001].

The economic rationale is identical across sources: frontier tokens are expensive and model performance degrades as context bloats, so premium tokens should be spent only on judgement while every other layer stays cheap, cached, inspectable and swappable — context engineering now matters more than raw context size, even with 1M-token windows available [S01-C016] [S02-C003].

Between 2024 and 2026 the field shifted from prompt engineering to a layered engineering discipline composed of a small number of composable, inspectable patterns rather than monolithic products [S01-C007]. Frontier AI usage in 2026 is now defined by how well teams orchestrate models, tools and evaluations, not by which single model they pick [S03-C001]. The durable layer is no longer "the best prompt": it is repo-resident capabilities plus a model router plus an eval and security harness, run locally and inspectably, extended with MCP and cloud automation only once the blast radius is understood [S02-C040].

## Terminology

"Context Engineering" names the sub-discipline concerned with what the model sees, and is a component of the wider discipline rather than the whole of it [S01-C005]. The term was coined by Shopify CEO Tobi Lutke on X on 19 June 2025, endorsed by Andrej Karpathy on 25 June 2025, and Anthropic now publishes formal guidance on it [S01-C006]. Note that the three sources disagree on the best umbrella term for the whole discipline; that disagreement is logged in the Conflicts section rather than resolved here.

## Claude Fable 5: Identity, Specs and Pricing

Claude Fable 5 (model id claude-fable-5) was released on 9 June 2026 as Anthropic's first generally available Mythos-class model and its most capable widely released model, available on the Claude API, Claude Platform on AWS, Amazon Bedrock, Vertex AI and Microsoft Foundry [S01-C045] [S03-C030] [S02-C005] [S03-C002]. All Fable 5 figures in S01 were verified against Anthropic's platform.claude.com and launch-day press coverage dated 9–10 June 2026 [S01-C078].

The model has a 1M-token context window by default and supports up to 128k output tokens per request [S01-C047]. Pricing is $10 per million input tokens and $50 per million output tokens, with a 90% prompt-caching input discount, batch pricing of $5/$25, and US-only inference at a 1.1x multiplier [S01-C048]; this is roughly twice the cost of Claude Opus 4.8 [S03-C027].

Claude Mythos 5 shares the same base model as Fable 5 with some safeguards lifted and is restricted to Project Glasswing approved organisations, while Fable 5 is the GA version made safe for public use [S01-C046] [S03-C046].

## Claude Fable 5: Safety, Routing and Refusals

Fable 5's safety classifiers cause queries flagged for cybersecurity, biology, chemistry or model distillation to return stop_reason "refusal" with HTTP 200, to be retried on Opus 4.8; Anthropic reports fallback triggers in under 5% of sessions, and documented refusal categories include cyber, bio and reasoning_extraction [S01-C049] [S02-C007] [S03-C003]. Refused requests are not billed before output, and a fallback credit refunds the prompt-cache switching cost when retrying on Opus 4.8 [S01-C050].

This makes Fable 5 unsuitable for offensive-security or pentest workflows: CTF, pentest and biology-adjacent codebases reroute to Opus 4.8 frequently, often on the first request [S01-C051]. When migrating, remove "show your reasoning" style instructions, because they can trigger the reasoning_extraction refusal category and force fallback [S01-C055]. Classifier behaviour can also change over time as Anthropic updates against new jailbreaks and false positives, so routing behaviour should be re-validated periodically [S03-C031].

## Claude Fable 5: Data Retention and Compliance

Fable 5 and Mythos 5 are "Covered Models" requiring 30-day data retention and are not available under zero data retention; non-compliant organisation configurations receive a 400 invalid_request_error, retention on Bedrock/Vertex/Foundry is governed by the platform instead, and Anthropic states the data is not used for training but retained to defend against novel attacks and tune classifiers — a hard blocker for ZDR-obligated client work, for which ZDR-eligible Opus 4.8 should be used [S01-C052] [S02-C006] [S03-C004]. Anthropic batch processing separately stores request and response data for up to 29 days [S02-C029]. Environments should therefore be separated by data sensitivity, with Mythos-class models used only where 30-day retention is acceptable [S03-C035]. Locally, note that Claude Code stores session transcripts in plaintext under ~/.claude/projects/ for 30 days by default, and some commands can be allowed to run unsandboxed [S02-C014].

## Claude Fable 5: Thinking, Effort and Capabilities

Adaptive thinking is the only mode on Fable 5 and cannot be disabled, and raw chain of thought is never returned, only summaries [S01-C053]; extended thinking is not available, the training cutoff is January 2026, and the tokenizer introduced with Opus 4.7+ can use up to 35% more tokens for the same text [S02-C008]. The effort parameter (low/medium/high/xhigh/max) is the primary quality-latency-cost dial, lower effort on Fable can still beat higher effort on older models, and in Claude Code ultracode combines xhigh effort with dynamic-workflow orchestration [S01-C054].

Fable 5 supports Anthropic's advanced tool use: the Tool Search Tool for dynamic tool discovery, programmatic tool calling via code execution, the memory tool, compaction and task budgets [S03-C025]. Programmatic tool calling lets the model write orchestration code in a sandbox so only the final aggregated summary enters context, enabling large tool catalogs without context bloat [S03-C026]. The model is reported state-of-the-art on most benchmarks, especially software engineering, knowledge work, vision and scientific research [S03-C028]; its vision can reconstruct web apps from screenshots, supporting design-DNA extraction and UX audits [S03-C029]. For long-horizon research, Fable 5 with 1M context and compaction can manage large corpora while cheaper models handle chunk-level summarisation and tagging [S03-C045].

## Claude Fable 5: Migration, Subscription and Verification

Migration guidance: increase client timeouts (single requests can run many minutes, autonomous runs hours or days), add a send_to_user tool for verbatim progress instead of inline reasoning, dispatch parallel subagents with asynchronous orchestrator/subagent communication, use memory for long-running work, and re-run evals on hard tasks rather than smoke tests [S01-C056]. Onboarding any new frontier model should follow a checklist: swap the model id, re-run evals on hard tasks, recheck retention/routing/pricing, recalibrate effort [S01-C069].

Fable 5 is included on Pro/Max/Team/seat Enterprise plans only through 22 June 2026, after which it moves to usage credits [S01-C057]. Subscription usage is governed by rolling limits: sessions reset every five hours, a weekly limit applies across models, and Claude Code agent teams can use roughly seven times more tokens than standard sessions in plan mode [S02-C009]. From 15 June 2026, Agent SDK and "claude -p" usage on subscription plans draw from a separate monthly Agent SDK credit, splitting interactive and programmatic use into distinct cost buckets [S02-C010].

Anthropic's own system prompt for Fable reportedly instructs the model to verify product details against current docs before answering — reported via a third-party mirror and to be treated as plausible but not canonical [S01-C058]. Apply the same rule yourself: reconfirm pricing, retention and routing on platform.claude.com before production use, because model-version specifics are fast-moving [S01-C059].

## Agent Skills Ecosystem

Anthropic published Agent Skills as an open standard on 18 December 2025 (agentskills.io); a skill is a folder with a SKILL.md (YAML frontmatter plus markdown body) and optional scripts/, references/ and assets/ directories, and SKILL.md-based skills are now a multi-platform standard spanning Claude, Copilot, Cursor, Codex and Gemini CLI [S01-C008] [S03-C005]. By March 2026, 32 tools from competing companies read the same SKILL.md files, with Microsoft and OpenAI integrating within 48 hours of release [S01-C009]. Versioned capability packs beside the codebase — rather than one-off chat prompts — make workflows easier to review, reuse, diff, test and secure [S02-C002].

Distribution has matured on two tracks: the npx skills package manager with Vercel's skills.sh registry (launched 20 January 2026, listing 89,753 skills by March 2026) [S01-C010], and GitHub's gh skill CLI (launched 16 April 2026) for discovering, installing, updating and publishing skills across hosts with an --agent targeting flag [S03-C012].

The format requires only name and description frontmatter and uses progressive disclosure: metadata loads at startup, the body on activation, resources on demand [S01-C024]. Authoring guidance: keep SKILL.md under ~500 lines and push detail into references/ [S01-C025]. Skills can restrict tools while active via allowed-tools frontmatter, and the risk concentrates in referenced scripts rather than the markdown itself [S03-C013]. Treat registry skills as npm-class supply-chain risk: Snyk scans at install, but verify install counts (prefer 1k+), repo stars, and read SKILL.md plus scripts before installing; metadata.internal can hide skills [S01-C026].

## Instruction Files (AGENTS.md / CLAUDE.md)

AGENTS.md is a model-neutral instruction-file standard under the Linux Foundation's Agentic AI Foundation, announced 9 December 2025 with Anthropic, OpenAI and Block as founding members, with MCP, AGENTS.md and Goose contributed as initial projects and 146 member organisations by February 2026 [S01-C013]. AGENTS.md carries the highest trial priority in S01's shortlist (cheap, high ROI), and S02 independently rates the AGENTS.md-plus-CLAUDE.md pattern the fastest, cheapest workflow improvement for coding agents [S01-C076] [S02-C020].

Quality matters: studies found LLM-generated context files can reduce task success and inflate cost, so hand-curate them [S01-C014]. GitHub's analysis of thousands of AGENTS.md files found that high-performing ones share a clear persona, explicit commands, project knowledge, concrete examples, and three-tier boundaries of "always do", "ask first" and "never do" [S03-C014]; including real examples of good output and explicit "never do" rules reduces generic AI tone [S03-C016]. Best practice is progressive disclosure: a minimal root file with detailed rules in linked topic docs, and a CLAUDE.md that points Claude at AGENTS.md [S03-C015]. The recommended layered layout is a root AGENTS.md for cross-tool repo facts, a root CLAUDE.md for Anthropic-specific workflows, and subtree files for high-risk areas like infra, auth and migrations [S02-C022]. A practical starting size is a 150–250 line root file, measuring rework, review noise and token use before and after [S02-C044].

Treat instruction files as executable policy: audit them for embedded secrets, stale commands and over-broad permissions, because they materially change agent behaviour despite being plain markdown [S02-C021]. They are low-risk as static text, but there is no enforcement mechanism — if agents ignore or truncate them, behaviour drifts [S03-C041].

## Orchestration Patterns and Delegation

BuilderIO/skills (/efficient-fable, /efficient-frontier) is rated the single most on-target artefact for a personal frontier-AI workflow because it directly encodes frontier-as-judge delegation [S01-C017]. The /efficient-fable skill keeps decomposition, architecture, tradeoffs, synthesis, risk and final review on the frontier model, pushes repo scanning, doc summarisation, log reduction, browser checks and bounded patches to lighter agents, and tells the orchestrator to verify important delegated claims before relying on them [S01-C019]. /efficient-frontier is the model-neutral variant for any high-cost model [S01-C023].

Delegation runs on self-contained handoff packets: repo path, exact objective, in/out of scope, expected evidence, verification commands and stop conditions, so workers need no hidden context from the orchestrator chat [S01-C020]. Skip delegation for tiny fixes, highly coupled edits and judgment-sensitive debugging [S01-C021]. The installer's --update-instructions flag writes the delegation convention into AGENTS.md/CLAUDE.md, so review the diff [S01-C022]. Both S01 and S02 flag the BuilderIO pattern as on-target but young — ~43 stars, 12 commits, no visible LICENSE, tiny adoption — to be forked as a pattern, not relied on as a dependency [S01-C018] [S02-C023]. The companion /stay-within-limits skill explicitly supports Fable, checking 5-hour and weekly usage and pausing new execution at 95% [S01-C077].

The most repeatable coding pattern is architect-worker-reviewer-judge: the architect produces plan and test strategy, workers execute bounded subtasks in separate worktrees, a reviewer checks diffs, tests and design conformance, and a final judge writes the human-facing summary with unresolved risks [S02-C034]. A complementary Fable-as-judge pattern has Fable 5 plan multi-step tasks and evaluate cheaper agents' outputs via DeepEval or custom LLM-as-judge loops [S03-C044]. The recommended model split: Fable 5 for long-horizon planning and final review; Opus 4.8 as default strong judge when retention or price matter; Sonnet-class or cheaper for bounded bulk work [S02-C011], with multi-tier routing via Deep Agents or LiteLLM-proxied deployments making the tiers easy to wire [S03-C042].

## Harnesses, SDKs and Frameworks

Claude Code is the primary Fable 5 harness — CLAUDE.md persistent context, skills, subagents in isolated context, experimental agent teams, hooks, MCP and plugins — and the Claude Agent SDK exposes the same machinery programmatically; S03 ranks the Agent SDK the single highest-value system for a personal frontier workflow [S01-C027] [S02-C013] [S03-C009]. The Python SDK installs via pip with a bundled Claude Code CLI binary (SDK MIT-licensed, CLI under Anthropic terms) [S03-C010], and can be pointed at non-Anthropic providers by setting ANTHROPIC_BASE_URL/ANTHROPIC_API_KEY to a LiteLLM proxy while keeping the same agent code [S03-C011]. Anthropic also supports self-hosted sandboxes for Managed Agents at enterprise scale [S02-C043]. One open question: no official public per-feature Claude Code × Fable 5 compatibility matrix existed at launch [S02-C012].

Security notes for the harness layer: a Claude Code RCE via poisoned repository config files was disclosed by Check Point in February 2026 [S01-C028], and exposing Claude Code as an MCP server controllable by other models is a documented community pattern but high risk, since it exposes remote code execution via MCP and needs strict least-privilege plus human-in-the-loop controls [S03-C040].

LiteLLM is the best current neutral gateway — routing, fallbacks, logging and cost control, including in front of Claude Code via an alternate base URL [S02-C015]. It must be treated as critical infrastructure: it disclosed a malicious PyPI wheel incident in March 2026 and carries a 2026 SQL injection advisory in its proxy key verification, so pin versions and monitor advisories [S02-C016]. A good deployment exposes named routes (frontier_judge, cheap_researcher, bulk_test_runner, safe_browser_agent) with model allowlists, token ceilings and logging policy [S02-C017].

Among frameworks: PydanticAI's capability system plus the Harness library packages instructions, model settings, tools and hooks into composable capability objects — the clearest framework expression of capability engineering [S02-C018]. LangGraph remains the clearest stateful graph framework for planner-worker-reviewer patterns with durable state, though 2026 issues still show routing, persistence and stopping-condition problems on long-horizon work [S02-C019]. Agent-MCP is an early multi-agent orchestration framework built as an MCP server with a shared knowledge graph, needing sandboxing and network controls [S03-C043]. DSPy offers structured signatures and optimiser loops for repeatable quality gains beyond manual prompt edits [S02-C042].

## MCP and Tool Ecosystems

MCP, originated at Anthropic and now under the Linux Foundation, is the de facto standard for model-neutral tool connectivity, with official SDKs in roughly ten languages, an inspector tool and a growing registry [S03-C006]; AAIF governance of MCP and AGENTS.md is corroborated by S01's account of the foundation's launch [S01-C013]. Servers expose three primitives — tools, resources and prompts — over a JSON-RPC-style protocol, and MCP security posture is only as good as each server implementation and host configuration [S03-C007]. The resources abstraction doubles as a context-engineering primitive, exposing documents and databases without bespoke retrieval schemas [S03-C047].

MCP is also the central new supply-chain risk: February–March 2026 saw the Claude Code repo-config RCE, 1,184 malicious skills on one marketplace, and hundreds of unauthenticated exposed MCP servers, making least-privilege, gateways and injection testing mandatory [S01-C073]. ToolHive (Stacklok) runs MCP servers in containers with named permission profiles and audit logging, converting MCP access from advisory prompt text into an enforced execution boundary, and the same least-privilege-per-server principle (separate read-only from write-capable servers, credentials from secure stores) is recommended independently [S01-C044] [S03-C048]. Remote MCP registries like Smithery are useful for distribution, but hosted servers and credential flows are a separate trust boundary deserving case-by-case review [S02-C032].

## Context Engineering and Token Efficiency

Chroma's "Context Rot" report (Hong et al., 2025) tested 18 frontier models and found performance grows increasingly unreliable as input length grows [S01-C011]. Anthropic's guidance names compaction the first lever, alongside observation masking, repo/dependency maps, selective loading and budgeting by fill percentage [S01-C012]; in practice, trigger compaction at roughly 60% context fill, hand-curate instruction files, and use subagents for heavy-context reads [S01-C061].

The native cost stack — token counting, prompt caching, half-price batch — rewards separating stable context (repo rules, skills, rubric: cache it) from volatile context (diffs, logs: summarise it) [S02-C028]. Tooling: claude-context-mode routes verbose shell/log/test/browser output through sandboxed tools claiming up to 98% token reduction (medium risk, it executes commands) [S01-C042]; Caveman strips narration for ~65% average output token reduction and compresses CLAUDE.md ~46% [S01-C043]; Context7 fetches current library docs to kill hallucinated APIs, Repomix produces bounded repo exports, MarkItDown converts files [S02-C030].

## Browser and Computer-Use Agents

Playwright MCP's accessibility-tree snapshots run 2–5KB versus 100KB+ screenshots (20–50x cheaper context), and the CLI variant saving YAML snapshots to disk uses ~4x fewer tokens again [S01-C031]; MCP mode suits persistent exploratory automation, CLI mode suits coding agents, and the project is actively maintained (v0.0.76 on 10 June 2026) [S02-C024]. Its origin allowlists are not a security boundary — use a separate browser profile and never production credentials [S01-C032] — and a public March 2026 issue documents a prompt-injection-to-arbitrary-code-execution path, so lock down capabilities and never attach it to high-trust sessions by default [S02-C025].

Browser Use is stronger for more autonomous browser work and offers MCP mode (start it sandboxed); Stagehand is worth watching for hybrid natural-language-plus-code automation [S02-C041]. browser-use itself is MIT, Playwright-based, with Python library, CLI, Web UI, optional cloud and a Claude Code skill installed into ~/.claude/skills [S03-C018]. Its cloud can see visited URLs and content, so self-host for sensitive work, and any agent reading arbitrary web pages remains injectable via page content [S03-C019].

## Evaluation and Red Teaming

promptfoo, Garak, PyRIT and DeepTeam form a mature open-source red-team stack, with LLM Guard, NeMo Guardrails and Llama Guard at runtime [S01-C015]. promptfoo (MIT, local-first, YAML evals, CI/CD, OWASP presets) is the consensus primary regression gate across all three sources — though not sufficient alone for full frontier agent evaluation, which needs task sandboxes and multi-turn scenarios — and it agreed to be acquired by OpenAI on 9 March 2026 while remaining open source, reporting 350k+ developers and Fortune-500 adoption [S01-C029] [S02-C026] [S03-C020]. A practical start: wire the OWASP preset against your system prompt, assert no leakage, and add a regression test for every injection fixed [S01-C030].

Garak (Apache-2.0) is the broad probe scanner for injection, leakage, encoding and jailbreaks; PyRIT (MIT) orchestrates multi-turn attack chains (Crescendo, TAP, Skeleton Key) that single-shot scanners miss, and is explicitly an augment to — not a replacement for — manual red teaming [S01-C033] [S03-C023]. Both generate harmful prompts by design: run them only against non-production or dedicated red-team endpoints with strict egress controls and legal review for third-party targets [S03-C024]. Recommended cadence: promptfoo per PR, Garak per release, PyRIT quarterly, tracking vulnerable-probe counts trending down [S01-C034]. In the eval loop, a delegated patch is not accepted by the orchestrator until promptfoo passes [S01-C062].

For richer evaluation: Inspect AI (UK AISI) is the best open framework for serious agent evaluation, and inspect-swe puts real coding agents like Claude Code into the eval loop [S02-C027]. DeepEval's G-Eval runs LLM-as-judge with chain-of-thought in a two-stage scored process with pytest integration [S03-C021]. Ragas supplies RAG-specific metrics (faithfulness, answer relevancy, context recall/precision) that separate retrieval quality from generation quality [S03-C022].

## Guardrails and Design Differentiation

LLM Guard is a commercial firewall that detects and redacts PII, secrets and adversarial content, but it becomes a chokepoint that must itself be audited for logging, retention and policy correctness [S03-C039]. (The sources disagree on NeMo Guardrails' production readiness; see Conflicts.)

For design quality: Hallmark (MIT, Together AI) is an anti-AI-slop skill with build/audit/redesign/study verbs, 65 pre-ship gates, project memory and design-DNA extraction emitting portable design.md [S01-C035] — but its gates are prompt-encoded rules, not a compiled validator, so enforcement depends on the model following instructions [S01-C036]. DESIGN.md gives agents persistent design memory so UI does not drift toward generic styling [S01-C037], and S02 independently recommends the same design-memory-plus-critic-layer pattern while noting the evidence is emergent [S02-C035].

## Coding Agent Landscape

OpenHands is the strongest open platform: MIT core (enterprise components separately licensed), Docker-sandboxed, SDK/CLI/GUI, Kubernetes-ready, any LLM via LiteLLM, with active CVE patching [S01-C075] [S03-C017]. Aider remains a clean git-native terminal agent but its cadence is slowing and its model guidance is stale [S01-C074]. Churn is real: Roo Code archived May 2026, Gemini CLI retiring June 2026, OpenCode dropped Claude Pro/Max login after a dispute — check last-commit dates before adopting anything [S01-C072], and Continue's main repo is now read-only, making it a weak bet for new builds [S02-C031].

Superpowers (obra/superpowers, MIT) installs a seven-stage methodology as composable skills [S01-C038], benchmarked at ~9% cheaper / ~14% fewer tokens but only in a 12-session test, so directional only [S01-C039]. It is genuinely risky: its own author calls the installer "literally a prompt injection and remote code execution toolkit" — it fetches and executes remote instructions and edits ~/.claude/CLAUDE.md with a SessionStart hook [S01-C040]. Read it in a sandbox VM only, and prefer hand-porting individual skills over running the installer [S01-C041].

## Security Audit Process

Treat every skill, MCP server and plugin as executable, prompt-injectable supply-chain risk: audit licence, maintainers, activity, scripts, network calls and permissions before trialling, and start every new tool sandbox-first in a disposable VM or container with no client data or production credentials [S01-C003] [S02-C036]. The full gate is staged: S01 prescribes nine steps (read-and-classify, sandbox, secrets isolation, dependency review, permission review, network monitoring, injection testing, retention review, sign-off), S03 a five-phase equivalent (inventory/triage, static review with SBOM and SCA, sandboxing design, behavioural testing, governance integration), and S02 five promotion gates (controlled environment, least-privilege credentials, understood egress, documented telemetry/retention, observed failure modes) [S01-C063] [S03-C034] [S02-C037].

Concrete controls: Docker hardened with read_only, cap_drop ALL, no-new-privileges and internal networking, MCP under ToolHive starting from the none profile [S01-C064]; throwaway read-only tokens only, no keys in skill/MCP config, scan for .env read attempts [S01-C065]; block all egress by default, allowlist hosts/ports, alert on unexpected destinations [S01-C066]. Injection testing should combine the promptfoo OWASP preset, Garak probes and a PyRIT multi-turn run, specifically covering indirect injection via tool/RAG/browser content [S01-C067], simulating malicious docs, poisoned pages, tool descriptions and instruction overrides to check whether hostile content can expose secrets or trigger unauthorised actions [S02-C038]. End-to-end, every high-trust action and merge stays behind human approval, with a UI showing plan, actions, diffs, eval scores and guardrail interventions, and instruction files updated like code when repeated issues appear [S03-C033].

## Recommended Architecture

Design so any new frontier model is a one-line swap [S01-C002]. The three sources converge on the same layered blueprint — S01's ten layers, S02's seven elements and S03's seven layers all comprise: a frontier orchestrator/judge; cheaper bounded workers; portable skills and instruction artefacts; MCP tools behind a least-privilege gateway; browser automation; context engineering with compaction; an eval loop where nothing merges until gates pass; security guardrails; visual recap with human approval; and cost controls (caching, effort dial, batch, model tiering) — plus, in S03's framing, an explicit observability and governance layer with tracing, SIEM integration and key management [S01-C060] [S02-C033] [S03-C032].

## Trial Roadmap

All three sources prescribe the same six phases: (1) read and classify the shortlist, recording licence, maintenance and risk; (2) sandbox install of the core blocks; (3) toy workflow on a throwaway repo, measuring tokens and failure points; (4) real but non-sensitive workflow with the eval gate active; (5) customise and combine — fork skills private, parameterise the model id, add design memory and least-privilege MCP; (6) document the repeatable operating model [S01-C068] [S02-C039]. The end product is a living playbook — approved tool/model combinations, standard skills and instruction files, eval suites with minimum scores, incident response steps — reviewed as classifiers and tools change; the playbook, not the model wiring, is the durable asset [S03-C036].

## Evidence Quality

Several figures across the sources — large OSS star counts, Superpowers' token-saving percentage — come from secondary sources or small samples and are directional, not definitive [S01-C070]. S03 applied the same discipline, explicitly treating early-stage, closed-source or marketing-described projects as medium maturity and higher audit priority [S03-C037].

## Conflicts

**G007 — Umbrella terminology.** The sources genuinely disagree on what to call the discipline. S01 recommends "Frontier AI Orchestration" as the headline term, with Context Engineering, Agentic Workflow Engineering and AI Capability Engineering nested beneath it [S01-C004]. S02 recommends "Frontier AI Capability Engineering" (short form "Capability Engineering"), explicitly arguing it is broader than context engineering and more durable than orchestration framings [S02-C004]. S03 inverts S01's hierarchy: "AI Capability Engineering" is the umbrella, with "Frontier AI Orchestration" and "Context Engineering" as subordinate sub-disciplines [S03-C008]. Two of three sources favour a capability-engineering umbrella, but the disagreement is recorded, not resolved.

**G029 — NeMo Guardrails production readiness.** S01 reports that NeMo Guardrails carries NVIDIA's own beta disclaimer that it is not production-ready as-is, requiring defence-in-depth rather than reliance on it [S01-C071]. S03 instead rates it high maturity — v0.20.0 (January 2026), Apache-2.0, actively maintained, with broad provider integrations [S03-C038]. Both can be simultaneously true (an actively maintained project can still carry a beta disclaimer), but the sources' maturity assessments point in opposite directions and are logged as a conflict.

## Gaps

- No official public per-feature compatibility matrix for Claude Code on Fable 5 existed at launch; per-feature rollout remains an open operational question (noted by S02).
- All three sources have unknown authorship and authority tier; no claim could be weighted by source authority, so corroboration count is the only strength signal.
- Skills/design-memory patterns (DESIGN.md, Hallmark, design critics) rest on emergent, community-led evidence rather than large public case studies.
- Pricing, plan-inclusion dates, routing behaviour and retention policy are all dated 9–11 June 2026 snapshots and decay quickly; reconfirm on platform.claude.com before relying on them.
- The sources do not cover fine-tuning, local model deployment, or non-Claude frontier models (GPT-5.x, Gemini) in comparable depth; the toolkit is Claude-centric.

## Appendix: Source Register

| Source | Title | Authority | Authored | Content hash |
| --- | --- | --- | --- | --- |
| S01 | Frontier AI Orchestration: A Practical, Security-Audited Toolkit for Building Your Own Workflow | unknown | unknown | 7ba9474ce8b8 |
| S02 | Frontier AI Capability Engineering for Claude Fable 5 and Beyond | unknown | unknown | 4e23a8418870 |
| S03 | Frontier AI Orchestration Toolkit: Systems, Skills, MCP Ecosystem, and Claude Fable 5 Workflows (2024–2026) | unknown | unknown | ff16e31eb6c0 |
