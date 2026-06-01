# ADR-002: No LangChain, LangGraph, or AutoGen

Date: 2026-06
Status: Accepted

## Decision

Do not use LangChain, LangGraph, AutoGen, or any other heavyweight agent framework.

## Context

As of mid-2026, Claude Code provides native subagent orchestration, tool use,
and memory integration. Introducing a framework layer adds abstraction overhead,
constrains model portability, and makes debugging harder.

## Consequences

- Orchestration logic lives in the Lab Controller CLI only.
- Agent behaviour is governed by CLAUDE.md and scoped context packs.
- No framework dependency to maintain or version-pin.

## Rejected Alternative

LangGraph for multi-agent orchestration. Deferred indefinitely.
AutoGen for agent communication. Deferred indefinitely.
