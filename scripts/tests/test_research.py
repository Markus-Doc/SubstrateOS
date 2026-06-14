"""Tests for the labctl research pipeline (ADR-021). Fully deterministic:
no real resynth, no real claude, no network."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from labctl import research
from labctl import review as review_mod
from labctl.research import ResynthResult


@pytest.fixture
def research_repo(tmp_path: Path) -> Path:
    (tmp_path / ".git").mkdir()
    sub = tmp_path / "substrate"
    sub.mkdir()
    (sub / "research-watch.json").write_text(
        json.dumps(
            {
                "version": 1,
                "items": [
                    {"name": "engines", "why": "w", "current_choice": "claude, codex",
                     "adr_refs": ["ADR-019"]},
                ],
            }
        ),
        encoding="utf-8",
    )
    (sub / "trusted-tools.json").write_text('{"trusted": []}', encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    (decisions / "ADR-001-x.md").write_text("# ADR-001\n\n- Status: Accepted\n", encoding="utf-8")
    research_docs = tmp_path / "docs" / "research"
    research_docs.mkdir(parents=True)
    (research_docs / "master-research.md").write_text("# master\n", encoding="utf-8")
    return tmp_path


class FakeResynth:
    """Records calls; gates in always_fail always exit 1, fail_once exit 1 first call."""

    def __init__(self, always_fail: set[str] = frozenset(), fail_once: set[str] = frozenset()):
        self.calls: list[list[str]] = []
        self.always_fail = set(always_fail)
        self.fail_once = set(fail_once)
        self._seen: dict[str, int] = {}

    def __call__(self, args: list[str], cwd: Path) -> ResynthResult:
        self.calls.append(list(args))
        cmd = args[0]
        n = self._seen.get(cmd, 0)
        self._seen[cmd] = n + 1
        if cmd in self.always_fail or (cmd in self.fail_once and n == 0):
            return ResynthResult(1, "", "gate not satisfied")
        return ResynthResult(0, "{}", "")


# --- watch-list resolution ---

def test_packaged_watch_list_bundled():
    path = research._packaged_watch_path()
    assert path is not None and path.is_file()
    assert json.loads(path.read_text(encoding="utf-8"))["items"]


def test_load_watch_list_repo_first(research_repo: Path):
    watch = research.load_watch_list(research_repo)
    assert watch["items"][0]["name"] == "engines"


def test_watch_list_falls_back_to_packaged(monkeypatch: pytest.MonkeyPatch):
    def _no_repo(*_a, **_k):
        raise FileNotFoundError

    monkeypatch.setattr(research, "find_repo_root", _no_repo)
    assert research.watch_list_path(None) == research._packaged_watch_path()


def test_slugify():
    assert research.slugify("Current AI Best Practices!") == "current-ai-best-practices"


def test_headless_default_reads_env(monkeypatch):
    monkeypatch.setenv("SUBSTRATEOS_RESEARCH_HEADLESS", "1")
    assert research.headless_default() is True


def test_headless_default_unset_is_false(monkeypatch):
    monkeypatch.delenv("SUBSTRATEOS_RESEARCH_HEADLESS", raising=False)
    assert research.headless_default() is False


# --- brief ---

def test_brief_scaffolds_project(research_repo: Path):
    fake = FakeResynth()
    result = research.brief(research_repo, "Current AI Best Practices", runner=fake)
    assert result.slug == "current-ai-best-practices"
    assert (result.project_dir / "research.json").is_file()
    commands = [c[0] for c in fake.calls]
    assert commands == ["init", "brief"]


# --- sync ---

def test_sync_interactive_stops_at_first_thinking_stage(research_repo: Path):
    fake = FakeResynth(always_fail={"extract-verify"})
    result = research.sync(research_repo, "topic", resynth_runner=fake)
    assert result.auto is False
    assert result.operator_action is not None
    assert result.operator_action.name == "extract"


def test_sync_interactive_completes_when_gates_pass(research_repo: Path):
    fake = FakeResynth()
    result = research.sync(research_repo, "topic", resynth_runner=fake)
    assert result.operator_action is None
    assert "extract" in result.completed and "export" in result.completed


def test_sync_default_never_spawns(research_repo: Path):
    # No stage_runner provided and auto=False: a spawn would raise; it must not happen.
    fake = FakeResynth(always_fail={"extract-verify"})
    result = research.sync(research_repo, "topic", resynth_runner=fake)  # no stage_runner
    assert result.operator_action.name == "extract"


def test_sync_auto_uses_injected_runner(research_repo: Path):
    fake = FakeResynth(fail_once={"extract-verify", "reconcile", "synth-verify"})
    runs: list[str] = []

    def stage_runner(role: str, name: str, prompt: str, budget: int):
        runs.append(role)
        return ("done", 10, False)

    result = research.sync(
        research_repo, "topic", auto=True, resynth_runner=fake, stage_runner=stage_runner
    )
    assert result.auto is True
    assert result.operator_action is None
    assert len(runs) == 3  # one agent run per thinking stage
    assert "export" in result.completed


def test_sync_intakes_reports(research_repo: Path, tmp_path: Path):
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "r1.md").write_text("report\n", encoding="utf-8")
    fake = FakeResynth()
    research.sync(research_repo, "topic", reports_dir=reports, resynth_runner=fake)
    assert any(c[0] == "intake" for c in fake.calls)


# --- review ---

def test_review_writes_unpromoted_report(research_repo: Path):
    result = research.review(research_repo, "topic")
    text = result.report_path.read_text(encoding="utf-8")
    assert "origin: derived" in text
    assert "promoted: false" in text
    assert "Watch-list verdicts" in text
    pending = [
        d for d in review_mod.list_derived(research_repo)
        if d.namespace == research.REVIEW_NAMESPACE and not d.promoted
    ]
    assert len(pending) == 1


def test_review_auto_uses_injected_runner(research_repo: Path):
    def stage_runner(role: str, name: str, prompt: str, budget: int):
        return ("# Generated\n\nAll watch items hold.", 5, False)

    result = research.review(research_repo, "topic", auto=True, stage_runner=stage_runner)
    assert "Generated" in result.report_path.read_text(encoding="utf-8")


def test_build_review_packet_is_side_effect_free(research_repo: Path):
    packet = research.build_review_packet(research_repo, "topic", None)
    assert "engines" in packet.render()
    assert not research.review_report_dir(research_repo).exists()
