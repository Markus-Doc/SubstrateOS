# Security Policy

## Reporting a Vulnerability

Please report vulnerabilities privately via **GitHub's private vulnerability
reporting** on this repository (Security tab → "Report a vulnerability").
Do not open public issues for security findings.

Alternatively, use the contact form at https://www.markuswalker.com.

You should receive an acknowledgement within a few days. Please include
reproduction steps and the affected component (`labctl` command, module, or
configuration).

## Scope

SubstrateOS is a local-first orchestration harness. The security-relevant
surfaces are:

- the release gate (`labctl gate`): secret scan, SAST, dependency/vuln scan
- capsule isolation guarantees (`templates/capsule-devcontainer/README.md`)
- the Lab host operator channel (ssh, ADR-017) — key-based, BatchMode only

No secrets, keys, or credentials are ever committed to this repository; all
machine-specific configuration lives in the gitignored `.env`.
