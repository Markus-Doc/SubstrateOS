from pathlib import Path

from labctl.config import init_project
from labctl.doctor import has_errors, run_checks, warnings


def test_checks_on_initialised_repo(repo: Path):
    init_project(repo)
    results = run_checks(repo)
    by_name = {r.name: r for r in results}
    assert by_name["python"].ok
    assert by_name["sqlite-fts5"].ok
    assert by_name["required-dirs"].ok
    assert by_name["manifest"].ok


def test_missing_manifest_is_warning_not_error(repo: Path):
    for rel in ("docs/decisions", "docs/planning", "docs/research", "scripts", "artifacts"):
        (repo / rel).mkdir(parents=True)
    results = run_checks(repo)
    by_name = {r.name: r for r in results}
    assert not by_name["manifest"].ok
    assert by_name["manifest"].severity == "warning"
    assert any(w.name == "manifest" for w in warnings(results))


def test_missing_dirs_is_error(repo: Path):
    results = run_checks(repo)
    assert has_errors(results)
