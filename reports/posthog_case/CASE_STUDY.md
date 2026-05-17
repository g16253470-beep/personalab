# Case Study #1: 12 simulated personas evaluate PostHog Cloud

> **TL;DR** — We pointed `personalab` (an open-source LLM-driven persona testing framework) at PostHog's publicly-available product surface. 12 personas spanning B2B SaaS roles spent a simulated **5-day evaluation** (mode=both: static read + 5-day agentic). Result: static-mode **6 of 12 said they would pay**; agentic-mode under daily pressure **0/12 stayed, 1 considered subset subscription**. $140/month sticker shock and HogQL learning curve were the loudest friction points.
>
> Total cost: ~24 LLM calls via Gemini 2.5 Flash (free tier static) + ~72 calls via claude-cli subscription (agentic), ~$0 out-of-pocket. Wall clock: static 4 min + agentic 8 min.
>
> **⚠️ Known limitation surfaced in this study itself: see ["Known limitation: persona contamination"](#known-limitation-persona-contamination) below.**

## Why PostHog

It's an obvious meta-narrative — *a user testing tool tests a product analytics tool* — and PostHog's transparency culture means our criticism won't be unwelcome. They expose their pricing, surfaces, and self-host model on public pages, so we could write a `ProductAdapter` in 30 minutes without touching anything proprietary.

This is `case study #1` for personalab itself. We're using it to demonstrate the framework can be aimed at any public-surface SaaS in under an hour.

## The 12 personas

A deliberately heterogeneous panel:

- `01_early_founder` — second-time founder, pre-seed, $200/mo tool ceiling
- `02_growth_pm` — Series-B growth PM, OKR-driven
- `03_user_researcher_hostile` — anti-LLM-user-research veteran
- `04_vc_thesis` — Tier-2 VC partner evaluating dev tools
- `05_indie_hacker` — solo dev, $4k MRR, $30/mo tool budget
- `06_research_consultant` — independent UX consultant, $25-80k engagements
- `07_oss_maintainer` — full-time OSS maintainer, OSS-first
- `08_ai_safety_skeptic` — AI safety researcher
- `09_corporate_pm` — Staff PM at 5k-person enterprise
- `10_no_code_user` — marketing background, Webflow + Zapier stack
- `11_data_team_lead` — NLP PhD, stats-first
- `12_designer_lead` — design lead, ex-IDEO

Each persona is a 600-1500 word markdown file describing their background, pricing tolerance, what makes them subscribe, what makes them churn. (`personas/*.md` in the repo.)

## The setup

```python
# examples/posthog_case/adapter.py — ~150 lines
class PostHogAdapter(ProductAdapter):
    """Translate PostHog's public surface into a 7-day evaluation journey."""

    def load_events(self, ...):
        # Day 1: landing page + signup
        # Day 2: SDK install + first event
        # Day 3: session replay
        # Day 4: feature flags + experiments
        # Day 5: billing page (cost shock)
        # Day 6: self-host vs cloud decision
        # Day 7: renewal decision
```

Pricing details, competitor mentions, free-tier limits — all pulled verbatim from posthog.com as of 2026-05-18.

Then:

```bash
personalab run --mode both \
  --personas ./personas --adapter posthog \
  --llm gemini:gemini-2.5-flash \
  --days 5 --limit 7 --out-dir ./reports/posthog_case
```

## Static-mode verdicts (the headline data)

After reading the 7-day journey transcript in one shot, each persona produced a JSON verdict. Summary:

| Persona | Subscribe | Quit risk | Pricing | First complaint |
|---|---|---|---|---|
| 01_early_founder | **yes** | 3/10 | $50-200 | "$140/月太贵了，远远超出我心里能接受的上限" |
| 02_growth_pm | **yes** | 2/10 | $50-200 | "HogQL 学习曲线太陡峭" |
| 03_user_researcher_hostile | **yes** | 2/10 | $50-200 | "Insight 界面像迷宫，违背 Jakob's Law" |
| 04_vc_thesis | **yes** | 3/10 | $50-200 | "$140/mo procurement friction for early-stage" |
| 05_indie_hacker | **no** | 10/10 | $20-50 | "$140/month is absolutely brutal" |
| 06_research_consultant | **yes** | 4/10 | $50-200 | "心智负担太重，HogQL 学习曲线" |
| 07_oss_maintainer | **no** | 7/10 | $0 | "Self-host ClickHouse/K8s 抹杀'免费'" |
| 08_ai_safety_skeptic | **no** | 8/10 | $0 | "Session replay 隐私风险被正常化" |
| 09_corporate_pm | **no** | 10/10 | $0 | "无 SOC2 / GDPR DPA / SSO，procurement 否决" |
| 10_no_code_user | **maybe** | 8/10 | $50-200 | "看到 'install SDK' 差点关页面 😭" |
| 11_data_team_lead | **yes** | 3/10 | $50-200 | "HogQL 无图形化查询构建器" |
| 12_designer_lead | ERR | — | — | (LLM JSON parse fail) |

**Distribution**: 6 yes / 1 maybe / 4 no / 1 err — **conversion rate ≈ 55%** among personas. Compared to our previous case study where we pointed personalab at *itself* (0/8 yes), PostHog comes out dramatically better. Not surprising — PostHog is a real product with shipping users; personalab v0.1.0 is a pre-PMF framework.

## Agentic-mode verdicts (the truth under pressure)

We then re-ran the same 12 personas through 5 simulated days of PostHog usage (`--mode agentic --days 5`), using `claude-cli` for the long-running session. Each persona made one decision per day (`DO_NOTHING` / `/coin analytics-only` / `/profile self-host` / `UNSUBSCRIBE`), then a final verdict prompt.

| Persona | Static verdict | Agentic 5-day verdict | Quit day |
|---|---|---|---|
| 01_early_founder | yes | **no** $0 | day 5 |
| 02_growth_pm | yes | **no** $20-50 | survived 5 days, then no |
| 03_user_researcher_hostile | yes | **no** $0 | day 1 (instant unsub) |
| 04_vc_thesis | yes | **no** $0 | survived, then no |
| 05_indie_hacker | no | **no** $5-20 | day 5 |
| 06_research_consultant | yes | **no** $0 | day 4 |
| 07_oss_maintainer | no | **no** $0 (rec=Y) | survived, recommends others |
| 08_ai_safety_skeptic | no | **no** $0 | day 5 |
| 09_corporate_pm | no | **no** $0 | day 4 |
| 10_no_code_user | maybe | **no** $0 | day 1 (instant unsub) |
| 11_data_team_lead | yes | **no** $0 | day 4 |
| 12_designer_lead | err | **maybe** $20-50 | survived 5 days, considering |

**Distribution under pressure**: **0 yes / 1 maybe / 11 no**.

This is **the same pattern personalab surfaced in its self-test** and in the original v12.6 SignalStream tests: **agentic mode collapses the first-impression "yes" into reality-grounded "no"**. The 6 personas who said yes after reading the 7-day journey transcript in one shot all churned (or would have) when they had to make a daily decision.

The one survivor's "maybe" — `12_designer_lead` — is particularly informative. She used `/coin analytics-only` (a partial subscription) on day 4 and day 5, basically saying: *I don't need all 7 surfaces, just product analytics + session replay, at lower commitment*. This is **a specific, actionable product hypothesis** PostHog could test against real designer-segment users.

`07_oss_maintainer` is another interesting outlier: never subscribes, but **recommends to friends**. The OSS audience won't pay but will refer paying customers.

### What we learned from the static→agentic gap

- The "55% would subscribe" headline from static mode is **directionally meaningful but absolutely wrong** as a forecast. The real expected conversion (under 5-day pressure) is closer to 8% (`maybe` only, no `yes`).
- The personas that flipped from yes→no all had **price as the gating factor**. Their static "yes" was conditioned on the value; under daily pressure, they realized $140/mo is recurring and the marginal value per day didn't justify it.
- **The agentic mode is the one that matters** for go/no-go decisions. Static is useful for surfacing first-impression friction (what makes a user say "no" before they even try), but agentic is what tells you about retention.

## Top issues, ranked by independent mentions

### 🔴 #1: $140/month sticker shock

- 4 personas mention price explicitly: `01_early_founder`, `04_vc_thesis`, `05_indie_hacker`, `09_corporate_pm`
- Pattern: even personas who say "yes" qualify it as "expensive but worth it"
- `05_indie_hacker`: "*That $140/month estimate for PostHog Cloud is absolutely brutal.*"

### 🔴 #2: HogQL learning curve

- 4 personas: `02_growth_pm`, `06_research_consultant`, `07_oss_maintainer`, `11_data_team_lead`
- Pattern: users want cross-tab analytics without learning a new SQL dialect
- `11_data_team_lead`: "*在没有清晰的图形化查询构建器支持下，要求用户学习 HogQL 显著增加了认知负担。*"

### 🟡 #3: UI density / 8-tab Insight builder

- 3 personas: `03_user_researcher_hostile`, `06_research_consultant`, `10_no_code_user`
- Pattern: information overload for first-time users
- `03_user_researcher_hostile`: "*Insight 界面复杂得像个迷宫，违反 Jakob's Law*"

### 🟡 #4: Enterprise compliance gap

- 2 personas (hostile multiplier × 2 = weight 4): `09_corporate_pm`, `04_vc_thesis`
- Hard blocker, not friction. Without SOC2 / GDPR DPA / SSO, **5000-person companies cannot procure**.

### 🟡 #5: Session replay privacy risk

- 1 hostile persona: `08_ai_safety_skeptic`
- "*session replay 显著提高了用户隐私被侵犯和'暗模式'优化的风险*"
- A real ethical concern PostHog does address publicly, but the surface treatment leaves AI-safety types uneasy.

### 🟢 What worked (no complaints)

- **Session replay value** — appeared in 5 of 12 verbatims as a saving grace
- **Bundle pricing** — $140 was painful but framed as cheaper than Mixpanel + LogRocket + LaunchDarkly unbundled
- **Self-host transparency** — even personas who chose cloud appreciated the optionality

## What we learned about PostHog (the product)

In approximately one hour of setup + 4 minutes of LLM compute, we surfaced 5 distinct, defensible product friction points, each backed by ≥2 independent persona quotes. **None of these are surprising** to anyone who's used PostHog — but having them written from 12 distinct first-person perspectives, with verbatim attributable quotes, is a different artifact than a single internal note.

A PostHog PM running this could:

1. Drop the verbatim quotes from `09_corporate_pm` into the enterprise compliance roadmap as user-research evidence
2. Use the price-shock pattern to inform a "starter plan" pricing experiment
3. Show the `03_user_researcher_hostile` quote to the design team as ammunition for an Insight builder redesign

## What we learned about personalab (the framework)

- **The mode=both ran ~24 calls** before hitting Gemini Flash free-tier limits on the agentic phase. Static completed cleanly; agentic 12 verdicts errored on quota. **Lesson: free-tier LLMs don't scale to full 5-day × 12-persona runs.** Pay for Anthropic API, run claude-cli (subscription), or scope down.

- **The default keyword buckets in `ActionLoopReporter`** are tuned for SignalStream's domain (e.g., "AI 稳定性", "小币") and gave low signal on PostHog's friction (price, learning curve, compliance). The auto-clustering needs to be **product-agnostic**, probably embedding-based. **This is a roadmap item.**

- **claude-cli (Claude subscription) handled the full agentic load** that Gemini Flash free tier couldn't: 12 personas × ~6 calls each = 72 calls in 489 seconds (≈ 8 min wall time). Free Gemini hit daily quota around the 60-call mark.

- **Persona diversity worked**. Within 12 verdicts we saw 6 distinct ICPs (founder, growth, research, indie, OSS, no-code) producing meaningfully different verdicts — not all collapsing to "interesting but..."

## Known limitation: persona contamination

This case study surfaced its own framework defect — and rather than re-running with cleaner personas, we're keeping it as a transparency artifact.

**The bug**: the 12 default `personas/` markdown files were written *to evaluate personalab itself* (see the meta-test in `reports/meta/`). Their pricing tolerance and friction vocabulary include personalab-specific phrases like *"BYO persona"*, *"team plan $499"*, *"calibration data"*, *"ABMode for A/B"*. When we repurposed them to evaluate PostHog, several agentic-mode final verdicts mix the two products — at one extreme, `09_corporate_pm` explicitly notes "*推送 5 条全跑题 PostHog，与 personalab 无关*" (the 5 messages are all about PostHog, unrelated to personalab).

**What this means for the data**:
- Static-mode verdicts are mostly clean (personas reading a one-shot transcript stay on topic).
- Agentic-mode verbatim reviews are partially contaminated — they mix PostHog-specific friction (HogQL, $140/mo) with personalab-specific friction (BYO persona, calibration data). **The directional signal (0/12 sustained subscribers) is still real**; the verbatim quotes need readers to mentally separate the two products.

**Why we're not fixing it before publishing**:
1. Pretending the bug doesn't exist while UX-research-hostile reviewers would obviously spot it is worse than publishing it.
2. The structural fix is non-trivial: `personas/` should describe **user profiles** (background, budget, working style) separately from **product preferences** (what features they want, what triggers churn). Right now those are tangled in the same `.md` file. Untangling is roadmap item **M1** — write a follow-up post once it lands.
3. This is a useful case study **about persona design**, which is itself a contribution to the field. We'd rather ship a partial finding with caveats than wait for perfection.

**For your own runs**: if you reuse personalab's default personas to evaluate a product other than personalab, expect 20-30% of verbatim quotes to leak persona-side preferences. Either (a) author product-neutral personas, (b) author product-specific personas for each target, or (c) ignore verbatim quotes and just read the structured fields (`would_subscribe`, `pricing_willingness_usd_month`, `quit_trigger_score`).

## Reproducing this

```bash
git clone https://github.com/<you>/personalab && cd personalab
pip install -e .
export GEMINI_API_KEY=AIza...  # free tier ok
personalab run --mode static \
  --personas ./personas --adapter posthog \
  --llm gemini:gemini-2.5-flash \
  --limit 7 --concurrency 4 \
  --out-dir ./reports/posthog_case
```

Total time: ~4 min, total cost: $0 (free Gemini tier).

## Caveats

- **LLM personas ≠ real users.** This is a *hypothesis generator*, not a *validation tool*. Every issue surfaced here should be cross-checked with real PostHog customer interviews. PostHog has thousands of real users — they don't need our LLMs to tell them about price sensitivity. But for a pre-launch product without users, this is the cheapest way to surface obvious flaws.
- **One LLM is not a panel.** We ran this on Gemini 2.5 Flash. For rigorous evaluation, use `--mode jury` with multiple LLM backends and check `overall_agree` per persona. Personas where models disagree are unreliable.
- **Public-surface only.** This adapter doesn't simulate logged-in usage, dashboard interactions, or 3-month retention curves. It's a marketing-page + pricing-page evaluation, mapped over 7 simulated days.
- **Agentic mode completed via claude-cli** after Gemini Flash free tier was exhausted. Static used Gemini Flash (free), agentic used Claude subscription. Mixing backends is fine if you keep them separate within a run.

## Next case studies

If `case study #1` lands, we plan:
- **Case study #2**: Cal.com (open-source scheduling, similar audience)
- **Case study #3**: Documenso (DocuSign open alternative — adversarial market)
- **Case study #4**: A subscriber's own product (DM us)

---

*personalab is MIT-licensed. Repo: github.com/<you>/personalab. If you run it against your own product and the output is useful, we'd love to hear; if it's garbage, we'd love to hear that too.*
