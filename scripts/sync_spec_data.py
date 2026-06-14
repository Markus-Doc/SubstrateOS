"""Sync bundled package-data copies of the canonical spec (ADR-026).

``substrate/methodology.md`` (and ``trusted-tools.json``) is the editable source
of truth; this copies it into ``labctl/data/`` so the installed package ships the
spec and ``subos`` resolves it from any directory or inside a container. Run after
editing the source:

    python scripts/sync_spec_data.py

A drift-guard test (``tests/test_packaging.py``) fails the release gate if the
bundled copies ever drift from the source.
"""

from __future__ import annotations

import shutil
from pathlib import Path

FILES = ("methodology.md", "trusted-tools.json", "research-watch.json")


def sync(repo_root: Path) -> list[Path]:
    """Copy the canonical source files into the package-data directory."""
    source_dir = repo_root / "substrate"
    dest_dir = repo_root / "scripts" / "labctl" / "data"
    dest_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name in FILES:
        shutil.copyfile(source_dir / name, dest_dir / name)
        written.append(dest_dir / name)
    return written


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    for path in sync(repo_root):
        print(f"synced {path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
