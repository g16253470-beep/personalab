"""ComparisonReporter — render Static + Agentic dual-track comparison.

Replicates the analytical structure of docs/persona_comparison_v12.6.md:
1. Method comparison table
2. Per-persona side-by-side verdict
3. Conversion delta (static vs agentic)
4. Top-N killer issues (mentioned by ≥2 personas in agentic)
5. Method conclusions

Takes TWO ModeResults — one static, one agentic — that ran the SAME personas
against the SAME product. Mismatched personas are flagged.
"""
from __future__ import annotations

from collections import Counter
from typing import Any

from personalab.core.mode import ModeResult
from personalab.core.reporter import Reporter
from personalab.core.timeutil import now_cst_str


_FRICTION_KEYWORDS = [
    "AI", "熔断", "RuntimeError", "schema", "稳定", "透明", "源码",
    "changelog", "版本", "默认", "whale", "onboarding", "新用户",
    "噪声", "太多", "复杂", "动作", "宏观", "小币", "BTC", "ETH",
    "compliance", "合规", "方向性", "导出", "API", "白标",
]


def _normalize_sub(v: dict) -> str:
    return str(v.get("final_subscribe") or v.get("would_subscribe") or "?")


def _classify(s: str) -> str:
    s = s.lower()
    if s == "yes":
        return "yes"
    if s == "maybe":
        return "maybe"
    if s == "no":
        return "no"
    return "?"


class ComparisonReporter(Reporter):
    name = "comparison-report"

    def __init__(self, product_label: str | None = None,
                 friction_keywords: list[str] | None = None) -> None:
        self.product_label = product_label
        self.friction_keywords = friction_keywords or list(_FRICTION_KEYWORDS)

    def render(self, result: ModeResult, **opts: Any) -> str:  # noqa: ARG002
        raise NotImplementedError("ComparisonReporter takes two results — "
                                  "use render_dual() instead")

    def render_dual(self, static: ModeResult, agentic: ModeResult) -> str:
        product = (self.product_label
                   or static.metadata.get("product")
                   or agentic.metadata.get("product")
                   or "?")
        s_by_name = {r["persona"]: r for r in static.results}
        a_by_name = {r["persona"]: r for r in agentic.results}
        all_names = sorted(set(s_by_name) | set(a_by_name))

        lines: list[str] = [
            f"# {product} 双轨人格测试对比",
            "",
            f"**生成**: {now_cst_str()}  ·  "
            f"static events: {static.metadata.get('n_events', '?')}  ·  "
            f"agentic events: {agentic.metadata.get('n_events', '?')}  ·  "
            f"days: {agentic.metadata.get('days', '?')}",
            "",
            "## 方法对比",
            "",
            "| 维度 | Static（Tier 2）| Agentic（Tier 4）|",
            "|---|---|---|",
            "| 输入 | 一次性 transcript | N 个虚拟日分段流，每日决策一次 |",
            f"| 人格 | {len(static.results)} | {len(agentic.results)} |",
            f"| LLM 调用 | {len(static.results)} | "
            f"~{len(agentic.results) * (agentic.metadata.get('days', 0) + 1)} |",
            "| 决策点 | 1 次（看完即评） | N+1 次/人格（每日 + 最终verdict）|",
            "| 可观察行为 | \"如果是我，我会...\" | 实际切配置 / mute / 退订 |",
            f"| LLM | {static.metadata.get('llm', '?')} | "
            f"{agentic.metadata.get('llm', '?')} |",
            "",
            "## 总结果对比",
            "",
            "| 人格 | Static | Agentic | 一致性 |",
            "|---|---|---|---|",
        ]

        s_counts = Counter()
        a_counts = Counter()
        s_err = a_err = 0

        for name in all_names:
            s = s_by_name.get(name)
            a = a_by_name.get(name)
            s_str = "—"
            if s:
                if "error" in s:
                    s_str = "ERR"
                    s_err += 1
                else:
                    s_sub = _classify(_normalize_sub(s))
                    s_q = s.get("quit_trigger_score", "?")
                    s_str = f"{s_sub} q{s_q}"
                    s_counts[s_sub] += 1
            a_str = "—"
            quit_day = None
            if a:
                v = a.get("verdict") or {}
                if "error" in v:
                    a_str = "ERR"
                    a_err += 1
                else:
                    a_sub = _classify(_normalize_sub(v))
                    price = v.get("pricing_willingness_usd_month", "?")
                    quit_day = a.get("quit_day")
                    quit_str = f" day{quit_day}退" if quit_day else ""
                    a_str = f"**{a_sub}** ${price}{quit_str}"
                    a_counts[a_sub] += 1
            # consistency tag
            consistency = "—"
            if s and a and "error" not in s and "error" not in (
                    a.get("verdict") or {}):
                s_sub = _classify(_normalize_sub(s))
                a_sub = _classify(_normalize_sub(a.get("verdict") or {}))
                if s_sub == a_sub:
                    consistency = "✅ 一致"
                elif s_sub == "maybe" and a_sub == "no":
                    consistency = "⬇️ 行为更严"
                elif s_sub == "no" and a_sub == "maybe":
                    consistency = "⬆️ 行为更宽"
                else:
                    consistency = "⚠️ 矛盾"
            lines.append(f"| {name} | {s_str} | {a_str} | {consistency} |")

        lines += [
            "",
            "**Verdict count**:",
            f"- Static:  {s_counts.get('yes', 0)} yes / "
            f"{s_counts.get('maybe', 0)} maybe / "
            f"{s_counts.get('no', 0)} no / {s_err} err",
            f"- Agentic: {a_counts.get('yes', 0)} yes / "
            f"{a_counts.get('maybe', 0)} maybe / "
            f"{a_counts.get('no', 0)} no / {a_err} err",
            "",
        ]
        downgrades = s_counts.get("maybe", 0) - a_counts.get("maybe", 0)
        if downgrades > 0:
            lines.append(f"**Agentic 把 {downgrades} 个 'maybe' 打回原形成 NO** —— "
                         f"一次性印象比多日体验宽容。")
            lines.append("")

        # Top friction keywords aggregated from agentic top_friction
        lines += ["## Top 痛点关键词（agentic top_friction，≥2 人格）", ""]
        kw_counts: Counter[str] = Counter()
        kw_personas: dict[str, list[str]] = {}
        for r in agentic.results:
            v = r.get("verdict") or {}
            tf = v.get("top_friction", "") or ""
            for kw in self.friction_keywords:
                if kw in tf:
                    kw_counts[kw] += 1
                    kw_personas.setdefault(kw, []).append(r["persona"])
        for kw, n in kw_counts.most_common():
            if n >= 2:
                lines.append(f"- `{kw}` × {n} — "
                             f"{', '.join(kw_personas[kw])}")
        if not any(n >= 2 for n in kw_counts.values()):
            lines.append("（无关键词被 ≥2 个人格提到）")

        # Method conclusions
        lines += [
            "",
            "## 方法学结论",
            "",
            "**Static 测试有用但乐观偏移**："
            "一次性 transcript 给了产品 benefit of doubt；"
            "Agentic 把 \"maybe 我可能会试试\" 转化成 \"试过了，不行\"。",
            "",
            "**最具决定性的差距：跨日行为**："
            "短 transcript 中只是 1-2 条异常的问题，多日运行就成 pattern。",
            "",
        ]

        # Pricing willingness distribution
        lines += [
            "## 💰 月费意愿分布（agentic verdict）", "",
            "| 价位 | 人格 |",
            "|---|---|",
        ]
        price_buckets: dict[str, list[str]] = {}
        for r in agentic.results:
            v = r.get("verdict") or {}
            price = v.get("pricing_willingness_usd_month")
            if price:
                price_buckets.setdefault(str(price), []).append(r["persona"])
        for price in ["200+", "50-200", "20-50", "5-20", "0"]:
            ps = price_buckets.get(price, [])
            if ps:
                lines.append(f"| ${price} | {', '.join(ps)} |")
        lines.append("")

        return "\n".join(lines) + "\n"
