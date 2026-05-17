"""LLM-annotate raw quotes — turn 392 noisy HN comments into structured tags.

LLM's job: compress + filter, NOT judge. Output schema:
{
  "id": "...",                  // from input
  "is_dev_tool_related": bool,  // filter out off-topic
  "unmet_need_one_line": "...", // 1-sentence summary
  "severity_1_5": int,          // 1=mild, 5=blocker
  "segment": "junior_dev|staff_eng|oss_maint|indie_hacker|sre|data|other",
  "category": "ide|build|deploy|monitor|debug|test|docs|collab|...",
  "wtp_clue": "string or null",
}

Usage:
    GEMINI_API_KEY=... python gap_discovery/scripts/annotate.py \
        --in gap_discovery/verticals/dev_tools/data/raw_quotes.jsonl \
        --out gap_discovery/verticals/dev_tools/data/tagged_quotes.jsonl \
        --batch 5
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

from google import genai


SYSTEM = """你是数据标注助手。下面给你一条 Hacker News 评论（HN comment）。

你的任务（只压缩信息，不评判事实）：

1. 判断这条评论是否在抱怨/讨论 dev tool 相关问题（IDE / build / deploy / monitor / debug / test / docs / collab / database / infra / API / CLI / framework / library / observability / CI/CD / version control 等）。
   - 如果跟 dev tool 完全无关（如纯法律、历史、社会话题），is_dev_tool_related=false。
2. 用一句话压缩这条评论里**最具体的 unmet need**（如果有）。如果只是泛泛抱怨，写 null。
3. 估计 severity 1-5（1=轻微吐槽，3=每天忍受，5=阻碍工作）。
4. 推断 segment（junior_dev / staff_eng / oss_maint / indie_hacker / sre / data / other / unknown）。
5. 分类 category（ide / build / deploy / monitor / debug / test / docs / collab / db / api / cli / framework / other / unknown）。
6. wtp_clue：评论里如果提到"愿付 $X" 或 "we pay $Y" 类的金额，提取出原句；没有则 null。

**输出严格 JSON，无 markdown 包裹，无解释**："""


SCHEMA_TEMPLATE = """
{{
  "id": "{id}",
  "is_dev_tool_related": true|false,
  "unmet_need_one_line": "string or null",
  "severity_1_5": 1-5,
  "segment": "...",
  "category": "...",
  "wtp_clue": "string or null"
}}
"""


def annotate_one(client, quote: dict, model: str = "gemini-2.5-flash") -> dict:
    schema = SCHEMA_TEMPLATE.format(id=quote["id"])
    prompt = (
        f"{SYSTEM}\n\n{schema}\n\n"
        f"=== HN comment (source: {quote['source']}) ===\n"
        f"{quote['raw_text'][:2000]}"
    )
    try:
        resp = client.models.generate_content(model=model, contents=prompt)
        text = (resp.text or "").strip()
        # strip codefences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text
            if text.endswith("```"):
                text = text.rsplit("```", 1)[0]
            text = text.strip()
        return json.loads(text)
    except Exception as e:
        return {"id": quote["id"], "error": str(e)[:200]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="gemini-2.5-flash")
    ap.add_argument("--limit", type=int, default=0, help="0=no limit")
    ap.add_argument("--throttle", type=float, default=0.0,
                    help="seconds between calls (Gemini free tier ~15 RPM)")
    args = ap.parse_args()

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        return 2
    client = genai.Client(api_key=key)

    quotes = [json.loads(l) for l in
              Path(args.in_path).read_text("utf-8").splitlines()
              if l.strip()]
    if args.limit:
        quotes = quotes[: args.limit]
    print(f"annotating {len(quotes)} quotes with {args.model}", file=sys.stderr)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # resume support
    already = set()
    if out_path.exists():
        for l in out_path.read_text("utf-8").splitlines():
            try:
                already.add(json.loads(l)["id"])
            except Exception:
                pass
    print(f"already annotated: {len(already)}, skipping", file=sys.stderr)

    t0 = time.time()
    written = 0
    errors = 0
    with out_path.open("a", encoding="utf-8") as f:
        for i, q in enumerate(quotes, 1):
            if q["id"] in already:
                continue
            tagged = annotate_one(client, q, args.model)
            if "error" in tagged:
                errors += 1
                if errors > 20:
                    print(f"too many errors ({errors}), stopping",
                          file=sys.stderr)
                    break
            f.write(json.dumps(tagged, ensure_ascii=False) + "\n")
            written += 1
            if args.throttle:
                time.sleep(args.throttle)
            if i % 25 == 0:
                elapsed = time.time() - t0
                rate = written / max(elapsed, 1)
                print(f"  {i}/{len(quotes)} written={written} "
                      f"errors={errors} rate={rate:.1f}/s", file=sys.stderr)

    print(f"\n[OK] annotated {written} quotes ({errors} errors) "
          f"to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
