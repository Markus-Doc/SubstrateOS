"""Overlay extension seam (ADR-019): Base + Overlay, one-way dependency.

The Base never imports or hardcodes an Overlay. Discovery is by the
``SUBSTRATEOS_OVERLAY`` environment variable only, pointing at a directory that
contains a ``substrateos_overlay`` module (``substrateos_overlay.py`` or a
package) exposing two optional hooks::

    def register(app: typer.Typer) -> None: ...        # mount extra commands
    def register_providers(registry: ProviderRegistry) -> None: ...  # add providers

Everything here is a no-op when the variable is unset, and every failure path is
non-fatal: a broken Overlay must never take down the Base CLI (the Base runs
naked, gate green with no Overlay present). Personal/private "flair" lives in the
Overlay repo; the Base ships this mechanism blank with the scaffold under
``templates/overlay-example/``.
"""

from __future__ import annotations

import importlib
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

OVERLAY_ENV = "SUBSTRATEOS_OVERLAY"
OVERLAY_MODULE = "substrateos_overlay"

# Names of overlays loaded this process, for observability (doctor/status).
_loaded: list[str] = []


def loaded_overlays() -> list[str]:
    """Return the overlay module names loaded this process (empty if none)."""
    return list(_loaded)


class ProviderRegistry:
    """Named provider factories an Overlay can extend (generalises ADR-009/005).

    A factory takes the repo root and returns a provider instance. The Base
    registers its built-in providers; an Overlay may add or override by name.
    """

    def __init__(self) -> None:
        self._factories: dict[str, dict[str, Callable[[Path], Any]]] = {}

    def register(self, kind: str, name: str, factory: Callable[[Path], Any]) -> None:
        self._factories.setdefault(kind, {})[name] = factory

    def names(self, kind: str) -> list[str]:
        return sorted(self._factories.get(kind, {}))

    def create(self, kind: str, name: str, root: Path) -> Any:
        try:
            factory = self._factories[kind][name]
        except KeyError as exc:
            available = self.names(kind)
            raise KeyError(
                f"no provider '{name}' of kind '{kind}' (have: {available})"
            ) from exc
        return factory(root)


def _warn(message: str) -> None:
    print(f"labctl: overlay: {message}", file=sys.stderr)


def _import_overlay(overlay_dir: Path) -> Any | None:
    """Import the overlay module from ``overlay_dir``; None on any failure."""
    sys.path.insert(0, str(overlay_dir))
    try:
        # Force a fresh import so repeated loads (and tests) see current code.
        sys.modules.pop(OVERLAY_MODULE, None)
        return importlib.import_module(OVERLAY_MODULE)
    except Exception as exc:  # noqa: BLE001 - a broken overlay must not crash the CLI
        _warn(f"could not import {OVERLAY_MODULE} from {overlay_dir}: {exc}")
        return None


def load_overlay(
    app: Any | None = None,
    *,
    registry: ProviderRegistry | None = None,
    environ: dict[str, str] | None = None,
) -> str | None:
    """Discover and apply an Overlay if ``SUBSTRATEOS_OVERLAY`` is set.

    Mounts overlay commands onto ``app`` via ``register(app)`` and lets the
    overlay add providers via ``register_providers(registry)``. Returns the
    overlay module name when applied, else None. No-op and non-fatal otherwise.
    """
    environ = os.environ if environ is None else environ
    raw = environ.get(OVERLAY_ENV)
    if not raw:
        return None

    overlay_dir = Path(raw).expanduser()
    if not overlay_dir.is_dir():
        _warn(f"{OVERLAY_ENV} is not a directory: {overlay_dir}")
        return None

    module = _import_overlay(overlay_dir)
    if module is None:
        return None

    applied = False
    if app is not None:
        hook = getattr(module, "register", None)
        if callable(hook):
            try:
                hook(app)
                applied = True
            except Exception as exc:  # noqa: BLE001
                _warn(f"register(app) failed: {exc}")
        else:
            _warn(f"{OVERLAY_MODULE} has no callable register(app)")

    if registry is not None:
        phook = getattr(module, "register_providers", None)
        if callable(phook):
            try:
                phook(registry)
                applied = True
            except Exception as exc:  # noqa: BLE001
                _warn(f"register_providers(registry) failed: {exc}")

    if applied and OVERLAY_MODULE not in _loaded:
        _loaded.append(OVERLAY_MODULE)
    return OVERLAY_MODULE if applied else None
