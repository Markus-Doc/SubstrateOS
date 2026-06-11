"""Deterministic ingestion pipeline.

Raw source -> normalised Markdown with provenance frontmatter (sha256, capture
timestamp, source link) BEFORE any model interprets it. Deterministic content
is promoted by construction; AI-derived content enters the review queue
unpromoted (promoted: false) until a human promotes it.

Web fetching (Firecrawl) is deliberately absent: ADR-005 keeps it optional and
metered behind a provider interface. URLs are recorded as source links only.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

INGEST_DIR_REL = "artifacts/ingest"
INGEST_LOG_REL = "artifacts/ingest/ingest-log.jsonl"


class MemoryStore(Protocol):
    """Anything chunks can be stored into (see labctl.memory.MemoryProvider)."""

    def store(
        self, namespace: str, content: str, sha256: str, source: str, captured_utc: str
    ) -> int: ...


@dataclass
class IngestResult:
    output_path: Path
    sha256: str
    captured_utc: str
    source: str
    namespace: str
    chunks_stored: int
    skipped: bool  # True when content was already ingested unchanged


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def chunk_markdown(text: str, max_chars: int = 4000) -> list[str]:
    """Split on top-level/secondary headings; oversized sections split on blank lines.

    Deterministic and order-preserving; no model involvement.
    """
    sections: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.startswith(("# ", "## ")) and current:
            sections.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append("\n".join(current).strip())

    chunks: list[str] = []
    for section in sections:
        if len(section) <= max_chars:
            if section:
                chunks.append(section)
            continue
        piece: list[str] = []
        size = 0
        for para in section.split("\n\n"):
            if size + len(para) > max_chars and piece:
                chunks.append("\n\n".join(piece))
                piece, size = [], 0
            piece.append(para)
            size += len(para) + 2
        if piece:
            chunks.append("\n\n".join(piece))
    return chunks


def _frontmatter(sha256: str, captured_utc: str, source: str, namespace: str) -> str:
    return (
        "---\n"
        f"sha256: {sha256}\n"
        f"captured_utc: {captured_utc}\n"
        f"source: {source}\n"
        f"namespace: {namespace}\n"
        "origin: deterministic\n"
        "promoted: true\n"
        "---\n\n"
    )


def _read_existing_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines()[:8]:
        if line.startswith("sha256: "):
            return line.removeprefix("sha256: ").strip()
    return None


def ingest_file(
    root: Path,
    source_path: Path,
    namespace: str,
    source_link: str | None = None,
    memory: MemoryStore | None = None,
) -> IngestResult:
    """Normalise one file into the ingest store; optionally index chunks into memory.

    Re-ingesting unchanged content is a no-op for the output file (skipped=True)
    but is still appended to the ingest log as a run record.
    """
    raw = source_path.read_bytes()
    digest = sha256_hex(raw)
    captured = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    source = source_link or str(source_path.resolve())

    out_dir = root / INGEST_DIR_REL / namespace
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"{source_path.stem}.md"

    skipped = _read_existing_hash(output_path) == digest
    text = raw.decode("utf-8", errors="replace")
    if not skipped:
        output_path.write_text(
            _frontmatter(digest, captured, source, namespace) + text, encoding="utf-8"
        )

    chunks_stored = 0
    if memory is not None:
        for chunk in chunk_markdown(text):
            memory.store(
                namespace=namespace,
                content=chunk,
                sha256=digest,
                source=source,
                captured_utc=captured,
            )
            chunks_stored += 1

    log_path = root / INGEST_LOG_REL
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "captured_utc": captured,
        "source": source,
        "sha256": digest,
        "namespace": namespace,
        "output": str(output_path.relative_to(root)),
        "chunks_stored": chunks_stored,
        "skipped": skipped,
    }
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")

    return IngestResult(
        output_path=output_path,
        sha256=digest,
        captured_utc=captured,
        source=source,
        namespace=namespace,
        chunks_stored=chunks_stored,
        skipped=skipped,
    )


def last_ingest_record(root: Path) -> dict | None:
    """Most recent ingest log entry, for the status dashboard."""
    log_path = root / INGEST_LOG_REL
    if not log_path.exists():
        return None
    lines = [ln for ln in log_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return json.loads(lines[-1]) if lines else None
