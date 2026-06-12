from pathlib import Path

from labctl.config import (
    MANIFEST_NAME,
    REQUIRED_DIRS,
    find_repo_root,
    init_project,
    load_manifest,
)


def test_find_repo_root_walks_up(repo: Path):
    nested = repo / "a" / "b"
    nested.mkdir(parents=True)
    assert find_repo_root(nested) == repo


def test_init_creates_manifest_and_dirs(repo: Path):
    manifest, actions = init_project(repo)
    assert (repo / MANIFEST_NAME).exists()
    assert manifest.project == "SubstrateOS"
    for rel in REQUIRED_DIRS:
        assert (repo / rel).is_dir()
    assert actions  # first run does work


def test_init_is_idempotent(repo: Path):
    init_project(repo)
    _, actions = init_project(repo)
    assert actions == []


def test_manifest_round_trip(repo: Path):
    init_project(repo)
    loaded = load_manifest(repo)
    assert loaded is not None
    assert loaded.providers["memory"] == "sqlite"
