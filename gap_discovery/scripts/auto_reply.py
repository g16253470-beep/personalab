"""Auto-reply drafter — for any inbound (HN reply / GitHub issue / email).

Input: a JSON file describing the inbound, e.g.
  {
    "channel": "hn_reply",
    "url": "https://news.ycombinator.com/item?id=...",
    "from_author": "...",
    "context_quote": "their original HN comment text",
    "their_reply": "what they wrote back",
    "our_context": "personalab + Gap Discovery C11 wedge"
  }

Output: 3 alternative draft replies (formal / casual / curious) + chosen winner.
Saved to inbox/<timestamp>_<author>.md for 1-sec human approval.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

from google import genai


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
INBOX = ROOT / "gap_discovery" / "inbox"
INBOX.mkdir(parents=True, exist_ok=True)


REPLY_PROMPT = """你是创业者，正在做 personalab + Gap Discovery + C11 (local-first DB GUI with cross-device sync) 项目。

有人 reply 你了。任务：起草 3 种不同语气的回复，让创业者 1 秒选一个。

# 收件方原始上下文 / quote
{context_quote}

# 他/她的 reply
{their_reply}

# 你想 advance 的目标
{our_goal}

# 你的项目背景 (供你 reference，不要直接堆里)
- personalab: open-source LLM persona testing framework, MIT
- Gap Discovery: 392 HN quotes → 5 真实 C11 candidate
- C11 wedge: local-first DB GUI + encrypted P2P sync, target $15/mo

# 输出严格 JSON，3 个 variant

{{
  "variant_curious": {{
    "tone": "curious / asking back",
    "body": "≤ 80 词，问他一个具体后续问题让他继续 talk"
  }},
  "variant_concrete": {{
    "tone": "concrete / offer next step",
    "body": "≤ 80 词，给他一个具体下一步 (link / demo / signup)"
  }},
  "variant_short": {{
    "tone": "short / casual / human",
    "body": "≤ 40 词，最 short 最 founder-voice 的版本"
  }},
  "recommended": "curious|concrete|short",
  "why_recommended": "1 句话",
  "ai_tell_self_score_1_to_10": 1-10
}}

# 风格要求
- ❌ 不要 "Thanks for the response!" 套话
- ❌ 不要 emoji
- ❌ 不要 "I hope this helps"
- ✅ 写得像创业者凌晨 2 点真情回复
- ✅ 引用他原话至少 1 个词
- ✅ 如果他问你问题，先答，再问

立即输出 JSON。"""


def strip_fence(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```\s*$", "", text)
    return text.strip()


def call_llm(client, prompt: str) -> dict:
    resp = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt)
    text = strip_fence(resp.text or "")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(m.group(0))


def draft_reply(inbound_path: Path) -> Path:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(2)
    client = genai.Client(api_key=api_key)

    inb = json.loads(inbound_path.read_text("utf-8"))
    drafts = call_llm(client, REPLY_PROMPT.format(
        context_quote=inb.get("context_quote", ""),
        their_reply=inb.get("their_reply", ""),
        our_goal=inb.get("our_goal",
                          "calibrate willingness to pay $15/mo, "
                          "advance toward signup or paid pilot"),
    ))

    ts = time.strftime("%Y%m%d_%H%M%S")
    out = INBOX / f"{ts}_{inb.get('from_author', 'unknown')}_reply.md"
    rec = drafts.get("recommended", "curious")
    out.write_text(
        f"# Auto-drafted reply for {inb.get('from_author', '?')}\n\n"
        f"**Channel**: {inb.get('channel', '?')}  \n"
        f"**Their URL**: {inb.get('url', '?')}  \n"
        f"**Generated**: {ts}  \n"
        f"**Recommended**: `{rec}` — {drafts.get('why_recommended', '')}  \n"
        f"**AI tell self-score**: {drafts.get('ai_tell_self_score_1_to_10', '?')}/10\n\n"
        f"---\n\n"
        f"## Context\n\n"
        f"**Their original quote:**\n> {inb.get('context_quote', '')}\n\n"
        f"**Their reply to you:**\n> {inb.get('their_reply', '')}\n\n"
        f"---\n\n"
        f"## 🎯 Recommended: {rec}\n\n"
        f"```\n{drafts.get(f'variant_{rec}', {}).get('body', '')}\n```\n\n"
        f"## Variant A — curious\n\n"
        f"```\n{drafts.get('variant_curious', {}).get('body', '')}\n```\n\n"
        f"## Variant B — concrete\n\n"
        f"```\n{drafts.get('variant_concrete', {}).get('body', '')}\n```\n\n"
        f"## Variant C — short\n\n"
        f"```\n{drafts.get('variant_short', {}).get('body', '')}\n```\n\n"
        f"---\n\n"
        f"## Action\n\n"
        f"- [ ] Pick variant + edit 1-2 sentences for personal voice\n"
        f"- [ ] Send back via {inb.get('channel', '?')}\n",
        encoding="utf-8",
    )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inbound", required=True,
                    help="path to JSON describing the inbound")
    args = ap.parse_args()
    out = draft_reply(Path(args.inbound))
    print(f"[OK] reply draft written: {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
