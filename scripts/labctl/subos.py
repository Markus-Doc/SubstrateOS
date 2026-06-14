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
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass

# importlib.resources is stdlib since 3.9; this project requires Python >= 3.11,
# so the python37-compatibility rule is a false positive here.
from importlib import resources  # nosemgrep
from pathlib import Path

from labctl import __version__
from labctl.compile_spec import compile_skill, compile_to, compile_warm_command
from labctl.config import find_repo_root
from labctl.engines import EngineAdapter, get_adapter
from labctl.handshake import build_handshake, render_handshake


@dataclass
class LaunchPlan:
    adapter: EngineAdapter
    instruction_file: Path
    argv: list[str]
    posture: str


SPEC_REL = ("substrate", "methodology.md")
PACKAGED_SPEC = "methodology.md"


def _packaged_spec_path() -> Path | None:
    """Path to the spec bundled as package data, or None if unavailable (ADR-026).

    Installed/container invocations resolve the spec from the package itself so
    ``subos`` works from any directory. Returns a real filesystem path for the
    normal (unzipped) pip/pipx/docker install.
    """
    try:
        resource = resources.files("labctl.data").joinpath(PACKAGED_SPEC)
    except (ModuleNotFoundError, AttributeError):
        return None
    try:
        if resource.is_file():
            return Path(str(resource))
    except (OSError, AttributeError):
        return None
    return None


def _default_spec_path() -> Path:
    """Resolve the canonical spec: repo source first, packaged copy as fallback.

    Inside a checkout the editable ``substrate/methodology.md`` wins so dev edits
    take effect immediately; outside a repo (installed globally or in a container)
    the bundled package-data copy is used (ADR-026).
    """
    try:
        candidate = find_repo_root().joinpath(*SPEC_REL)
        if candidate.is_file():
            return candidate
    except FileNotFoundError:
        pass
    packaged = _packaged_spec_path()
    if packaged is not None:
        return packaged
    return Path.cwd().joinpath(*SPEC_REL)


def _full_auto_default() -> bool:
    """Opt-in default posture from the environment (12-factor, ADR-026 §6).

    ``SUBSTRATEOS_FULL_AUTO`` truthy makes ``full-auto`` the default posture. The
    public Base ships safe (unset); an installer ``--full-auto-default`` or an
    Overlay sets this in user-scope config, never in the Base.
    """
    return os.environ.get("SUBSTRATEOS_FULL_AUTO", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


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
    if args.platform_default:
        posture = "platform-default"
    elif args.full_auto or _full_auto_default():
        posture = "full-auto"
    else:
        posture = "platform-default"
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
        skill = compile_skill(plan.adapter, target, force=args.force)
    except FileExistsError as exc:
        print(f"subos: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"subos version : {__version__}")
        print(f"engine        : {plan.adapter.name}")
        print(f"posture       : {plan.posture}")
        print(f"instruction   : {written}")
        print(f"warm command  : {warm if warm else '(engine has no /substrateos slot)'}")
        print(f"skill         : {skill if skill else '(engine has no skills dir)'}")
        print(f"launch argv   : {' '.join(plan.argv)}")
        print("---")
        print(render_handshake(build_handshake(plan.adapter), mode="cold"))
        print("(dry run — engine not launched)")
        return 0

    # Resolve to the full path: on Windows a bare name only matches `<name>.exe`,
    # but npm-installed engines are `<name>.CMD`/`.ps1` (no .exe), so launching the
    # bare name raises FileNotFoundError. shutil.which honours PATHEXT and returns
    # the launchable path on every platform.
    binary = shutil.which(plan.argv[0])
    if binary is None:
        print(f"subos: engine binary not on PATH: {plan.argv[0]}", file=sys.stderr)
        return 127
    print(
        f"SubstrateOS v{__version__} active — launching {plan.adapter.name} "
        f"({plan.posture}); the engine will confirm the kernel on boot."
    )
    try:
        return subprocess.run([binary, *plan.argv[1:]], cwd=target).returncode
    except OSError as exc:
        print(f"subos: failed to launch {plan.argv[0]}: {exc}", file=sys.stderr)
        return 127
    except KeyboardInterrupt:
        print("\nsubos: interrupted", file=sys.stderr)
        return 130


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="subos", description="Launch an AI engine as a SubstrateOS kernel."
    )
    parser.add_argument(
        "--version", action="version", version=f"SubstrateOS (subos) {__version__}"
    )
    parser.add_argument("engine", help="engine to launch (claude, codex, gemini, cursor)")
    parser.add_argument(
        "--target", default=".", help="project directory to launch in (default: cwd)"
    )
    parser.add_argument(
        "--full-auto", action="store_true", help="use the engine's full-auto posture"
    )
    parser.add_argument(
        "--platform-default",
        action="store_true",
        help="force the safe platform-default posture (overrides SUBSTRATEOS_FULL_AUTO)",
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
