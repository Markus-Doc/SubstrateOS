# Research v2 → Whole-Repo Impact Assessment

Date: 2026-06-13
Author: Branch-2 deep-consideration session (Opus 4.8)
Status: Analysis only — no code changes; proposes ADRs, implements none.

## Purpose

Answer one question: **does the new master research (v2,
`docs/research/master-research.md`, RESYNTH, 66 sources) mandate any changes to
the overall SubstrateOS repo?** This de-risks the branch-1 multi-agent build-out
by confirming the base before more is built on it.

Inputs read in full: `docs/research/master-research.md`; every ADR
(001–021); `docs/architecture/system-overview.md`; `docs/planning/phase-2-plan.md`
and `open-questions.md`; the live gate implementation (`scripts/labctl/gate.py`)
and provider seam (`scripts/labctl/providers.py`) to ground claims in code.

Verdict legend (per the handoff brief):

- **CONFIRMS** — research independently validates the existing choice; no action.
- **REFINES** — choice stands, but research adds detail worth folding in.
- **CONTRADICTS** — research points the other way; reconcile or log a divergence.
- **GAP** — research treats something as standard/important that the repo does
  not yet address.

---

## Bottom line (read this first)

**The base is sound. v2 mandates no architecture rewrite and exposes no genuine
contradiction with the hard constraints.** Every apparent contradiction
(LangGraph/AutoGen in `## Agent Frameworks`; vLLM/Ollama in `## Model Serving`;
Postgres MCP server in `## Mcp`) is already pre-adjudicated by a deliberate ADR
(ADR-002, ADR-017, ADR-001) and the research lists these as *options*, never
mandates. So nothing forces a change.

What v2 *does* surface is **five things worth a decision**, in priority order:

1. **Model default should flip from Fable 5 to Opus 4.8** (P1). Fable 5 is
   *suspended* as of 2026-06-12, mandates 30-day retention with no zero-retention
   option, costs 2×, and reroutes cyber/bio/chem to Opus 4.8 anyway — and this is
   a security engineer's harness. ADR-019 already makes the model a swappable
   kernel, so this is a default-selection ADR, not architecture. (This very
   session runs on Opus 4.8 for exactly these reasons.)
2. **A supply-chain audit gate for skills / MCP servers / plugins** (P1).
   v2 is emphatic that every skill/MCP/plugin is executable, prompt-injectable
   supply-chain risk (`## Red Teaming`, `## Gh Skill`, `## Least Privilege`).
   ADR-019 adopts SKILL.md/AGENTS.md as compile targets and the Base will host
   skills, yet no gate stage audits third-party tool provenance before it runs.
3. **An MCP tool seam for labctl capabilities** (P2). v2 treats MCP as *the*
   model-neutral tool seam; SubstrateOS exposes capabilities (memory, web, usage)
   as in-process Python providers but not yet as engine-portable tools. In-process
   MCP servers (`## Claude Agent Sdk`) bridge this without standing up daemons or
   breaking ADR-009's "defer external MCP."
4. **The trace half of the trace-and-evaluation layer** (P2). v2 calls trace+eval
   "non-optional in 2026" (`## Agent Stack`). The gate has the *eval* half
   (promptfoo, ADR-012) but no *tracing* / agentic metrics — exactly what Phase 2's
   Dynamic Workflows (architect→workers→reviewer→judge) will need to be auditable.
5. **Log two deliberate divergences** (P3) so the next audit scores them as
   decisions, not drift: (a) engine-neutrality via compile-many adapters *instead
   of* a LiteLLM proxy (`## Litellm`), and (b) a thin `labctl` orchestrator
   *instead of* a discrete "agent framework" layer (`## Agent Stack`).

Items 1, 2, and 5(a) touch the security posture directly and should land before
the branch-1 multi-agent build adds skills and engines on top of the base.

---

## Part 1 — Architecture layers vs v2

SubstrateOS has five layers (`system-overview.md`) plus a cross-cutting security
gate. v2 describes a **six-layer 2026 stack** (`## Agent Stack`: model serving,
model, agent framework, retrieval+memory, tooling+integration,
trace+evaluation) and a **buildable stack** (`## Architecture`: model router,
local coding agent, repo-resident instruction packs, browser tool, eval harness,
security gate). Mapping one onto the other is the cleanest way to see the gaps.

| SubstrateOS layer | v2 counterpart | Verdict | Finding (cited) |
|---|---|---|---|
| **1. Lab Controller** (`labctl`) | "agent framework" layer + model router (`## Agent Stack`, `## Architecture`, `## Ai Orchestration`) | **CONFIRMS / REFINES** | v2's core thesis — "usage is defined more by how well teams orchestrate models, tools, and evaluations than by which single model they pick" (`## Ai Orchestration`) — directly validates a durable harness underneath replaceable engines. **Divergence to log:** SubstrateOS deliberately makes `labctl` a *thin* orchestrator, not a discrete framework library; v2 lists frameworks as options, not requirements, so this is defensible (see Part 4). |
| **2. Ingestion Pipeline** (Firecrawl + Docling) | retrieval+memory / tooling (`## Architecture`, browser tool) | **CONFIRMS / GAP** | Firecrawl-cloud-behind-a-provider (ADR-005) matches v2's "add cloud agents and remote MCP servers only after every permission boundary can be audited" caution (`## Architecture`). **GAP:** v2's buildable stack names a *browser tool* (Browser Use / Playwright, `## Browser Use`, `## Browser Automation`); SubstrateOS has none. Low priority — Firecrawl covers extraction and a browser tool is a capsule/engine capability, not a base requirement. |
| **3. Memory Layer** (SQLite FTS5, BM25) | retrieval+memory (`## Agent Stack`) | **CONFIRMS** | v2 offers no claim that contradicts SQLite-first. Agent-MCP's shared-SQLite design (`## Agent Mcp`) is explicitly flagged AGPL-3.0 + maintenance-paused-since-Sept-2025 → SubstrateOS's in-house `SQLiteMemory` + `MemoryProvider` seam (ADR-009) is the safer call. Hybrid/vector deferral (ADR-017) untouched by v2. |
| **4. Capsules** (devcontainers) | sandboxed execution (`## Openhands`, `## Model Agnostic`, `## Architecture`) | **CONFIRMS** | v2 strongly validates sandboxed, isolated execution: OpenHands "native sandboxed execution," "optional isolation, local by default, sandboxable," Docker/K8s (`## Comparison`, `## Architecture`, `## Model Agnostic`). Confirms ADR-014 isolation and ADR-015's plan to move execution in-container (Phase 2 M4). |
| **5. Execution Engines** (Claude Code, Codex) | model + model serving (`## Agent Stack`, `## Claude Fable 5`) | **CONFIRMS / CONTRADICTS-default** | "Treated as replaceable, no vendor lock-in" is confirmed by v2's model-neutral theme and validated by ADR-019. **But** the *named default* (Fable 5) is contradicted by current facts: suspended 2026-06-12 (`## Availability`), 30-day retention (`## Claude Fable 5`), cyber rerouting to Opus 4.8 (`## Cybersecurity`). → P1 model-default ADR. Model serving (vLLM/Ollama, `## Model Serving`) stays correctly out of scope (no local inference). |
| **Security Gate** (6 stages) | trace+evaluation + security gate (`## Agent Stack`, `## Evaluation`, `## Red Teaming`) | **CONFIRMS / GAP** | The *eval* half is present and well-grounded (promptfoo, ADR-012; cadence promptfoo-per-PR / Garak-per-release / PyRIT-quarterly matches `## Evaluation`). **Two GAPs:** (a) no *trace* / agentic-metrics layer though v2 calls it "non-optional in 2026" (`## Agent Stack`, `## Agentic Metrics`); (b) no *supply-chain* audit of skills/MCP/plugins though v2 demands it (`## Red Teaming`, `## Gh Skill`). |
| **Tooling/Integration** (no dedicated layer; providers) | tooling+integration / MCP seam (`## Mcp`, `## Integration`, `## Claude Agent Sdk`) | **GAP** | This is the v2 layer SubstrateOS most under-builds. v2 treats MCP as the de-facto model-neutral tool seam; SubstrateOS has in-process Python providers but exposes no engine-portable tool interface. In-process MCP servers (`## Claude Agent Sdk`: "Custom tools are implemented as in-process MCP servers that run directly within the Python application") are the constraint-respecting bridge. → P2 MCP-seam ADR. |

**Layer-level conclusion:** SubstrateOS cleanly covers four of v2's six layers,
*deliberately* omits model-serving (rejected), and has real GAPs in the
**tooling/integration (MCP) layer** and the **trace half of trace-and-evaluation**.
No layer needs rearchitecting.

---

## Part 2 — ADR-by-ADR matrix

| ADR | Subject | Verdict | Finding (cited) |
|---|---|---|---|
| 001 | SQLite over Postgres | **CONFIRMS** | v2 mentions a Postgres MCP server (`## Mcp`) only as a pre-built connector, never mandates Postgres. SQLite-first stands. |
| 002 | No LangChain/LangGraph/AutoGen | **CONFIRMS (apparent-contradiction, adjudicated)** | `## Agent Frameworks` *lists* LangGraph/CrewAI/AutoGen/MS Agent Framework as options — surface tension only. v2's own spine ("model-neutral orchestration… lets any new frontier model drop in with a one-line change," `## Agents Md`; thin frontier-as-judge layering, `## Ai Orchestration`) actively supports the thin-harness choice. No change. |
| 003 | MCP as memory interface | **REFINES** | Direction confirmed (MCP is the portable seam, `## Mcp`). Refinement: the *in-process* MCP server pattern (`## Claude Agent Sdk`) lets the existing `SQLiteMemory` be MCP-exposed without an external daemon — ties into the P2 MCP-seam ADR. |
| 004 | agentmemory optional, not source of truth | **CONFIRMS** | v2's supply-chain caution (`## Red Teaming`) and Agent-MCP's AGPL/maintenance risk (`## Agent Mcp`) reinforce keeping any external memory server optional behind a provider. |
| 005 | Firecrawl cloud, metered, behind provider | **CONFIRMS** | Matches "add cloud/remote services only after permission boundaries can be audited" (`## Architecture`). Provider seam is exactly the audit point. |
| 006 | Lab Controller = Typer CLI | **CONFIRMS** | No v2 claim disturbs a Python CLI orchestrator. The CLI *is* the auditable control plane v2 wants. |
| 007 | Devcontainers WSL2-first | **CONFIRMS** | Sandboxed Docker execution is the v2-endorsed isolation model (`## Openhands`, `## Architecture`). |
| 008 | v1 master promotion | **REFINES (already superseded)** | ADR-020 supersedes the *which/where*; v2 carries the same orchestration spine forward, so ADR-008's intent is intact. |
| 009 | Built-in SQLite FTS5; agentmemory deferred | **CONFIRMS / REFINES** | Deferral of external MCP is confirmed. Refinement: in-process MCP exposure (`## Claude Agent Sdk`) is the path to *some* MCP without contradicting "defer the external server." |
| 010 | Milestone-driven, agent-executed | **CONFIRMS / REFINES-default** | Long-running autonomous campaigns match "Fable 5 can work for days… planning across stages, delegating to sub-agents, checking its own work" (`## Agents`). Refinement: "currently Claude Fable 5" should read "currently Opus 4.8" given suspension/rerouting (P1). |
| 011 | Rename to SubstrateOS | **CONFIRMS** | "Substrate underneath replaceable kernels" is precisely v2's model-neutral framing. Naming aside, no impact. |
| 012 | promptfoo gate; Garak/PyRIT Phase 2 | **CONFIRMS / REFINES** | Cadence matches `## Evaluation` / `## Ci Cd`. Refinement: as M4/M5 give capsule agents real system prompts, activate the OWASP injection preset placeholder, and add *agentic* metrics (Task Completion, Tool Correctness, Plan Adherence — `## Agentic Metrics`) for Dynamic Workflows. Ties into P2 trace/eval ADR. |
| 013 | Dev toolchain in gate; Win+WSL2 control plane | **CONFIRMS** | The "gate tooling ≠ stack additions" reasoning is the precedent for admitting a supply-chain audit and trace tooling as *gate hygiene*, not stack growth — see P1/P2 proposals. |
| 014 | Capsules as sibling dirs | **CONFIRMS** | Isolation-by-separate-repo aligns with sandbox/least-privilege themes (`## Least Privilege`). |
| 015 | `lab build` host-scoped headless claude | **CONFIRMS / REFINES** | Headless `claude -p` stdin contract is sound. Refinement: ADR-015 already flags `--dangerously-skip-permissions` as owner-not-product policy — ADR-019's engine-neutral posture formalises this; consistent. Model name → Opus (P1). |
| 016 | Token budget circuit breaker | **CONFIRMS / minor-GAP** | Metering is good practice. Minor GAP: post-June-15 billing is a *separate Agent SDK credit bucket* (`## Billing`), not token-priced; token metering is a proxy. `labctl usage` may eventually need credit-bucket accounting, not just tokens. Low priority. |
| 017 | Lab host = remote operator, not compute | **CONFIRMS** | GTX-950M-no-compute + subscription-auth + "operate for agency not compute" aligns with model-neutral, cloud-engine framing. v2's model-serving layer (`## Model Serving`) correctly stays out of scope. |
| 018 | Telegram + RTC self-wake + Tailscale | **CONFIRMS** | Outbound-only, zero-inbound-exposure, numeric-id allowlist, stdin-only mission text is textbook least-privilege (`## Least Privilege`) and supply-chain/injection hygiene (`## Red Teaming`). No impact. |
| 019 | Base+Overlay; engine-agnostic front-end | **CONFIRMS (strongly) / REFINES** | Directly validated: "model-neutral skills + AGENTS.md/CLAUDE.md + MCP tools + an eval-and-safety gate lets any new frontier model drop in with a one-line change" (`## Agents Md`); write-once/compile-many to SKILL.md/AGENTS.md is the open standard (`## Agent Skills`). Refinements: (a) instruction budget ~150–200 (`## Agents Md`) → keep compiled CLAUDE.md lean + progressive-disclosure skills; (b) CLAUDE.md↔AGENTS.md symlink option for the compiler (`## Agents Md`); (c) the engine-neutral tool layer is MCP (P2); (d) log the LiteLLM-not-used divergence (P3). |
| 020 | v2 supersession; root declutter | **CONFIRMS** | Self-consistent; "notable findings carried forward" already names the SKILL.md/AGENTS.md, instruction-budget, supply-chain, and Fable-retention points this assessment expands into concrete proposals. |
| 021 | Scheduled research/review pipeline (Proposed) | **CONFIRMS / REFINES** | v2's rapid-change reality (promptfoo→OpenAI acquisition `## Acquisition`; Claude MCP Tools *archived* 2026-02-14 `## Archived`; AAIF formation `## Aaif`) is the case-in-point for ADR-021. Refinement: the pipeline should explicitly watch the **supply-chain advisory surface** for installed skills/MCP servers, feeding the P1 supply-chain gate. |

**No ADR requires reversal.** ADR-010/015's "currently Fable 5" phrasing is the
only place where a *current fact* (suspension/rerouting) argues for an
amendment, handled by the P1 model-default ADR.

---

## Part 3 — Special-attention deep-dives (the eight named items)

### 3.1 Multi-agent / sub-agent orchestration (frontier as planner/judge + workers)
`## Ai Orchestration`, `## Agents`, `## Multi Agent` — **CONFIRMS.** The
"frontier model as planner/architect/judge while cheaper/specialised agents
handle scanning, code edits, browser automation, bulk processing… preserves
expensive frontier tokens while keeping the whole workflow inspectable and
auditable" is *exactly* Phase 2 M5's architect→workers→reviewer→judge Dynamic
Workflow. **One refinement:** v2 advocates *tiering to cheaper models* for the
bulk worker roles; SubstrateOS currently dispatches a single frontier engine per
run. True model-tiering within one workflow is a GAP, but it collides with
subscription-auth-single-model (ADR-017) and the no-framework constraint — so it
is a Phase 3 consideration, not a Phase 2 change.

### 3.2 Trace-and-evaluation layer ("non-optional in 2026")
`## Agent Stack`, `## Agentic Metrics`, `## Deepeval` — **GAP (P2).** The gate
has the eval half. It has no *trace* half and no agentic metrics (Task
Completion, Tool Correctness, Goal Accuracy, Step Efficiency, Plan Adherence,
Plan Quality). The moment Phase 2 ships multi-step Dynamic Workflows, "did the
workflow actually follow its plan and use tools correctly?" becomes the audit
question — and stream-json run logs (ADR-015/016) are already a proto-trace to
build on. v2 names FutureAGI traceAI / ai-evaluation (Apache 2.0, "recommended
regardless of framework"). This is gate hygiene by the ADR-013 precedent, not a
stack addition.

### 3.3 MCP as the tool seam vs CLI-driving
`## Mcp`, `## Integration`, `## Claude Agent Sdk`, `## Function Calling` —
**GAP/REFINE (P2).** SubstrateOS drives the engine via the `claude` CLI and
mediates tools through filesystem + in-process Python providers. v2 treats MCP
as the de-facto portable tool seam, and crucially endorses **in-process MCP
servers** ("no subprocess management, no IPC overhead, single-process,
type-safe"). That is the bridge: expose `MemoryProvider` / `WebProvider` /
`usage` as in-process/stdio MCP servers so *any* engine reaches the same tools
identically — without contradicting ADR-009 (no external daemon) and reusing the
ADR-019 adapter pattern. Phase 2 M4 already anticipates this ("MCP exposure only
if multi-agent access truly needs it") — this finding gives that decision a home.

### 3.4 Supply-chain risk of skills / MCP / plugins
`## Red Teaming`, `## Gh Skill`, `## Least Privilege` — **GAP (P1).** The
strongest single mandate in v2: "Every skill, MCP server and plugin should be
treated as executable, prompt-injectable supply-chain risk: audit licence,
maintainers, activity, scripts, network calls and permissions, sandbox in
Docker/devcontainer, and run injection tests before any tool touches real data."
Concrete mechanisms v2 supplies: `gh skill` content-addressed provenance,
immutable releases, `--pin` to a SHA, `gh skill preview` before install
(`## Gh Skill`); ToolHive named permission profiles (none/network/custom) as an
enforced least-privilege boundary (`## Least Privilege`). SubstrateOS's gate
scans *its own* tree but audits *no third-party skill/MCP/plugin* before it runs
— and ADR-019 is about to make skills first-class. This is the highest-leverage
gap for a security engineer's harness.

### 3.5 Model choice — Fable 5 retention + cyber rerouting vs Opus 4.8
`## Claude Fable 5`, `## Availability`, `## Cybersecurity`, `## Alignment`,
`## Billing` — **CONTRADICTS the default (P1).** Facts from v2: Fable 5 access
*suspended* 2026-06-12; mandatory 30-day retention even for prior
zero-retention enterprises, no zero-retention option; reroutes
cyber/bio/chem/distillation to Opus 4.8; ~2× Opus price; usage credits required
after 2026-06-22. For a security-focused harness whose capstone is a codebase
audit, Opus 4.8 is the better *default*: no rerouting surprise, lower cost,
better-understood retention. ADR-019 already makes this a kernel swap. (The M5
plan's "frame as engineering/code-quality audits, not pentest language" is a
smart workaround, but choosing the model that does not reroute is cleaner.)
Alignment is not a concern in the swap: Fable/Mythos/Opus 4.8 show "low and
similar" misalignment (`## Alignment`).

### 3.6 June-15 headless-build billing change
`## Billing` — **CONFIRMS (already handled).** Separate monthly Agent SDK credit
bucket; non-rolling; stop-or-fall-to-API after exhaustion. ADR-017's consequence
and phase-2-plan Standing Constraints already encode stop-and-report,
never-silent-API-fallback. Only minor refinement: metering is token-based
(ADR-016) while the bucket is credit-based — a proxy, fine for now.

### 3.7 In-container execution
`## Openhands`, `## Model Agnostic`, `## Architecture`, `## Comparison` —
**CONFIRMS.** Sandboxed in-container execution is the v2-endorsed model and
validates Phase 2 M4. OpenHands' credentials (MIT, SWE-Bench SOTA, composable
SDK, model-agnostic, native sandboxing) also **confirm ADR-021's choice of
OpenHands as the execution-engine contingency** — triggered by the pipeline, not
adopted pre-emptively. No change; reinforces M4 and ADR-021.

### 3.8 (Bonus) Context engineering & advanced tool use
`## Context Engineering`, `## Advanced Tool Use`, `## Agents Md` — **REFINE.**
Instruction budget (~150–200; every token loads every request) and context-rot
findings reinforce ADR-019/020's lean-CLAUDE.md + progressive-disclosure-skills
direction (already carried forward). Anthropic's Tool Search Tool / Programmatic
Tool Calling / Tool Use Examples are Claude-specific ergonomics → they belong in
the **SHOULD tier** of ADR-019's capability handshake, not as base requirements.

---

## Part 4 — Two divergences to log (so the next audit scores them as decisions)

ADR-013 set the precedent: when the implementation defensibly differs from the
research, write it down so the next alignment audit reads it as a decision, not
drift. Two such divergences exist against v2:

1. **Engine-neutrality via compile-many adapters, not a LiteLLM proxy.**
   `## Litellm` calls LiteLLM "the best current neutral control plane for mixing
   frontier and cheap models, but its supply-chain history means it needs
   stricter auditing and sandboxing." ADR-019 instead achieves neutrality by
   compiling per-engine instruction files + CLI adapters. This is *safer* here:
   it avoids LiteLLM's flagged supply-chain risk and is compatible with
   subscription-auth-only (ADR-017), which a LiteLLM proxy (API-key-oriented)
   is not. Worth one logged paragraph.

2. **A thin `labctl` orchestrator, not a discrete "agent framework" layer.**
   v2's six-layer stack (`## Agent Stack`) names an "agent framework" layer;
   ADR-002 deliberately rejects framework libraries. v2's own spine supports the
   thin-harness choice, so this is a defensible omission rather than a missing
   layer — but stating it pre-empts a future "where's your agent-framework
   layer?" finding.

These can be a single short ADR ("logged divergences from master-research v2")
mirroring ADR-013, or footnotes in ADR-019. Either is fine; the point is the
paper trail.

---

## Part 5 — Proposed ADR backlog (prioritised; propose-only)

> All proposals respect the hard constraints: no heavyweight agent framework
> (ADR-002), no Postgres (ADR-001), no local inference, subscription-auth-only.
> Eval/trace/supply-chain tooling enters as **gate hygiene** under the ADR-013
> precedent, not as orchestration-stack growth.

| # | Proposed ADR | One-line rationale | Cites | Phase-2 scope impact |
|---|---|---|---|---|
| **P1-A** | **Default execution model = Opus 4.8; Fable 5 opt-in when restored** | Fable 5 is suspended, mandates 30-day retention, reroutes cyber, and costs 2× — wrong default for a security harness; ADR-019 makes it a kernel swap. | `## Claude Fable 5`, `## Availability`, `## Cybersecurity`, `## Billing` | None (default change); amends "currently Fable 5" in ADR-010/015/017. |
| **P1-B** | **Supply-chain audit gate for skills / MCP servers / plugins** | Every third-party skill/MCP/plugin is executable + prompt-injectable; audit provenance/license/network/scripts, pin to SHA, sandbox + injection-test before trust. | `## Red Teaming`, `## Gh Skill`, `## Least Privilege` | **Expands Phase 2** — adds a 7th gate concern. Reconcile with phase-2-plan's "keeps six stages / no red-team expansion" (this is supply-chain hygiene, *distinct* from Garak/PyRIT red-team). Owner decision needed. |
| **P2-A** | **In-process MCP tool seam for labctl capabilities** | Expose `MemoryProvider`/`WebProvider`/`usage` as in-process/stdio MCP servers so any engine reaches identical tools; no external daemon (honours ADR-009). | `## Mcp`, `## Integration`, `## Claude Agent Sdk`, `## Function Calling` | Folds into M4's "MCP exposure only if multi-agent access truly needs it"; gives ADR-019 its tool layer. |
| **P2-B** | **Trace + agentic-eval layer for Dynamic Workflows** | trace+eval is "non-optional in 2026"; multi-step workflows need Plan Adherence / Tool Correctness / Task Completion metrics over the existing stream-json run logs. | `## Agent Stack`, `## Agentic Metrics`, `## Deepeval` | Folds into M5 (Dynamic Workflows) or a small M5 addendum; extends ADR-012. |
| **P3-A** | **Log divergences from master-research v2** (LiteLLM-not-used; thin-harness-not-framework) | Pre-empts future audit "drift" findings; mirrors ADR-013. | `## Litellm`, `## Agent Stack`, `## Ai Orchestration` | None (documentation). |
| **P3-B** | **Activate OWASP injection preset once capsule agents carry system prompts** | M4/M5 give agents real prompts; the ADR-012 placeholder becomes testable; "run injection tests before any tool touches real data." | `## Red Teaming`, `## Ci Cd` | Folds into M4/M5; extends ADR-012; pairs with P1-B. |
| **P3-C** | **(Watch-list, not yet an ADR) Browser-tool capability** | v2's buildable stack names a browser tool; Firecrawl covers extraction today, so this is a deferred capsule/engine capability. | `## Browser Use`, `## Browser Automation`, `## Architecture` | Out of Phase 2 scope; candidate for the ADR-021 watch-list. |

### Phase-2 scope flags (explicit)

- **P1-B (supply-chain gate) is the one proposal that changes Phase 2 scope.**
  phase-2-plan locks "the release gate keeps its six stages" and "no red-team
  expansion." A supply-chain *audit* is not red-team (it is provenance + license
  + injection hygiene before a tool runs), but it *is* new gate surface — so it
  needs an explicit owner decision: add it as a Phase 2 stage, or schedule it as
  the first Phase 3 / ADR-021-triggered item. **Recommendation:** land at least a
  minimal provenance/pin check in Phase 2, because ADR-019's skill compilation
  ships *in* the base that branch-1 builds on.
- **P1-A, P2-A, P2-B, P3-A/B fold into existing milestones or are
  documentation-only** — no scope expansion.

---

## Part 6 — Constraints & contradictions check

- **No genuine contradiction with the hard constraints.** `## Agent Frameworks`
  (LangGraph/AutoGen), `## Model Serving` (vLLM/Ollama), and the Postgres MCP
  connector (`## Mcp`) are *options* in v2, each already adjudicated by ADR-002 /
  ADR-017 / ADR-001. v2's own orchestration spine supports those rejections.
- **No new heavyweight framework is proposed.** Every proposal is gate/tooling
  hygiene (ADR-013 precedent) or a default/documentation change.
- **Subscription-auth-only is preserved** by every proposal (notably P1-A and the
  LiteLLM divergence in P3-A).
- **Gate stays green:** this report is a single Markdown file under
  `docs/planning/` — it touches no code, secret, dependency, or eval config, so
  `secret-scan / lint / tests / sast / vuln-scan / evals` are unaffected.

## Definition-of-done check

- [x] Read `master-research.md` in full, every ADR (001–021),
      `system-overview.md`, plus phase-2-plan / open-questions and the live gate
      code for grounding.
- [x] Per-layer and per-ADR CONFIRMS / REFINES / CONTRADICTS / GAP matrix with a
      cited research section for every finding.
- [x] All eight special-attention items addressed.
- [x] Prioritised proposed-ADR backlog; propose-only, hard constraints respected.
- [x] Phase-2 scope impact flagged (P1-B is the one scope-changer).
- [x] No code changes; gate remains green.
