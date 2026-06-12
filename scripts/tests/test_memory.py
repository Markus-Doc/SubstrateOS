"""Tests for the SQLite memory provider."""

from __future__ import annotations

from pathlib import Path

import pytest

from labctl.memory import SQLiteMemory


@pytest.fixture
def memory(tmp_path: Path):
    with SQLiteMemory(tmp_path / "memory.db") as mem:
        yield mem


def _store(mem: SQLiteMemory, namespace: str, content: str, **overrides: str) -> int:
    return mem.store(
        namespace=namespace,
        content=content,
        sha256=overrides.get("sha256", "0" * 64),
        source=overrides.get("source", "https://example.com/doc"),
        captured_utc=overrides.get("captured_utc", "2026-06-11T00:00:00Z"),
    )


def test_namespace_isolation(memory: SQLiteMemory) -> None:
    _store(memory, "capsule-a", "orchestration harness notes about sqlite memory")
    _store(memory, "capsule-b", "orchestration harness notes about sqlite memory too")

    hits_a = memory.search_keyword("capsule-a", "sqlite memory")
    hits_b = memory.search_keyword("capsule-b", "sqlite memory")

    assert hits_a and all(h.namespace == "capsule-a" for h in hits_a)
    assert hits_b and all(h.namespace == "capsule-b" for h in hits_b)
    assert memory.search_keyword("capsule-empty", "sqlite memory") == []


def test_bm25_relevance_ordering(memory: SQLiteMemory) -> None:
    dense_id = _store(
        memory,
        "ns",
        "firecrawl ingestion: firecrawl crawls pages, firecrawl extracts markdown, "
        "and firecrawl deduplicates output.",
    )
    sparse_id = _store(
        memory,
        "ns",
        "The ingest layer has many options; one candidate among several others is "
        "firecrawl, alongside plain HTTP fetching and manual capture of documents.",
    )

    hits = memory.search_keyword("ns", "firecrawl")
    assert [h.id for h in hits[:2]] == [dense_id, sparse_id]
    assert hits[0].score <= hits[1].score  # bm25: lower is better


def test_round_trip_fields(memory: SQLiteMemory) -> None:
    row_id = _store(
        memory,
        "ns",
        "round trip content",
        sha256="a" * 64,
        source="https://example.com/source-page",
        captured_utc="2026-01-02T03:04:05Z",
    )
    (hit,) = memory.search_keyword("ns", "round trip")
    assert hit.id == row_id
    assert hit.sha256 == "a" * 64
    assert hit.source == "https://example.com/source-page"
    assert hit.captured_utc == "2026-01-02T03:04:05Z"
    assert isinstance(hit.score, float)


def test_search_vector_stubbed(memory: SQLiteMemory) -> None:
    with pytest.raises(NotImplementedError, match="stubbed in Phase 1"):
        memory.search_vector("ns", "anything")


def test_punctuation_query_does_not_raise(memory: SQLiteMemory) -> None:
    _store(memory, "ns", "content mentioning labctl and sqlite")
    for query in ('labctl: "quoted" -dash', "a*b (c) OR NOT", '""', "co-located near:term"):
        memory.search_keyword("ns", query)  # must not raise


def test_store_dedupes_identical_chunks(memory: SQLiteMemory) -> None:
    first = _store(memory, "ns", "the same chunk of content")
    second = _store(memory, "ns", "the same chunk of content")
    assert first == second
    rows = memory.conn.execute("SELECT COUNT(*) AS n FROM chunks").fetchone()
    assert rows["n"] == 1
    # different namespace or different source hash is NOT a duplicate
    _store(memory, "other-ns", "the same chunk of content")
    _store(memory, "ns", "the same chunk of content", sha256="f" * 64)
    rows = memory.conn.execute("SELECT COUNT(*) AS n FROM chunks").fetchone()
    assert rows["n"] == 3


def test_dedupe_cleans_pre_guard_duplicates(memory: SQLiteMemory) -> None:
    # simulate pre-guard duplicate rows via direct inserts
    for _ in range(3):
        memory.conn.execute(
            "INSERT INTO chunks (namespace, content, sha256, source, captured_utc) "
            "VALUES ('ns', 'duplicated chunk text', ?, 's', 't')",
            ("a" * 64,),
        )
    memory.conn.commit()
    removed = memory.dedupe()
    assert removed == 2
    hits = memory.search_keyword("ns", "duplicated chunk")
    assert len(hits) == 1  # FTS index stayed consistent through the deletes
