"""Capability handshake for the engine-agnostic front-end (ADR-019).

On activation an engine reports what it can do "as SubstrateOS": the MUST tier
always holds (enforced by the labctl harness regardless of model); the SHOULD
tier maps ergonomic features to each engine's native capabilities, with
graceful degradation and honest self-report of gaps.
"""

from __future__ import annotations

from dataclasses import dataclass

from labctl.engines import EngineAdapter

# MUST tier — mirrors substrate/methodology.md. Enforced by the harness on any
# engine, so it holds even where the engine is otherwise weak.
MUST: tuple[str, ...] = (
    "Drive labctl; never route around the harness.",
    "Never bypass the seven-stage release gate.",
    "Respect capsule isolation and memory namespaces.",
    "Honour the review queue (AI-derived content unpromoted until approved).",
    "Stay within the token circuit-breaker budget.",
    "No secrets in any file; no new heavyweight frameworks.",
    "Report honestly; self-report capability gaps.",
)

# SHOULD-tier ergonomic feature -> the engine capability it needs.
SHOULD_FEATURES: dict[str, str] = {
    "in-session activation (/substrateos)": "slash_commands",
    "sub-agent orchestration": "subagents",
    "session-start hooks + banner": "hooks",
    "native MCP tool integration": "mcp",
}


@dataclass
class Handshake:
    engine: str
    must: list[str]
    should: list[tuple[str, str, str]]  # (feature, "native"|"degraded", capability)
    gaps: list[str]


def build_handshake(adapter: EngineAdapter) -> Handshake:
    should: list[tuple[str, str, str]] = []
    gaps: list[str] = []
    for feature, cap in SHOULD_FEATURES.items():
        native = cap in adapter.capabilities
        should.append((feature, "native" if native else "degraded", cap))
        if not native:
            gaps.append(feature)
    return Handshake(adapter.name, list(MUST), should, gaps)


def render_handshake(hs: Handshake, *, mode: str = "cold") -> str:
    lines = [f"SubstrateOS active — {hs.engine} ({mode})"]
    lines.append("MUST (enforced by labctl on any engine):")
    lines += [f"  - {m}" for m in hs.must]
    lines.append("SHOULD (native vs degraded on this engine):")
    lines += [f"  - [{status}] {feature}" for (feature, status, _cap) in hs.should]
    if hs.gaps:
        lines.append("gaps (degrade gracefully): " + ", ".join(hs.gaps))
    if mode == "warm":
        lines.append(
            "warm mode: permission mode / MCP servers / session-start hooks cannot "
            "be retro-enabled — relaunch via `subos` for full integration."
        )
    return "\n".join(lines)
