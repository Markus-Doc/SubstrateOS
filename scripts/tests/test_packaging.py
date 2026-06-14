"""Packaging guarantees: version single-sourcing and spec-as-package-data (ADR-026)."""

from __future__ import annotations

import importlib.metadata
import re
from pathlib import Path

import pytest

import labctl
from labctl import subos
from labctl.config import find_repo_root

BUNDLED_FILES = ("methodology.md", "trusted-tools.json", "research-watch.json")


def test_version_single_sourced():
    # pyproject reads labctl.__version__ dynamically, so installed metadata matches.
    assert importlib.metadata.version("labctl") == labctl.__version__


def test_packaged_spec_is_bundled():
    spec = subos._packaged_spec_path()
    assert spec is not None
    assert spec.is_file()
    assert spec.read_text(encoding="utf-8").strip() != ""


def test_default_spec_falls_back_to_packaged(monkeypatch: pytest.MonkeyPatch):
    def _no_repo(*_a, **_k):
        raise FileNotFoundError("no repo")

    monkeypatch.setattr(subos, "find_repo_root", _no_repo)
    resolved = subos._default_spec_path()
    assert resolved.is_file()
    assert resolved == subos._packaged_spec_path()


def test_repo_source_wins_in_checkout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    source = tmp_path / "substrate"
    source.mkdir()
    spec = source / "methodology.md"
    spec.write_text("# local editable source\n", encoding="utf-8")
    monkeypatch.setattr(subos, "find_repo_root", lambda *_a, **_k: tmp_path)
    assert subos._default_spec_path() == spec


def test_bundled_copies_match_source():
    """The package-data copies must stay byte-identical to the substrate source."""
    try:
        root = find_repo_root()
    except FileNotFoundError:  # pragma: no cover - only outside a checkout
        pytest.skip("substrate source only present in a repo checkout")
    data_dir = Path(labctl.__file__).resolve().parent / "data"
    for name in BUNDLED_FILES:
        source = root / "substrate" / name
        if not source.is_file():  # pragma: no cover
            pytest.skip(f"source {name} not present")
        bundled = data_dir / name
        assert bundled.is_file(), f"{name} not bundled under labctl/data/"
        assert bundled.read_bytes() == source.read_bytes(), (
            f"{name} drifted from substrate/{name}; run `python scripts/sync_spec_data.py`"
        )


def test_no_onedrive_paths_in_shipped_sources():
    """Guard against the pre-move layout leaking back (the OneDrive -> D: migration).

    Live code and the canonical spec must never hardcode a `...\\OneDrive\\...` path;
    engines resolve via PATH and the spec via find_repo_root/package-data, so any
    OneDrive path literal is a stale assumption that breaks on a moved checkout. We
    match `OneDrive` followed by a path separator so prose that merely mentions the
    migration (like a comment) does not trip the guard.
    """
    try:
        root = find_repo_root()
    except FileNotFoundError:  # pragma: no cover - only outside a checkout
        pytest.skip("sources only present in a repo checkout")
    code_root = Path(labctl.__file__).resolve().parent  # scripts/labctl
    path_literal = re.compile(r"onedrive[\\/]", re.IGNORECASE)
    offenders: list[str] = []
    scopes = [
        (code_root, "*.py"),
        (root / "substrate", "*.md"),
    ]
    for base, pattern in scopes:
        for path in base.rglob(pattern):
            if "__pycache__" in path.parts:
                continue
            if path_literal.search(path.read_text(encoding="utf-8", errors="ignore")):
                offenders.append(str(path.relative_to(root)))
    assert not offenders, f"OneDrive path literal found in shipped sources: {offenders}"
