"""ABReporter — render ABMode diff report.

Headline metrics:
- per-persona subscribe delta (no→maybe = +1 = improvement)
- count of personas that "got better" / "got worse" / "no change"
- net impact score = Σ(sub_delta) + Σ(price_delta) - Σ(quit_score_delta)
"""
from __future__ import annotations

from typing import Any

from personalab.core.mode import ModeResult
from personalab.core.reporter import Reporter
from personalab.core.timeutil import now_cst_str


_DELTA_ICON = {
    None: "—",
    -2: "⬇⬇", -1: "⬇",
    0: "·",
    1: "⬆", 2: "⬆⬆",
}


def _icon(d) -> str:
    if d is None:
        return "—"
    if isinstance(d, (int, float)):
        if d <= -2:
            return "⬇⬇"
        if d == -1:
            return "⬇"
        if d == 0:
            return "·"
        if d == 1:
            return "⬆"
        return "⬆⬆"
    return "?"


class ABReporter(Reporter):
    name = "ab-report"

    def render(self, result: ModeResult, **opts: Any) -> str:
        meta = result.metadata
        a_name = meta.get("label_a", "A") + f" ({meta.get('product_a', '?')})"
        b_name = meta.get("label_b", "B") + f" ({meta.get('product_b', '?')})"
        inner = meta.get("inner_mode", "?")

        lines: list[str] = [
            f"# A/B 测试报告 — {a_name} vs {b_name}",
            "",
            f"生成: {now_cst_str()} · 内层模式: `{inner}` · "
            f"LLM: `{meta.get('llm', '?')}` · 人格: {len(result.results)}",
            "",
            "## Headline",
            "",
        ]

        sub_deltas: list[int] = []
        price_deltas: list[int] = []
        improved = worsened = unchanged = 0
        for r in result.results:
            d = r["diff"]
            sd = d.get("sub_delta")
            pd = d.get("price_delta")
            if isinstance(sd, int):
                sub_deltas.append(sd)
                if sd > 0:
                    improved += 1
                elif sd < 0:
                    worsened += 1
                else:
                    unchanged += 1
            if isinstance(pd, int):
                price_deltas.append(pd)

        sub_sum = sum(sub_deltas) if sub_deltas else 0
        price_sum = sum(price_deltas) if price_deltas else 0
        net = sub_sum + price_sum

        lines.append(f"- 订阅意愿变化: **改善 {improved}** / 不变 {unchanged} / "
                     f"恶化 {worsened}")
        lines.append(f"- 订阅 delta 累计: **{sub_sum:+d}**  ·  "
                     f"价格 delta 累计: {price_sum:+d}")
        lines.append(f"- **净影响分**: {net:+d}  "
                     f"（正数 = B 产品在人格视角下更好）")
        if net > 0:
            lines.append(f"- ✅ 结论：B 比 A 更好（人格视角，n={len(result.results)}）")
        elif net < 0:
            lines.append("- ❌ 结论：B 比 A 更糟")
        else:
            lines.append("- ⚪ 结论：B 与 A 无显著差异")
        lines.append("")

        lines += ["## 人格 × 产品矩阵", "",
                  f"| 人格 | {a_name} | {b_name} | sub Δ | price Δ | quit Δ |",
                  "|---|---|---|---|---|---|"]
        for r in result.results:
            d = r["diff"]
            sub_a = d.get("subscribe_a") or "?"
            sub_b = d.get("subscribe_b") or "?"
            price_a = d.get("price_a") or "?"
            price_b = d.get("price_b") or "?"
            lines.append(
                f"| {r['persona']} | {sub_a} / ${price_a} | "
                f"{sub_b} / ${price_b} | "
                f"{_icon(d.get('sub_delta'))} {d.get('sub_delta', '—')} | "
                f"{_icon(d.get('price_delta'))} {d.get('price_delta', '—')} | "
                f"{_icon(-(d.get('quit_score_delta') or 0)) if d.get('quit_score_delta') is not None else '—'} "
                f"{d.get('quit_score_delta', '—')} |"
            )

        # Highlights
        lines += ["", "## 显著变化人格（|sub_delta| ≥ 1 或 |price_delta| ≥ 2）", ""]
        notable = [r for r in result.results
                   if (isinstance(r["diff"].get("sub_delta"), int)
                       and abs(r["diff"]["sub_delta"]) >= 1)
                   or (isinstance(r["diff"].get("price_delta"), int)
                       and abs(r["diff"]["price_delta"]) >= 2)]
        if not notable:
            lines.append("（无人格出现显著变化 —— B 的修改未触动 verdict）")
        else:
            for r in notable:
                d = r["diff"]
                a = r["a"]; b = r["b"]
                lines.append(f"### {r['persona']}")
                lines.append("")
                lines.append(f"- **{a_name}**: subscribe={d.get('subscribe_a')} "
                             f"price=${d.get('price_a')}")
                # original quotes
                quote_a = (a.get("verbatim_review")
                           or a.get("verbatim_reaction")
                           or (a.get("verdict") or {}).get("verbatim_review"))
                if quote_a:
                    lines.append(f"  > {quote_a[:240]}")
                lines.append(f"- **{b_name}**: subscribe={d.get('subscribe_b')} "
                             f"price=${d.get('price_b')}")
                quote_b = (b.get("verbatim_review")
                           or b.get("verbatim_reaction")
                           or (b.get("verdict") or {}).get("verbatim_review"))
                if quote_b:
                    lines.append(f"  > {quote_b[:240]}")
                lines.append("")

        return "\n".join(lines) + "\n"
