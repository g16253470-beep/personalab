#!/usr/bin/env bash
# launch.sh — one-button publish trigger.
# 95% autonomous; the only manual step is: provide GitHub PAT once.
#
# What this does:
#   1. Optionally create GitHub repo + push (if GH_TOKEN set)
#   2. Create a public Gist with the bundle (if GH_TOKEN set)
#   3. Generate Twitter thread (LAUNCH.md already has it)
#   4. Print Show HN URL skeleton you click once
#   5. Start monitor.py in a screen/tmux session
#
# Setup ONCE (5 sec):
#   gh auth login        OR
#   export GH_TOKEN=ghp_...
#
# Then run:
#   ./launch.sh
set -e

cd "$(dirname "$0")"

echo "=== personalab launch — autonomous publish trigger ==="
echo

# Refresh public bundle from latest data
echo "[1/5] Regenerating public bundle..."
python gap_discovery/scripts/self_publish.py --dry-run > /dev/null
echo "      wrote gap_discovery/verticals/dev_tools/public_bundle.md"

# Check git status — commit any pending
echo
echo "[2/5] Committing any pending changes..."
git add -A
if ! git diff --cached --quiet; then
  git commit -m "auto: pre-launch snapshot $(date -u +%Y-%m-%dT%H:%MZ)"
else
  echo "      working tree clean"
fi

# GitHub publish (if token available)
echo
echo "[3/5] GitHub publish..."
if [ -z "${GH_TOKEN:-}" ] && ! command -v gh >/dev/null 2>&1; then
  echo "      ⚠️  GH_TOKEN not set + gh CLI not installed; skip GitHub push."
  echo "      To enable: export GH_TOKEN=ghp_... then re-run."
else
  # Try gh CLI first
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    # Repo already exists?
    if gh repo view personalab/personalab >/dev/null 2>&1; then
      git push origin main 2>&1 || git push -u origin master
    else
      echo "      Creating GitHub repo (public)..."
      gh repo create personalab --public --source=. --push --description \
        "LLM-driven persona testing + Gap Discovery framework. MIT."
    fi
    # Create public Gist with C11 brief
    gh gist create \
      gap_discovery/verticals/dev_tools/public_bundle.md \
      --public \
      --desc "personalab Gap Discovery — dev tools vertical, C11 finding" \
      2>&1 | tee gap_discovery/verticals/dev_tools/gist_url.txt
  else
    echo "      gh CLI not authenticated; manual fallback:"
    echo "        1. Create repo at github.com/new (public, name 'personalab')"
    echo "        2. cd $(pwd) && git remote add origin <url> && git push -u origin master"
    echo "        3. Upload gap_discovery/verticals/dev_tools/public_bundle.md as Gist"
  fi
fi

# Generate Show HN URL skeleton
echo
echo "[4/5] Show HN submit URL (paste this in browser):"
SHOWHN_TITLE="Show HN: personalab — I built a Gap Discovery framework and used it to find this"
SHOWHN_URL_PARAM=$(python -c "import urllib.parse; print(urllib.parse.quote('${SHOWHN_TITLE}'))")
echo "      https://news.ycombinator.com/submit"
echo "      Title: ${SHOWHN_TITLE}"
echo "      Body: see LAUNCH.md (Option B)"

# Start monitor
echo
echo "[5/5] Starting autonomous monitor (every 2h)..."
if command -v crontab >/dev/null 2>&1; then
  CRON_LINE="0 */2 * * * cd $(pwd) && python gap_discovery/scripts/monitor.py --once >> gap_discovery/monitor/cron.log 2>&1"
  (crontab -l 2>/dev/null | grep -v "personalab/gap_discovery/scripts/monitor.py"; echo "${CRON_LINE}") | crontab -
  echo "      ✅ crontab updated: monitor runs every 2h"
elif command -v schtasks >/dev/null 2>&1; then
  echo "      Windows detected; create task manually:"
  echo "      schtasks /create /tn 'personalab monitor' /tr 'python $(pwd)/gap_discovery/scripts/monitor.py --once' /sc hourly /mo 2"
else
  echo "      ⚠️  no cron/schtasks; run manually: python gap_discovery/scripts/monitor.py --once"
fi

echo
echo "=== DONE ==="
echo "Next manual steps:"
echo "  - Click the Show HN URL above when ready (use LAUNCH.md Option B body)"
echo "  - Watch gap_discovery/monitor/monitor_dashboard.md for organic mentions"
echo "  - Any inbound reply → run: python gap_discovery/scripts/auto_reply.py --inbound <json>"
