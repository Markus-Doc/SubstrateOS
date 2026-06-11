import json
from pathlib import Path

from labctl.ingest import (
    INGEST_LOG_REL,
    chunk_markdown,
    ingest_file,
    last_ingest_record,
    sha256_hex,
)


class FakeMemory:
    def __init__(self):
        self.stored = []

    def store(self, namespace, content, sha256, source, captured_utc):
        self.stored.append((namespace, content, sha256, source, captured_utc))
        return len(self.stored)


def make_source(repo: Path, text: str = "# Title\n\nBody text here.\n") -> Path:
    src = repo / "raw.md"
    src.write_text(text, encoding="utf-8")
    return src


def test_hash_stability_and_frontmatter(repo: Path):
    src = make_source(repo)
    result = ingest_file(repo, src, "test-ns")
    assert result.sha256 == sha256_hex(src.read_bytes())
    content = result.output_path.read_text(encoding="utf-8")
    assert content.startswith("---\n")
    for key in ("sha256:", "captured_utc:", "source:", "namespace: test-ns",
                "origin: deterministic", "promoted: true"):
        assert key in content
    assert "# Title" in content


def test_reingest_unchanged_is_skipped_but_logged(repo: Path):
    src = make_source(repo)
    first = ingest_file(repo, src, "test-ns")
    second = ingest_file(repo, src, "test-ns")
    assert not first.skipped
    assert second.skipped
    assert second.sha256 == first.sha256
    log_lines = (repo / INGEST_LOG_REL).read_text(encoding="utf-8").strip().splitlines()
    assert len(log_lines) == 2


def test_changed_content_rewrites(repo: Path):
    src = make_source(repo)
    first = ingest_file(repo, src, "test-ns")
    src.write_text("# Title\n\nDifferent body.\n", encoding="utf-8")
    second = ingest_file(repo, src, "test-ns")
    assert not second.skipped
    assert second.sha256 != first.sha256


def test_chunks_stored_in_memory(repo: Path):
    text = "# A\n\nalpha\n\n## B\n\nbeta\n\n## C\n\ngamma\n"
    src = make_source(repo, text)
    memory = FakeMemory()
    result = ingest_file(repo, src, "test-ns", memory=memory)
    assert result.chunks_stored == len(memory.stored) == 3
    namespaces = {entry[0] for entry in memory.stored}
    assert namespaces == {"test-ns"}
    assert all(entry[2] == result.sha256 for entry in memory.stored)


def test_chunk_markdown_splits_oversized_sections():
    big = "# Big\n\n" + "\n\n".join(f"para {i} " + "x" * 200 for i in range(40))
    chunks = chunk_markdown(big, max_chars=1000)
    assert len(chunks) > 1
    assert all(len(c) <= 1300 for c in chunks)  # paragraphs + joins stay near the cap


def test_last_ingest_record(repo: Path):
    assert last_ingest_record(repo) is None
    src = make_source(repo)
    ingest_file(repo, src, "test-ns")
    record = last_ingest_record(repo)
    assert record is not None
    assert record["namespace"] == "test-ns"
    assert json.dumps(record)  # serialisable
