# substrate/ — the engine-neutral SubstrateOS spec (compile source)

`methodology.md` is the **canonical, engine-neutral** specification of how any AI
engine behaves "as SubstrateOS." It is the single source of truth for the
write-once-compile-many model (ADR-019).

- **Authored here, by hand.** This is the source.
- **Per-engine files are generated from it** (`CLAUDE.md`, `AGENTS.md`,
  `.claude/skills/`, `GEMINI.md`, `.cursor/rules/`, …) by the compiler (M-C).
  Never hand-edit the generated outputs — edit `methodology.md` and recompile.
- **Universal fallback.** An engine with no dedicated adapter reads
  `methodology.md` cold and still behaves correctly.

The compiler and the `subos` launcher live in the `labctl` package
(`scripts/labctl/`), per the project code-location rule.
