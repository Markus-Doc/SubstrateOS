from pathlib import Path

import pytest

from labctl.ingest import ingest_source, sha256_hex, url_stem
from labctl.providers import WebIngestError, load_firecrawl_key, make_web_provider


class FakeMemory:
    def __init__(self):
        self.stored = []

    def store(self, namespace, content, sha256, source, captured_utc):
        self.stored.append((namespace, content, sha256, source, captured_utc))
        return len(self.stored)


class FakeWebProvider:
    def __init__(self, markdown: str = "# Fetched\n\nweb body\n"):
        self.markdown = markdown
        self.calls: list[str] = []

    def fetch_markdown(self, url: str) -> str:
        self.calls.append(url)
        return self.markdown


def fake_pdf_converter(path: Path) -> str:
    return "# From PDF\n\nconverted body\n"


def test_pdf_dispatch_hashes_raw_bytes_and_promotes(repo: Path):
    pdf = repo / "paper.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake pdf bytes")
    memory = FakeMemory()
    result = ingest_source(
        repo, str(pdf), "test-ns", memory=memory, pdf_converter=fake_pdf_converter
    )
    assert result.sha256 == sha256_hex(pdf.read_bytes())
    content = result.output_path.read_text(encoding="utf-8")
    assert "origin: deterministic" in content
    assert "promoted: true" in content
    assert "# From PDF" in content
    assert memory.stored and "converted body" in memory.stored[0][1]


def test_url_dispatch_uses_provider_and_url_provenance(repo: Path):
    provider = FakeWebProvider()
    memory = FakeMemory()
    url = "https://example.com/docs/page"
    result = ingest_source(repo, url, "test-ns", memory=memory, web_fetcher=provider)
    assert provider.calls == [url]
    assert result.source == url
    assert result.sha256 == sha256_hex(provider.markdown.encode("utf-8"))
    content = result.output_path.read_text(encoding="utf-8")
    assert f"source: {url}" in content
    assert "origin: deterministic" in content


def test_text_dispatch_unchanged(repo: Path):
    src = repo / "note.md"
    src.write_text("# Plain\n\ntext body\n", encoding="utf-8")
    result = ingest_source(repo, str(src), "test-ns")
    assert "text body" in result.output_path.read_text(encoding="utf-8")


def test_missing_source_raises(repo: Path):
    with pytest.raises(FileNotFoundError):
        ingest_source(repo, str(repo / "nope.md"), "test-ns")


def test_missing_firecrawl_key_is_actionable(repo: Path, monkeypatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    with pytest.raises(WebIngestError, match="FIRECRAWL_API_KEY"):
        make_web_provider(repo)
    with pytest.raises(WebIngestError, match="ADR-005"):
        ingest_source(repo, "https://example.com", "test-ns")


def test_key_loaded_from_env_file(repo: Path, monkeypatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    (repo / ".env").write_text("FIRECRAWL_API_KEY=fc-test-value\n", encoding="utf-8")
    assert load_firecrawl_key(repo) == "fc-test-value"


def test_url_stem_is_safe_and_deterministic():
    assert url_stem("https://example.com/docs/page") == "example.com-docs-page"
    assert url_stem("https://example.com/docs/page") == url_stem(
        "https://example.com/docs/page"
    )
    assert "/" not in url_stem("https://a.b/c?d=e&f=g")
