"""24/7 organic signal monitor — autonomous market listener.

Scans every N hours for mentions of personalab / Gap Discovery / C11
keywords across:
- Hacker News (Algolia, no auth)
- GitHub: stars on personalab repo (when public) + trending dev tools
- Reddit: search via google site:reddit.com (no auth needed)
- generic Google "site:" search

Output: monitor_ledger.jsonl append-only log + monitor_dashboard.md auto-updated.

Designed to run via cron `*/120 * * * *` (every 2h) or once-on-demand.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
LEDGER_DIR = ROOT / "gap_discovery" / "monitor"
LEDGER_DIR.mkdir(parents=True, exist_ok=True)
LEDGER = LEDGER_DIR / "monitor_ledger.jsonl"
DASHBOARD = LEDGER_DIR / "monitor_dashboard.md"


KEYWORDS = {
    # personalab brand mentions
    "brand": [
        "personalab",
    ],
    # C11 wedge area
    "c11_pain": [
        "tableplus sync",
        "dbeaver settings sync",
        "datagrip sync config",
        "database GUI cross device",
        "local-first database client",
        "encrypted DB config sync",
    ],
    # Adjacent verticals we plan to expand to (track competition)
    "competitors": [
        "synthetic users tool",
        "AI personas product",
        "GapRadar",
        "TinyTroupe",
        "Synthetic Users syntheticusers",
    ],
}


def hn_search(query: str, days_back: int = 7) -> list[dict]:
    """HN Algolia API, comments and stories from last N days."""
    since_ts = int(time.time()) - days_back * 86400
    url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode({
        "query": query,
        "tags": "(story,OR_comment)",
        "numericFilters": f"created_at_i>{since_ts}",
        "hitsPerPage": 30,
    })
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.loads(r.read())
    except Exception as e:
        return [{"source": "hn", "error": str(e)[:100], "query": query}]
    hits = []
    for h in data.get("hits", []):
        hits.append({
            "source": "hn",
            "query": query,
            "id": str(h.get("objectID")),
            "url": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
            "text": (h.get("title") or "") + "\n" +
                    (h.get("comment_text") or h.get("story_text") or ""),
            "author": h.get("author"),
            "points": h.get("points") or 0,
            "created_at": h.get("created_at"),
        })
    return hits


def github_search_repos(query: str, days_back: int = 30) -> list[dict]:
    """GitHub public search (no auth needed for low rate)."""
    since = (datetime.now(timezone.utc) -
              __import__("datetime").timedelta(days=days_back)
              ).strftime("%Y-%m-%d")
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({
        "q": f"{query} created:>={since}",
        "sort": "stars",
        "order": "desc",
        "per_page": 10,
    })
    req = urllib.request.Request(url, headers={
        "User-Agent": "personalab-monitor",
        "Accept": "application/vnd.github+json",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
    except Exception as e:
        return [{"source": "github", "error": str(e)[:100], "query": query}]
    return [{
        "source": "github",
        "query": query,
        "id": str(item.get("id")),
        "url": item.get("html_url"),
        "text": item.get("full_name", "") + ": " +
                (item.get("description") or "")[:300],
        "stars": item.get("stargazers_count"),
        "created_at": item.get("created_at"),
    } for item in data.get("items", [])]


def load_seen() -> set[str]:
    """Load already-seen ids from ledger to dedupe."""
    if not LEDGER.exists():
        return set()
    seen = set()
    for line in LEDGER.read_text("utf-8").splitlines():
        if line.strip():
            try:
                seen.add(json.loads(line)["id"])
            except Exception:
                pass
    return seen


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-back", type=int, default=7)
    ap.add_argument("--once", action="store_true",
                    help="run one pass and exit (for cron)")
    args = ap.parse_args()

    seen = load_seen()
    new_hits: list[dict] = []
    run_started = datetime.now(timezone.utc).isoformat()

    for category, queries in KEYWORDS.items():
        for q in queries:
            for fn in (hn_search, github_search_repos):
                results = fn(q, args.days_back)
                for h in results:
                    if "error" in h:
                        print(f"[warn] {h.get('source')}/{q}: {h['error']}",
                              file=sys.stderr)
                        continue
                    key = f"{h['source']}:{h['id']}"
                    if key in seen:
                        continue
                    seen.add(key)
                    h["category"] = category
                    h["detected_at"] = run_started
                    new_hits.append(h)
                    print(f"  [new] [{category}] [{h['source']}] "
                          f"q={q!r} → {h.get('url')}",
                          file=sys.stderr)

    if new_hits:
        with LEDGER.open("a", encoding="utf-8") as f:
            for h in new_hits:
                # store under composite key for dedupe
                h["id"] = f"{h['source']}:{h['id']}"
                f.write(json.dumps(h, ensure_ascii=False) + "\n")
        print(f"\n[OK] {len(new_hits)} new mentions logged to {LEDGER}",
              file=sys.stderr)
    else:
        print("\n[OK] no new mentions this pass", file=sys.stderr)

    # Update dashboard
    update_dashboard()

    return 0


def update_dashboard() -> None:
    if not LEDGER.exists():
        return
    hits = [json.loads(l) for l in LEDGER.read_text("utf-8").splitlines()
            if l.strip()]
    hits.sort(key=lambda h: h.get("created_at") or "", reverse=True)

    by_cat: dict[str, list[dict]] = {}
    for h in hits:
        by_cat.setdefault(h.get("category", "?"), []).append(h)

    lines = [
        "# personalab — autonomous monitor dashboard",
        "",
        f"_Last updated: {datetime.now(timezone.utc).isoformat()}_",
        f"_Total mentions tracked: **{len(hits)}**_",
        "",
        "## 🚨 Brand mentions (highest priority)",
        "",
    ]
    for h in by_cat.get("brand", [])[:20]:
        lines.append(
            f"- [{h.get('source')}] {h.get('created_at','?')[:10]}  "
            f"`{(h.get('text','') or '')[:80].replace(chr(10),' ')}`...  "
            f"[link]({h.get('url')})"
        )

    lines += ["", "## 🎯 C11 pain mentions", ""]
    for h in by_cat.get("c11_pain", [])[:30]:
        lines.append(
            f"- [{h.get('source')}] {h.get('created_at','?')[:10]}  "
            f"`{(h.get('text','') or '')[:80].replace(chr(10),' ')}`...  "
            f"[link]({h.get('url')})"
        )

    lines += ["", "## 🥊 Competitor mentions", ""]
    for h in by_cat.get("competitors", [])[:30]:
        lines.append(
            f"- [{h.get('source')}] {h.get('created_at','?')[:10]}  "
            f"`{(h.get('text','') or '')[:80].replace(chr(10),' ')}`...  "
            f"[link]({h.get('url')})"
        )

    DASHBOARD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
