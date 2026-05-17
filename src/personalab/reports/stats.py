"""StatsReporter — render StatsMode results with variance bars + noisy flags."""
from __future__ import annotations

from typing import Any

from personalab.core.mode import ModeResult
from personalab.core.reporter import Reporter
from personalab.core.timeutil import now_cst_str


def _fmt_summary(s: dict | None) -> str:
    if not s or s.get("n", 0) == 0:
        return "—"
    mean = s.get("mean", "?")
    std = s.get("std", "?")
    ci = s.get("ci95")
    ci_str = f"[{ci[0]}, {ci[1]}]" if ci else ""
    return f"{mean} ± {std} {ci_str}"


class StatsReporter(Reporter):
    name = "stats-report"

    def render(self, result: ModeResult, **opts: Any) -> str:
        meta = result.metadata
        inner = meta.get("inner_mode", "?")
        repeats = meta.get("repeats", "?")
        lines: list[str] = [
            f"# 统计稳健性报告 — inner mode `{inner}` × {repeats} 次重复",
            "",
            f"生成: {now_cst_str()}  ·  人格: {len(result.results)}  ·  "
            f"LLM: `{meta.get('llm', '?')}`",
            "",
            "## 解读",
            "",
            "- **agreement** < 0.5 表示该 persona 在多次跑里 verdict 翻转，"
            "**LLM 抖动 > 人格稳定信号**，不要把这条 verdict 当真",
            "- 数值 `mean ± std [CI95]` 的 std 接近或大于 mean 时同上",
            "- 整张表里 `noisy` 列非空的行，所有结论都要打折",
            "",
            "## 汇总（订阅意愿）",
            "",
            "| 人格 | 主流 verdict | 一致率 | quit_score | noisy fields |",
            "|---|---|---|---|---|",
        ]
        for r in result.results:
            a = r.get("aggregated", {})
            sub = (a.get("would_subscribe_modal")
                   or a.get("final_subscribe_modal") or "?")
            agr = (a.get("would_subscribe_agreement")
                   or a.get("final_subscribe_agreement") or "?")
            score = _fmt_summary(a.get("quit_trigger_score"))
            noisy = ", ".join(r.get("noisy", [])) or "—"
            lines.append(f"| {r['persona']} | {sub} | {agr} | {score} | "
                         f"{noisy} |")

        lines += ["", "## 月费意愿分布（多次跑）", "",
                  "| 人格 | 主流价位 | 一致率 |",
                  "|---|---|---|"]
        for r in result.results:
            a = r.get("aggregated", {})
            price = a.get("pricing_willingness_usd_month_modal") or "?"
            agr = a.get("pricing_willingness_usd_month_agreement") or "?"
            lines.append(f"| {r['persona']} | ${price} | {agr} |")

        # Highlight noisy personas
        noisy_personas = [r for r in result.results if r.get("noisy")]
        if noisy_personas:
            lines += ["", "## ⚠️ 高方差人格 — verdict 不稳定", ""]
            for r in noisy_personas:
                lines.append(f"### {r['persona']}")
                lines.append(f"- noisy fields: `{', '.join(r['noisy'])}`")
                lines.append(f"- 跨 {r['n_runs']} 次跑的 raw verdict:")
                for i, run in enumerate(r["runs"], 1):
                    sub = run.get("would_subscribe") \
                        or (run.get("verdict") or {}).get("final_subscribe")
                    score = run.get("quit_trigger_score") or "-"
                    lines.append(f"  - run {i}: subscribe={sub} "
                                 f"quit_score={score}")
                lines.append("")

        return "\n".join(lines) + "\n"
