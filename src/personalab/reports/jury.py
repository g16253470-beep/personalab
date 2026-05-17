"""JuryReporter — render JuryMode results as persona × LLM matrix + agreement."""
from __future__ import annotations

from typing import Any

from personalab.core.mode import ModeResult
from personalab.core.reporter import Reporter
from personalab.core.timeutil import now_cst_str


def _sub_icon(v: str | None) -> str:
    return {"yes": "✅", "maybe": "⚠", "no": "❌"}.get(str(v), "?")


class JuryReporter(Reporter):
    name = "jury-report"

    def __init__(self, product_label: str | None = None) -> None:
        self.product_label = product_label

    def render(self, result: ModeResult, **opts: Any) -> str:
        meta = result.metadata
        product = self.product_label or meta.get("product", "?")
        jury = meta.get("jury", [])
        n_events = meta.get("n_events", "?")

        lines: list[str] = [
            f"# {product} — Jury Mode（多模型评委）",
            "",
            f"生成: {now_cst_str()} · 事件: {n_events} · "
            f"陪审团: {len(jury)} 个模型",
            "",
            "模型列表:",
            "",
        ]
        for j in jury:
            lines.append(f"- `{j}`")
        lines += ["", "## 订阅意愿矩阵", "",
                  "| 人格 | " + " | ".join(jury) + " | overall_agree |",
                  "|---|" + "---|" * (len(jury) + 1)]
        for r in result.results:
            per_llm = r.get("per_llm", [])
            cells = []
            for j in jury:
                hit = next((x for x in per_llm if x["llm"] == j), None)
                if not hit:
                    cells.append("—")
                elif "error" in hit:
                    cells.append("ERR")
                else:
                    sub = hit.get("would_subscribe", "?")
                    score = hit.get("quit_trigger_score", "?")
                    cells.append(f"{_sub_icon(sub)} {sub} q{score}")
            agree = r.get("agreement", {}).get("_overall", "?")
            lines.append(f"| {r['persona']} | " + " | ".join(cells)
                         + f" | **{agree}** |")

        lines += ["", "## 月费意愿矩阵", "",
                  "| 人格 | " + " | ".join(jury) + " | agree |",
                  "|---|" + "---|" * (len(jury) + 1)]
        for r in result.results:
            per_llm = r.get("per_llm", [])
            cells = []
            for j in jury:
                hit = next((x for x in per_llm if x["llm"] == j), None)
                if hit and "error" not in hit:
                    cells.append(str(hit.get("pricing_willingness_usd_month",
                                              "?")))
                else:
                    cells.append("—")
            agree = r.get("agreement", {}).get(
                "pricing_willingness_usd_month", "?")
            lines.append(f"| {r['persona']} | " + " | ".join(cells)
                         + f" | {agree} |")

        # Highlight low-agreement personas
        low_agree = [r for r in result.results
                     if isinstance(r.get("agreement", {}).get("_overall"),
                                    (int, float))
                     and r["agreement"]["_overall"] < 0.66]
        lines += ["", "## ⚠️ 低一致性人格（overall_agree < 0.66）", ""]
        if low_agree:
            lines.append("这些人格在不同 LLM 间分歧大 —— 不要据其单一结论决策。")
            lines.append("")
            for r in low_agree:
                lines.append(f"### {r['persona']} (agree={r['agreement']['_overall']})")
                for entry in r.get("per_llm", []):
                    if "error" in entry:
                        lines.append(f"- **{entry['llm']}**: ERROR — "
                                     f"{entry['error'][:80]}")
                        continue
                    lines.append(
                        f"- **{entry['llm']}**: {entry.get('would_subscribe')}"
                        f" / q{entry.get('quit_trigger_score')} / "
                        f"${entry.get('pricing_willingness_usd_month')}"
                    )
                lines.append("")
        else:
            lines.append("（所有人格的多模型 verdict 都达到 ≥0.66 一致）")
            lines.append("")

        return "\n".join(lines) + "\n"
