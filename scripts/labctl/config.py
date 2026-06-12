"""Repo root discovery and project manifest handling.

The manifest (substrateos.json at repo root) is the single project-state file
the dashboard and doctor read. Repo files remain the source of truth (ADR-004);
the manifest only records project identity and provider configuration status.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

MANIFEST_NAME = "substrateos.json"

REQUIRED_DIRS = (
    "docs/decisions",
    "docs/planning",
    "docs/research",
    "scripts",
    "artifacts",
)


@dataclass
class Manifest:
    project: str = "SubstrateOS"
    phase: str = "1"
    namespace: str = "substrateos"
    source_of_truth: str = "MASTER_AI_System_Research.md"
    providers: dict[str, str] = field(
        default_factory=lambda: {
            "memory": "sqlite",
            "ingest_web": "unconfigured (firecrawl optional, ADR-005)",
            "execution": "claude-code",
        }
    )


def find_repo_root(start: Path | None = None) -> Path:
    """Walk up from start until a .git directory or manifest is found."""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() or (candidate / MANIFEST_NAME).exists():
            return candidate
    raise FileNotFoundError(f"No repo root found above {current}")


def manifest_path(root: Path) -> Path:
    return root / MANIFEST_NAME


def load_manifest(root: Path) -> Manifest | None:
    path = manifest_path(root)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return Manifest(**data)


def save_manifest(root: Path, manifest: Manifest) -> Path:
    path = manifest_path(root)
    path.write_text(json.dumps(asdict(manifest), indent=2) + "\n", encoding="utf-8")
    return path


def init_project(root: Path) -> tuple[Manifest, list[str]]:
    """Idempotent init: create manifest if missing, ensure required dirs.

    Returns the manifest and a list of actions taken (empty if nothing to do).
    """
    actions: list[str] = []
    manifest = load_manifest(root)
    if manifest is None:
        manifest = Manifest()
        save_manifest(root, manifest)
        actions.append(f"created {MANIFEST_NAME}")
    for rel in REQUIRED_DIRS:
        directory = root / rel
        if not directory.exists():
            directory.mkdir(parents=True)
            actions.append(f"created {rel}/")
    return manifest, actions
