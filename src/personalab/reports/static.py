"""StaticReporter — render StaticMode results as markdown.

Translates a StaticMode ModeResult into the same markdown shape the original
okx_pulse persona_report.md used, plus cross-persona keyword aggregation.
"""
from __future__ import annotations

from typing import Any

from personalab.core.mode import ModeResult
from personalab.core.reporter import Reporter
from personalab.core.timeutil import now_cst_str


_PATTERN_KEYWORDS = [
    "噪声", "太多", "术语", "复杂", "动作", "建议", "不懂", "宏观",
    "小币", "复盘", "API", "白标", "导出", "稳定", "透明", "熔断",
    "onboarding", "默认",
]


class StaticReporter(Reporter):
    name = "static-report"

    def __init__(self, keywords: list[str] | None = None,
                 product_label: str | None = None) -> None:
        self.keywords = keywords or list(_PATTERN_KEYWORDS)
        self.product_label = product_label

    def render(self, result: ModeResult, **opts: Any) -> str:
        meta = result.metadata
        product = self.product_label or meta.get("product", "?")
        n_events = meta.get("n_events", "?")
        lines: list[str] = [
            f"# {product} 人格静态测试报告",
            "",
            f"生成时间: {now_cst_str()}  ·  样本事件: {n_events}  ·  LLM: {meta.get('llm', '?')}",
            "",
            "## 📊 汇总",
            "",
            "| 人格 | 会订阅 | 退订风险 | 愿付 USD/月 | 第一抱怨 |",
            "|---|---|---|---|---|",
        ]
        for r in result.results:
            if "error" in r:
                lines.append(f"| {r['persona']} | ❌ ERROR | - | - | "
                             f"{r['error'][:60]} |")
                continue
            ws = r.get("would_subscribe", "?")
            ws_icon = {"yes": "✅ yes", "maybe": "⚠ maybe",
                       "no": "❌ no"}.get(ws, str(ws))
            score = r.get("quit_trigger_score", "?")
            score_str = (f"{score}/10" if isinstance(score, (int, float))
                         else str(score))
            price = r.get("pricing_willingness_usd_month", "?")
            complaint = (r.get("first_complaint") or "")[:80].replace("|", "/")
            lines.append(f"| {r['persona']} | {ws_icon} | {score_str} | "
                         f"{price} | {complaint} |")

        lines += ["", "## 🗣 详细反馈", ""]
        for r in result.results:
            if "error" in r:
                continue
            lines.append(f"### {r['persona']}")
            lines.append("")
            lines.append(f"- **会订阅**: {r.get('would_subscribe', '?')}")
            lines.append(f"- **退订风险**: {r.get('quit_trigger_score', '?')}/10")
            lines.append(f"- **愿付月费**: "
                         f"{r.get('pricing_willingness_usd_month', '?')}")
            lines.append(f"- **吐槽**: {r.get('first_complaint', '')}")
            lines.append(f"- **欣赏**: {r.get('what_works', '')}")
            lines.append("- **TOP 3 改进**:")
            for ch in r.get("top_3_changes") or []:
                lines.append(f"  - {ch}")
            lines.append("- **原话**:")
            lines.append(f"  > {r.get('verbatim_reaction', '')}")
            lines.append("")

        # Cross-persona keyword pattern
        lines += ["## 🔄 跨人格模式", ""]
        complaints = [r.get("first_complaint", "")
                      for r in result.results if "error" not in r]
        counts: dict[str, int] = {}
        for c in complaints:
            for kw in self.keywords:
                if kw in c:
                    counts[kw] = counts.get(kw, 0) + 1
        if counts:
            ranked = sorted(counts.items(), key=lambda x: -x[1])
            lines.append("最常被提到的关键词（≥2 人格）:")
            any_shown = False
            for kw, n in ranked:
                if n >= 2:
                    lines.append(f"- `{kw}` × {n}")
                    any_shown = True
            if not any_shown:
                lines.append("（无关键词被 ≥2 个人格提到）")
        else:
            lines.append("（无关键词匹配）")

        return "\n".join(lines) + "\n"
