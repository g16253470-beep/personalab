"""CalibrationReporter — render persona-vs-real-user metrics."""
from __future__ import annotations

from personalab.calibration.metrics import CalibrationResult
from personalab.core.timeutil import now_cst_str


class CalibrationReporter:
    """Stand-alone reporter — not part of ModeResult pipeline."""

    def __init__(self, product_label: str | None = None) -> None:
        self.product_label = product_label

    def render(self, result: CalibrationResult, **_) -> str:
        cm = result.subscribe
        product = self.product_label or "?"

        verdict = "✅ 人格预测有效"
        if cm.accuracy() < 0.6:
            verdict = "❌ 人格预测不可靠（accuracy < 0.6）"
        elif cm.accuracy() < 0.75:
            verdict = "⚠️ 人格预测仅供参考（accuracy 0.6-0.75）"

        lines = [
            f"# {product} 人格预测校准报告",
            "",
            f"生成: {now_cst_str()} · 真实用户样本: {result.n} · "
            f"已匹配 personas: {len(result.matched_personas)}",
            "",
            f"## 总判定: {verdict}",
            "",
            "## 订阅意愿（二分类）",
            "",
            "| metric | value |",
            "|---|---|",
            f"| Accuracy | {cm.accuracy():.2%} |",
            f"| Precision | {cm.precision():.2%} |",
            f"| Recall    | {cm.recall():.2%} |",
            f"| F1        | {cm.f1():.2%} |",
            "",
            "### Confusion matrix",
            "",
            "|  | 真实订阅 | 真实未订阅 |",
            "|---|---|---|",
            f"| 预测会订阅 | TP={cm.tp} | FP={cm.fp} |",
            f"| 预测不订阅 | FN={cm.fn} | TN={cm.tn} |",
            "",
        ]

        if result.price_mae is not None:
            lines += [
                "## 月费意愿（价格回归）",
                "",
                f"- **MAE** ≈ ${result.price_mae:.2f}/月  "
                f"(bucket 中点 vs 实付)",
                "",
            ]
        if result.action_jaccard_mean is not None:
            lines += [
                "## 行动序列（Jaccard 相似度）",
                "",
                f"- 预测命令集 vs 真实命令集 平均 Jaccard = "
                f"{result.action_jaccard_mean:.2%}",
                "",
            ]

        lines += [
            "## 已对照人格",
            "",
            ", ".join(f"`{p}`" for p in result.matched_personas) or "（无）",
            "",
            "## Per-user 明细",
            "",
            "| user_id | persona | real sub | real $ | pred sub | pred $ |",
            "|---|---|---|---|---|---|",
        ]
        for u in result.per_user:
            if u.get("status") == "no_prediction":
                lines.append(f"| {u['real_user_id']} | {u['match']} | "
                             f"— | — | NO PREDICTION | — |")
                continue
            lines.append(
                f"| {u['real_user_id']} | {u['persona_match']} | "
                f"{u['real_subscribed']} | {u['real_pricing']} | "
                f"{u['pred_subscribe']} | {u['pred_pricing']} |"
            )

        return "\n".join(lines) + "\n"
