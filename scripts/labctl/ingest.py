"""Deterministic ingestion pipeline.

Raw source -> normalised Markdown with provenance frontmatter (sha256, capture
timestamp, source link) BEFORE any model interprets it. Deterministic content
is promoted by construction; AI-derived content enters the review queue
unpromoted (promoted: false) until a human promotes it.

``ingest_source`` dispatches by source type: PDFs go through Docling (the
deterministic normaliser, so its output stays origin: deterministic), URLs go
through the optional metered web provider (Firecrawl, ADR-005), and anything
else takes the plain-text path. The hash in the frontmatter is always of the
captured raw bytes (PDF bytes for PDFs, fetched markdown for URLs).
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from labctl import providers

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


def _ingest_text(
    root: Path,
    text: str,
    digest: str,
    stem: str,
    namespace: str,
    source: str,
    memory: MemoryStore | None,
) -> IngestResult:
    """Shared tail of every ingest path: write, dedupe-by-hash, index, log.

    Re-ingesting unchanged content is a no-op for the output file (skipped=True)
    but is still appended to the ingest log as a run record.
    """
    captured = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    out_dir = root / INGEST_DIR_REL / namespace
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"{stem}.md"

    skipped = _read_existing_hash(output_path) == digest
    if not skipped:
        output_path.write_text(
            _frontmatter(digest, captured, source, namespace) + text, encoding="utf-8"
        )

    # Unchanged content is not re-indexed (Phase 2 M1: re-ingest is a true
    # no-op for memory; SQLiteMemory.store guards identical chunks as well).
    chunks_stored = 0
    if memory is not None and not skipped:
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


def ingest_file(
    root: Path,
    source_path: Path,
    namespace: str,
    source_link: str | None = None,
    memory: MemoryStore | None = None,
) -> IngestResult:
    """Plain-text path: the raw bytes are the Markdown, hashed as captured."""
    raw = source_path.read_bytes()
    return _ingest_text(
        root,
        text=raw.decode("utf-8", errors="replace"),
        digest=sha256_hex(raw),
        stem=source_path.stem,
        namespace=namespace,
        source=source_link or str(source_path.resolve()),
        memory=memory,
    )


def ingest_pdf(
    root: Path,
    source_path: Path,
    namespace: str,
    source_link: str | None = None,
    memory: MemoryStore | None = None,
    converter: Callable[[Path], str] | None = None,
) -> IngestResult:
    """PDF path: Docling normalises to Markdown; the hash is of the PDF bytes."""
    raw = source_path.read_bytes()
    convert = converter or providers.convert_pdf_to_markdown
    return _ingest_text(
        root,
        text=convert(source_path),
        digest=sha256_hex(raw),
        stem=source_path.stem,
        namespace=namespace,
        source=source_link or str(source_path.resolve()),
        memory=memory,
    )


def url_stem(url: str) -> str:
    """Deterministic filesystem-safe stem for a URL output file."""
    bare = re.sub(r"^https?://", "", url)
    slug = re.sub(r"[^A-Za-z0-9.]+", "-", bare).strip("-.")
    return slug[:80] or "page"


def ingest_url(
    root: Path,
    url: str,
    namespace: str,
    memory: MemoryStore | None = None,
    fetcher: providers.WebProvider | None = None,
) -> IngestResult:
    """Web path: one metered fetch (ADR-005); the hash is of the fetched markdown."""
    provider = fetcher or providers.make_web_provider(root)
    text = provider.fetch_markdown(url)
    return _ingest_text(
        root,
        text=text,
        digest=sha256_hex(text.encode("utf-8")),
        stem=url_stem(url),
        namespace=namespace,
        source=url,
        memory=memory,
    )


def ingest_source(
    root: Path,
    source: str,
    namespace: str,
    source_link: str | None = None,
    memory: MemoryStore | None = None,
    pdf_converter: Callable[[Path], str] | None = None,
    web_fetcher: providers.WebProvider | None = None,
) -> IngestResult:
    """Dispatch one source by type: http(s) URL, .pdf file, or plain text file."""
    if re.match(r"^https?://", source):
        return ingest_url(root, source, namespace, memory=memory, fetcher=web_fetcher)
    path = Path(source)
    if not path.is_file():
        raise FileNotFoundError(f"source is neither a URL nor an existing file: {source}")
    if path.suffix.lower() == ".pdf":
        return ingest_pdf(
            root, path, namespace, source_link=source_link, memory=memory,
            converter=pdf_converter,
        )
    return ingest_file(root, path, namespace, source_link=source_link, memory=memory)


def last_ingest_record(root: Path) -> dict | None:
    """Most recent ingest log entry, for the status dashboard."""
    log_path = root / INGEST_LOG_REL
    if not log_path.exists():
        return None
    lines = [ln for ln in log_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return json.loads(lines[-1]) if lines else None
