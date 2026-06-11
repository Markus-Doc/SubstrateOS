"""Session time budget: read artifacts/run-meta.json and report remaining time.

Used by autonomous build runs to enforce the runtime cap and wind-down window.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

RUN_META_REL = "artifacts/run-meta.json"


@dataclass
class TimeBudget:
    start_utc: datetime
    cap_ends_utc: datetime
    winddown_at_utc: datetime

    @property
    def now(self) -> datetime:
        return datetime.now(UTC)

    @property
    def remaining_minutes(self) -> float:
        return (self.cap_ends_utc - self.now).total_seconds() / 60

    @property
    def in_winddown(self) -> bool:
        return self.now >= self.winddown_at_utc

    @property
    def expired(self) -> bool:
        return self.now >= self.cap_ends_utc


def _parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def load_budget(root: Path) -> TimeBudget | None:
    path = root / RUN_META_REL
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return TimeBudget(
        start_utc=_parse(data["start_utc"]),
        cap_ends_utc=_parse(data["cap_ends_utc"]),
        winddown_at_utc=_parse(data["winddown_at_utc"]),
    )
