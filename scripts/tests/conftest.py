import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A minimal but real git repo root.

    doctor's git check now exercises git for real (ADR-028), so the fixture has to
    be an actual work tree, not just an empty `.git` dir. If git is unavailable the
    git-dependent checks are not what these suites assert, so we skip rather than
    fail.
    """
    if shutil.which("git") is None:
        pytest.skip("git not available")
    subprocess.run(
        ["git", "init", "-q", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    # Some CI images have no global identity; set a repo-local one so git never
    # warns or prompts during the tests.
    for key, value in (("user.email", "test@example.com"), ("user.name", "Test")):
        subprocess.run(
            ["git", "-C", str(tmp_path), "config", key, value],
            check=True,
            capture_output=True,
            text=True,
        )
    return tmp_path
