# syntax=docker/dockerfile:1
# SubstrateOS golden image (ADR-026): one unit that runs identically locally and
# on EKS. Packages the `labctl` + `subos` console scripts; the canonical spec
# ships as package data so `subos` resolves it from any directory or in-container.
#
# 12-factor: configure via environment variables. NO secrets are baked — engine
# OAuth tokens (e.g. CLAUDE_CODE_OAUTH_TOKEN) are passed by env name at run time,
# never copied into a layer. Pins no model; launches the engine on PATH as-is.
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# tini = correct PID-1 signal handling (matches the capsule image); git supports
# the repo-bound labctl commands when a project is mounted.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git tini \
    && rm -rf /var/lib/apt/lists/*

# Install SubstrateOS from the package using system pip (no venv inside a container).
WORKDIR /opt/substrateos
COPY scripts/ ./scripts/
RUN pip install ./scripts

# Drop privileges: run as a non-root user (uid 1000, as in templates/capsule-devcontainer).
RUN useradd --create-home --uid 1000 substrate
USER substrate
WORKDIR /home/substrate

# tini as PID 1; default command is self-describing. Override to run subos/labctl,
# e.g.  docker run --rm -it -e CLAUDE_CODE_OAUTH_TOKEN substrateos:latest subos claude
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["labctl", "--help"]
