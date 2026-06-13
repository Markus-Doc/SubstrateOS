# ADR-023: Logged divergences from master-research v2

Date: 2026-06-13
Status: Accepted

## Decision

Two places where SubstrateOS's implementation deliberately differs from a
recommendation in `docs/research/master-research.md` (v2) are **logged as
decisions, not drift**, following the ADR-013 precedent. Recording them means the
next alignment / RESYNTH-pipeline audit (ADR-021) scores them as choices with a
rationale rather than flagging them as gaps.

### Divergence 1 — engine-neutrality via compile-many adapters, not a LiteLLM proxy

The master research calls LiteLLM "the best current neutral control plane for
mixing frontier and cheap models, but its supply-chain history means it needs
stricter auditing and sandboxing" (`## Litellm`; the Claude Agent SDK + LiteLLM
proxy pattern in `## Claude Agent Sdk`).

SubstrateOS instead achieves model-neutrality with **write-once / compile-many**
per-engine instruction files plus CLI adapters (ADR-019: `subos`,
`labctl/engines.py`, `labctl/compile_spec.py`). This is the safer fit here:

- It avoids LiteLLM's flagged supply-chain risk surface entirely.
- It is compatible with **subscription-auth-only** (ADR-017): a LiteLLM proxy is
  API-key-oriented, which SubstrateOS deliberately avoids.
- The neutrality boundary is an inspectable, in-repo adapter table, not an
  external routing daemon.

LiteLLM is not rejected forever — if an Overlay (ADR-019) needs API-keyed
multi-provider routing, it may add LiteLLM as an **Overlay-only**, audited and
sandboxed provider. The Base stays proxy-free.

### Divergence 2 — a thin `labctl` orchestrator, not a discrete "agent framework" layer

The master research's six-layer 2026 stack names an "agent framework" layer and
lists LangGraph / CrewAI / AutoGen / Microsoft Agent Framework as options
(`## Agent Stack`, `## Agent Frameworks`).

SubstrateOS deliberately has **no framework library layer** (ADR-002). `labctl`
is a thin Python orchestrator; multi-agent behaviour is driven by the engine's
native sub-agent support plus repo-resident skills/instruction files. The master
research's own spine supports this — "model-neutral skills + instruction files +
MCP + an eval/safety gate lets any new frontier model drop in with a one-line
change" (`## Agents Md`) and the thin frontier-as-judge layering in
`## Ai Orchestration` — so the omission is a deliberate, research-aligned choice,
not a missing layer.

## Context

Branch-2's whole-repo impact assessment
(`docs/planning/research-v2-impact-assessment.md`, proposal **P3-A**)
recommended logging both divergences so a future audit does not re-flag them.
v2 lists both LiteLLM and the framework layer as *options*, never mandates, so
neither divergence is a contradiction — only an un-recorded choice until now.

## Consequences

- The ADR-021 research/review pipeline can diff against this record and skip
  re-raising "why no LiteLLM?" / "where is the agent-framework layer?".
- If either premise changes (subscription-only constraint relaxes; a framework
  becomes the only way to hit a required capability), this ADR is the
  amendment point.
- No code change accompanies this ADR; it is a pure decision record.
