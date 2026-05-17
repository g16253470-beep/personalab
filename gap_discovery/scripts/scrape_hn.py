"""Hacker News scraper using Algolia public API.

Algolia public search API: no auth, no rate limit issues at small scale.
Docs: https://hn.algolia.com/api

Usage:
    python gap_discovery/scripts/scrape_hn.py \
        --queries "I wish there was,why is there no,frustrated with,better alternative" \
        --tags story,comment \
        --out gap_discovery/verticals/dev_tools/data/raw_quotes.jsonl \
        --max-per-query 100
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


HN_SEARCH = "https://hn.algolia.com/api/v1/search"


def hn_search(query: str, tags: str = "story,comment",
              hits_per_page: int = 100,
              numeric_filters: str | None = None) -> list[dict]:
    params = {
        "query": query,
        "tags": f"({tags.replace(',', ',OR_')})" if "," in tags else tags,
        "hitsPerPage": str(hits_per_page),
    }
    if numeric_filters:
        params["numericFilters"] = numeric_filters
    url = HN_SEARCH + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "personalab/0.2"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  [warn] {query!r}: {e}", file=sys.stderr)
        return []
    hits = []
    for h in data.get("hits", []):
        # Story has title, comment has comment_text
        text = (h.get("title") or "") + "\n" + (
            h.get("story_text") or h.get("comment_text") or "")
        text = text.strip()
        if len(text) < 50 or len(text) > 4000:
            continue
        hits.append({
            "id": f"hn_{h.get('objectID')}",
            "source": f"hn/{','.join(h.get('_tags', []))}",
            "url": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
            "timestamp_utc": h.get("created_at"),
            "score": h.get("points") or 0,
            "num_comments": h.get("num_comments") or 0,
            "author": h.get("author"),
            "query_matched": query,
            "raw_text": text,
        })
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--queries", required=True,
                    help="comma-separated queries")
    ap.add_argument("--tags", default="comment",
                    help="HN tags: story,comment,ask_hn,show_hn (comma)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-per-query", type=int, default=100)
    ap.add_argument("--min-points", type=int, default=0,
                    help="minimum HN points (only applies to stories — "
                         "comments don't carry a points field in Algolia)")
    ap.add_argument("--sleep", type=float, default=1.0)
    args = ap.parse_args()

    queries = [q.strip() for q in args.queries.split(",") if q.strip()]
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    seen: set[str] = set()
    numeric = f"points>={args.min_points}" if args.min_points > 0 else None

    with out_path.open("a", encoding="utf-8") as f:
        for q in queries:
            print(f"[hn] q={q!r} ...", file=sys.stderr)
            hits = hn_search(q, tags=args.tags,
                              hits_per_page=args.max_per_query,
                              numeric_filters=numeric)
            new_count = 0
            for h in hits:
                if h["id"] in seen:
                    continue
                seen.add(h["id"])
                f.write(json.dumps(h, ensure_ascii=False) + "\n")
                new_count += 1
            total += new_count
            print(f"  +{new_count} (cumulative {total})", file=sys.stderr)
            time.sleep(args.sleep)

    print(f"\n[OK] wrote {total} HN quotes to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
