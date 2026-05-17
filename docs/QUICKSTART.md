# QUICKSTART (5 minutes)

You will: install personalab, run it against a toy product, read the report, then point it at your own product.

## 1. Install (1 min)

```bash
git clone https://github.com/<you>/personalab && cd personalab
pip install -e .
personalab version  # should print: personalab 0.1.0
```

## 2. Smoke test with the toy adapter (30 sec)

This uses **no LLM calls** — just a fake LLM emitting templated JSON. Confirms the pipeline is wired.

```bash
python tests/test_e2e_smoke.py
```

Expected:
```
[OK] L1 end-to-end smoke test passed
[OK] L3 jury smoke test passed
[OK] L4 ab smoke test passed
[OK] L5 stats smoke test passed
[OK] L6 calibration smoke test passed
[OK] L7 toy-adapter smoke test passed
```

If any line fails, file an issue with the traceback.

## 3. First real run (2 min)

You need an LLM backend. Pick one:

- **Claude subscription** (recommended if you have a Claude Code/Anthropic subscription): `--llm claude-cli`
- **OpenAI**: `export OPENAI_API_KEY=sk-...` then `--llm openai:gpt-4o`
- **Gemini** (has free tier): `export GEMINI_API_KEY=AIza...` then `--llm gemini:gemini-2.5-flash`

Run against either bundled example. Easiest is the **toy** adapter (no setup, in-memory events):

```bash
# Run static mode against the toy adapter (cheapest — 12 LLM calls, ~$0.20)
personalab run --mode static \
  --personas ./personas \
  --adapter toy \
  --llm gemini:gemini-2.5-flash \
  --limit 3 --concurrency 3 \
  --out-dir ./reports
```

For a more realistic example, use the **posthog** case-study adapter
(7-day evaluation of PostHog Cloud — public material only):

```bash
personalab run --mode static \
  --personas ./personas \
  --adapter posthog \
  --llm gemini:gemini-2.5-flash \
  --limit 7 --concurrency 3 \
  --out-dir ./reports/posthog
```

Or against the original **signalstream** example (an okx_pulse-shaped
sqlite db — useful for testing the agentic/severity/category filters):

```bash
python scripts/seed_demo_db.py demo.db 200
personalab run --mode static \
  --personas ./personas_signalstream \
  --adapter signalstream --db demo.db \
  --llm gemini:gemini-2.5-flash \
  --limit 20 --concurrency 3 \
  --out-dir ./reports
```

Open `./reports/static_report.md` — you should see 12 personas writing 12 distinct verdicts in their own voice.

## 4. Run the full battery (5 min)

```bash
personalab run --mode both \
  --personas ./personas \
  --adapter posthog \
  --llm gemini:gemini-2.5-flash \
  --limit 7 --days 5 --concurrency 3 \
  --html \
  --out-dir ./reports
```

`--html` produces a sibling `.html` next to every `.md` report — single-file,
self-contained, shareable with non-technical stakeholders.

Now you get 4 reports:
- `static_report.md` — first impressions
- `agentic_report.md` — 5-day behavior, when each persona churned
- `comparison_report.md` — static vs agentic, where the "maybes" got pushed to "no"
- `action_loop.md` — auto-clustered P0/P1/P2 issue list with persona quotes

## 5. Cross-model jury (optional, 2 min)

Detect single-LLM bias by running multiple judges on the same prompt:

```bash
personalab run --mode jury \
  --personas ./personas \
  --adapter posthog \
  --llm "claude-cli,gemini:gemini-2.5-flash" \
  --limit 7 \
  --out-dir ./reports
```

Open `./reports/jury_report.md` — flagged rows with `overall_agree < 0.66` are personas where the LLMs disagree; **don't trust those verdicts**.

## 6. Point it at YOUR product (15-30 min)

Two files to write:

1. **Adapter** — copy `examples/toy/adapter.py` (~40 lines), implement `load_events()` and `render_event()` against your product's events/messages/UI states. See [ADAPTER_GUIDE.md](ADAPTER_GUIDE.md).
2. **Personas** — write or borrow `.md` files describing your target users. The 12 in `./personas/` are SaaS-flavored; rewrite for your domain. See [PERSONA_WRITING.md](PERSONA_WRITING.md).

Then:
```bash
personalab run --mode both \
  --personas ./my_personas \
  --adapter your_adapter \
  --llm claude-cli \
  --out-dir ./reports
```

## What's normal, what's a problem

| You see... | Meaning |
|---|---|
| `Agentic 把 N 个 maybe 打回 no` | Working as intended — 5-day behavior tightens verdicts |
| `LLM ... attempt 1/3 failed: parse error` | LLM emitted malformed JSON; retries usually save it |
| `jury overall_agree=0.0` for one persona | Persona ambiguous to LLMs; rewrite that .md tighter |
| All 12 personas write the same complaint | Either your product has one massive flaw, or personas aren't differentiated. Check `personas/` files for redundancy |
| `Quota exceeded` | Your LLM key is rate-limited; switch backends or wait |

## Next

- [ARCHITECTURE.md](ARCHITECTURE.md) — how the framework fits together
- [ADAPTER_GUIDE.md](ADAPTER_GUIDE.md) — write a ProductAdapter
- [PERSONA_WRITING.md](PERSONA_WRITING.md) — write personas that produce useful (not generic) feedback
