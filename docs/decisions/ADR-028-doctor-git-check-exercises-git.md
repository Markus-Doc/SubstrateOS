# ADR-028: doctor's git check exercises git instead of sniffing for files

Date: 2026-06-14
Status: Accepted

## Decision

`labctl doctor`'s git check (`scripts/labctl/doctor.py::_check_git`) now runs a
real git command in the target repo rather than inferring health from the
presence of a `.git/` directory and the `git` binary on PATH.

The check classifies the result:

1. Presence still gates the work: no `.git/` directory or no `git` on PATH yields
   an error-severity failure with the old messages, and git is **not** invoked
   (so tool-absent environments do not raise).
2. With both present, it runs `git -C <root> rev-parse --is-inside-work-tree`
   through a single monkeypatchable seam (`_run_git`).
   - exit 0 -> ok, "repo and CLI present (git ok)".
   - exit non-zero whose stderr contains "dubious ownership" -> error-severity
     FAIL whose detail names the real fix (correct on-disk ownership with
     takeown/icacls so the directory is owned by the user, not
     `BUILTIN\Administrators`) and the trust escape hatch
     (`git config --global --add safe.directory "<root>"`).
   - any other non-zero exit -> error-severity FAIL surfacing the trimmed stderr.

The `repo` pytest fixture (`scripts/tests/conftest.py`) becomes a real `git init`
work tree (it previously made an empty `.git/` dir, which a real `git rev-parse`
rejects), and skips when git is unavailable.

## Context

A prior elevated session migrated the local GitHub tree off OneDrive onto
`D:\GitHub`. The migrated repos came out owned by `BUILTIN\Administrators` rather
than `DESKTOP1\marku`, which trips git's dubious-ownership guard: every real git
operation fails with "detected dubious ownership", yet `labctl doctor` reported
`[ok] git` because it only checked that the files existed. A diagnostic that
passes while the thing it diagnoses is broken is worse than no check. doctor's
whole job is to tell the truth about the environment, so the check has to run git,
not look at it.

The host ownership repair (takeown/icacls) is handled separately; this ADR is the
harness side: detect and report the condition with actionable remediation.

## Consequences

- doctor now needs git to be invocable to fully validate a repo. The presence
  branch still degrades safely when git is missing.
- The git stage is error-severity, so a dubious-ownership or otherwise broken repo
  makes `labctl doctor` exit non-zero. That is the intended signal, including in
  the release gate's environment posture.
- Tests that rely on the `repo` fixture now run against a real git repo; suites
  that need git will skip on a machine without it rather than fail spuriously.
- Regression coverage in `tests/test_doctor.py` simulates the dubious-ownership
  stderr and asserts doctor never reports git as ok in that state.
