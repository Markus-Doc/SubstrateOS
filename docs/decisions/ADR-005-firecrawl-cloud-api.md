# ADR-005: Firecrawl Cloud API, Optional and Metered

Date: 2026-06
Status: Accepted

## Decision

Use the Firecrawl cloud API for web extraction. It is optional, metered, and sits behind a provider interface.

## Context

Self-hosting a scraping stack in Phase 1 would consume build time without advancing the core loop. Firecrawl cloud provides managed scraping, crawling, search, extraction, proxies, and browser handling immediately. The Lab hardware is not the strongest, making cloud a more reliable baseline.

## Constraints

- Start on the free or lowest practical tier.
- Use cheaper retrieval methods first; invoke Firecrawl only when higher-quality extraction or browser handling is required.
- Firecrawl API key stored in secrets, never committed to the repo.
- Provider interface must allow Firecrawl to be replaced, self-hosted, rate-limited, or disabled without redesigning the system.

## Consequences

- No scraping infrastructure to maintain in Phase 1.
- Cost is metered and visible from day one.
- Self-hosted Firecrawl remains a viable Phase 2 option if cloud costs or reliability become a concern.
