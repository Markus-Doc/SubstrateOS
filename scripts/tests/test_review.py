from pathlib import Path

import pytest

from labctl.ingest import ingest_file
from labctl.review import approve, generate_summary, list_derived


class FakeMemory:
    def __init__(self):
        self.stored = []

    def store(self, namespace, content, sha256, source, captured_utc):
        self.stored.append((namespace, content, sha256, source, captured_utc))
        return len(self.stored)


def fake_summarise(body: str) -> str:
    return "# Summary\n\nA short derived summary.\n"


def ingested_doc(repo: Path) -> Path:
    src = repo / "raw.md"
    src.write_text("# Source\n\nLong source body about capsules.\n", encoding="utf-8")
    return ingest_file(repo, src, "test-ns").output_path


def test_generate_summary_is_unpromoted_and_not_indexed(repo: Path):
    out = generate_summary(repo, ingested_doc(repo), summarise=fake_summarise)
    assert out.parent.name == "derived"
    content = out.read_text(encoding="utf-8")
    assert "origin: derived" in content
    assert "promoted: false" in content
    assert "A short derived summary." in content


def test_generate_summary_rejects_non_ingested_file(repo: Path):
    plain = repo / "plain.md"
    plain.write_text("no frontmatter here\n", encoding="utf-8")
    with pytest.raises(ValueError, match="namespace"):
        generate_summary(repo, plain, summarise=fake_summarise)


def test_list_derived_shows_pending_then_promoted(repo: Path):
    out = generate_summary(repo, ingested_doc(repo), summarise=fake_summarise)
    docs = list_derived(repo)
    assert len(docs) == 1
    assert not docs[0].promoted
    assert docs[0].namespace == "test-ns"

    approve(repo, out, FakeMemory())
    assert list_derived(repo)[0].promoted


def test_approve_indexes_chunks_once(repo: Path):
    out = generate_summary(repo, ingested_doc(repo), summarise=fake_summarise)
    memory = FakeMemory()
    chunks = approve(repo, out, memory)
    assert chunks == len(memory.stored) == 1
    assert memory.stored[0][0] == "test-ns"
    assert "promoted: true" in out.read_text(encoding="utf-8")

    with pytest.raises(ValueError, match="already promoted"):
        approve(repo, out, memory)


def test_approve_rejects_deterministic_docs(repo: Path):
    doc = ingested_doc(repo)
    with pytest.raises(ValueError, match="not a derived document"):
        approve(repo, doc, FakeMemory())
