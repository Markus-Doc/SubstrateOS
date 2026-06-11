# Agent Brain capsule base image.
# Minimal by design: capsules install their own project dependencies.
FROM python:3.11-slim

# git for repo operations inside the capsule; tini as a minimal init (PID 1).
RUN apt-get update \
    && apt-get install -y --no-install-recommends git tini \
    && rm -rf /var/lib/apt/lists/*

# Non-root capsule user. No sudo installed; the container never runs as root
# after build time.
ARG USERNAME=capsule
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd --gid "${USER_GID}" "${USERNAME}" \
    && useradd --uid "${USER_UID}" --gid "${USER_GID}" --create-home --shell /bin/bash "${USERNAME}"

USER capsule
WORKDIR /home/capsule

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["sleep", "infinity"]
