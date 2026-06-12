"""labctl: SubstrateOS Lab Controller CLI.

Commands per ADR-006: init, status, ingest, doctor (plus gate for the release gate).
Commands are registered as their milestones land; unimplemented ones do not exist.
"""

from __future__ import annotations

from pathlib import Path

import typer

from labctl import doctor as doctor_mod
from labctl import gate as gate_mod
from labctl.config import find_repo_root, init_project, load_manifest
from labctl.ingest import ingest_file
from labctl.memory import SQLiteMemory
from labctl.status import build_report, render

MEMORY_DB_REL = "artifacts/memory.sqlite"

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _root() -> Path:
    try:
        return find_repo_root()
    except FileNotFoundError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=2) from exc


@app.command()
def init() -> None:
    """Create the project manifest and required directories (idempotent)."""
    root = _root()
    manifest, actions = init_project(root)
    if actions:
        for action in actions:
            typer.echo(action)
    else:
        typer.echo("nothing to do")
    typer.echo(f"project: {manifest.project} (phase {manifest.phase})")


@app.command()
def status() -> None:
    """Render the project status dashboard from local repo state."""
    root = _root()
    typer.echo(render(build_report(root)))


@app.command()
def ingest(
    path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    namespace: str = typer.Option(None, help="Memory namespace (defaults to project namespace)"),
    source_link: str = typer.Option(None, help="Original source URL, recorded as provenance"),
) -> None:
    """Normalise a file into the ingest store and index it into memory."""
    root = _root()
    manifest = load_manifest(root)
    ns = namespace or (manifest.namespace if manifest else "default")
    with SQLiteMemory(root / MEMORY_DB_REL) as memory:
        result = ingest_file(root, path, ns, source_link=source_link, memory=memory)
    status_word = "unchanged" if result.skipped else "ingested"
    typer.echo(f"{status_word}: {result.output_path.relative_to(root)}")
    typer.echo(f"sha256: {result.sha256}")
    typer.echo(f"namespace: {ns}  chunks indexed: {result.chunks_stored}")


@app.command()
def doctor() -> None:
    """Run environment health checks. Exit 1 on any error-severity failure."""
    root = _root()
    results = doctor_mod.run_checks(root)
    for r in results:
        mark = "ok " if r.ok else ("WARN" if r.severity == "warning" else "FAIL")
        typer.echo(f"[{mark}] {r.name}: {r.detail}")
    if doctor_mod.has_errors(results):
        raise typer.Exit(code=1)


@app.command()
def gate() -> None:
    """Run the release gate: secret scan, lint, tests. Exit 1 on any failure."""
    root = _root()
    results = gate_mod.run_gate(root)
    failed = False
    for stage in results:
        mark = "PASS" if stage.passed else "FAIL"
        typer.echo(f"[{mark}] {stage.name}: {stage.detail}")
        failed = failed or not stage.passed
    if failed:
        raise typer.Exit(code=1)
    typer.echo("gate: all stages passed")


if __name__ == "__main__":
    app()
