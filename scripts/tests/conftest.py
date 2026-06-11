from pathlib import Path

import pytest


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A minimal fake repo root."""
    (tmp_path / ".git").mkdir()
    return tmp_path
