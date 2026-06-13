"""Example SubstrateOS Overlay module (ADR-019).

Copy this into your private overlay repo and point SUBSTRATEOS_OVERLAY at the
folder that contains it. Both hooks below are OPTIONAL — delete whichever you do
not need. Keep this file dependency-light; it is imported into the Base process.

This is an EXAMPLE shipped blank with the Base. It is never auto-loaded from
templates/; it only runs when SUBSTRATEOS_OVERLAY points at a copy of it.
"""

from __future__ import annotations

from typing import Any


def register(app: Any) -> None:
    """Mount extra `labctl` subcommands. ``app`` is the Base's Typer app.

    Example: `labctl hello` becomes available when this overlay is active.
    Replace this with your own private workflows.
    """
    import typer

    @app.command()
    def hello(name: str = typer.Argument("world")) -> None:
        """Example overlay command (remove me)."""
        typer.echo(f"hello {name} — SubstrateOS overlay active")


def register_providers(registry: Any) -> None:
    """Add or override named providers. Optional.

    ``registry`` is a labctl.extensions.ProviderRegistry. Example::

        registry.register("web", "myscraper", lambda root: MyWebProvider(root))

    Left empty in this example.
    """
    return None
