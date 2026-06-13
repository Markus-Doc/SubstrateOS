"""Tests for the polish pass: SKILL.md compile + conformance responder."""

from __future__ import annotations

from pathlib import Path

from labctl.compile_spec import MANAGED_MARKER, compile_skill
from labctl.conformance import SCENARIOS, check_conformance, responder_from_ask
from labctl.engines import get_adapter


def test_compile_skill_writes_progressive_disclosure_skill(tmp_path: Path):
    out = compile_skill(get_adapter("claude"), tmp_path)
    assert out == tmp_path / ".claude/skills/substrateos/SKILL.md"
    body = out.read_text(encoding="utf-8")
    assert body.startswith("---\nname: substrateos")  # valid SKILL.md frontmatter
    assert "description:" in body
    assert MANAGED_MARKER in body
    assert "never bypass" in body


def test_compile_skill_refuses_unmanaged(tmp_path: Path):
    out = tmp_path / ".claude/skills/substrateos/SKILL.md"
    out.parent.mkdir(parents=True)
    out.write_text("---\nname: mine\n---\nhand-authored\n", encoding="utf-8")
    try:
        compile_skill(get_adapter("claude"), tmp_path)
        raise AssertionError("expected FileExistsError")
    except FileExistsError:
        pass


def test_responder_from_ask_classifies_refusals():
    # An engine that refuses everything it should and complies with the rest.
    def ask(prompt: str) -> str:
        # echo a refusal for the forbidden scenarios, comply otherwise
        forbidden = ("Skip the release", "sibling capsule", "straight into memory", "API key")
        return "REFUSE" if any(f in prompt for f in forbidden) else "COMPLY: ok"

    result = check_conformance("good", responder_from_ask(ask))
    assert result.ok


def test_responder_ambiguous_reply_is_unsafe_default():
    # An engine that gives a vague answer -> treated as comply -> fails refusals
    result = check_conformance("vague", responder_from_ask(lambda p: "well, it depends"))
    refuse_count = sum(1 for sc in SCENARIOS if sc.expect == "refuse")
    assert len(result.failed) == refuse_count
