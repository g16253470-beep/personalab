"""Test fixtures: FakeLLM that emits canned JSON + in-memory SignalStream DB."""
from __future__ import annotations

import json
import random
import sqlite3
import time

from personalab.core.llm import LLMAdapter


class FakeLLM(LLMAdapter):
    """Deterministic LLM stub. Detects whether the prompt is a static verdict,
    an agentic day step, or an agentic final verdict, and returns matching JSON.
    """
    name = "fake-llm"

    def __init__(self, seed: int = 0) -> None:
        self.rng = random.Random(seed)
        self.call_count = 0

    async def complete(self, prompt: str, timeout: float = 180.0) -> str:
        self.call_count += 1
        if "100-200 字 你对朋友" in prompt or "final_subscribe" in prompt:
            return json.dumps({
                "final_subscribe": self.rng.choice(["yes", "maybe", "no", "no"]),
                "pricing_willingness_usd_month": self.rng.choice(
                    ["0", "5-20", "20-50"]),
                "top_friction": "推送过多 + AI 偶发报错 + 默认 profile 不匹配",
                "what_worked": "数据扎实，根因分析有时一针见血",
                "would_recommend_to_friend": self.rng.choice([True, False]),
                "verbatim_review": (
                    "fake verdict review — 数据扎实但 onboarding 太硬核，"
                    "AI 偶发熔断让我不放心放真钱进去。"
                ),
            }, ensure_ascii=False)
        if "engagement_score" in prompt:
            actions = ["DO_NOTHING", "/severity high", "/coin BTC ETH",
                       "/profile swing", "/mute 6h", "UNSUBSCRIBE"]
            return json.dumps({
                "action": self.rng.choices(actions,
                                            weights=[5, 2, 2, 1, 1, 1])[0],
                "reason": "fake daily reason",
                "mood": self.rng.choice(["calm", "annoyed", "curious",
                                          "considering_quit"]),
                "engagement_score": self.rng.randint(3, 8),
            }, ensure_ascii=False)
        return json.dumps({
            "would_subscribe": self.rng.choice(["yes", "maybe", "no"]),
            "quit_trigger_score": self.rng.randint(3, 9),
            "first_complaint": "fake static complaint — 推送密度过高",
            "what_works": "信号源数据扎实",
            "top_3_changes": ["改进1：减少噪声",
                              "改进2：清晰的 onboarding",
                              "改进3：AI 稳定性"],
            "pricing_willingness_usd_month": self.rng.choice(
                ["0", "5-20", "20-50"]),
            "verbatim_reaction": "fake reaction — 概念有意思，但音量太大。",
        }, ensure_ascii=False)


def make_in_memory_signalstream_db(n_events: int = 60,
                                    seed: int = 0) -> sqlite3.Connection:
    """Build an in-memory sqlite db with okx_pulse.events schema."""
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE events (
            pushed_at REAL,
            ccy TEXT,
            market TEXT,
            max_severity TEXT,
            primary_indicator TEXT,
            primary_category TEXT,
            primary_headline TEXT,
            triggers_json TEXT,
            ai_confidence TEXT,
            ai_evidence_used TEXT,
            ai_root_cause TEXT
        )
    """)
    rng = random.Random(seed)
    ccys = ["BTC", "ETH", "SOL", "BNB", "DOGE", "PEPE"]
    cats = ["price", "volume", "funding", "oi", "long_short",
            "premium", "taker", "macro", "fng", "news"]
    sevs = ["low", "mid", "high"]
    indicators = ["taker_imbalance", "oi_spike", "funding_flip",
                   "vol_breakout", "premium_swing"]
    t0 = time.time() - 12 * 3600
    rows = []
    for i in range(n_events):
        ts = t0 + i * (12 * 3600 / max(n_events, 1))
        cat = rng.choice(cats)
        rows.append((
            ts,
            rng.choice(ccys),
            "PERP",
            rng.choice(sevs),
            rng.choice(indicators),
            cat,
            f"{cat} signal #{i}",
            "[]",
            rng.choice(["low", "mid", "high"]),
            "vol,taker",
            f"fake root cause #{i}: 量价背离 / 资金费率倒挂",
        ))
    conn.executemany(
        "INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)
    conn.commit()
    return conn
