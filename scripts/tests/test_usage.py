import json
from pathlib import Path

from labctl.capsule import CAPSULE_MANIFEST_NAME, RUN_LOG_DIR_REL
from labctl.lab import RUN_LOG_DIR_REL as LAB_RUN_LOG_DIR_REL
from labctl.usage import collect_usage, read_run_log, render


def usage_line(tokens: int) -> str:
    return json.dumps(
        {"type": "assistant", "message": {"usage": {"input_tokens": tokens, "output_tokens": 0}}}
    )


def write_log(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_read_run_log_counts_like_the_breaker(tmp_path: Path):
    log = tmp_path / "run-1.jsonl"
    write_log(
        log,
        [
            usage_line(100),
            "not json",
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "usage": {
                            "input_tokens": 50,
                            "output_tokens": 25,
                            "cache_creation_input_tokens": 10,
                            "cache_read_input_tokens": 99999,  # excluded (ADR-016)
                        }
                    },
                }
            ),
        ],
    )
    run = read_run_log(log, "demo")
    assert run.tokens == 185
    assert run.events == 2
    assert not run.breaker_tripped


def test_read_run_log_flags_breaker(tmp_path: Path):
    log = tmp_path / "run-2.jsonl"
    write_log(log, [usage_line(500), json.dumps({"type": "circuit-breaker"})])
    run = read_run_log(log, "lab")
    assert run.breaker_tripped
    assert run.tokens == 500


def test_collect_usage_spans_lab_and_capsule_logs(repo: Path):
    write_log(repo / LAB_RUN_LOG_DIR_REL / "run-a.jsonl", [usage_line(100)])
    capsule = repo.parent / "democapsule"
    capsule.mkdir()
    (capsule / CAPSULE_MANIFEST_NAME).write_text("{}", encoding="utf-8")
    write_log(capsule / RUN_LOG_DIR_REL / "run-b.jsonl", [usage_line(200)])
    (repo.parent / "not-a-capsule").mkdir()

    runs = collect_usage(repo)
    assert [(r.origin, r.tokens) for r in runs] == [("lab", 100), ("democapsule", 200)]

    output = render(runs)
    assert "cumulative: 300 tokens across 2 runs" in output
    assert "[lab]" in output and "[democapsule]" in output


def test_render_empty():
    assert "no run logs" in render([])
