"""Per-engine adapters for the engine-agnostic front-end (ADR-019).

An adapter is the thin, declarative knowledge the launcher needs to treat an AI
engine as a SubstrateOS kernel: which binary to launch, where its instruction
file lives (the compile target), its skills directory, and the flags that map
the engine-neutral "full-auto" permission posture onto that engine.

Adding a new engine = adding one entry here; nothing else in the Base changes.
"""

from __future__ import annotations

from dataclasses import dataclass


# Capability vocabulary used by the handshake (labctl/handshake.py).
CAPABILITIES = ("slash_commands", "subagents", "hooks", "mcp")


@dataclass(frozen=True)
class EngineAdapter:
    name: str
    binary: str
    instruction_file: str  # project-relative path the spec compiles to
    skills_dir: str | None
    full_auto_flags: tuple[str, ...]  # posture=full-auto -> these flags
    capabilities: frozenset[str] = frozenset()  # native SHOULD features
    warm_command_file: str | None = None  # where /substrateos compiles to


# Built-in adapters. Permission flags are the real, current flags per engine;
# capabilities reflect each engine's native SHOULD-tier features (handshake).
ADAPTERS: dict[str, EngineAdapter] = {
    "claude": EngineAdapter(
        "claude", "claude", "CLAUDE.md", ".claude/skills",
        ("--dangerously-skip-permissions",),
        capabilities=frozenset({"slash_commands", "subagents", "hooks", "mcp"}),
        warm_command_file=".claude/commands/substrateos.md",
    ),
    "codex": EngineAdapter(
        "codex", "codex", "AGENTS.md", ".agents/skills",
        ("--dangerously-bypass-approvals-and-sandbox",),
        capabilities=frozenset({"slash_commands", "mcp"}),
        warm_command_file=".codex/prompts/substrateos.md",
    ),
    "gemini": EngineAdapter(
        "gemini", "gemini", "GEMINI.md", ".gemini/skills", (),
        capabilities=frozenset({"mcp"}),
    ),
    "cursor": EngineAdapter(
        "cursor", "cursor", ".cursor/rules/substrateos.mdc", ".cursor/skills", (),
        capabilities=frozenset({"slash_commands"}),
        warm_command_file=".cursor/commands/substrateos.md",
    ),
}


def get_adapter(name: str) -> EngineAdapter:
    try:
        return ADAPTERS[name]
    except KeyError as exc:
        available = ", ".join(sorted(ADAPTERS))
        raise KeyError(f"unknown engine '{name}' (have: {available})") from exc
