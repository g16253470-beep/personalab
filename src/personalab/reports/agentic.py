"""AgenticReporter — render AgenticMode results as markdown.

Mirrors the shape of okx_pulse docs/agentic_report_v12.6.md: summary table,
per-persona day-by-day action trace, final verdict and verbatim review.
"""
from __future__ import annotations

from typing import Any

from personalab.core.mode import ModeResult
from personalab.core.reporter import Reporter
from personalab.core.timeutil import now_cst_str


class AgenticReporter(Reporter):
    name = "agentic-report"

    def __init__(self, product_label: str | None = None) -> None:
        self.product_label = product_label

    def render(self, result: ModeResult, **opts: Any) -> str:
        meta = result.metadata
        product = self.product_label or meta.get("product", "?")
        days = meta.get("days", "?")
        n_events = meta.get("n_events", "?")
        lines: list[str] = [
            f"# {product} Agentic 行为仿真报告",
            "",
            f"生成: {now_cst_str()} · 仿真 {days} 天 · "
            f"{len(result.results)} 个人格 · 事件: {n_events} · LLM: {meta.get('llm', '?')}",
            "",
            "## 📊 汇总",
            "",
            "| 人格 | 完成天数 | 退订日 | 累计收到 | 最终 | 月费 | 推荐? |",
            "|---|---|---|---|---|---|---|",
        ]
        for r in result.results:
            v = r.get("verdict", {})
            if "error" in v:
                lines.append(f"| {r['persona']} | {r['days_completed']}/{days} "
                             f"| {r.get('quit_day') or '-'} | "
                             f"{r['total_received']} | ❌ ERROR | - | - |")
                continue
            sub_icon = {"yes": "✅", "maybe": "⚠", "no": "❌"}.get(
                v.get("final_subscribe", "?"), "?")
            lines.append(
                f"| {r['persona']} | {r['days_completed']}/{days} | "
                f"{r.get('quit_day') or '-'} | {r['total_received']} | "
                f"{sub_icon} {v.get('final_subscribe', '?')} | "
                f"{v.get('pricing_willingness_usd_month', '?')} | "
                f"{'✅' if v.get('would_recommend_to_friend') else '❌'} |"
            )

        lines += ["", "## 🎬 每人格行动序列", ""]
        for r in result.results:
            lines.append(f"### {r['persona']}")
            lines.append("")
            for d in r.get("decisions", []):
                lines.append(
                    f"- **day {d['day']}** (收 {d['received']} 条, "
                    f"mood: *{d['mood']}*, engage {d['engagement']}/10) → "
                    f"`{d['action']}` — {d['reason']}"
                )
            v = r.get("verdict", {})
            if "error" not in v:
                lines.append("")
                lines.append("**最终判定**:")
                lines.append(f"- 续订: {v.get('final_subscribe', '?')}")
                lines.append(f"- 月费意愿: "
                             f"{v.get('pricing_willingness_usd_month', '?')}")
                lines.append(f"- 最大阻力: {v.get('top_friction', '?')}")
                lines.append(f"- 欣赏: {v.get('what_worked', '?')}")
                lines.append("- 原话:")
                lines.append(f"  > {v.get('verbatim_review', '?')}")
            lines.append("")

        return "\n".join(lines) + "\n"
