"""Per-engine adapters for the engine-agnostic front-end (ADR-019).

An adapter is the thin, declarative knowledge the launcher needs to treat an AI
engine as a SubstrateOS kernel: which binary to launch, where its instruction
file lives (the compile target), its skills directory, and the flags that map
the engine-neutral "full-auto" permission posture onto that engine.

Adding a new engine = adding one entry here; nothing else in the Base changes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineAdapter:
    name: str
    binary: str
    instruction_file: str  # project-relative path the spec compiles to
    skills_dir: str | None
    full_auto_flags: tuple[str, ...]  # posture=full-auto -> these flags


# Built-in adapters. Permission flags are the real, current flags per engine.
ADAPTERS: dict[str, EngineAdapter] = {
    "claude": EngineAdapter(
        "claude", "claude", "CLAUDE.md", ".claude/skills",
        ("--dangerously-skip-permissions",),
    ),
    "codex": EngineAdapter(
        "codex", "codex", "AGENTS.md", ".agents/skills",
        ("--dangerously-bypass-approvals-and-sandbox",),
    ),
    "gemini": EngineAdapter(
        "gemini", "gemini", "GEMINI.md", ".gemini/skills", (),
    ),
    "cursor": EngineAdapter(
        "cursor", "cursor", ".cursor/rules/substrateos.mdc", ".cursor/skills", (),
    ),
}


def get_adapter(name: str) -> EngineAdapter:
    try:
        return ADAPTERS[name]
    except KeyError as exc:
        available = ", ".join(sorted(ADAPTERS))
        raise KeyError(f"unknown engine '{name}' (have: {available})") from exc
