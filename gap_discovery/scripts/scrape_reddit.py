"""Reddit scraper for dev complaints — uses public JSON API, no auth required.

Usage:
    python gap_discovery/scripts/scrape_reddit.py \
        --subreddits devops,webdev,programming,sideproject \
        --queries "I wish,frustrated,annoying,broken,better than" \
        --out gap_discovery/verticals/dev_tools/data/raw_quotes.jsonl \
        --max-per-query 50

Output: JSONL, each line = one quote (post or top comment).
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


UA = ("personalab gap-discovery research 2026-05 "
      "(github.com/personalab/personalab)")
REDDIT_SEARCH = "https://www.reddit.com/r/{sub}/search.json"


def reddit_search(sub: str, query: str, limit: int = 25,
                    sort: str = "relevance", t: str = "year") -> list[dict]:
    """Search a subreddit for query. Returns list of post dicts."""
    params = {
        "q": query,
        "restrict_sr": "on",
        "limit": str(limit),
        "sort": sort,
        "t": t,
    }
    url = REDDIT_SEARCH.format(sub=sub) + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  [warn] {sub}/{query!r}: {e}", file=sys.stderr)
        return []
    posts = []
    for child in data.get("data", {}).get("children", []):
        p = child.get("data", {})
        if p.get("over_18") or p.get("stickied"):
            continue
        text = (p.get("title", "") + "\n" + p.get("selftext", "")).strip()
        if len(text) < 50 or len(text) > 4000:
            continue
        posts.append({
            "id": f"reddit_{sub}_{p.get('id')}",
            "source": f"reddit/r/{sub}",
            "url": "https://www.reddit.com" + p.get("permalink", ""),
            "timestamp_utc": datetime.fromtimestamp(
                p.get("created_utc", 0), timezone.utc).isoformat(),
            "score": p.get("score", 0),
            "num_comments": p.get("num_comments", 0),
            "query_matched": query,
            "raw_text": text,
        })
    return posts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subreddits", required=True,
                    help="comma-separated subreddit names (no r/)")
    ap.add_argument("--queries", required=True,
                    help="comma-separated search queries (quotes optional)")
    ap.add_argument("--out", required=True, help="output JSONL path")
    ap.add_argument("--max-per-query", type=int, default=25,
                    help="results per (subreddit, query) pair")
    ap.add_argument("--sleep", type=float, default=2.0,
                    help="seconds between requests (Reddit allows ~1 req/sec)")
    ap.add_argument("--time-window", default="year",
                    choices=["hour", "day", "week", "month", "year", "all"])
    args = ap.parse_args()

    subreddits = [s.strip() for s in args.subreddits.split(",") if s.strip()]
    queries = [q.strip() for q in args.queries.split(",") if q.strip()]
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    seen_ids: set[str] = set()
    with out_path.open("a", encoding="utf-8") as f:
        for sub in subreddits:
            for q in queries:
                print(f"[{sub}] q={q!r} ...", file=sys.stderr)
                posts = reddit_search(sub, q, limit=args.max_per_query,
                                        t=args.time_window)
                new_count = 0
                for p in posts:
                    if p["id"] in seen_ids:
                        continue
                    seen_ids.add(p["id"])
                    f.write(json.dumps(p, ensure_ascii=False) + "\n")
                    new_count += 1
                total += new_count
                print(f"  +{new_count} (cumulative {total})", file=sys.stderr)
                time.sleep(args.sleep)

    print(f"\n[OK] wrote {total} quotes to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
