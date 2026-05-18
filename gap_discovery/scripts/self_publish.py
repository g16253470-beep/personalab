"""Self-publish — generate a complete public launch package as GitHub Gist.

Uses anonymous Gist API (no auth, ratelimited to a few/IP/hour) to publish:
- C11 gap brief (markdown)
- Top 5 cold email targets (anonymized, no emails)
- defensible_clusters.json (cleaned)
- AUTONOMY_VISION.md (project north star)

Output: 1 public Gist URL that anyone can read. This URL becomes the share
target for HN / Twitter / Reddit / Discord — no domain needed.

Note: Anonymous gists were deprecated in 2018 by GitHub. Fallback:
- Pastebin (paste.ee) public API — also no auth
- Or 0bin / dpaste / sprunge / ix.io — all no-auth public paste services
- Or just bundle ZIP for human upload

This script tries multiple no-auth paste backends in order.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
VERT = ROOT / "gap_discovery" / "verticals" / "dev_tools"


def post_to_dpaste(content: str, title: str = "personalab") -> str | None:
    """dpaste.com public API, no auth, 1 year expiry."""
    data = urllib.parse.urlencode({
        "content": content[:250_000],
        "syntax": "markdown",
        "expiry_days": "365",
    }).encode()
    req = urllib.request.Request("https://dpaste.com/api/v2/",
                                   data=data,
                                   headers={"User-Agent": "personalab/0.2"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode().strip()
    except Exception as e:
        print(f"[dpaste] {e}", file=sys.stderr)
        return None


def post_to_paste_ee(content: str, title: str) -> str | None:
    """paste.ee public API (no auth for anonymous paste, 1 day expiry)."""
    # paste.ee requires API key for proper use; skipping for now
    return None


def post_to_termbin(content: str) -> str | None:
    """termbin.com via netcat. Works only if `nc` is available. Skip on Windows."""
    return None


def post_via_pastes(content: str, title: str) -> tuple[str, str] | None:
    """Try paste backends in priority order. Returns (backend, url)."""
    url = post_to_dpaste(content, title)
    if url:
        return "dpaste", url
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="generate bundle, don't publish")
    args = ap.parse_args()

    bundle_parts = [
        "# personalab Gap Discovery — public artifact bundle",
        "",
        "_Published autonomously by personalab. MIT licensed._",
        "",
        "## Contents",
        "",
        "1. C11 gap brief (highest confidence wedge)",
        "2. Defensible clusters summary",
        "3. Methodology + autonomy roadmap",
        "",
        "---",
        "",
        "## 1. C11 Gap Brief",
        "",
    ]

    brief = VERT / "gap_brief.md"
    if brief.exists():
        bundle_parts.append(brief.read_text("utf-8"))

    bundle_parts += ["", "---", "",
                     "## 2. Defensible Clusters Summary", "", "```json"]
    defensible = VERT / "defensible_clusters.json"
    if defensible.exists():
        data = json.loads(defensible.read_text("utf-8"))
        # strip member_ids for brevity
        clean = []
        for c in data.get("clusters", []):
            clean.append({
                "id": c.get("id"),
                "name": c.get("name"),
                "members": len(c.get("member_ids", [])),
                "severity": c.get("estimated_severity_mean"),
                "down_votes": c.get("down_vote_count"),
                "segment": c.get("dominant_segment"),
                "category": c.get("dominant_category"),
            })
        bundle_parts.append(json.dumps(clean, ensure_ascii=False, indent=2))
    bundle_parts += ["```", "", "---", "",
                     "## 3. Methodology + Autonomy Vision", ""]
    vision = ROOT / "docs" / "AUTONOMY_VISION.md"
    if vision.exists():
        bundle_parts.append(vision.read_text("utf-8")[:15000])  # truncate

    bundle = "\n".join(bundle_parts)
    bundle_path = VERT / "public_bundle.md"
    bundle_path.write_text(bundle, encoding="utf-8")
    print(f"[bundle] wrote {bundle_path} ({len(bundle)} chars)",
          file=sys.stderr)

    if args.dry_run:
        print("[dry-run] not publishing", file=sys.stderr)
        return 0

    result = post_via_pastes(bundle, "personalab-gap-discovery")
    if result:
        backend, url = result
        print(f"\n[OK] published via {backend}: {url}", file=sys.stderr)
        (VERT / "public_url.txt").write_text(
            f"{backend}: {url}\n", encoding="utf-8")
    else:
        print("\n[FAIL] no paste backend succeeded. "
              "Bundle file is local-only.", file=sys.stderr)
        print(f"      manual upload candidate: {bundle_path}",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
