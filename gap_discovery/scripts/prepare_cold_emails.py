"""Day 7-8 — Auto-prepare cold email queue for human review/send.

Pipeline:
  1. Find C11-relevant high-severity quotes (data sync / DB GUI complaints)
  2. For each: fetch HN author profile → look for public email/github/twitter
  3. LLM drafts personalized email referencing their specific quote
  4. LLM critic scores each email (spam-likeness, AI-tell, reply-likelihood)
  5. Outputs:
     - cold_emails/queue/<id>.md   (one per email, ready for human review)
     - cold_emails/to_send.csv     (master list)

Human reviews 5 mins, edits 1-2 sentences for human voice, sends manually via
gmail OR explicitly authorizes auto-send via Resend.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from google import genai


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
VERT = ROOT / "gap_discovery" / "verticals" / "dev_tools"
QUEUE = VERT / "cold_emails" / "queue"


PRODUCT_PITCH = """
Local-first database GUI client that natively syncs your DB connection
settings + query history + saved snippets across all your devices via
encrypted P2P (no cloud server). Works with Postgres / MySQL / SQLite.
Aimed at devs who switch between home/work laptops and don't want
TablePlus settings to drift or sit on someone else's server.
Target pricing: $14-19/mo personal, $39/mo team-3.
""".strip()


DRAFT_PROMPT = """你是 cold email 助手。任务：给一位真实 dev 写一封 cold email，引用他/她的具体抱怨，介绍我正在做的工具，问他/她两个简短问题。

## 收件人具体 quote (来自 HN)
- HN id: {hn_id}
- date: {date}
- quote: "{quote}"

## 我正在做的产品 (一句话)
{product}

## 邮件要求

1. **Subject**: 短（≤ 8 词），引用他/她 quote 里的具体词（让他打开率高）
2. **Body**: ≤ 100 词，3 段：
   - 段 1: "saw your <date> HN comment about <他/她原话片段>" — 让他知道你真读过他抱怨
   - 段 2: "I'm prototyping <一句话产品> — would this have helped?"
   - 段 3: "Two quick questions if you have 30 seconds: (1) did you ever find a fix? (2) would you pay $15/mo for it? Just calibrating — I'll share the full data in 2 weeks."
3. **签名**: 简短 "Best, <name>"，不要 "I hope this email finds you well" 类套话

## 严格要求
- ❌ 不要 "I hope this finds you well"
- ❌ 不要长段
- ❌ 不要 marketing 腔（"revolutionary"/"game-changing"/"empower"/"unlock"）
- ❌ 不要 emoji
- ✅ 要写得**像 founder 自己一夜写的**，可以有小 typo（不用刻意加，但不要完美）
- ✅ 引用他原话至少 1 句具体词
- ✅ 总长度 80-130 词

## 输出严格 JSON

{{
  "subject": "...",
  "body": "..."
}}

立即输出。"""


CRITIC_PROMPT = """你是 cold email 审查员。下面这封 cold email 会发给一个真实 dev。
评估它**像不像 AI 写的** 以及**收件人会不会回**。

# Email

Subject: {subject}

Body:
{body}

# 你的评估

输出严格 JSON：

{{
  "ai_tell_score_1_to_10": 1=完全像人手写 10=AI 味十足,
  "spam_risk_1_to_10": 1=安全 10=必进 spam,
  "estimated_reply_rate_pct": 估算回复率 0-25,
  "specific_problems": ["问题1", "问题2", ...],
  "rewrite_suggestions": "如果你重写其中 1 句让它更像人，你会改哪句？给出改写后版本。"
}}

立即输出。"""


def hn_user_profile(user_id: str) -> dict | None:
    """Fetch HN user profile via Firebase API."""
    url = f"https://hacker-news.firebaseio.com/v0/user/{user_id}.json"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read())
    except Exception:
        return None


def extract_emails_from_text(text: str) -> list[str]:
    return re.findall(
        r"\b[\w.-]+@[\w.-]+\.\w{2,}\b", text or "", re.UNICODE)


def hn_get_item_author(item_id: str) -> str | None:
    """Get the HN author handle for a given item id."""
    iid = item_id.replace("hn_", "")
    url = f"https://hacker-news.firebaseio.com/v0/item/{iid}.json"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read()).get("by")
    except Exception:
        return None


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


def pick_c11_candidates(tagged: list[dict], min_severity: int = 3,
                          want_n: int = 8) -> list[dict]:
    """Find quotes most relevant to C11 (data sync / DB GUI)."""
    c11_keywords = ["sync", "database", "db gui", "tableplus", "dbeaver",
                     "datagrip", "schema", "data sync", "connection",
                     "across device", "cross-device", "across machine",
                     "config sync"]
    candidates = []
    for t in tagged:
        if not t.get("is_dev_tool_related"):
            continue
        sev = t.get("severity_1_5") or 0
        if sev < min_severity:
            continue
        un = (t.get("unmet_need_one_line") or "").lower()
        cat = t.get("category", "").lower()
        score = sum(1 for k in c11_keywords if k in un)
        if cat in ("data", "db", "sync"):
            score += 3
        if score == 0:
            continue
        t["_c11_score"] = score
        candidates.append(t)
    candidates.sort(key=lambda x: -x.get("_c11_score", 0))
    return candidates[:want_n]


def main() -> int:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        return 2
    client = genai.Client(api_key=key)
    QUEUE.mkdir(parents=True, exist_ok=True)

    tagged = [json.loads(l) for l in
              (VERT / "data" / "tagged_quotes.jsonl").read_text(
                  "utf-8").splitlines() if l.strip()]
    by_id = {t["id"]: t for t in tagged}

    raw = {json.loads(l)["id"]: json.loads(l) for l in
           (VERT / "data" / "raw_quotes.jsonl").read_text(
               "utf-8").splitlines() if l.strip()}

    candidates = pick_c11_candidates(tagged, min_severity=3, want_n=12)
    print(f"[stage 1] {len(candidates)} C11-relevant quote candidates",
          file=sys.stderr)

    csv_rows = []
    drafted = 0

    for c in candidates:
        qid = c["id"]
        raw_q = raw.get(qid, {})
        author = hn_get_item_author(qid)
        if not author:
            print(f"  [skip] {qid}: no author", file=sys.stderr)
            continue

        profile = hn_user_profile(author) or {}
        about = profile.get("about", "") or ""
        emails = extract_emails_from_text(about)
        karma = profile.get("karma", 0)

        # Draft email
        try:
            draft = call_llm(client, DRAFT_PROMPT.format(
                hn_id=qid,
                date=raw_q.get("timestamp_utc", "?")[:10],
                quote=raw_q.get("raw_text", "")[:500],
                product=PRODUCT_PITCH,
            ))
        except Exception as e:
            print(f"  [warn] {qid}: draft failed: {e}", file=sys.stderr)
            continue

        # Critic
        critic = {}
        try:
            critic = call_llm(client, CRITIC_PROMPT.format(
                subject=draft.get("subject", ""),
                body=draft.get("body", ""),
            ))
        except Exception as e:
            critic = {"error": str(e)[:100]}

        ai_tell = critic.get("ai_tell_score_1_to_10", 999)
        spam_risk = critic.get("spam_risk_1_to_10", 999)

        # Save individual queue file
        md = QUEUE / f"{qid}.md"
        md.write_text(
            f"# Cold email queue: {qid}\n\n"
            f"**HN author**: `{author}` (karma {karma})  \n"
            f"**HN url**: https://news.ycombinator.com/item?id={qid.replace('hn_','')}  \n"
            f"**Public email(s) from profile**: "
            f"{', '.join(emails) if emails else '(none — search GitHub/Twitter manually)'}  \n"
            f"**About**: {about[:200]}\n\n"
            f"---\n\n"
            f"## Original quote\n\n"
            f"> {raw_q.get('raw_text','')[:600]}\n\n"
            f"## Draft email\n\n"
            f"**Subject**: {draft.get('subject','')}\n\n"
            f"```\n{draft.get('body','')}\n```\n\n"
            f"## AI critic\n\n"
            f"- ai_tell_score: **{ai_tell}/10** (1=human, 10=AI)\n"
            f"- spam_risk: **{spam_risk}/10**\n"
            f"- estimated_reply_rate: **"
            f"{critic.get('estimated_reply_rate_pct','?')}%**\n"
            f"- problems: {critic.get('specific_problems',[])}\n"
            f"- rewrite suggestion:\n  > "
            f"{critic.get('rewrite_suggestions','')}\n\n"
            f"## Next action\n\n"
            f"- [ ] Confirm public email above OR find via "
            f"github.com/{author} / twitter / blog\n"
            f"- [ ] Edit 1-2 sentences for human voice "
            f"(remove AI tell)\n"
            f"- [ ] Send via your gmail OR move to send_queue.csv "
            f"for auto-send\n",
            encoding="utf-8",
        )

        csv_rows.append({
            "queue_file": str(md.relative_to(ROOT)),
            "hn_id": qid,
            "hn_author": author,
            "hn_karma": karma,
            "candidate_email": emails[0] if emails else "",
            "subject": draft.get("subject", ""),
            "ai_tell_score": ai_tell,
            "spam_risk": spam_risk,
            "estimated_reply_rate_pct":
                critic.get("estimated_reply_rate_pct", ""),
            "ready_to_send": (ai_tell <= 5 and spam_risk <= 5
                              and bool(emails)),
        })
        drafted += 1
        print(f"  [{qid}] author={author} karma={karma} "
              f"email={'YES' if emails else 'NO'} "
              f"ai_tell={ai_tell}/10 spam={spam_risk}/10",
              file=sys.stderr)

        if drafted >= 8:
            break

    # Write master CSV
    out_csv = VERT / "cold_emails" / "to_send.csv"
    if csv_rows:
        with out_csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            w.writeheader()
            w.writerows(csv_rows)

    print(f"\n[OK] {drafted} email drafts in {QUEUE}", file=sys.stderr)
    print(f"     master csv: {out_csv}", file=sys.stderr)
    print(f"     ready_to_send count: "
          f"{sum(1 for r in csv_rows if r['ready_to_send'])}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
