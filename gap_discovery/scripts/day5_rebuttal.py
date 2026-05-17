"""Day 5 — Persona rebuttal pipeline.

Stages:
  1. Load 235 dev-tool unmet needs from tagged_quotes.jsonl
  2. Ask LLM to propose 15-25 clusters from these needs
  3. For each of 12 personas, ask: which clusters do you think WON'T sell?
  4. Aggregate down-votes per cluster
  5. Save personas_rebuttal.md (full transcript) + defensible_clusters.json (votes <= 4)

Cost: ~14 Gemini Flash calls total (1 cluster + 1 sample + 12 personas).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

from google import genai


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
VERT = ROOT / "gap_discovery" / "verticals" / "dev_tools"
PERSONAS_DIR = ROOT / "personas"
DOWNVOTE_GATE = 4  # clusters with strictly more than this fail


CLUSTER_PROMPT = """你是产品研究分析师。下面是 {n} 条 dev tool 真实抱怨/未满足需求（来自 HN 评论，已过滤 dev-tool 相关）。

任务：把它们聚类成 **15-25 个高密度 cluster**。每个 cluster 满足：
- name 是 1 句话的需求描述（< 50 字）
- description 解释这个 cluster 的特征（< 100 字）
- 包含至少 3 条原始 quote 的 id

要求：
- 单一 cluster 内的 quote 描述同一类痛点，不能太散
- cluster 之间应有清晰差异，不要重复
- 优先 high severity + 集中 segment 的 cluster
- 跨多次提及的痛点（多个 ids）权重更高

输出严格 JSON（无 markdown 包裹）：
{{
  "clusters": [
    {{"id": "C1", "name": "...", "description": "...", "member_ids": ["hn_xxx", ...], "dominant_segment": "...", "dominant_category": "...", "estimated_severity_mean": 3.5}},
    ...
  ]
}}

=== 235 条 dev-tool unmet need ===

{items_text}

立即输出 JSON。"""


REBUTTAL_PROMPT = """你是下面这个虚构 SaaS 买家人格。

# 你的人格

{persona_body}

---

# 任务：反驳器（不是投票器）

下面是 {n_clusters} 个 dev tool 未满足需求 cluster，来自真实 HN 抱怨。
**从你这个人格视角**，找出 **哪些 cluster 不靠谱**（无法卖出去 / 没人付钱 / 已有产品解决 / 抱怨太分散 / 你这个人格也认为是 noise）。

每个被你 vote down 的 cluster，请给出 1 句话理由。

**严格约束**：
- 你必须 vote down 至少 3 个 cluster（即便所有都看起来 OK，也挑最弱的 3 个）
- 不要超过 8 个 vote down（否则只是宣泄）
- 理由要具体，引用 cluster 名字 + 你人格的具体顾虑

# 25 个 cluster

{clusters_text}

# 输出严格 JSON：

{{
  "persona": "{persona_name}",
  "vote_downs": [
    {{"cluster_id": "C1", "reason": "..."}},
    ...
  ]
}}

立即输出 JSON。"""


def strip_fence(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```\s*$", "", text)
    return text.strip()


def call_llm(client, prompt: str, model: str = "gemini-2.5-flash") -> dict:
    resp = client.models.generate_content(model=model, contents=prompt)
    text = strip_fence(resp.text or "")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            raise
        return json.loads(m.group(0))


def main() -> int:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        return 2
    client = genai.Client(api_key=api_key)

    # ── Stage 1: load + filter ──────────────────────────────────────
    tagged = [json.loads(l) for l in (VERT / "data" / "tagged_quotes.jsonl"
                                       ).read_text("utf-8").splitlines()
              if l.strip()]
    dev = [t for t in tagged if t.get("is_dev_tool_related")
           and t.get("unmet_need_one_line")]
    print(f"[stage 1] {len(dev)} dev-tool unmet needs ready", file=sys.stderr)

    # ── Stage 2: ask LLM to cluster ─────────────────────────────────
    items_text = "\n".join(
        f"[{t['id']}] sev={t.get('severity_1_5','?')} "
        f"seg={t.get('segment','?')} cat={t.get('category','?')} :: "
        f"{t.get('unmet_need_one_line','')}"
        for t in dev
    )
    print("[stage 2] asking LLM to cluster ...", file=sys.stderr)
    t0 = time.time()
    cluster_resp = call_llm(client, CLUSTER_PROMPT.format(
        n=len(dev), items_text=items_text))
    clusters = cluster_resp.get("clusters", [])
    print(f"[stage 2] got {len(clusters)} clusters in {time.time()-t0:.1f}s",
          file=sys.stderr)

    (VERT / "clusters.json").write_text(
        json.dumps(cluster_resp, ensure_ascii=False, indent=2),
        encoding="utf-8")

    # ── Stage 3: persona rebuttal ──────────────────────────────────
    persona_files = sorted(PERSONAS_DIR.glob("*.md"))
    clusters_text = "\n\n".join(
        f"### {c['id']}: {c['name']}\n"
        f"  描述: {c.get('description','')}\n"
        f"  主导 segment: {c.get('dominant_segment','?')}  "
        f"主导 category: {c.get('dominant_category','?')}  "
        f"成员数: {len(c.get('member_ids',[]))}  "
        f"sev≈{c.get('estimated_severity_mean','?')}"
        for c in clusters
    )

    all_rebuttals: list[dict] = []
    for pf in persona_files:
        persona_name = pf.stem
        persona_body = pf.read_text("utf-8")
        print(f"[stage 3] rebutting via {persona_name} ...", file=sys.stderr)
        try:
            rb = call_llm(client, REBUTTAL_PROMPT.format(
                persona_body=persona_body,
                n_clusters=len(clusters),
                clusters_text=clusters_text,
                persona_name=persona_name,
            ))
            all_rebuttals.append(rb)
            n_down = len(rb.get("vote_downs", []))
            print(f"  → {n_down} vote downs", file=sys.stderr)
        except Exception as e:
            print(f"  [warn] {persona_name} failed: {e}", file=sys.stderr)
            all_rebuttals.append({"persona": persona_name,
                                   "error": str(e)[:200]})

    # ── Stage 4: aggregate down-votes ──────────────────────────────
    vote_count: dict[str, int] = {c["id"]: 0 for c in clusters}
    reasons_by_cluster: dict[str, list[tuple[str, str]]] = {c["id"]: []
                                                              for c in clusters}
    for rb in all_rebuttals:
        if "error" in rb:
            continue
        for vd in rb.get("vote_downs", []):
            cid = vd.get("cluster_id")
            if cid in vote_count:
                vote_count[cid] += 1
                reasons_by_cluster[cid].append(
                    (rb.get("persona", "?"), vd.get("reason", "")))

    defensible = [c for c in clusters
                  if vote_count.get(c["id"], 0) <= DOWNVOTE_GATE]
    rejected = [c for c in clusters
                if vote_count.get(c["id"], 0) > DOWNVOTE_GATE]

    print(f"\n[stage 4] {len(defensible)} defensible (≤{DOWNVOTE_GATE} down) / "
          f"{len(rejected)} rejected", file=sys.stderr)

    # ── Stage 5: save outputs ──────────────────────────────────────
    (VERT / "defensible_clusters.json").write_text(
        json.dumps({
            "downvote_gate": DOWNVOTE_GATE,
            "clusters": [
                {**c, "down_vote_count": vote_count.get(c["id"], 0),
                 "reasons": reasons_by_cluster.get(c["id"], [])}
                for c in defensible
            ],
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # personas_rebuttal.md
    lines: list[str] = [
        "# Day 5 — Persona Rebuttal Report",
        "",
        f"_Generated: {time.strftime('%Y-%m-%d %H:%M')}_  ",
        f"_Source: 235 dev-tool unmet needs → {len(clusters)} clusters → "
        f"12 personas as rebutters._",
        "",
        "## 汇总",
        "",
        f"| Cluster | Name | Members | Sev | Down-votes | Verdict |",
        f"|---|---|---|---|---|---|",
    ]
    for c in clusters:
        v = vote_count.get(c["id"], 0)
        verdict = "✅ defensible" if v <= DOWNVOTE_GATE else "❌ rejected"
        lines.append(
            f"| {c['id']} | {c['name'][:60]} | "
            f"{len(c.get('member_ids',[]))} | "
            f"{c.get('estimated_severity_mean','?')} | "
            f"**{v}/12** | {verdict} |"
        )

    lines += ["", "## ✅ Defensible clusters (≤ 4 down-votes) — 进入 Day 6", ""]
    for c in defensible:
        v = vote_count.get(c["id"], 0)
        lines.append(f"### {c['id']} — {c['name']} (down: {v}/12)")
        lines.append("")
        lines.append(f"**描述**: {c.get('description','')}")
        lines.append(f"**主导 segment**: `{c.get('dominant_segment','?')}` · "
                     f"**主导 category**: `{c.get('dominant_category','?')}` · "
                     f"成员: {len(c.get('member_ids',[]))} · "
                     f"sev≈{c.get('estimated_severity_mean','?')}")
        if reasons_by_cluster.get(c["id"]):
            lines.append("")
            lines.append("**Persona rebuttals**（少数派意见）：")
            for p, r in reasons_by_cluster[c["id"]]:
                lines.append(f"- `{p}`: {r}")
        lines.append("")

    lines += ["", "## ❌ Rejected clusters (> 4 down-votes)", ""]
    for c in rejected:
        v = vote_count.get(c["id"], 0)
        lines.append(f"### {c['id']} — {c['name']} (down: {v}/12)")
        lines.append("")
        lines.append(f"**描述**: {c.get('description','')}")
        lines.append("")
        lines.append("**Persona rebuttals**:")
        for p, r in reasons_by_cluster.get(c["id"], []):
            lines.append(f"- `{p}`: {r}")
        lines.append("")

    (VERT / "personas_rebuttal.md").write_text(
        "\n".join(lines), encoding="utf-8")

    print(f"\n[OK] wrote:", file=sys.stderr)
    print(f"  - {VERT / 'clusters.json'}", file=sys.stderr)
    print(f"  - {VERT / 'defensible_clusters.json'}", file=sys.stderr)
    print(f"  - {VERT / 'personas_rebuttal.md'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
