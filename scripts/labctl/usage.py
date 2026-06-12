"""Cumulative token accounting across run logs (ADR-016's open consequence).

Every metered run — capsule builds (`.substrateos/logs/run-*.jsonl` inside
sibling capsules, ADR-014/015) and lab dispatches (`artifacts/lab-runs/`,
ADR-017) — leaves a stream-json log. `labctl usage` replays them through the
same counting rule the circuit breaker uses (`capsule._usage_tokens`: input,
output, and cache-creation tokens; cache reads excluded) and reports per-run
and cumulative campaign totals.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from labctl.capsule import CAPSULE_MANIFEST_NAME, RUN_LOG_DIR_REL, _usage_tokens
from labctl.lab import RUN_LOG_DIR_REL as LAB_RUN_LOG_DIR_REL


@dataclass
class RunUsage:
    log_path: Path
    origin: str  # capsule project name or "lab"
    tokens: int
    events: int
    breaker_tripped: bool


def read_run_log(log_path: Path, origin: str) -> RunUsage:
    tokens = 0
    events = 0
    tripped = False
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        events += 1
        tokens += _usage_tokens(event)
        if event.get("type") == "circuit-breaker":
            tripped = True
    return RunUsage(
        log_path=log_path, origin=origin, tokens=tokens, events=events,
        breaker_tripped=tripped,
    )


def collect_usage(root: Path) -> list[RunUsage]:
    """All run logs reachable from this repo, oldest first by file name.

    Capsules are sibling directories of the repo identified by their manifest
    (ADR-014); lab dispatch logs live under the repo's own artifacts.
    """
    runs: list[RunUsage] = []
    for log in sorted((root / LAB_RUN_LOG_DIR_REL).glob("run-*.jsonl")):
        runs.append(read_run_log(log, "lab"))
    for sibling in sorted(root.parent.iterdir()):
        if not sibling.is_dir() or sibling == root:
            continue
        if not (sibling / CAPSULE_MANIFEST_NAME).is_file():
            continue
        for log in sorted((sibling / RUN_LOG_DIR_REL).glob("run-*.jsonl")):
            runs.append(read_run_log(log, sibling.name))
    return runs


def render(runs: list[RunUsage]) -> str:
    if not runs:
        return "no run logs found (capsule builds or lab dispatches)"
    lines = []
    total = 0
    for run in runs:
        total += run.tokens
        mark = " BREAKER-TRIPPED" if run.breaker_tripped else ""
        lines.append(
            f"{run.log_path.name}  [{run.origin}]  "
            f"tokens: {run.tokens:>10,}  events: {run.events}{mark}"
        )
    lines.append(f"cumulative: {total:,} tokens across {len(runs)} runs")
    return "\n".join(lines)
