# personalab

> LLM-driven user testing framework. Pit 12 simulated personas against your product before real users do.

## What it does

You give it:

1. **Personas** — `.md` files describing virtual users (background, motivations, pet peeves, pricing tolerance)
2. **A ProductAdapter** — ~40 lines of Python connecting your product to the framework

It returns:

- Will each persona subscribe? (`yes / maybe / no`)
- What's their first complaint, in their voice?
- What's their pricing tolerance? `$0 / 5-20 / 20-50 / 50-200 / 200+`
- In agentic mode: their 5-day usage trajectory — when do they churn, why?
- Cross-persona pattern detection → automatic P0/P1 issue list

Designed to **augment**, not replace, real user research — it's cheaper and faster for "find obvious flaws before talking to real users", not for "validate final pricing tier".

## Test modes (composable)

| Mode | LLM calls (12 personas) | What it tells you |
|------|---|---|
| **Static** | 12 | First-impression verdict from each persona |
| **Agentic** | 12 × (days + 1) | Multi-day behavioral trajectory + churn day |
| **Jury** | 12 × N models | Cross-model agreement (detect single-LLM bias) |
| **AB** | 2 × inner-mode | Diff between two product versions |
| **Stats** | inner × N repeats | Variance / confidence intervals on numeric fields |
| **Calibrate** | 0 (offline) | Your personas' predictions vs real user behavior |

Modes nest: `StatsMode(AgenticMode(...))`, `ABMode(StatsMode(StaticMode(...)))`.

## Install

```bash
git clone https://github.com/<you>/personalab && cd personalab
pip install -e .
```

Optional extras: `pip install -e .[openai]` / `.[gemini]` for non-Anthropic LLM backends.

## 60-second example

```bash
# Run all default personas against an adapter, both static + agentic
personalab run --mode both \
  --personas ./personas \
  --adapter signalstream --db ./demo.db \
  --llm claude-cli \
  --limit 25 --days 5 --concurrency 3 \
  --out-dir ./reports
```

Outputs four reports into `./reports/`:

- `static_report.md` — each persona's one-shot verdict + verbatim
- `agentic_report.md` — multi-day decisions per persona
- `comparison_report.md` — static vs agentic, divergence analysis
- `action_loop.md` — auto-clustered P0/P1/P2 issue list with persona quotes

More: [QUICKSTART](docs/QUICKSTART.md) · [Architecture](docs/ARCHITECTURE.md) · [Write an adapter](docs/ADAPTER_GUIDE.md) · [Write a persona](docs/PERSONA_WRITING.md)

## What's in the box

- **12 default personas** spanning B2B SaaS roles: founder, growth PM, user researcher (hostile), VC, indie hacker, research consultant, OSS maintainer, AI safety skeptic, corporate PM, no-code user, data team lead, design lead — swap or extend for your domain.
- **Reference ProductAdapter** at `examples/signalstream/` — full okx_pulse / SignalStream port showing severity / category / coin filters and 8 user commands.
- **Toy adapter** at `examples/toy/` — 40-line minimum demonstrating the contract.
- **Meta adapter** at `examples/personalab_meta/` — personalab evaluating itself as a commercial product.

## Honest disclaimers

- **LLM personas ≠ real users.** Use the output to find obvious flaws fast, then validate with real interviews. The Calibration mode exists precisely so you can measure how reliable your personas are against actual user behavior.
- **Pre-PMF status.** This is `v0.2.0`. The framework is feature-complete (all 6 modes work, 6 smoke tests pass), but it has not been validated against many real products yet. Expect rough edges.
- **CLI-only today.** No web UI, no Slack integration, no team plan. If those matter, wait for `v0.3.0` or fork.
- **HTML reporting included.** Pass `--html` to `personalab run` and every markdown report gets a sibling `.html` (self-contained, shareable). For Notion/PDF, render from there.
- **Persona contamination is real.** When you reuse personas across products, their pricing tolerance and friction vocabulary leaks. Our PostHog case study surfaces this in itself ([see CASE_STUDY known limitations](reports/posthog_case/CASE_STUDY.md)). Roadmap M1 separates user profile from product preference vocabulary.

## Why this exists

Most user-testing tools either (a) need real recruited users (slow, expensive, hard-to-iterate) or (b) are a single ChatGPT prompt that doesn't surface diverging perspectives or multi-day behavior. personalab sits in the middle: structured enough to be useful before real users, light enough to run 30 times during a single design review.

It started as `persona_test.py` + `agentic_persona_test.py` for the SignalStream crypto-signals product (see `examples/signalstream/` and `personas_signalstream/` for the original artifacts), then got abstracted into a framework so it could be applied to any product.

## License

MIT.
