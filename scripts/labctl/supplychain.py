"""Supply-chain audit (M-F, P1-B): vet skills/MCP/plugins before they run.

The master research is emphatic that every skill, MCP server, and plugin is
executable, prompt-injectable supply-chain risk and must be audited (licence,
maintainers, scripts, network, permissions) and sandboxed before it touches real
data. This module discovers third-party tools declared in the repo and flags any
that are not on the audited allowlist (``substrate/trusted-tools.json``).

The Base ships blank — no third-party skills, an empty allowlist — so the audit
finds nothing and the gate stays green when SubstrateOS runs naked. Findings
appear only once an Overlay or installed skills introduce unvetted tools.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

SKILLS_DIRS = (".claude/skills", ".agents/skills", ".gemini/skills", ".cursor/skills")
ALLOWLIST_REL = "substrate/trusted-tools.json"
MCP_CONFIG_REL = ".mcp.json"


@dataclass
class AuditResult:
    scanned: int
    findings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.findings


def _load_allowlist(root: Path) -> set[str]:
    path = root / ALLOWLIST_REL
    if not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    return set(data.get("trusted", []))


def _discover_skills(root: Path) -> list[Path]:
    found: list[Path] = []
    for rel in SKILLS_DIRS:
        base = root / rel
        if base.is_dir():
            found.extend(sorted(base.rglob("SKILL.md")))
    return found


def _discover_mcp_servers(root: Path) -> list[str]:
    path = root / MCP_CONFIG_REL
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return sorted(data.get("mcpServers", {}))


def audit(root: Path) -> AuditResult:
    """Audit discovered third-party tools against the trusted allowlist."""
    allow = _load_allowlist(root)
    findings: list[str] = []

    skills = _discover_skills(root)
    for skill_md in skills:
        name = skill_md.parent.name
        if name not in allow:
            findings.append(
                f"unvetted skill: {skill_md.relative_to(root).as_posix()} "
                f"(audit it, then add '{name}' to {ALLOWLIST_REL})"
            )

    servers = _discover_mcp_servers(root)
    for name in servers:
        if name not in allow:
            findings.append(
                f"unvetted MCP server: '{name}' in {MCP_CONFIG_REL} "
                f"(audit it, then add '{name}' to {ALLOWLIST_REL})"
            )

    return AuditResult(scanned=len(skills) + len(servers), findings=findings)
