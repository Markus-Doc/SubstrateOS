"""`subos` launcher: boot an AI engine as a SubstrateOS kernel (ADR-019).

`subos <engine>` compiles the canonical methodology into the target project's
engine instruction file, then launches that engine with the requested permission
posture. The Base default posture is **platform-default** (safe); full-auto is
opt-in via ``--full-auto`` (an Overlay/alias may set it by default).

`--dry-run` assembles and prints the plan (compiled file + engine argv) without
launching — used by tests and for inspection.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from labctl.compile_spec import compile_to, compile_warm_command
from labctl.config import find_repo_root
from labctl.engines import EngineAdapter, get_adapter
from labctl.handshake import build_handshake, render_handshake


@dataclass
class LaunchPlan:
    adapter: EngineAdapter
    instruction_file: Path
    argv: list[str]
    posture: str


def _default_spec_path() -> Path:
    try:
        root = find_repo_root()
    except FileNotFoundError:
        root = Path.cwd()
    return root / "substrate" / "methodology.md"


def build_plan(
    engine: str,
    *,
    target_dir: Path,
    posture: str = "platform-default",
    binary: str | None = None,
) -> LaunchPlan:
    """Assemble the launch plan for ``engine`` (pure; no filesystem/exec)."""
    adapter = get_adapter(engine)
    argv = [binary or adapter.binary]
    if posture == "full-auto":
        argv.extend(adapter.full_auto_flags)
    return LaunchPlan(
        adapter=adapter,
        instruction_file=Path(target_dir) / adapter.instruction_file,
        argv=argv,
        posture=posture,
    )


def run(args: argparse.Namespace) -> int:
    target = Path(args.target).expanduser().resolve()
    posture = "full-auto" if args.full_auto else "platform-default"
    try:
        plan = build_plan(args.engine, target_dir=target, posture=posture)
    except KeyError as exc:
        print(f"subos: {exc}", file=sys.stderr)
        return 2

    spec_path = Path(args.spec).expanduser() if args.spec else _default_spec_path()
    if not spec_path.is_file():
        print(f"subos: canonical spec not found: {spec_path}", file=sys.stderr)
        return 2
    try:
        written = compile_to(spec_path, plan.adapter, target, force=args.force)
        warm = compile_warm_command(plan.adapter, target, force=args.force)
    except FileExistsError as exc:
        print(f"subos: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"engine        : {plan.adapter.name}")
        print(f"posture       : {plan.posture}")
        print(f"instruction   : {written}")
        print(f"warm command  : {warm if warm else '(engine has no /substrateos slot)'}")
        print(f"launch argv   : {' '.join(plan.argv)}")
        print("---")
        print(render_handshake(build_handshake(plan.adapter), mode="cold"))
        print("(dry run — engine not launched)")
        return 0

    if shutil.which(plan.argv[0]) is None:
        print(f"subos: engine binary not on PATH: {plan.argv[0]}", file=sys.stderr)
        return 127
    print(f"SubstrateOS active — launching {plan.adapter.name} ({plan.posture})")
    return subprocess.run(plan.argv, cwd=target).returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="subos", description="Launch an AI engine as a SubstrateOS kernel."
    )
    parser.add_argument("engine", help="engine to launch (claude, codex, gemini, cursor)")
    parser.add_argument(
        "--target", default=".", help="project directory to launch in (default: cwd)"
    )
    parser.add_argument(
        "--full-auto", action="store_true", help="use the engine's full-auto posture"
    )
    parser.add_argument("--spec", default=None, help="override canonical spec path")
    parser.add_argument(
        "--force", action="store_true", help="overwrite a non-SubstrateOS instruction file"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="print the plan without launching"
    )
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
