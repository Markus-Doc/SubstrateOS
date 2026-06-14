"""Bundled package data (ADR-026).

This subpackage carries the canonical spec shipped with the installed package so
``subos`` resolves it from any directory and inside a container. The editable
source of truth is ``substrate/methodology.md`` at the repo root; the copies here
are kept byte-identical by ``scripts/sync_spec_data.py`` and a drift-guard test.
"""
