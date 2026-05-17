"""Second-pass filter: LLM judges which queue drafts truly relate to C11.

Reads queue/*.md, asks Gemini: "Is this HN quote ACTUALLY complaining about
database GUI / cross-device sync / connection mgmt — or did the keyword
filter match incorrectly?"
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from google import genai


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
QUEUE = ROOT / "gap_discovery" / "verticals" / "dev_tools" / "cold_emails" / "queue"


PROMPT = """C11 cluster 定义: "Local-first database GUI client + cross-device sync of DB connection settings/query history/snippets, encrypted P2P, no cloud server. Targets devs who use TablePlus / DBeaver / DataGrip and switch between home/work machines."

下面这条 HN quote 是否在抱怨:
(a) Database GUI 工具的问题（TablePlus/DBeaver/DataGrip 等）
(b) 跨设备同步 DB 连接配置/query history 的痛点
(c) Local-first / privacy-centric DB 工具需求
(d) 大数据 client-side analytics 需求

或者 keyword 命中但 context 完全无关（e.g. 在聊 web apps / 政治审查 / 跨设备文件同步而不是 DB / 编程哲学 etc）?

# Quote

{quote}

# 输出 JSON

{{
  "truly_c11_related": true|false,
  "confidence_1_to_5": 1-5,
  "reason": "1 句话",
  "if_true_then_subtype": "db_gui_pain|cross_device_sync|local_first|big_data_analytics|null"
}}

立即输出。"""


def call_llm(client, prompt: str):
    resp = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt)
    text = (resp.text or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```\s*$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(m.group(0))


def main() -> int:
    key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=key)

    results = []
    for f in sorted(QUEUE.glob("hn_*.md")):
        text = f.read_text("utf-8")
        # Extract original quote section
        m = re.search(r"## Original quote\s*\n\n> (.+?)\n\n##",
                       text, re.DOTALL)
        if not m:
            continue
        quote = m.group(1).strip()[:1500]
        try:
            verdict = call_llm(client, PROMPT.format(quote=quote))
        except Exception as e:
            verdict = {"error": str(e)[:120]}
        verdict["file"] = f.name
        results.append(verdict)
        related = verdict.get("truly_c11_related")
        sub = verdict.get("if_true_then_subtype", "")
        conf = verdict.get("confidence_1_to_5", "?")
        print(f"  {f.name}: related={related} conf={conf}/5  "
              f"sub={sub}  reason: {verdict.get('reason','')[:80]}",
              file=sys.stderr)

    print(f"\n--- summary ---", file=sys.stderr)
    kept = [r for r in results if r.get("truly_c11_related")]
    print(f"truly C11-related: {len(kept)}/{len(results)}", file=sys.stderr)
    for r in kept:
        print(f"  ✓ {r['file']}  ({r.get('if_true_then_subtype','?')})",
              file=sys.stderr)

    out = QUEUE.parent / "filter_verdicts.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                    encoding="utf-8")
    print(f"\n[OK] wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
