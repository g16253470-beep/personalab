"""ActionLoopReporter — convert persona feedback into P0/P1/P2 issue list.

Takes static and/or agentic results and clusters complaints (`top_friction`,
`first_complaint`, `top_3_changes`) by keyword. Issues mentioned by more
personas + hostile personas (competitor_ceo, compliance, yc_partner, troll)
get higher priority.

Output is markdown ready to paste into GitHub/Linear/Jira — each issue cites
the ≥2 persona quotes that motivated it, so engineering can argue with the
evidence, not the framework.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from personalab.core.mode import ModeResult
from personalab.core.reporter import Reporter
from personalab.core.timeutil import now_cst_str


HOSTILE_PERSONA_HINTS = (
    "competitor", "compliance", "troll", "yc_partner", "skeptical",
)


# Pre-defined keyword buckets. Each bucket = one issue candidate.
# A persona "mentions" the bucket if ANY of its synonyms appear in their
# friction/complaint/changes text.
DEFAULT_BUCKETS: dict[str, list[str]] = {
    "AI 稳定性": ["AI", "熔断", "RuntimeError", "schema", "fallback",
                   "placeholder", "_ai_unavailable"],
    "推送音量": ["太多", "噪声", "音量", "刷屏", "每天 10", "上百", "塞了"],
    "Onboarding / 默认": ["默认", "whale", "onboarding", "新用户", "/start",
                            "引导"],
    "透明度": ["源码", "transparency", "透明", "changelog", "版本号",
                "OSS", "审计"],
    "方向性语言 / 合规": ["主导", "测试支撑", "买盘", "建议", "动作",
                          "方向性", "compliance", "合规", "警告函"],
    "用户控制": ["导出", "API", "白标", "self-host", "webhook"],
    "复盘": ["复盘", "每周", "周报", "summary", "总结"],
    "小币 / 币种过滤": ["小币", "宏观", "BTC", "ETH", "macro", "altcoin"],
}


# Hostile-or-technical personas count double for priority weighting.
PRIORITY_THRESHOLDS = {"P0": 5, "P1": 3, "P2": 2}


@dataclass
class IssueCandidate:
    bucket: str
    weight: float
    mentions: list[tuple[str, str]] = field(default_factory=list)  # (persona, quote)

    def priority(self) -> str:
        if self.weight >= PRIORITY_THRESHOLDS["P0"]:
            return "P0"
        if self.weight >= PRIORITY_THRESHOLDS["P1"]:
            return "P1"
        if self.weight >= PRIORITY_THRESHOLDS["P2"]:
            return "P2"
        return "P3"


def _is_hostile(persona_name: str) -> bool:
    name = persona_name.lower()
    return any(h in name for h in HOSTILE_PERSONA_HINTS)


def _persona_texts(result: ModeResult, agentic: bool) -> list[tuple[str, str]]:
    """Return list of (persona_name, combined_complaint_text)."""
    out: list[tuple[str, str]] = []
    for r in result.results:
        name = r.get("persona", "?")
        if agentic:
            v = r.get("verdict") or {}
            if "error" in v:
                continue
            text = " ".join(filter(None, [
                str(v.get("top_friction", "")),
                str(v.get("what_worked", "")),
                str(v.get("verbatim_review", "")),
                " ".join(str(d.get("reason", ""))
                          for d in r.get("decisions", [])),
            ]))
        else:
            if "error" in r:
                continue
            text = " ".join(filter(None, [
                str(r.get("first_complaint", "")),
                str(r.get("verbatim_reaction", "")),
                " ".join(str(c) for c in r.get("top_3_changes") or []),
            ]))
        if text.strip():
            out.append((name, text))
    return out


class ActionLoopReporter(Reporter):
    name = "action-loop-report"

    def __init__(self, buckets: dict[str, list[str]] | None = None,
                 product_label: str | None = None) -> None:
        self.buckets = buckets or {k: list(v) for k, v in DEFAULT_BUCKETS.items()}
        self.product_label = product_label

    # The base render() takes one ModeResult; the comparison case uses render_dual()
    def render(self, result: ModeResult, **opts: Any) -> str:
        return self._render_combined(static=None, agentic=result) \
            if result.mode == "agentic" else \
            self._render_combined(static=result, agentic=None)

    def render_dual(self, static: ModeResult, agentic: ModeResult) -> str:
        return self._render_combined(static=static, agentic=agentic)

    # ------------------------------------------------------------------
    def _collect_candidates(
        self, static: ModeResult | None,
        agentic: ModeResult | None,
    ) -> list[IssueCandidate]:
        all_texts: list[tuple[str, str, bool]] = []  # (persona, text, is_agentic)
        if static:
            for n, t in _persona_texts(static, agentic=False):
                all_texts.append((n, t, False))
        if agentic:
            for n, t in _persona_texts(agentic, agentic=True):
                all_texts.append((n, t, True))

        candidates: list[IssueCandidate] = []
        for bucket, kws in self.buckets.items():
            mentions: list[tuple[str, str]] = []
            seen_personas: set[str] = set()
            weight = 0.0
            for persona, text, is_agentic in all_texts:
                if any(kw in text for kw in kws):
                    if persona in seen_personas:
                        continue
                    seen_personas.add(persona)
                    quote = _quote_for_bucket(text, kws)
                    mentions.append((persona, quote))
                    base = 1.5 if is_agentic else 1.0
                    weight += base * (2.0 if _is_hostile(persona) else 1.0)
            if mentions:
                candidates.append(IssueCandidate(
                    bucket=bucket, weight=round(weight, 1), mentions=mentions))
        candidates.sort(key=lambda c: -c.weight)
        return candidates

    def _render_combined(self, static: ModeResult | None,
                          agentic: ModeResult | None) -> str:
        product = (self.product_label
                   or (static and static.metadata.get("product"))
                   or (agentic and agentic.metadata.get("product"))
                   or "?")
        n_personas = max(
            len(static.results) if static else 0,
            len(agentic.results) if agentic else 0,
        )
        cands = self._collect_candidates(static, agentic)
        by_p: dict[str, list[IssueCandidate]] = {"P0": [], "P1": [],
                                                  "P2": [], "P3": []}
        for c in cands:
            by_p[c.priority()].append(c)

        lines: list[str] = [
            f"# {product} — 行动闭环（人格反馈 → issue 清单）",
            "",
            f"生成: {now_cst_str()} · 人格池: {n_personas} · "
            f"{'static' if static else ''}"
            f"{' + ' if static and agentic else ''}"
            f"{'agentic' if agentic else ''}",
            "",
            "## 优先级规则",
            "",
            "- **权重** = Σ(per-persona base × hostile_multiplier)",
            "- agentic 提及 base=1.5（行为证据强于第一印象 base=1.0）",
            "- 敌意/技术挑剔 persona × 2（competitor / compliance / yc / skeptical / troll）",
            f"- P0 ≥ {PRIORITY_THRESHOLDS['P0']} · P1 ≥ {PRIORITY_THRESHOLDS['P1']} · "
            f"P2 ≥ {PRIORITY_THRESHOLDS['P2']}",
            "",
        ]
        for prio in ("P0", "P1", "P2", "P3"):
            issues = by_p[prio]
            if not issues:
                continue
            lines.append(f"## {prio}")
            lines.append("")
            for i, c in enumerate(issues, 1):
                lines.append(f"### {prio}.{i} {c.bucket}  (weight={c.weight})")
                lines.append("")
                lines.append(f"**提及人格**（{len(c.mentions)}）: " + ", ".join(
                    f"`{p}`" for p, _ in c.mentions))
                lines.append("")
                lines.append("**引用**:")
                for p, quote in c.mentions:
                    lines.append(f"- **{p}**: \"{quote}\"")
                lines.append("")
        if not any(by_p.values()):
            lines.append("_（无任何 keyword bucket 命中。可能 personas 反馈太杂"
                         "或 buckets 太窄，考虑扩词典。）_")
        return "\n".join(lines) + "\n"


def _quote_for_bucket(text: str, kws: list[str], window: int = 60) -> str:
    """Return ~window-char excerpt centered on the first keyword hit."""
    for kw in kws:
        idx = text.find(kw)
        if idx >= 0:
            start = max(0, idx - window // 2)
            end = min(len(text), idx + window // 2)
            return text[start:end].strip().replace("\n", " ")
    return text[:window].strip()
