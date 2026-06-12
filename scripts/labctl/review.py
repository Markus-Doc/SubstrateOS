"""Review queue for AI-derived content.

AI-derived summaries are generated headlessly (claude -p) from already-ingested
deterministic documents and written under artifacts/ingest/<ns>/derived/ with
``origin: derived, promoted: false``. They are NOT indexed into memory until a
human approves them: ``approve`` flips ``promoted: true`` in place and only
then chunks the body into the memory store. Deterministic content never passes
through here — it is promoted by construction (see labctl.ingest).
"""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from labctl.ingest import INGEST_DIR_REL, MemoryStore, chunk_markdown, sha256_hex

DERIVED_SUBDIR = "derived"

SUMMARY_INSTRUCTION = (
    "Summarise the following ingested research source in at most 300 words of "
    "plain Markdown. Lead with what the source is, then its key claims and "
    "anything actionable. Output only the summary body, no preamble."
)


@dataclass
class DerivedDoc:
    path: Path
    namespace: str
    promoted: bool
    source: str
    sha256: str


def _split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse the simple key: value frontmatter block; return (fields, body)."""
    if not text.startswith("---\n"):
        return {}, text
    head, _, body = text.removeprefix("---\n").partition("\n---\n")
    fields: dict[str, str] = {}
    for line in head.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields, body.lstrip("\n")


def _derived_frontmatter(
    digest: str, captured_utc: str, source: str, namespace: str, promoted: bool
) -> str:
    return (
        "---\n"
        f"sha256: {digest}\n"
        f"captured_utc: {captured_utc}\n"
        f"source: {source}\n"
        f"namespace: {namespace}\n"
        "origin: derived\n"
        f"promoted: {'true' if promoted else 'false'}\n"
        "---\n\n"
    )


def run_claude_summary(body: str) -> str:
    """Headless summary via claude -p; the document arrives on stdin.

    --dangerously-skip-permissions reflects the owner's standing authorisation
    on this machine; end-users of a public release would run plain claude
    under their own permission model.
    """
    claude = shutil.which("claude")
    if claude is None:
        raise RuntimeError("claude CLI not found on PATH (needed for summaries)")
    proc = subprocess.run(
        [claude, "-p", SUMMARY_INSTRUCTION, "--dangerously-skip-permissions"],
        input=body,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=600,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        tail = "\n".join(proc.stderr.strip().splitlines()[-5:])
        raise RuntimeError(f"claude -p failed (exit {proc.returncode}): {tail}")
    return proc.stdout.strip() + "\n"


def generate_summary(
    root: Path,
    ingested_path: Path,
    summarise: Callable[[str], str] | None = None,
) -> Path:
    """Summarise one ingested document into the review queue (unpromoted)."""
    fields, body = _split_frontmatter(ingested_path.read_text(encoding="utf-8"))
    namespace = fields.get("namespace")
    if not namespace:
        raise ValueError(f"not an ingested document (no namespace): {ingested_path}")
    summary = (summarise or run_claude_summary)(body)
    captured = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_dir = root / INGEST_DIR_REL / namespace / DERIVED_SUBDIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{ingested_path.stem}-summary.md"
    out_path.write_text(
        _derived_frontmatter(
            sha256_hex(summary.encode("utf-8")),
            captured,
            source=fields.get("source", str(ingested_path)),
            namespace=namespace,
            promoted=False,
        )
        + summary,
        encoding="utf-8",
    )
    return out_path


def list_derived(root: Path) -> list[DerivedDoc]:
    """Every derived document across namespaces, pending and promoted alike."""
    docs: list[DerivedDoc] = []
    ingest_dir = root / INGEST_DIR_REL
    if not ingest_dir.is_dir():
        return docs
    for path in sorted(ingest_dir.glob(f"*/{DERIVED_SUBDIR}/*.md")):
        fields, _ = _split_frontmatter(path.read_text(encoding="utf-8"))
        docs.append(
            DerivedDoc(
                path=path,
                namespace=fields.get("namespace", path.parts[-3]),
                promoted=fields.get("promoted") == "true",
                source=fields.get("source", ""),
                sha256=fields.get("sha256", ""),
            )
        )
    return docs


def approve(root: Path, path: Path, memory: MemoryStore) -> int:
    """Promote one derived document and index its chunks; returns chunk count."""
    text = path.read_text(encoding="utf-8")
    fields, body = _split_frontmatter(text)
    if fields.get("origin") != "derived":
        raise ValueError(f"not a derived document: {path}")
    if fields.get("promoted") == "true":
        raise ValueError(f"already promoted: {path}")
    path.write_text(
        text.replace("promoted: false", "promoted: true", 1), encoding="utf-8"
    )
    chunks_stored = 0
    for chunk in chunk_markdown(body):
        memory.store(
            namespace=fields["namespace"],
            content=chunk,
            sha256=fields.get("sha256", ""),
            source=fields.get("source", str(path)),
            captured_utc=fields.get("captured_utc", ""),
        )
        chunks_stored += 1
    return chunks_stored
