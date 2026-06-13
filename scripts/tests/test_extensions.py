"""Tests for the Overlay extension seam (ADR-019)."""

from __future__ import annotations

from pathlib import Path

import pytest
import typer

from labctl.extensions import (
    OVERLAY_ENV,
    ProviderRegistry,
    load_overlay,
)


def _write_overlay(directory: Path, body: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "substrateos_overlay.py").write_text(body, encoding="utf-8")
    return directory


def test_no_op_when_env_unset():
    app = typer.Typer()
    assert load_overlay(app, environ={}) is None


def test_loads_and_mounts_command():
    overlay_body = (
        "import typer\n"
        "def register(app):\n"
        "    @app.command()\n"
        "    def overlay_ping():\n"
        "        typer.echo('pong')\n"
    )
    app = typer.Typer()
    with _tmp_overlay(overlay_body) as overlay_dir:
        name = load_overlay(app, environ={OVERLAY_ENV: str(overlay_dir)})
    assert name == "substrateos_overlay"
    commands = {c.name or c.callback.__name__ for c in app.registered_commands}
    assert "overlay_ping" in commands


def test_register_providers_extends_registry():
    overlay_body = (
        "def register_providers(registry):\n"
        "    registry.register('web', 'fake', lambda root: ('fake', root))\n"
    )
    registry = ProviderRegistry()
    with _tmp_overlay(overlay_body) as overlay_dir:
        name = load_overlay(registry=registry, environ={OVERLAY_ENV: str(overlay_dir)})
    assert name == "substrateos_overlay"
    assert registry.names("web") == ["fake"]
    assert registry.create("web", "fake", Path("/repo")) == ("fake", Path("/repo"))


def test_missing_directory_is_non_fatal():
    app = typer.Typer()
    assert load_overlay(app, environ={OVERLAY_ENV: "/no/such/overlay/dir"}) is None


def test_overlay_without_hooks_is_non_fatal():
    app = typer.Typer()
    with _tmp_overlay("X = 1\n") as overlay_dir:
        assert load_overlay(app, environ={OVERLAY_ENV: str(overlay_dir)}) is None


def test_broken_overlay_does_not_raise():
    app = typer.Typer()
    with _tmp_overlay("raise RuntimeError('boom')\n") as overlay_dir:
        assert load_overlay(app, environ={OVERLAY_ENV: str(overlay_dir)}) is None


def test_registry_unknown_provider_raises():
    registry = ProviderRegistry()
    with pytest.raises(KeyError):
        registry.create("web", "nope", Path("/repo"))


# --- helper: temp overlay dir on a unique path so imports do not collide ---

import contextlib  # noqa: E402
import sys  # noqa: E402
import tempfile  # noqa: E402


@contextlib.contextmanager
def _tmp_overlay(body: str):
    with tempfile.TemporaryDirectory() as tmp:
        overlay_dir = Path(tmp)
        _write_overlay(overlay_dir, body)
        try:
            yield overlay_dir
        finally:
            sys.modules.pop("substrateos_overlay", None)
            with contextlib.suppress(ValueError):
                sys.path.remove(str(overlay_dir))
