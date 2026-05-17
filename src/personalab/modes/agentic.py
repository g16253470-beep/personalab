"""AgenticMode — multi-day behavioral simulation (Tier 4).

Each persona "uses" the product for N simulated days. Each day they:
  1. See events that reach them under current SubscriptionState
  2. Decide an action (issue a command, do nothing, or unsubscribe)
  3. State mutates via product.apply_action()

After N days (or churn), a final verdict prompt asks whether they'd subscribe
in reality, what price, and a verbatim review.

Migrated from okx_pulse v12.6 agentic_persona_test.py, decoupled from
SignalStream — product-specific filtering and commands live in ProductAdapter.
"""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

from personalab.core.llm import LLMAdapter
from personalab.core.mode import ModeResult, TestMode
from personalab.core.parsing import parse_json_with_retry
from personalab.core.persona import Persona
from personalab.core.product import Event, ProductAdapter, SubscriptionState

log = logging.getLogger(__name__)


DAY_PROMPT = """你扮演下面的人格，正在使用这个产品的第 {day_num} 天（共计划 {days} 天）。

# 你的人格
{persona_body}

---

# 今天的状态
- 当前订阅配置: {state_str}
- 临时静音: {muted}
- 累计收到: {total_received} 条

# 今天你收到的推送（{n_today} 条）
{messages}

# 前几天你的动作历史
{history}

---

# 可选动作（只能选一个）
{actions_help}

请基于你这个人格的心理状态，输出严格 JSON：
{{
  "action": "上面之一",
  "reason": "30 字内 为什么这么做",
  "mood": "annoyed|curious|calm|excited|considering_quit|done",
  "engagement_score": 1-10 (今天你对这产品的好感度)
}}

立即输出 JSON。"""


VERDICT_PROMPT = """你刚完成 {days} 天产品试用测试。请基于这 {days_done} 天的实际体验，
而非第一印象，给出最终判定。

# 你的人格
{persona_body}

# 你的行动轨迹
{trace}

# 累计收到 {total_received} 条推送
# 你已 {quit_status}

输出严格 JSON：
{{
  "final_subscribe": "yes|maybe|no",
  "pricing_willingness_usd_month": "0|5-20|20-50|50-200|200+",
  "top_friction": "30-60 字 最让你想退订的点",
  "what_worked": "30-60 字 真正欣赏的点",
  "would_recommend_to_friend": true|false,
  "verbatim_review": "100-200 字 你对朋友/Twitter 说的真实评价"
}}

立即输出。"""


def _render_messages(events: list[Event], product: ProductAdapter,
                       max_show: int = 15) -> str:
    if not events:
        return "(今天没有消息)"
    shown = events[:max_show]
    body = "\n".join(product.render_event(e, compact=True) for e in shown)
    if len(events) > max_show:
        body += f"\n... +{len(events) - max_show} more today"
    return body


def _render_history(decisions: list[dict], tail: int = 5) -> str:
    if not decisions:
        return "（第一天）"
    recent = decisions[-tail:]
    return "\n".join(
        f"day {d['day']}: {d['action']} ({d['reason'][:40]})"
        for d in recent
    )


def _render_trace(decisions: list[dict]) -> str:
    return "\n".join(
        f"day {d['day']}: 收 {d['received']} 条 → {d['action']} ({d['reason']}) "
        f"[mood:{d['mood']} engage:{d['engagement']}/10]"
        for d in decisions
    )


class AgenticMode(TestMode):
    """N-day behavioral simulation per persona, parallel across personas."""

    name = "agentic"

    def __init__(self, days: int = 7, concurrency: int = 2,
                 retries: int = 3, timeout: float = 180.0,
                 max_events_shown_per_day: int = 15) -> None:
        self.days = days
        self.concurrency = concurrency
        self.retries = retries
        self.timeout = timeout
        self.max_events_shown_per_day = max_events_shown_per_day

    async def _simulate_one(self, persona: Persona,
                              daily_events: list[list[Event]],
                              product: ProductAdapter,
                              llm: LLMAdapter) -> dict:
        state: SubscriptionState = product.default_state()
        decisions: list[dict] = []
        total_received = 0
        quit_day: int | None = None
        now_ts = time.time()

        for day_idx in range(self.days):
            day_num = day_idx + 1
            todays = daily_events[day_idx] if day_idx < len(daily_events) else []
            matched = [e for e in todays if product.matches_filter(e, state)]
            if state.hourly_cap > 0:
                matched = matched[: state.hourly_cap * 24]
            if state.muted_until > now_ts:
                matched = []
            total_received += len(matched)

            prompt = DAY_PROMPT.format(
                day_num=day_num,
                days=self.days,
                persona_body=persona.body,
                state_str=product.render_state(state),
                muted="yes" if state.muted_until > now_ts else "no",
                total_received=total_received,
                n_today=len(matched),
                messages=_render_messages(matched, product,
                                            self.max_events_shown_per_day),
                history=_render_history(decisions),
                actions_help=product.actions_help(),
            )
            try:
                data = await parse_json_with_retry(
                    llm, prompt,
                    retries=self.retries, timeout=self.timeout,
                    label=f"agentic/{persona.name}/d{day_num}",
                )
            except Exception as e:
                log.error("[%s] day %d giving up: %s",
                          persona.name, day_num, str(e)[:120])
                data = {"action": "DO_NOTHING",
                        "reason": "llm_unavailable",
                        "mood": "calm", "engagement_score": 5}

            action = str(data.get("action", "DO_NOTHING")).strip()
            result = product.apply_action(state, action)
            decisions.append({
                "day": day_num,
                "received": len(matched),
                "action": action,
                "result": result,
                "reason": data.get("reason", ""),
                "mood": data.get("mood", ""),
                "engagement": data.get("engagement_score", 5),
            })
            log.info("[%s] day %d: recv=%d action=%s mood=%s engage=%s",
                     persona.name, day_num, len(matched),
                     action[:30], data.get("mood"),
                     data.get("engagement_score"))

            if action == "UNSUBSCRIBE" or result == "UNSUBSCRIBED":
                quit_day = day_num
                break

        # Final verdict
        verdict_prompt = VERDICT_PROMPT.format(
            days=self.days,
            days_done=len(decisions),
            persona_body=persona.body,
            trace=_render_trace(decisions),
            total_received=total_received,
            quit_status=(f"退订（day {quit_day}）" if quit_day else "坚持到底"),
        )
        try:
            verdict = await parse_json_with_retry(
                llm, verdict_prompt,
                retries=self.retries, timeout=self.timeout,
                backoff_base=5.0,
                label=f"agentic/{persona.name}/verdict",
            )
        except Exception as e:
            log.error("[%s] verdict gave up: %s", persona.name, str(e)[:200])
            verdict = {"error": f"verdict_failed: {str(e)[:160]}"}

        return {
            "persona": persona.name,
            "days_completed": len(decisions),
            "quit_day": quit_day,
            "total_received": total_received,
            "decisions": decisions,
            "verdict": verdict,
            "final_state": {
                "profile": state.profile,
                "categories": sorted(state.categories),
                "filters": state.filters,
                "min_severity": state.min_severity,
                "hourly_cap": state.hourly_cap,
                "quiet_hours": state.quiet_hours,
            },
        }

    async def run(self, personas: list[Persona], product: ProductAdapter,
                  llm: LLMAdapter,
                  config: dict[str, Any] | None = None) -> ModeResult:
        cfg = config or {}
        events = product.load_events(limit=cfg.get("event_limit"))
        daily = product.split_by_day(events, self.days)
        log.info("agentic: %d events split into %d days (%s), %d personas, conc=%d",
                 len(events), self.days,
                 [len(d) for d in daily],
                 len(personas), self.concurrency)

        sem = asyncio.Semaphore(self.concurrency)

        async def _bounded(p: Persona) -> dict:
            async with sem:
                return await self._simulate_one(p, daily, product, llm)

        t0 = time.time()
        results = await asyncio.gather(*(_bounded(p) for p in personas))
        log.info("agentic: all %d personas done in %.0fs",
                 len(personas), time.time() - t0)

        return ModeResult(
            mode=self.name,
            results=list(results),
            metadata={
                "n_events": len(events),
                "days": self.days,
                "llm": llm.name,
                "product": product.name,
                "events_per_day": [len(d) for d in daily],
                "config": cfg,
            },
        )
