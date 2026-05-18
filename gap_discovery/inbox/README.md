# Inbox — auto-drafted replies

This directory holds auto-generated reply drafts. Workflow:

1. **Someone replies** to a HN comment / GitHub issue / cold email
2. **You create** an inbound JSON (`templates/inbound_example.json`)
3. **Run** `python gap_discovery/scripts/auto_reply.py --inbound inbox/_pending/<file>.json`
4. **AI generates** 3 variant drafts (curious / concrete / short) + AI tell self-score
5. **You pick + edit 1-2 sentences** for personal voice (5 sec)
6. **Send** through original channel

## Inbound JSON schema

```json
{
  "channel": "hn_reply | github_issue | cold_email | twitter | other",
  "url": "https://...",
  "from_author": "their handle",
  "context_quote": "their original quote that started the thread",
  "their_reply": "what they just wrote back to you",
  "our_goal": "(optional) what you want to advance — calibrate WTP / get demo / etc"
}
```

## Templates

- `templates/inbound_example.json` — copy & fill
