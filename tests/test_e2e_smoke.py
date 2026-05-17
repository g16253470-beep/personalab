"""End-to-end smoke test for L1: static + agentic + comparison.

Uses FakeLLM + in-memory sqlite db, so no network, no real LLM, no real db.
Verifies the full L1 pipeline works without raising.
"""
from __future__ import annotations

import asyncio
import sys
import tempfile
from pathlib import Path

# Ensure src/ and project root are importable when running pytest directly
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))
sys.path.insert(0, str(HERE.parent))

from personalab.core.persona import load_personas  # noqa: E402
from personalab.modes import (ABMode, AgenticMode,  # noqa: E402
                                JuryMode, StatsMode, StaticMode)
from personalab.reports import (ABReporter, ActionLoopReporter,  # noqa: E402
                                  AgenticReporter,
                                  ComparisonReporter, JuryReporter,
                                  StaticReporter, StatsReporter)
from tests.fakes import FakeLLM, make_in_memory_signalstream_db  # noqa: E402


def _make_adapter():
    """Build a SignalStreamAdapter pointing at a temp on-disk db file
    (in-memory connections aren't shareable across our adapter's fresh
    sqlite3.connect calls)."""
    from examples.signalstream import SignalStreamAdapter
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    db_path = tmp.name
    # Copy schema + data to the disk file
    import sqlite3
    src_conn = make_in_memory_signalstream_db(n_events=80, seed=42)
    dst_conn = sqlite3.connect(db_path)
    src_conn.backup(dst_conn)
    dst_conn.close()
    src_conn.close()
    return SignalStreamAdapter(db_path=db_path), db_path


def test_l1_end_to_end_smoke(tmp_path):
    personas = load_personas(HERE.parent / "personas")
    assert len(personas) == 12, f"expected 12 personas, got {len(personas)}"

    adapter, db_path = _make_adapter()
    try:
        events = adapter.load_events(limit=20)
        assert len(events) == 20
        rendered = adapter.render_event(events[0])
        assert isinstance(rendered, str) and len(rendered) > 0

        llm = FakeLLM(seed=1)

        # Use just 3 personas to keep test cheap
        sample = personas[:3]

        # Static
        static = asyncio.run(
            StaticMode(concurrency=3).run(sample, adapter, llm,
                                            config={"limit": 20})
        )
        assert static.mode == "static"
        assert len(static.results) == 3
        for r in static.results:
            assert "error" not in r, f"static error: {r}"
            assert r["would_subscribe"] in ("yes", "maybe", "no")

        # Agentic — 2 days only for speed
        agentic = asyncio.run(
            AgenticMode(days=2, concurrency=2).run(sample, adapter, llm)
        )
        assert agentic.mode == "agentic"
        assert len(agentic.results) == 3
        for r in agentic.results:
            assert r["days_completed"] >= 1
            v = r["verdict"]
            assert "error" not in v, f"verdict error: {v}"

        # Reporters
        static_md = StaticReporter(product_label="test").render(static)
        agentic_md = AgenticReporter(product_label="test").render(agentic)
        cmp_md = ComparisonReporter(product_label="test").render_dual(
            static, agentic)
        for md, name in [(static_md, "static"),
                          (agentic_md, "agentic"),
                          (cmp_md, "comparison")]:
            assert "# " in md, f"{name} report missing header"
            (tmp_path / f"{name}.md").write_text(md, encoding="utf-8")

        # Ensure something was actually written
        for name in ("static.md", "agentic.md", "comparison.md"):
            f = tmp_path / name
            assert f.exists() and f.stat().st_size > 100, f"{name} too small"

        # FakeLLM was actually called.
        # Lower bound: 3 static + 3 * (1 day + 1 verdict) = 9 (everyone quits day1)
        # Upper bound: 3 static + 3 * (2 days + 1 verdict) = 12
        assert 9 <= llm.call_count <= 12, \
            f"expected 9-12 LLM calls, got {llm.call_count}"

        # ActionLoop reporter — covers L2
        action_md = ActionLoopReporter(product_label="test")._render_combined(
            static=static, agentic=agentic
        )
        assert "行动闭环" in action_md
        (tmp_path / "action_loop.md").write_text(action_md, encoding="utf-8")
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_l6_calibration_smoke(tmp_path):
    """L6: synthesize predictions + real users, compute calibration metrics."""
    from personalab.calibration import RealUser, calibrate
    from personalab.reports.calibration import CalibrationReporter

    # Predictions = same shape as StaticMode results
    predictions = [
        {"persona": "01_burnt_veteran",
         "would_subscribe": "maybe",
         "pricing_willingness_usd_month": "5-20",
         "quit_trigger_score": 7},
        {"persona": "03_scalper",
         "would_subscribe": "no",
         "pricing_willingness_usd_month": "0",
         "quit_trigger_score": 9},
        {"persona": "07_noise_allergic_manager",
         "would_subscribe": "no",
         "pricing_willingness_usd_month": "0",
         "quit_trigger_score": 10},
    ]
    real_users = [
        RealUser("u1", "01_burnt_veteran", True, None, 10.0),
        RealUser("u2", "03_scalper", False, "2026-01-15", 0.0),
        RealUser("u3", "07_noise_allergic_manager", False, "2026-01-10", 0.0),
        RealUser("u4", "01_burnt_veteran", True, None, 10.0),
    ]
    result = calibrate(predictions, real_users, maybe_as="yes")
    assert result.n == 4
    assert result.subscribe.tp + result.subscribe.fp + \
        result.subscribe.fn + result.subscribe.tn == 4
    assert result.subscribe.accuracy() == 1.0  # perfect
    assert result.price_mae is not None
    assert "矩阵" in CalibrationReporter().render(result) \
        or "Confusion" in CalibrationReporter().render(result)
    md = CalibrationReporter().render(result)
    (tmp_path / "calibration.md").write_text(md, encoding="utf-8")


def test_l7_toy_adapter_smoke(tmp_path):
    """L7 framework abstraction: a 40-line non-SignalStream adapter must
    flow through StaticMode without core/ knowing anything about it."""
    from examples.toy import ToyAdapter
    adapter = ToyAdapter()
    personas = load_personas(HERE.parent / "personas")[:2]
    llm = FakeLLM(seed=42)
    result = asyncio.run(
        StaticMode(concurrency=2).run(personas, adapter, llm,
                                         config={"limit": 3})
    )
    assert result.mode == "static"
    assert len(result.results) == 2
    md = StaticReporter(product_label="toy").render(result)
    assert "toy" in md
    (tmp_path / "toy.md").write_text(md, encoding="utf-8")


def test_l5_stats_smoke(tmp_path):
    """StatsMode: wrap StaticMode and repeat N times, aggregate variance."""
    personas = load_personas(HERE.parent / "personas")[:3]
    adapter, db_path = _make_adapter()
    try:
        # Different seeds across runs produce variance (intended)
        llm = FakeLLM(seed=99)
        sm = StatsMode(inner=StaticMode(concurrency=3), repeats=3)
        result = asyncio.run(sm.run(personas, adapter, llm,
                                      config={"limit": 15}))
        assert result.mode == "stats"
        assert len(result.results) == 3
        for r in result.results:
            assert r["n_runs"] == 3
            assert "aggregated" in r
            assert "noisy" in r

        md = StatsReporter().render(result)
        assert "统计稳健性报告" in md
        (tmp_path / "stats.md").write_text(md, encoding="utf-8")
        # 3 personas × 3 runs = 9 LLM calls
        assert llm.call_count == 9, f"expected 9 calls, got {llm.call_count}"
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_l4_ab_smoke(tmp_path):
    """ABMode: same personas, same LLM, two adapters → per-persona diff."""
    from examples.signalstream import SignalStreamAdapter
    import sqlite3
    # Build two distinct dbs simulating v12.6 vs v12.7
    paths = []
    for seed in (10, 20):
        f = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        f.close()
        src = make_in_memory_signalstream_db(n_events=40, seed=seed)
        dst = sqlite3.connect(f.name)
        src.backup(dst); dst.close(); src.close()
        paths.append(f.name)
    a = SignalStreamAdapter(paths[0])
    b = SignalStreamAdapter(paths[1])
    a.name, b.name = "v12.6", "v12.7"
    try:
        personas = load_personas(HERE.parent / "personas")[:3]
        llm = FakeLLM(seed=7)
        result = asyncio.run(
            ABMode(inner=StaticMode(concurrency=3),
                   product_a=a, product_b=b,
                   label_a="before-fix", label_b="after-fix"
                   ).run(personas, a, llm, config={"limit": 15})
        )
        assert result.mode == "ab"
        assert len(result.results) == 3
        for r in result.results:
            assert "a" in r and "b" in r and "diff" in r

        md = ABReporter().render(result)
        assert "A/B 测试报告" in md
        assert "净影响分" in md
        (tmp_path / "ab.md").write_text(md, encoding="utf-8")
    finally:
        for p in paths:
            Path(p).unlink(missing_ok=True)


def test_l3_jury_smoke(tmp_path):
    """JuryMode with 3 FakeLLMs (different seeds → different verdicts)."""
    personas = load_personas(HERE.parent / "personas")[:3]
    adapter, db_path = _make_adapter()
    try:
        jury = [FakeLLM(seed=i) for i in (1, 2, 3)]
        for j, llm in enumerate(jury):
            llm.name = f"fake-{j}"

        result = asyncio.run(
            JuryMode(jury=jury, concurrency=3).run(
                personas, adapter, jury[0],
                config={"limit": 20}
            )
        )
        assert result.mode == "jury"
        assert len(result.results) == 3
        for r in result.results:
            assert len(r["per_llm"]) == 3
            assert "_overall" in r["agreement"]

        md = JuryReporter(product_label="test").render(result)
        assert "Jury Mode" in md
        assert "订阅意愿矩阵" in md
        (tmp_path / "jury.md").write_text(md, encoding="utf-8")
        # 3 personas × 3 LLMs = 9 calls total
        total_calls = sum(j.call_count for j in jury)
        assert total_calls == 9, f"expected 9 calls, got {total_calls}"
    finally:
        Path(db_path).unlink(missing_ok=True)


if __name__ == "__main__":
    # Allow direct invocation: python tests/test_e2e_smoke.py
    # (tempfile already imported at top)
    with tempfile.TemporaryDirectory() as td:
        test_l1_end_to_end_smoke(Path(td))
    print("[OK] L1 end-to-end smoke test passed")
    with tempfile.TemporaryDirectory() as td:
        test_l3_jury_smoke(Path(td))
    print("[OK] L3 jury smoke test passed")
    with tempfile.TemporaryDirectory() as td:
        test_l4_ab_smoke(Path(td))
    print("[OK] L4 ab smoke test passed")
    with tempfile.TemporaryDirectory() as td:
        test_l5_stats_smoke(Path(td))
    print("[OK] L5 stats smoke test passed")
    with tempfile.TemporaryDirectory() as td:
        test_l6_calibration_smoke(Path(td))
    print("[OK] L6 calibration smoke test passed")
    with tempfile.TemporaryDirectory() as td:
        test_l7_toy_adapter_smoke(Path(td))
    print("[OK] L7 toy-adapter smoke test passed")
