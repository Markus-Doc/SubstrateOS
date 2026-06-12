"""labctl: SubstrateOS Lab Controller CLI.

Commands per ADR-006: init, status, ingest, doctor (plus gate for the release gate).
Commands are registered as their milestones land; unimplemented ones do not exist.
"""

from __future__ import annotations

from pathlib import Path

import typer

from labctl import capsule as capsule_mod
from labctl import doctor as doctor_mod
from labctl import gate as gate_mod
from labctl import review as review_mod
from labctl.config import find_repo_root, init_project, load_manifest
from labctl.ingest import ingest_source
from labctl.memory import SQLiteMemory
from labctl.providers import WebIngestError
from labctl.status import build_report, render

MEMORY_DB_REL = "artifacts/memory.sqlite"

app = typer.Typer(no_args_is_help=True, add_completion=False)
review_app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(review_app, name="review", help="Review queue for AI-derived content.")


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
    source: str = typer.Argument(..., help="File path (.pdf or text) or http(s) URL"),
    namespace: str = typer.Option(None, help="Memory namespace (defaults to project namespace)"),
    source_link: str = typer.Option(None, help="Original source URL, recorded as provenance"),
) -> None:
    """Normalise a source (text file, PDF, or URL) and index it into memory."""
    root = _root()
    manifest = load_manifest(root)
    ns = namespace or (manifest.namespace if manifest else "default")
    try:
        with SQLiteMemory(root / MEMORY_DB_REL) as memory:
            result = ingest_source(root, source, ns, source_link=source_link, memory=memory)
    except (WebIngestError, FileNotFoundError) as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    status_word = "unchanged" if result.skipped else "ingested"
    typer.echo(f"{status_word}: {result.output_path.relative_to(root)}")
    typer.echo(f"sha256: {result.sha256}")
    typer.echo(f"namespace: {ns}  chunks indexed: {result.chunks_stored}")


@review_app.command("generate")
def review_generate(
    path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
) -> None:
    """Summarise an ingested document into the review queue (claude -p, unpromoted)."""
    root = _root()
    try:
        out_path = review_mod.generate_summary(root, path.resolve())
    except (RuntimeError, ValueError) as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"derived (pending review): {out_path.relative_to(root)}")


@review_app.command("list")
def review_list() -> None:
    """List derived documents and their promotion state."""
    root = _root()
    docs = review_mod.list_derived(root)
    if not docs:
        typer.echo("review queue empty")
        return
    for doc in docs:
        mark = "promoted" if doc.promoted else "PENDING "
        typer.echo(f"[{mark}] {doc.path.relative_to(root)}  (ns: {doc.namespace})")


@review_app.command("approve")
def review_approve(
    path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
) -> None:
    """Promote a derived document and index its chunks into memory."""
    root = _root()
    path = path.resolve()
    try:
        with SQLiteMemory(root / MEMORY_DB_REL) as memory:
            chunks = review_mod.approve(root, path, memory)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"promoted: {path.relative_to(root)}  chunks indexed: {chunks}")


@app.command()
def new(
    project: str = typer.Argument(..., help="Capsule project name (simple slug)"),
    mission: str = typer.Option(
        "(mission not yet defined)", help="Mission statement written into the capsule CLAUDE.md"
    ),
    token_budget: int = typer.Option(
        capsule_mod.DEFAULT_TOKEN_BUDGET, help="Cumulative token budget per build run"
    ),
) -> None:
    """Scaffold a capsule as a sibling directory (its own future GitHub repo)."""
    root = _root()
    try:
        capsule_dir = capsule_mod.scaffold_capsule(
            root, project, mission=mission, token_budget=token_budget
        )
    except (ValueError, FileExistsError, FileNotFoundError) as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"capsule scaffolded: {capsule_dir}")
    typer.echo(f"namespace: {project}  token budget: {token_budget}")


@app.command()
def build(
    project: str = typer.Argument(..., help="Capsule project name (sibling directory)"),
    mission: str = typer.Option(None, help="Override the capsule manifest mission"),
    token_budget: int = typer.Option(None, help="Override the capsule manifest token budget"),
) -> None:
    """Run a headless claude build in the capsule with the circuit breaker armed."""
    root = _root()
    try:
        result = capsule_mod.run_build(
            root, project, mission=mission, token_budget=token_budget
        )
    except (FileNotFoundError, RuntimeError) as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"run log: {result.run_log}")
    typer.echo(f"tokens used: {result.tokens_used} / budget {result.token_budget}")
    if result.breaker_tripped:
        typer.echo("CIRCUIT BREAKER: token budget exceeded, build terminated", err=True)
        raise typer.Exit(code=1)
    if result.exit_code != 0:
        typer.echo(f"build exited non-zero: {result.exit_code}", err=True)
        raise typer.Exit(code=result.exit_code)
    typer.echo("build completed within budget")


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
def gate(
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Fail stages whose tool is missing instead of skipping them.",
    ),
) -> None:
    """Run the release gate: secret scan, lint, tests, SAST, vuln scan, evals."""
    root = _root()
    results = gate_mod.run_gate(root, strict=strict)
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
