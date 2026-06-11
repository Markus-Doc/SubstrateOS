"""Memory provider abstraction and SQLite implementation.

Phase 1 memory layer (stdlib sqlite3 only, no third-party deps). Chunks are
stored per capsule namespace with SHA256 hash and source URL, and keyword
retrieval uses FTS5 ranked by bm25(). Namespace isolation is a hard
requirement ("Zero Context Bleed"): every search filters by namespace in SQL.
Vector retrieval is deliberately stubbed in Phase 1.
"""

from __future__ import annotations

import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MemoryHit:
    id: int
    namespace: str
    content: str
    sha256: str
    source: str
    captured_utc: str
    score: float


class MemoryProvider(ABC):
    """Abstract memory provider. Implementations must isolate namespaces."""

    @abstractmethod
    def store(
        self, namespace: str, content: str, sha256: str, source: str, captured_utc: str
    ) -> int:
        """Store one chunk; return its row id."""

    @abstractmethod
    def search_keyword(self, namespace: str, query: str, limit: int = 10) -> list[MemoryHit]:
        """Keyword search within a single namespace, best matches first."""

    @abstractmethod
    def search_vector(self, namespace: str, query: str, limit: int = 10) -> list[MemoryHit]:
        """Vector search. Deliberately stubbed in Phase 1."""


def _quote_fts_query(query: str) -> str:
    """Wrap each whitespace-separated term in double quotes for FTS5 MATCH.

    This prevents user punctuation (e.g. '-', ':', '*') from being parsed as
    FTS5 query syntax. Embedded double quotes are escaped by doubling.
    """
    terms = [t.replace('"', '""') for t in query.split()]
    return " ".join(f'"{t}"' for t in terms)


class SQLiteMemory(MemoryProvider):
    """SQLite-backed memory: `chunks` table plus an FTS5 index kept via triggers."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY,
                namespace TEXT NOT NULL,
                content TEXT NOT NULL,
                sha256 TEXT NOT NULL,
                source TEXT NOT NULL,
                captured_utc TEXT NOT NULL
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                content, content='chunks', content_rowid='id'
            );
            CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
                INSERT INTO chunks_fts(rowid, content) VALUES (new.id, new.content);
            END;
            CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, content)
                VALUES ('delete', old.id, old.content);
            END;
            CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, content)
                VALUES ('delete', old.id, old.content);
                INSERT INTO chunks_fts(rowid, content) VALUES (new.id, new.content);
            END;
            """
        )
        self.conn.commit()

    def store(
        self, namespace: str, content: str, sha256: str, source: str, captured_utc: str
    ) -> int:
        cursor = self.conn.execute(
            "INSERT INTO chunks (namespace, content, sha256, source, captured_utc) "
            "VALUES (?, ?, ?, ?, ?)",
            (namespace, content, sha256, source, captured_utc),
        )
        self.conn.commit()
        assert cursor.lastrowid is not None
        return cursor.lastrowid

    def search_keyword(self, namespace: str, query: str, limit: int = 10) -> list[MemoryHit]:
        fts_query = _quote_fts_query(query)
        if not fts_query:
            return []
        rows = self.conn.execute(
            """
            SELECT c.id, c.namespace, c.content, c.sha256, c.source, c.captured_utc,
                   bm25(chunks_fts) AS score
            FROM chunks_fts
            JOIN chunks AS c ON c.id = chunks_fts.rowid
            WHERE chunks_fts MATCH ? AND c.namespace = ?
            ORDER BY score
            LIMIT ?
            """,
            (fts_query, namespace, limit),
        ).fetchall()
        return [
            MemoryHit(
                id=row["id"],
                namespace=row["namespace"],
                content=row["content"],
                sha256=row["sha256"],
                source=row["source"],
                captured_utc=row["captured_utc"],
                score=row["score"],
            )
            for row in rows
        ]

    def search_vector(self, namespace: str, query: str, limit: int = 10) -> list[MemoryHit]:
        raise NotImplementedError("vector retrieval is stubbed in Phase 1")

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> SQLiteMemory:
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()
