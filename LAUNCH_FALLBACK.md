# Launch fallback — HN 新账号被拦后的替代渠道

> HN 在 2026-05-18 09:18 BJT 拒绝 Show HN（新账号 anti-spam 政策）。这份文档是 4 个替代渠道的 platform-specific drafts。

## 🎯 Indie Hackers — 最高优先级

**URL**: https://www.indiehackers.com/post/new
**Category**: Tech (Open Source / AI)
**Tags**: ai, open-source, market-research, saas

### Title
```
I built an AI tool that tests products before users do. Then I used it on myself. The result was brutal.
```

### Body

```
Two months ago I was building a crypto signal product. It "worked technically" but I had no idea if anyone would subscribe.

So I wrote 12 fictional user personas — a burnt veteran trader, a quant, a compliance officer, a hostile YC partner — and built a Python harness that fed each one the actual product transcripts and asked: "what would you actually do?"

The honest answers — including "this is what compliance officers fine you for" — made me kill features I'd spent weeks on.

I open-sourced the harness as `personalab` (MIT). Then I pointed it at three more products:

**1. personalab itself** (yes, my own tool tested my own tool):
0 of 8 simulated B2B SaaS buyers said they'd pay $99/mo. The case study became my own roadmap.

**2. PostHog** (open-source product analytics, 20k+ stars):
6 of 12 personas said "yes I'd pay" after reading a 7-day product transcript. Same 12 over 5-day agentic simulation: **0/12 sustained**. The "yes" was first-impression optimism. The "no" was multi-day reality.

**3. Cal.com** (open-source scheduling):
8 of 12 said yes at $5-20/mo. And here's the gold: 75% of complaints converged on ONE thing — the free-plan "Powered by Cal.com" branding. 8 distinct personas independently identified it as the dominant conversion lever.

After 3 case studies, a pattern: the *number of dominant friction clusters* in a personalab run looks like it correlates with PMF stage. Pre-PMF products show 4-5 diffuse clusters; later-stage products show 1-2 clean conversion levers. If this hypothesis holds in case study #3 and #4, personalab becomes a **free PMF-stage diagnostic from a $1 LLM run**.

All MIT-licensed. The honest disclaimer is the default personas accidentally encoded personalab-specific preferences, so when I reused them some quotes leak. I kept the bug in the case study writeup and made the fix a roadmap item rather than hiding it. It surfaces persona-design as a real engineering concern.

GitHub: https://github.com/g16253470-beep/personalab

If you'd find it useful to test your own product before launch:
`pip install -e .` from repo, write a 40-line adapter, run.

If you find it terrible — please tell me; that's the next case study.

Three questions for IH:
1. What product would you point this at first?
2. Is there a way this can actually become a $5k MRR business, or is it just an open-source curiosity?
3. Has anyone else built similar tooling?
```

---

## 🎯 Reddit r/SaaS

**URL**: https://www.reddit.com/r/SaaS/submit
**Flair**: Open Source / Product Launch

### Title
```
I built an LLM persona testing framework, then used it to test 3 real SaaS products (PostHog, Cal.com, my own). The results were brutal.
```

### Body

```
**TL;DR**: Open-source framework where 12 LLM-simulated user personas evaluate your product. I tested it on 3 real products. All my static "yes" verdicts collapsed to "no" under 5-day agentic simulation.

**The Method**

Each "persona" is a 600-1500 word markdown file describing a user's background, budget, friction tolerance, what makes them subscribe/churn. The framework runs:

1. Static mode: persona reads a transcript, produces one-shot JSON verdict
2. Agentic mode: persona "uses" the product 5 days, makes daily decisions
3. Jury mode: same prompt across N LLMs (Claude/GPT/Gemini), check agreement
4. Calibration: compare predictions to real user data

**The Results**

- **My own tool (self-test)**: 0/8 personas would pay $99/mo. Brutal honesty.
- **PostHog**: 6/12 static "yes" → 0/12 agentic. Friction: $140/mo, HogQL learning curve, UI density, compliance gap.
- **Cal.com**: 8/12 static "yes" → 0/12 agentic. 75% of complaints converged on ONE thing: free-plan "Powered by Cal.com" branding looks like spam.

**The Real Finding**

After 3 case studies, I think the *number of dominant friction clusters* correlates with PMF stage:
- Pre-PMF: 4-5 diffuse complaints (my tool: vaporware features, persona contamination, no calibration, CLI-only)
- Late-funnel: 1-2 clean levers (Cal.com: branding)

If this holds across 5+ products, the framework becomes a free PMF-stage diagnostic from a ~$1 LLM run.

**Why I'm Posting**

- Looking for product owners who'd let me test their thing (free, share results)
- Curious if r/SaaS thinks this can be a $5k MRR business or just an OSS curiosity
- Want to find collaborators for case studies #4 onwards

**Repo**: https://github.com/g16253470-beep/personalab (MIT)

**Honest disclaimer**: my default personas had personalab-specific preferences leaked in. When reused on other products some verdicts contaminate. I kept the bug in the case study rather than hiding it — surfaces persona design as a real engineering problem.
```

---

## 🎯 Reddit r/sideproject

**URL**: https://www.reddit.com/r/sideproject/submit
**Flair**: Show & Tell

### Title (HN-style allowed here)
```
[Show] I tested my AI product tester on 3 real SaaS products. Every single persona said no.
```

### Body
Shorter version of r/SaaS body (~200 words):

```
Open-source framework where 12 LLM personas evaluate your product like real buyers. Static + 5-day agentic simulation + cross-model jury.

Tested on 3 real products:
- personalab (my own): 0/8 yes
- PostHog: 6/12 → 0/12 (static→agentic collapse)
- Cal.com: 8/12 → 0/12, ONE dominant lever (free-plan branding looks spam)

Cal.com result is the cleanest single-lever finding I've extracted. 8 personas independently nailed the same issue.

The framework surfaces its own bug honestly — persona contamination. Kept it in writeup rather than hiding.

MIT licensed: https://github.com/g16253470-beep/personalab

`pip install -e .` from repo. 40-line adapter, 12 default personas (or write your own), run.

Curious if r/sideproject has thoughts on:
- Real PMF or just OSS curiosity?
- Which product should be case study #4?
```

---

## 🎯 dev.to (technical audience)

**URL**: https://dev.to/new
**Tags**: opensource, ai, python, productivity

### Title
```
How I built an LLM persona framework, then used it to predict my own product would fail
```

### Body (truncated)

Longer technical version focused on architecture (TestMode composition, persona schema, jury cross-validation). 800-1500 words. Skip for now if time-constrained.

---

## 🎯 Hashnode / personal blog

If you have one, cross-post the IH version.

---

## Posting cadence (recommended)

| Hour | Action |
|---|---|
| **+0** (now) | Post Indie Hackers (slow burn, surfaces over 24h) |
| **+30 min** | Post r/sideproject |
| **+60 min** | Post r/SaaS (different angle, less repetitive) |
| **+2 hr** | (optional) dev.to long technical version |
| **+24 hr** | reply to comments + cross-link |

**Don't blast all at once** — Reddit / IH have community guidelines against multi-cross-post within minutes. 30-60 min spacing looks organic.

## HN warm-up parallel (2-4 weeks)

Every day, log into HN under `g16253470-beep`:
1. **Comment** 1-2 thoughtful comments on existing Show HN / Ask HN
2. **Upvote** 5-10 good posts
3. **Submit** 1 interesting article (someone else's, not yours)

Goal: 50+ karma + 2 weeks activity. Then **retry Show HN** — will be allowed.

In meantime, **organic HN traffic still comes** via Google search "Show HN" cache + the public repo (HN bots index GitHub trending).
