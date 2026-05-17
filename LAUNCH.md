# Launch kit — personalab v0.2.0

Drafts for public release. Pick the one that fits the channel.

## Option A — "Tool" framing (safe)

### Show HN title

> Show HN: personalab – LLM personas test your product before real users do

### Show HN body (~250 words)

I've been building personalab — an open-source framework that runs your product through 12 LLM-simulated user personas. Each persona reads a multi-day evaluation transcript and produces a structured verdict: would they subscribe, what's their first complaint, how much would they pay, when would they churn.

The framework has 5 test modes: static (one-shot read), agentic (multi-day decision loop), jury (cross-LLM agreement check), AB (compare two product versions), and stats (variance bounds across N runs).

To demonstrate, I pointed it at three real products:

- **personalab itself**: 0/8 personas would subscribe to v0.1.0 — the case study became my own product roadmap.
- **PostHog**: 6/12 static "yes" collapsed to 0/12 sustained agentic — exactly the pattern personalab predicts (first-impression optimism crumbles under daily pressure).
- **Cal.com**: 8/12 yes converging on $5-20/mo, with one issue dominating 75% of complaints ("Powered by Cal.com" branding makes recipients suspect spam).

The Cal.com result is the cleanest signal I've extracted in any case study — eight distinct personas independently identified the same conversion-trigger lever.

`pip install personalab`, write a 40-line ProductAdapter for your product, run. MIT licensed. Roadmap (M3) is `MarketGapMode` — pointing it at a whole market instead of one product, to find the highest-confidence unfilled gap.

I'm publishing my own framework's failure honestly: see the "Known limitation: persona contamination" section in the PostHog case study. If you've built anything similar — or have a market you want gap-tested — I'd love feedback.

GitHub: <repo-url>
Cal.com case study: <link>
Why personalab failed at v0.1.0 (self-test): <link>

## Option B — "Thesis engine" framing (sharper, future-bet)

### Show HN title

> Show HN: personalab – let 12 AI personas tell you which $500/yr SaaS to build next

### Show HN body (~250 words)

Most "AI for user research" tools are LLM-prettified survey software. personalab is the opposite bet: a framework where 12 LLM-simulated user personas evaluate your product (or an entire market) and produce structured verdicts — would they pay, what's their first complaint, when would they churn.

Two demos against real products:

- **PostHog**: 6/12 static "yes" → 0/12 sustained over 5-day agentic simulation. Same pattern the framework's self-test produced.
- **Cal.com**: 8/12 yes → one issue (free-plan branding looking like spam) dominates 75% of complaints. The kind of high-signal single-lever finding a real product team can act on this week.

The bigger bet — currently a vision doc, not code yet — is `MarketGapMode`: point personalab at a whole market (say, "scheduling SaaS") plus public dissatisfaction signals (HN/Reddit/G2), and rank unfilled gaps by triangulated confidence. The asset that compounds: every gap is a public prediction; six months later you check whether someone filled it. Build a calibration track record no clone can replicate.

Three case studies for your sanity check:
- Self-test (0/8 would pay for v0.1.0): brutal but honest.
- PostHog (6/12 → 0/12 collapse): the static→agentic gap, exactly as theorized.
- Cal.com (8/12 → one dominant lever): the cleanest signal so far.

`pip install personalab`. MIT. CLI-only today; web UI is v0.3.0.

Honest disclaimer: the framework surfaced its own persona-design defect in the PostHog case study, and we kept that in the writeup rather than rerunning with clean data. It's worth reading for the methodology critique alone.

GitHub: <repo-url>

## Tweet thread (5 tweets)

**1/** I built personalab — an open-source framework where 12 LLM-simulated personas test your product before real users do. Then I pointed it at itself and at PostHog and Cal.com. The results changed my mind about what to build.

**2/** PostHog test: 6/12 personas said "yes I'd pay" after reading a 7-day evaluation transcript. Same 12 personas over 5-day agentic simulation: 0/12 sustained. The "static→agentic collapse" is the framework's central finding — first-impression optimism crumbles under daily pressure.

**3/** Cal.com test: 8/12 said yes at $5-20/mo. But here's the clean signal: 75% of complaints converged on ONE thing — the "Powered by Cal.com" branding on free-plan booking links. Eight distinct personas independently described it as making recipients suspect spam.

**4/** This is what personalab is built for: surfacing whether a product has diffuse pre-PMF friction (PostHog: 5 friction clusters) or one obvious lever (Cal.com: 1). It's a free PMF-stage diagnostic from a 12-call LLM run.

**5/** What's next: `MarketGapMode` — point it at a whole market + public dissatisfaction signals (HN/Reddit/G2), and rank unfilled gaps. Every gap is a public prediction with a 6-month accuracy check. Building it in the open. GitHub: <repo-url>

## Indie Hackers post (~400 words)

### Title

> I built an AI tool that finds product gaps, then I used it on my own tool. The results were brutal.

### Body

Two months ago I was building a crypto-signals product (SignalStream). It worked technically but I had no clue if anyone would actually subscribe. I wrote 12 fictional user personas — a burnt veteran trader, a quant, a noise-averse fund manager, a hostile regulator — and built a Python harness that fed each one the actual app output and asked: "what would you do?"

The honest answers — including "this is what compliance officers actually fine you for" — made me kill features I'd spent weeks on. I open-sourced the harness as `personalab`.

Then I pointed personalab at three other products and ran the same test:

1. **personalab itself** (yes, I tested my own product): 0 of 8 simulated dev-tool buyers said they'd pay $99/mo. The case study became my own roadmap.

2. **PostHog**: 6 of 12 said yes after reading a 7-day product transcript. Same 12 over a 5-day agentic simulation: 0 of 12 sustained. The "yes" was first-impression optimism. The "no" was reality.

3. **Cal.com**: 8 of 12 said yes at $5-20/mo. And here's the gold: 75% of complaints converged on ONE thing — the free-plan "Powered by Cal.com" branding. The PMs already know, but having 8 personas write it in 8 voices with attributable quotes is a different kind of evidence.

After three case studies, a pattern: the *number* of dominant friction clusters in a personalab run looks like it correlates with PMF stage. Pre-PMF products show 4-5 diffuse clusters; later-stage products show 1-2 clean conversion levers. If that hypothesis holds in case study #3 and #4, personalab becomes a free PMF-stage diagnostic from a $1 LLM run.

This is all MIT-licensed. There's no SaaS. The honest disclaimer is that my default personas accidentally encoded personalab-specific preferences, so when I reused them on PostHog/Cal.com some quotes leak — I kept the bug in the case study writeup and made the fix a roadmap item rather than hiding it.

If you'd find it useful to test your own product before launch, `pip install personalab`, write a 40-line adapter, run. If you find it terrible — please tell me; that's the next case study.

GitHub: <repo-url>

## Posting sequence (recommended)

1. **T-1 hour**: post Indie Hackers (slow burn, surfaces over 24h)
2. **T-0**: post Show HN (best 9am-11am PT weekday) — use **Option B** if you can survive Q&A about MarketGapMode, otherwise Option A
3. **T+15 min**: post Tweet thread, quote-RT the HN post
4. **T+1 day**: post to Lobsters
5. **T+2 days**: post to r/SaaS, r/sideproject (linkback to HN top comment with the case study summaries)
6. **T+3 days**: if Show HN >100 upvotes, write Indie Hackers follow-up "What I learned from launching personalab" with response data
