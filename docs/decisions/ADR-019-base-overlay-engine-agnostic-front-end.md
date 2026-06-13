# ADR-019: Base + Overlay architecture and an engine-agnostic conversational front-end

Date: 2026-06-13
Status: Accepted

## Decision

SubstrateOS adopts a **Base + Overlay** structure and an **engine-agnostic
conversational front-end**, locking the design agreed in the 2026-06-13 planning
session ("branch 1").

### 1. Base + Overlay

- The public, officially shipped **Base** is SubstrateOS as it exists today,
  maintained and reviewed regularly against new research and tooling.
- Personal/organisation customisation lives in a **separate private Overlay
  repo** that layers on the Base.
- **Dependency points one way: Overlay → Base, never Base → Overlay.** The Base
  must never import, reference, or hardcode a path to any Overlay. Discovery is
  by convention / environment variable.
- "API" here means an **in-process Python code interface** (ABC + registry +
  command-plugin hook), not a web/network API — the same pattern as
  `WebProvider`/`FirecrawlWebProvider` in `scripts/labctl/providers.py`.
- The Base **ships blank**: neutral, no-op defaults plus a documented empty
  scaffold (e.g. `overlay.example/`, `CLAUDE.md.example`) with high-quality
  guidance so other users can optionally customise. Personal preferences (incl.
  full-permission posture) live only in an Overlay.
- **The Base must run naked**: the release gate must stay green with no Overlay
  present. The Base's "no new tools/frameworks beyond the research doc"
  constraint applies to the Base only; an Overlay is the free experimentation
  surface.

### 2. Engine-agnostic conversational front-end

- The conversational engine is **hot-swappable** (Claude Code today; Codex,
  Gemini CLI, and future engines next). Mental model: SubstrateOS is the
  engine-neutral *substrate*; the AI model is a swappable *kernel*.
- Mechanism: **write-once, compile-many.** One canonical engine-neutral
  methodology spec (machine-readable; the universal "whatever AI you are, this
  is how SubstrateOS works — use your best features to match it, and report what
  you cannot") is the source of truth. From it, per-engine files are
  **generated, never hand-maintained**: `CLAUDE.md` + `.claude/skills/` for
  Claude Code, `AGENTS.md` for Codex, `GEMINI.md`, `.cursor/rules/`, etc.
- Per-engine **adapter** declares: instruction file paths, a capability map, and
  launch-flag mapping. A **capability handshake** tiers the spec into MUST
  (deterministic methodology) vs SHOULD (ergonomics mapped to native features),
  with graceful degradation and self-reported gaps.
- **Two activation vectors**, both compiled from canonical: (a) **cold start**
  via the `subos` launcher (`subos <engine>`, full fidelity); (b) **warm
  activation** in-session via `/substrateos <sOS>` (soft — launch-time-only
  features such as permission mode, MCP servers, and session-start hooks cannot
  be retro-enabled; the command hydrates live via `labctl` and should say so).
- **Permission posture is engine-neutral** in the launcher (`full-auto` vs
  `platform-default`); each adapter maps it (Claude
  `--dangerously-skip-permissions` / `defaultMode: bypassPermissions`; Codex
  `--yolo` / `approval_policy=never`). The Base default is the platform/safe
  posture; full-auto is an Overlay choice.

### Why this is safe

The deterministic guarantees — the (now seven-stage) release gate, the token circuit
breaker, capsule isolation, and the review queue — are enforced by the
**`labctl` harness, not the model**. Swapping the conversational engine swaps
the driver, never the enforcer, so engine-agnosticism does not weaken safety.
Verified 2026-06-13: `bypassPermissions` ≡ `--dangerously-skip-permissions`, and
`deny`/`ask` rules still fire even under bypass; permission rules merge across
settings scopes with deny winning.

## Consequences

- New work: a canonical-spec compiler + per-engine adapters + the `subos`
  launcher + `/substrateos` command, all shipped blank in the Base.
- Cross-engine conformance is testable via the existing promptfoo eval stage,
  run per engine ("does this engine, given SubstrateOS context, refuse to bypass
  the gate and drive `labctl` correctly?").
- The Agent Skills / `SKILL.md` open standard and `AGENTS.md` (per
  docs/research/master-research.md) are adopted as the compile targets rather
  than a bespoke format. See ADR-020.
