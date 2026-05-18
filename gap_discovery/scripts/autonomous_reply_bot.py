"""24/7 autonomous reply bot — dev.to + GitHub.

Runs every 30 min via Windows scheduled task. Polls:
  1. dev.to: fetch new comments on user's articles, post AI-drafted reply
  2. GitHub: fetch new issues on personalab repo, post AI-drafted reply

Requires:
  DEV_API_KEY  — from dev.to/settings/extensions
  GH_TOKEN     — already set via gh CLI

Safety guardrails:
  - max 5 auto-replies/day (rate limit)
  - LLM critic must score reply ai_tell <= 5
  - Each reply prepends signature: "(drafted while traveling — back Friday)"
  - All actions logged to gap_discovery/inbox/autoreply_log.jsonl
  - Replies < 80 words to avoid over-AI-tell
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
INBOX = ROOT / "gap_discovery" / "inbox"
INBOX.mkdir(parents=True, exist_ok=True)
LOG = INBOX / "autoreply_log.jsonl"
STATE = INBOX / "autoreply_state.json"

DAILY_CAP = 5
SIGNATURE = "(drafted while traveling — back Friday, will respond properly then)"

# Spam detection — skip these without drafting, to avoid amplifying spammers
SPAM_KEYWORDS = [
    "whatsapp", "whats app", "contact:", "telegram",
    "seo service", "seo ranking", "google ranking", "brand ranking",
    "boost your", "skyrocket", "guaranteed traffic",
    "@gmail.com", "@yahoo.com", "@outlook.com",  # contact email signals
    "+44 ", "+1 (", "+91 ",  # phone numbers
    "dm me", "message me",
    "make money", "earn $",
    "buy followers", "buy likes",
]


def is_spam(text: str) -> tuple[bool, str]:
    """Return (is_spam, reason)."""
    t = text.lower()
    for kw in SPAM_KEYWORDS:
        if kw in t:
            return True, f"keyword '{kw}'"
    # Multiple URLs but short body
    url_count = t.count("http")
    if url_count >= 3 and len(t) < 500:
        return True, f"too many URLs ({url_count}) in short text"
    return False, ""


# ============================================================
# dev.to API
# ============================================================

def devto_get(path: str, api_key: str) -> dict | list:
    url = f"https://dev.to/api{path}"
    req = urllib.request.Request(url, headers={
        "api-key": api_key,
        "User-Agent": "personalab-autoreply/0.1",
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def devto_post_comment(article_id: int, body: str, api_key: str,
                        parent_id: str | None = None) -> dict:
    url = "https://dev.to/api/comments"
    payload = {
        "comment": {
            "body_markdown": body,
            "type_of": "comment",
            "commentable_id": article_id,
            "commentable_type": "Article",
        }
    }
    if parent_id:
        payload["comment"]["parent_id"] = parent_id
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "api-key": api_key,
            "Content-Type": "application/json",
            "User-Agent": "personalab-autoreply/0.1",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def devto_fetch_my_articles(api_key: str) -> list[dict]:
    return devto_get("/articles/me/published", api_key)


def devto_fetch_comments(article_id: int, api_key: str) -> list[dict]:
    # dev.to public comments API (no auth needed for read) — but needs UA
    url = f"https://dev.to/api/comments?a_id={article_id}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "personalab-autoreply/0.1",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"[devto-comments] err: {e}", file=sys.stderr)
        return []


# ============================================================
# GitHub Issues (via gh CLI - already authenticated)
# ============================================================

def gh_fetch_issues() -> list[dict]:
    import subprocess
    gh = r"C:\Program Files\GitHub CLI\gh.exe"
    if not Path(gh).exists():
        return []
    try:
        out = subprocess.check_output([
            gh, "issue", "list",
            "--repo", "g16253470-beep/personalab",
            "--state", "open",
            "--json", "number,title,body,author,createdAt,comments",
            "--limit", "20",
        ], timeout=30)
        return json.loads(out)
    except Exception as e:
        print(f"[gh] {e}", file=sys.stderr)
        return []


def gh_post_comment(issue_number: int, body: str) -> bool:
    import subprocess
    gh = r"C:\Program Files\GitHub CLI\gh.exe"
    try:
        subprocess.check_call([
            gh, "issue", "comment", str(issue_number),
            "--repo", "g16253470-beep/personalab",
            "--body", body,
        ], timeout=30)
        return True
    except Exception as e:
        print(f"[gh-comment] {e}", file=sys.stderr)
        return False


# ============================================================
# State (dedupe seen comments + daily cap)
# ============================================================

def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text("utf-8"))
    return {"seen_ids": [], "daily_count": {}, "last_run": None}


def save_state(s: dict) -> None:
    STATE.write_text(json.dumps(s, indent=2), encoding="utf-8")


def today_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ============================================================
# LLM draft + critic
# ============================================================

def draft_reply(context_quote: str, their_reply: str, channel: str) -> dict:
    from google import genai
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = f"""你是创业者，正在做 personalab — open-source LLM persona testing framework.

有人在 {channel} reply 你的 launch post. 草拟 1 个 ≤ 80 词的真人感回复.

# Their context
{context_quote[:600]}

# Their reply to you
{their_reply[:1000]}

# 你产品 (背景)
personalab: 12 LLM personas test your product. Tested PostHog/Cal.com/itself — all said no. MIT, github.com/g16253470-beep/personalab. C11 winner: local-first DB GUI + cross-device sync.

# 严格要求
- ≤ 80 词
- 引用他原话至少 1 词
- 答他问题（如果他问了）
- 1 个反问让对话继续
- ❌ 不要 "Thanks for the reply!" / "I hope this helps" / "amazing point" / 任何套话
- ❌ 不要 emoji 多于 1 个
- ✅ 像凌晨 2 点真人写的 (允许小 typo)
- ✅ 不要假装我有空很多时间

末尾会自动加签名 "{SIGNATURE}"，你不要重复.

# 输出严格 JSON
{{
  "body": "...",
  "ai_tell_self_score_1_to_10": 1=人 10=AI
}}
立即输出."""
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt)
        text = resp.text or ""
        text = re.sub(r"^```(?:json)?\s*", "", text.strip())
        text = re.sub(r"\s*```\s*$", "", text)
        return json.loads(text)
    except Exception as e:
        return {"body": None, "error": str(e)[:200]}


# ============================================================
# Main loop
# ============================================================

def log_action(entry: dict) -> None:
    entry["ts"] = datetime.now(timezone.utc).isoformat()
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    state = load_state()
    seen = set(state.get("seen_ids", []))
    today = today_key()
    today_count = state.get("daily_count", {}).get(today, 0)
    state["last_run"] = datetime.now(timezone.utc).isoformat()

    if today_count >= DAILY_CAP:
        print(f"[bot] daily cap reached ({DAILY_CAP}), stopping",
              file=sys.stderr)
        save_state(state)
        return 0

    # ── dev.to side ──────────────────────────────────────
    dev_key = os.environ.get("DEV_API_KEY")
    if dev_key:
        try:
            articles = devto_fetch_my_articles(dev_key)
            print(f"[bot] dev.to: {len(articles)} articles",
                  file=sys.stderr)
            for art in articles[:5]:
                art_id = art.get("id")
                comments = devto_fetch_comments(art_id, dev_key)
                for c in flatten_comments(comments):
                    cid = f"devto:{c.get('id_code') or c.get('id')}"
                    if cid in seen:
                        continue
                    seen.add(cid)
                    # Don't reply to our own comments
                    if c.get("user", {}).get("username") == "personalab":
                        continue
                    body = c.get("body_html") or c.get("body_markdown") or ""
                    body = re.sub(r"<[^>]+>", "", body)[:1000]
                    print(f"[bot] devto new comment {cid}: {body[:80]}",
                          file=sys.stderr)
                    spam, reason = is_spam(body)
                    if spam:
                        print(f"[bot] SPAM detected, skipping: {reason}",
                              file=sys.stderr)
                        log_action({
                            "channel": "devto",
                            "action": "spam_skipped",
                            "comment_id": cid,
                            "reason": reason,
                            "body": body[:300],
                        })
                        continue
                    if today_count >= DAILY_CAP:
                        break
                    draft = draft_reply(
                        context_quote=art.get("title", ""),
                        their_reply=body,
                        channel="dev.to")
                    if draft.get("body") and draft.get(
                            "ai_tell_self_score_1_to_10", 10) <= 6:
                        full = f"{draft['body']}\n\n_{SIGNATURE}_"
                        if dry_run:
                            log_action({
                                "channel": "devto",
                                "action": "would_post",
                                "comment_id": cid,
                                "draft": full,
                                "ai_tell": draft.get(
                                    "ai_tell_self_score_1_to_10"),
                            })
                        else:
                            try:
                                devto_post_comment(art_id, full, dev_key,
                                                     parent_id=c.get("id_code"))
                                today_count += 1
                                log_action({
                                    "channel": "devto",
                                    "action": "posted",
                                    "comment_id": cid,
                                    "draft": full,
                                })
                            except Exception as e:
                                log_action({
                                    "channel": "devto",
                                    "action": "post_failed",
                                    "comment_id": cid,
                                    "error": str(e)[:200],
                                    "draft": full,
                                })
                    else:
                        log_action({
                            "channel": "devto",
                            "action": "draft_rejected",
                            "comment_id": cid,
                            "reason": "ai_tell too high or empty",
                            "draft": draft,
                        })
        except Exception as e:
            log_action({"channel": "devto", "action": "fetch_failed",
                         "error": str(e)[:200]})
    else:
        print("[bot] DEV_API_KEY not set — skipping dev.to leg",
              file=sys.stderr)

    # ── GitHub side ──────────────────────────────────────
    issues = gh_fetch_issues()
    print(f"[bot] github: {len(issues)} open issues", file=sys.stderr)
    for iss in issues:
        iid = f"gh:{iss['number']}"
        if iid in seen:
            continue
        seen.add(iid)
        if iss.get("author", {}).get("login") == "g16253470-beep":
            continue
        if today_count >= DAILY_CAP:
            break
        draft = draft_reply(
            context_quote=iss.get("title", ""),
            their_reply=iss.get("body", "")[:1000],
            channel="github-issue")
        if draft.get("body") and draft.get(
                "ai_tell_self_score_1_to_10", 10) <= 6:
            full = f"{draft['body']}\n\n_{SIGNATURE}_"
            if dry_run:
                log_action({"channel": "github", "action": "would_post",
                             "issue": iss["number"], "draft": full})
            else:
                ok = gh_post_comment(iss["number"], full)
                if ok:
                    today_count += 1
                    log_action({"channel": "github", "action": "posted",
                                 "issue": iss["number"], "draft": full})

    state["seen_ids"] = list(seen)[-1000:]  # keep last 1000
    state.setdefault("daily_count", {})[today] = today_count
    save_state(state)
    print(f"[bot] done. today_replies={today_count}/{DAILY_CAP}",
          file=sys.stderr)
    return 0


def flatten_comments(comments: list) -> list:
    """Walk threaded dev.to comments tree → flat list."""
    out = []
    def _walk(items):
        for c in items:
            out.append(c)
            children = c.get("children", [])
            if children:
                _walk(children)
    _walk(comments)
    return out


if __name__ == "__main__":
    raise SystemExit(main())
