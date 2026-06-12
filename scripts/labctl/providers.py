"""Source-type providers for ingestion: PDF (Docling) and web (Firecrawl).

Docling is the deterministic normaliser for PDFs (per the master research):
its Markdown output is deterministic content, promoted by construction.
Firecrawl is optional and metered behind ``WebProvider`` (ADR-005): the key
comes from the environment or the gitignored ``.env``, and a missing key is
an actionable error for the CLI to report — never a crash or traceback.

Both third-party imports are deliberately lazy so that importing labctl (and
running its tests, which mock these providers) never pays their startup cost
or requires them to be installed.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path

FIRECRAWL_KEY_VAR = "FIRECRAWL_API_KEY"


class WebIngestError(RuntimeError):
    """Web ingestion cannot proceed; the message is user-actionable."""


def convert_pdf_to_markdown(path: Path) -> str:
    """Convert a PDF to Markdown with Docling (deterministic normaliser)."""
    from docling.document_converter import DocumentConverter

    result = DocumentConverter().convert(path)
    return result.document.export_to_markdown()


def load_firecrawl_key(root: Path) -> str | None:
    """Key from the environment first, then the gitignored .env at repo root."""
    key = os.environ.get(FIRECRAWL_KEY_VAR)
    if key:
        return key
    env_file = root / ".env"
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith(f"{FIRECRAWL_KEY_VAR}="):
                value = line.split("=", 1)[1].strip()
                if value:
                    return value
    return None


class WebProvider(ABC):
    """Fetch one URL as Markdown. Implementations are replaceable (ADR-005)."""

    @abstractmethod
    def fetch_markdown(self, url: str) -> str: ...


class FirecrawlWebProvider(WebProvider):
    """Firecrawl cloud API: one metered scrape per fetch, markdown format only."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def fetch_markdown(self, url: str) -> str:
        from firecrawl import Firecrawl

        doc = Firecrawl(api_key=self.api_key).scrape(url, formats=["markdown"])
        markdown = getattr(doc, "markdown", None) or (
            doc.get("markdown") if isinstance(doc, dict) else None
        )
        if not markdown:
            raise WebIngestError(f"firecrawl returned no markdown for {url}")
        return markdown


def make_web_provider(root: Path) -> WebProvider:
    """Default web provider, or an actionable error when unconfigured."""
    key = load_firecrawl_key(root)
    if not key:
        raise WebIngestError(
            "web ingestion is unconfigured: set FIRECRAWL_API_KEY in the "
            "environment or the gitignored .env at the repo root (ADR-005: "
            "Firecrawl is optional and metered)"
        )
    return FirecrawlWebProvider(key)
