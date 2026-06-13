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
from labctl import conformance as conformance_mod
from labctl import lab as lab_mod
from labctl import orchestrate as orchestrate_mod
from labctl import review as review_mod
from labctl import trigger as trigger_mod
from labctl import usage as usage_mod
from labctl.config import find_repo_root, init_project, load_manifest
from labctl.extensions import load_overlay
from labctl.ingest import ingest_source
from labctl.memory import SQLiteMemory
from labctl.providers import WebIngestError
from labctl.status import build_report, render

MEMORY_DB_REL = "artifacts/memory.sqlite"

app = typer.Typer(no_args_is_help=True, add_completion=False)
review_app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(review_app, name="review", help="Review queue for AI-derived content.")
lab_app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(lab_app, name="lab", help="Lab host operator: wake, status, sync, dispatch.")
trigger_app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(
    trigger_app, name="trigger", help="Remote trigger: Telegram channel + RTC duty cycle (ADR-018)."
)
workflow_app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(
    workflow_app, name="workflow", help="Dynamic Workflows: multi-agent orchestration."
)


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


@lab_app.command("wake")
def lab_wake(
    wait: bool = typer.Option(False, "--wait", help="Poll ssh until the host answers."),
    timeout: float = typer.Option(120.0, help="Seconds to wait for ssh with --wait."),
) -> None:
    """Send the Wake-on-LAN magic packet to the lab host."""
    root = _root()
    config = lab_mod.load_lab_config(root)
    if not config.wol_mac:
        typer.echo(
            "error: LAB_WOL_MAC not set (environment or gitignored .env)", err=True
        )
        raise typer.Exit(code=1)
    try:
        lab_mod.send_wol(config.wol_mac, config.wol_broadcast)
    except (ValueError, OSError) as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"magic packet sent (broadcast {config.wol_broadcast}:{lab_mod.WOL_PORT})")
    if wait:
        typer.echo(f"waiting for ssh on {config.ssh_host} (timeout {timeout:.0f}s)...")
        if lab_mod.wait_for_ssh(config, timeout=timeout):
            typer.echo("lab host is reachable")
        else:
            typer.echo("lab host did not answer ssh in time", err=True)
            raise typer.Exit(code=1)


@lab_app.command("sleep")
def lab_sleep() -> None:
    """Suspend the lab host (S3). Never poweroff - wake it with `lab wake`."""
    root = _root()
    config = lab_mod.load_lab_config(root)
    try:
        lab_mod.sleep_host(config)
    except lab_mod.LabError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"suspend sent to {config.ssh_host} (resume with `labctl lab wake`)")


@lab_app.command("status")
def lab_status() -> None:
    """One ssh round trip: hostname, uptime, claude/codex/gh auth, repo HEAD."""
    root = _root()
    config = lab_mod.load_lab_config(root)
    try:
        parsed = lab_mod.probe_status(config)
    except lab_mod.LabError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    verdicts = lab_mod.status_ok(parsed)
    failed = False
    for key in lab_mod.STATUS_KEYS:
        ok = verdicts.get(key, False)
        mark = "ok " if ok else "FAIL"
        typer.echo(f"[{mark}] {key}: {parsed.get(key, 'missing')}")
        failed = failed or not ok
    if failed:
        raise typer.Exit(code=1)


@lab_app.command("sync")
def lab_sync() -> None:
    """Clone or fast-forward the SubstrateOS checkout on the lab host."""
    root = _root()
    config = lab_mod.load_lab_config(root)
    try:
        head = lab_mod.sync(config)
    except lab_mod.LabError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"lab repo HEAD: {head}")


@lab_app.command("dispatch")
def lab_dispatch(
    mission: str = typer.Argument(..., help="Mission text, delivered on stdin (ADR-015)"),
    token_budget: int = typer.Option(
        None, help="Cumulative token budget for this run (default: ADR-016 value)"
    ),
    workdir: str = typer.Option(
        None, help="Remote working directory (default: the lab repo checkout)"
    ),
) -> None:
    """Run a metered headless claude mission on the lab host (breaker armed)."""
    root = _root()
    try:
        result = lab_mod.dispatch(
            root, mission, token_budget=token_budget, workdir=workdir
        )
    except lab_mod.LabError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"run log: {result.run_log}")
    typer.echo(f"tokens used: {result.tokens_used} / budget {result.token_budget}")
    if result.breaker_tripped:
        typer.echo("CIRCUIT BREAKER: token budget exceeded, dispatch terminated", err=True)
        raise typer.Exit(code=1)
    if result.exit_code != 0:
        typer.echo(f"dispatch exited non-zero: {result.exit_code}", err=True)
        raise typer.Exit(code=result.exit_code)
    typer.echo("dispatch completed within budget")


def _trigger_config(root: Path) -> trigger_mod.TriggerConfig:
    try:
        return trigger_mod.load_trigger_config(root)
    except trigger_mod.TriggerError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc


@trigger_app.command("status")
def trigger_status(
    probe: bool = typer.Option(False, "--probe", help="Attempt one getMe API call."),
) -> None:
    """Local trigger configuration and state (no network unless --probe)."""
    root = _root()
    config = _trigger_config(root)
    deadline = trigger_mod.inhibit_until(root)
    typer.echo(f"token: {'set' if config.token else 'MISSING'}")
    typer.echo(f"allowlist: {len(config.allowed_user_ids)} user id(s)")
    typer.echo(
        f"poll timeout: {config.poll_timeout}s  wake interval: "
        f"{config.wake_interval_min} min  linger: {config.linger_seconds}s"
    )
    typer.echo(f"token budget: {config.token_budget}")
    typer.echo(
        f"inhibit: {deadline.strftime(trigger_mod.UTC_FORMAT) if deadline else 'none'}"
    )
    typer.echo(f"offset: {trigger_mod.read_offset(root)}")
    if probe:
        if not config.token:
            typer.echo("probe: FAIL (TRIGGER_TELEGRAM_TOKEN missing)", err=True)
            raise typer.Exit(code=1)
        try:
            me = trigger_mod.api_call(config.token, "getMe", {})
        except trigger_mod.TriggerError as exc:
            typer.echo(f"probe: FAIL {exc}", err=True)
            raise typer.Exit(code=1) from exc
        username = me.get("username", "unknown") if isinstance(me, dict) else "unknown"
        typer.echo(f"probe: ok (bot @{username})")


@trigger_app.command("listen")
def trigger_listen(
    once: bool = typer.Option(False, "--once", help="Drain one batch and exit."),
) -> None:
    """Drain the Telegram queue without ever suspending (dev / always-on mode)."""
    root = _root()
    config = _trigger_config(root)
    if not config.token:
        typer.echo("trigger not configured (TRIGGER_TELEGRAM_TOKEN missing)")
        return
    try:
        processed = trigger_mod.run_listen(root, config, iterations=1 if once else None)
    except trigger_mod.TriggerError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"processed: {processed}")


@trigger_app.command("cycle")
def trigger_cycle(
    once: bool = typer.Option(False, "--once", help="Run one duty cycle and exit."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Report instead of suspending."),
) -> None:
    """Full duty cycle: listen window, guards, RTC-armed suspend (ADR-018)."""
    root = _root()
    config = _trigger_config(root)
    if not config.token:
        typer.echo("trigger not configured (TRIGGER_TELEGRAM_TOKEN missing)")
        return
    try:
        outcome = trigger_mod.run_cycle(
            root, config, dry_run=dry_run, iterations=1 if once else None
        )
    except trigger_mod.TriggerError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    if outcome is not None:
        typer.echo(f"suspended: {outcome['suspended']}")
        if outcome.get("reason"):
            typer.echo(f"reason: {outcome['reason']}")


@trigger_app.command("install")
def trigger_install() -> None:
    """Install + enable the systemd unit for the duty cycle (does not start it)."""
    root = _root()
    try:
        actions = trigger_mod.install_systemd_unit(root)
    except trigger_mod.TriggerError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    for action in actions:
        typer.echo(action)


@app.command()
def usage() -> None:
    """Cumulative token accounting across capsule and lab run logs (ADR-016)."""
    root = _root()
    typer.echo(usage_mod.render(usage_mod.collect_usage(root)))


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
    """Run the release gate: secret scan, lint, tests, SAST, vuln scan, evals, supply-chain."""
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


@workflow_app.command("run")
def workflow_run(
    mission: str = typer.Argument(..., help="The mission for the orchestrated workflow"),
    workers: int = typer.Option(2, help="Number of parallel worker sub-agents"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print the stage plan; do not run"),
) -> None:
    """Run architect -> workers -> reviewer -> judge with per-agent budget caps."""
    root = _root()
    if dry_run:
        budget = orchestrate_mod.DEFAULT_STAGE_BUDGET
        typer.echo(f"workflow plan for: {mission}")
        typer.echo(f"  architect      (budget {budget})")
        for i in range(1, workers + 1):
            typer.echo(f"  worker-{i}       (budget {budget})")
        typer.echo(f"  reviewer       (budget {budget})")
        typer.echo(f"  judge          (budget {budget})  [verify-before-accept]")
        return
    runner = orchestrate_mod.claude_stage_runner(root)
    log_dir = root / orchestrate_mod.RUN_LOG_DIR_REL
    result = orchestrate_mod.run_workflow(
        mission, runner=runner, n_workers=workers, log_dir=log_dir
    )
    for stage in result.stages:
        mark = "ok" if stage.ok else "BREAKER"
        typer.echo(f"[{mark}] {stage.name}: {stage.tokens_used}/{stage.budget} tokens")
    typer.echo(f"verdict: {result.verdict}")
    typer.echo(f"metrics: {result.metrics}")
    if result.run_log is not None:
        typer.echo(f"run log: {result.run_log}")
    if not result.accepted:
        raise typer.Exit(code=1)


@app.command()
def conformance() -> None:
    """Print the cross-engine conformance contract (MUST scenarios, ADR-019)."""
    typer.echo("SubstrateOS cross-engine conformance suite:")
    for sc in conformance_mod.SCENARIOS:
        typer.echo(f"  [{sc.expect:>6}] {sc.prompt}")
        typer.echo(f"           -> {sc.rationale}")
    typer.echo(
        "\nAny certified engine must satisfy all scenarios given SubstrateOS context."
    )


# Mount any optional Overlay (ADR-019). No-op unless SUBSTRATEOS_OVERLAY is set;
# a broken Overlay never takes down the Base CLI.
load_overlay(app)


if __name__ == "__main__":
    app()
