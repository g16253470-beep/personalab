"""Day 6 — Incumbent teardown for Top 4 defensible clusters.

For each (cluster, incumbent) pair, LLM judges:
- coverage_score 1-5 (1=completely unsolved, 5=fully solved)
- missing_gap: the single most important thing incumbent doesn't cover
- typical_user_complaint: what real users complain about for this incumbent
- price_anchor: USD/month equivalent

Aggregate per cluster:
- mean_coverage (1-5)
- non_coverage_ratio = 1 - (mean_coverage / 5)  → 0 to 1, higher = more opportunity
- consolidated_missing_gaps: union of all incumbents' missing pieces
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


# Hardcoded incumbent list per cluster (from DECISIONS.md D-15)
INCUMBENTS = {
    "C3": [
        {"name": "CodeRabbit", "url": "coderabbit.ai",
         "blurb": "AI code review for GitHub/GitLab PRs, summarizes diffs and suggests fixes",
         "price": "$15/user/mo Pro"},
        {"name": "Sourcery", "url": "sourcery.ai",
         "blurb": "AI Python code review + auto-refactor, IDE plugins",
         "price": "$10/user/mo"},
        {"name": "Linear", "url": "linear.app",
         "blurb": "issue tracker + project management for engineering teams",
         "price": "$8/user/mo Standard"},
        {"name": "GitHub PR Reviews", "url": "github.com",
         "blurb": "native PR review, comments, suggestions, code owners",
         "price": "Free / GH plan"},
        {"name": "Graphite", "url": "graphite.dev",
         "blurb": "stacked PR workflow + AI review, made for fast-shipping teams",
         "price": "$25/user/mo Team"},
    ],
    "C4": [
        {"name": "Cursor", "url": "cursor.sh",
         "blurb": "AI-native IDE forked from VSCode, deep LLM integration",
         "price": "$20/mo Pro"},
        {"name": "GitHub Copilot", "url": "github.com/features/copilot",
         "blurb": "AI pair programmer for VSCode/JetBrains, completes code inline",
         "price": "$10/mo Individual, $19/user/mo Business"},
        {"name": "Aider", "url": "aider.chat",
         "blurb": "OSS terminal AI coding assistant, BYO LLM key",
         "price": "Free OSS + LLM usage"},
        {"name": "Windsurf (Codeium)", "url": "codeium.com/windsurf",
         "blurb": "AI-native IDE with 'Cascade' agent flows",
         "price": "Free / $15/mo Pro"},
        {"name": "Claude Code", "url": "claude.ai/code",
         "blurb": "Anthropic CLI for terminal-based AI coding",
         "price": "Bundled with Claude subscription"},
    ],
    "C11": [
        {"name": "TablePlus", "url": "tableplus.com",
         "blurb": "modern GUI for many SQL/NoSQL DBs, fast native macOS/Win",
         "price": "$99 one-time per major version"},
        {"name": "DBeaver", "url": "dbeaver.io",
         "blurb": "OSS universal DB GUI tool with Java backend",
         "price": "Free OSS + $9/mo Lite"},
        {"name": "DataGrip", "url": "jetbrains.com/datagrip",
         "blurb": "JetBrains polyglot DB IDE, deep SQL features",
         "price": "$25/mo / $229/yr"},
        {"name": "Beekeeper Studio", "url": "beekeeperstudio.io",
         "blurb": "modern OSS DB GUI, simpler than DBeaver",
         "price": "Free OSS / $49/yr Ultimate"},
        {"name": "iCloud / Syncthing", "url": "syncthing.net",
         "blurb": "OS-level file sync, no DB-aware, cross-device",
         "price": "Free OSS"},
    ],
    "C14": [
        {"name": "Datadog", "url": "datadoghq.com",
         "blurb": "comprehensive APM + infra + logs + RUM, enterprise heavy",
         "price": "$15/host/mo APM, $0.10/GB logs"},
        {"name": "Honeycomb", "url": "honeycomb.io",
         "blurb": "observability with high-cardinality events, distributed trace focus",
         "price": "Free 20M events + $130/mo Pro paid tier"},
        {"name": "Sentry", "url": "sentry.io",
         "blurb": "error tracking, perf monitoring, session replay",
         "price": "Free + $26/mo Team"},
        {"name": "LangSmith", "url": "langchain.com/langsmith",
         "blurb": "LLM-app observability + dataset eval (LangChain ecosystem)",
         "price": "Free + $39/user/mo Plus"},
        {"name": "Helicone", "url": "helicone.ai",
         "blurb": "open-source LLM observability proxy",
         "price": "Free + $99/mo Pro"},
    ],
}


TEARDOWN_PROMPT = """你是 dev tool 市场分析师，独立评估一个 incumbent 产品是否解决某个 cluster 的痛点。

# Cluster (来自真实 HN 抱怨聚类)
- id: {cluster_id}
- 名称: {cluster_name}
- 描述: {cluster_desc}
- 主导 segment: {segment}
- 主导 category: {category}
- 严重度均值: {severity}

# Incumbent
- 名称: {inc_name}
- URL: {inc_url}
- 产品 blurb: {inc_blurb}
- 价格: {inc_price}

# 任务

基于你对 incumbent 的认知（公开 landing / 产品描述 / 真实用户口碑），评估：

1. **coverage_score** (1-5)：incumbent 解决 cluster 痛点的程度
   - 1 = 完全没解决，需求与 incumbent 无交集
   - 2 = 一点点交集，但核心需求未触及
   - 3 = 部分解决，覆盖一半需求
   - 4 = 大部分解决，缺一些边缘需求
   - 5 = 完全解决，cluster 主要痛点 incumbent 都覆盖

2. **missing_gap**: 1 句话说出 incumbent **最重要的没覆盖**的东西（基于 cluster 描述）。

3. **typical_user_complaint**: 1 句话总结真实用户对此 incumbent 的常见抱怨（从你训练数据 / GitHub Issues / Reddit 印象）。

4. **wedge_opportunity**: 如果有人做一个 challenger 专门攻这个 cluster，最锐利的 wedge 是什么？1 句话。

# 输出严格 JSON：

{{
  "cluster_id": "{cluster_id}",
  "incumbent_name": "{inc_name}",
  "coverage_score": 1-5,
  "missing_gap": "...",
  "typical_user_complaint": "...",
  "wedge_opportunity": "..."
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
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        return 2
    client = genai.Client(api_key=key)

    # Load defensible clusters to get name/desc/segment
    defensible = json.loads(
        (VERT / "defensible_clusters.json").read_text("utf-8"))
    by_id = {c["id"]: c for c in defensible["clusters"]}

    target_ids = ["C3", "C4", "C11", "C14"]
    target_clusters = [by_id[cid] for cid in target_ids if cid in by_id]
    print(f"[day6] tearing down {len(target_clusters)} clusters × "
          f"{sum(len(INCUMBENTS[c['id']]) for c in target_clusters)} incumbents",
          file=sys.stderr)

    all_evals: list[dict] = []
    for c in target_clusters:
        cid = c["id"]
        for inc in INCUMBENTS[cid]:
            prompt = TEARDOWN_PROMPT.format(
                cluster_id=cid,
                cluster_name=c["name"],
                cluster_desc=c.get("description", ""),
                segment=c.get("dominant_segment", "?"),
                category=c.get("dominant_category", "?"),
                severity=c.get("estimated_severity_mean", "?"),
                inc_name=inc["name"],
                inc_url=inc["url"],
                inc_blurb=inc["blurb"],
                inc_price=inc["price"],
            )
            try:
                ev = call_llm(client, prompt)
                ev["_incumbent_meta"] = inc
                all_evals.append(ev)
                print(f"  {cid}/{inc['name']:20s} coverage="
                      f"{ev.get('coverage_score', '?')}/5  "
                      f"gap: {ev.get('missing_gap', '')[:70]}",
                      file=sys.stderr)
            except Exception as e:
                print(f"  [warn] {cid}/{inc['name']} failed: {e}",
                      file=sys.stderr)

    # Aggregate per cluster
    aggregates = []
    for c in target_clusters:
        cid = c["id"]
        evs = [e for e in all_evals if e.get("cluster_id") == cid]
        scores = [e.get("coverage_score", 0) for e in evs
                  if isinstance(e.get("coverage_score"), (int, float))]
        mean_cov = sum(scores) / len(scores) if scores else 0
        non_cov = round(1 - mean_cov / 5, 2)
        aggregates.append({
            "cluster_id": cid,
            "cluster_name": c["name"],
            "incumbents_evaluated": len(evs),
            "mean_coverage": round(mean_cov, 2),
            "non_coverage_ratio": non_cov,
            "missing_gaps": [e.get("missing_gap") for e in evs
                              if e.get("missing_gap")],
            "wedge_opportunities": [e.get("wedge_opportunity") for e in evs
                                      if e.get("wedge_opportunity")],
            "complaints": [e.get("typical_user_complaint") for e in evs
                            if e.get("typical_user_complaint")],
        })

    # Save raw JSON + markdown
    (VERT / "incumbent_teardown.json").write_text(json.dumps({
        "all_evaluations": all_evals,
        "aggregates": aggregates,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    lines: list[str] = [
        "# Day 6 — Incumbent Teardown",
        "",
        f"_Generated: {time.strftime('%Y-%m-%d %H:%M')}_",
        "",
        "## Aggregate (sorted by non-coverage opportunity)",
        "",
        "| Cluster | Mean Coverage | Non-coverage Ratio | Incumbents | "
        "Top Wedge |",
        "|---|---|---|---|---|",
    ]
    for agg in sorted(aggregates, key=lambda x: -x["non_coverage_ratio"]):
        wedge = (agg["wedge_opportunities"][0]
                 if agg["wedge_opportunities"] else "—")[:80]
        lines.append(
            f"| **{agg['cluster_id']}** {agg['cluster_name'][:40]} | "
            f"{agg['mean_coverage']}/5 | "
            f"**{agg['non_coverage_ratio']}** | "
            f"{agg['incumbents_evaluated']} | "
            f"{wedge} |"
        )

    lines += ["", "## 详细评估", ""]
    for c in target_clusters:
        cid = c["id"]
        agg = next(a for a in aggregates if a["cluster_id"] == cid)
        lines.append(f"### {cid}: {c['name']}")
        lines.append("")
        lines.append(f"**mean coverage**: {agg['mean_coverage']}/5  ·  "
                     f"**non-coverage**: {agg['non_coverage_ratio']}")
        lines.append("")
        lines.append("| Incumbent | Coverage | Missing Gap | "
                     "User Complaint | Wedge |")
        lines.append("|---|---|---|---|---|")
        for ev in [e for e in all_evals if e.get("cluster_id") == cid]:
            inc = ev.get("_incumbent_meta", {})
            lines.append(
                f"| **{inc.get('name','?')}** ({inc.get('price','?')}) | "
                f"{ev.get('coverage_score','?')}/5 | "
                f"{(ev.get('missing_gap','') or '')[:120]} | "
                f"{(ev.get('typical_user_complaint','') or '')[:100]} | "
                f"{(ev.get('wedge_opportunity','') or '')[:100]} |"
            )
        lines.append("")

    (VERT / "incumbent_teardown.md").write_text(
        "\n".join(lines), encoding="utf-8")

    print(f"\n[OK] wrote:", file=sys.stderr)
    print(f"  - {VERT / 'incumbent_teardown.json'}", file=sys.stderr)
    print(f"  - {VERT / 'incumbent_teardown.md'}", file=sys.stderr)
    print(f"\nAggregate non-coverage scores (higher = more opportunity):",
          file=sys.stderr)
    for agg in sorted(aggregates, key=lambda x: -x["non_coverage_ratio"]):
        print(f"  {agg['cluster_id']}: {agg['non_coverage_ratio']} "
              f"(mean cov {agg['mean_coverage']}/5)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
