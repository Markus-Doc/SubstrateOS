# SubstrateOS Overlay (example scaffold)

An **Overlay** layers your private customisation onto the public SubstrateOS
**Base** without modifying it. The Base ships this mechanism blank; your actual
"flair" lives in a *separate, private* repo built from this scaffold.

The rule (ADR-019): **the dependency points one way — Overlay → Base, never the
reverse.** The Base never imports or hardcodes your Overlay; it discovers it only
via the `SUBSTRATEOS_OVERLAY` environment variable.

## Use it

1. Copy this folder into your private overlay repo (or point at it directly).
2. Set the environment variable to the folder that contains
   `substrateos_overlay.py`:

   ```bash
   export SUBSTRATEOS_OVERLAY=/path/to/your/overlay      # bash/zsh
   $env:SUBSTRATEOS_OVERLAY = "C:\path\to\your\overlay"  # PowerShell
   ```

3. Run any `labctl` command. Your overlay's extra commands are now mounted; with
   the variable unset, the Base behaves exactly as shipped (it "runs naked").

## What you can add

`substrateos_overlay.py` may expose either or both hooks:

- `register(app)` — mount extra `labctl` subcommands (your private workflows).
- `register_providers(registry)` — add or override named providers
  (memory, web ingestion, …) via `registry.register(kind, name, factory)`.

Both are optional and loaded on demand. A broken overlay never crashes the
Base — failures are reported to stderr and skipped.

See `substrateos_overlay.py` (heavily commented) and `CLAUDE.md.example` in this
folder for a working starting point.
