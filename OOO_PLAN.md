# OOO plan — 2026-05-18 to 2026-05-22 (Mon → Fri)

> User unavailable Mon-Fri this week. Autonomous bot covers dev.to + GitHub replies.

## What runs autonomously (no user action needed)

| Task | Frequency | Coverage |
|---|---|---|
| `personalab_monitor` (Windows task) | Every 2h | Scan HN/GitHub for personalab/C11 mentions |
| `personalab_autoreply` (Windows task) | Every 30 min | Reply to new dev.to comments + GitHub issues |
| Spam filter | Per-comment | SKIP comments with WhatsApp / SEO / phone / contact-email signals |
| Daily cap | 5 replies/day | Prevent over-engagement |
| Signature | All bot replies | "_(drafted while traveling — back Friday, will respond properly then)_" |
| AI tell critic | Per draft | If self-score > 6, log only, don't post |

## What does NOT run autonomously (waits for Friday)

| Channel | Why blocked | Plan Friday |
|---|---|---|
| IH launch post | No official API | Triage comments manually |
| Reddit (r/SideProject, r/indiehackers) | Filtered + no easy API | Modmail follow-up |
| HN | No API + account needs warm-up | Continue warm-up 2-4 weeks |

## Bot config

```
DAILY_CAP        = 5 replies/day
REPLY_LENGTH     ≤ 80 words
SPAM_KEYWORDS    = whatsapp, seo, brand ranking, contact:, phone#, "+44", "+1 (" etc.
AI_TELL_THRESHOLD = ≤ 6/10 (else log only)
SIGNATURE        = "(drafted while traveling — back Friday, will respond properly then)"
```

## Where to look Friday

| File | Purpose |
|---|---|
| `gap_discovery/inbox/autoreply_log.jsonl` | Every bot action: posted / draft_rejected / spam_skipped |
| `gap_discovery/inbox/autoreply_state.json` | seen_ids + daily counts |
| `gap_discovery/monitor/monitor_ledger.jsonl` | All HN/GitHub mentions captured |
| `gap_discovery/monitor/monitor_dashboard.md` | Auto-updated dashboard |
| GitHub: github.com/g16253470-beep/personalab — Issues tab | Any inbound issues |
| Indie Hackers: indiehackers.com/post/launched-personalab... | Manual triage queue |

## Known risks during 5-day window

1. **Bot draft replies sub-optimally** — daily cap = 5 限制损害规模，signature 揭示AI assist 让 reader 知道  
2. **Spam evades filter** — possible. Log captures everything; you can roll back any bad post Friday by deleting from dev.to UI  
3. **dev.to mass spammers** — SEO bots target launch posts. Spam filter catches keyword-based ones; novel spam may pass once before keyword added  
4. **IH/Reddit silence** — 5 days of unanswered comments may dampen post  

## First 24h check (Mon evening if you have 30 sec)

```bash
cat G:\gpt\personalab\gap_discovery\inbox\autoreply_log.jsonl | tail -10
```

Look for `"action": "posted"` lines — those are real bot replies on dev.to.

## Rollback procedure (if any bot reply is bad)

1. Open dev.to → your launch post → comments
2. Find offending bot reply → ⋮ menu → Delete
3. Edit `gap_discovery/scripts/autonomous_reply_bot.py` to disable or tune
4. Or just delete `personalab_autoreply` task: `schtasks /delete /tn personalab_autoreply`

## Friday 2026-05-22 morning kickoff

1. `cd G:/gpt/personalab && git pull` (in case auto-commit ran)
2. Review `gap_discovery/inbox/autoreply_log.jsonl` — see all bot actions
3. Check IH post manually for accumulated comments → reply personally
4. Check dev.to engagement metrics (views/reactions/comments_count)
5. Decide next vertical / W2 Tauri progress / case study #4

## Bot lifetime

This is scoped to **2026-05-18 to 2026-05-22**. Friday you should either:
- Disable `personalab_autoreply` task (return to manual reply for higher quality)
- Or extend with new bot config (e.g. add IH if API surfaces)

```powershell
# To disable Friday:
Disable-ScheduledTask -TaskName personalab_autoreply
# Or delete entirely:
Unregister-ScheduledTask -TaskName personalab_autoreply -Confirm:$false
```
