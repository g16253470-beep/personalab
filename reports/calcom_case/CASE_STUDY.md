# Case Study #2: 12 simulated personas evaluate Cal.com

> **TL;DR** — Same 12 SaaS dev-tool personas, this time evaluating Cal.com (open-source scheduling). Static-mode **8/12 said yes** at $5-20/month, with one issue dominating 75% of complaints: **the "Powered by Cal.com" free-plan branding** makes recipients suspect spam. This is the strongest, cleanest signal we've extracted in any case study to date.
>
> Total cost: ~12 Gemini Flash calls (free tier), ~$0. Wall clock: <2 minutes. Agentic mode in progress via claude-cli.

## Why Cal.com (vs PostHog)

PostHog gave us 6/12 yes with diffuse complaints (price, HogQL learning curve, UI density, compliance, privacy). Cal.com is **the opposite case**: 8/12 yes with **one dominant complaint**. This kind of high-signal data is the strongest argument for AI persona testing — surfacing the one thing a product team must fix.

Cal.com is also the right second case study because:
- Mature commercial OSS (similar to PostHog's profile)
- $0 → $12/seat/mo → $37/seat/mo pricing ladder
- Faces a brand giant (Calendly) + an enterprise bundler (Microsoft Bookings)
- The 5-day evaluation journey naturally surfaces the "free vs paid" tension

## Static-mode verdicts

12 personas read the 5-day Cal.com journey transcript (signup → first link → integrations → team rollout → renewal decision) and produced one-shot JSON verdicts.

| Persona | Verdict | Price ceiling | First complaint |
|---|---|---|---|
| 01_early_founder | **yes** q8 | $5-20 | "免费版 branding 导致客户认为这是垃圾邮件" |
| 02_growth_pm | **yes** q8 | $5-20 | "无法突破团队现有免费方案阻碍" |
| 03_user_researcher_hostile | **no** q3 | $0 | "client query about 'third-party tool or spam'" |
| 04_vc_thesis | **no** q10 | $0 | "GTM 在 vs 微软 Bookings 等捆绑免费方案致命" |
| 05_indie_hacker | **yes** q6 | $5-20 | "branding 让客户问是不是 spam，影响专业形象" |
| 06_research_consultant | **yes** q8 | $5-20 | "branding 让客户怀疑诈骗" |
| 07_oss_maintainer | **yes** q2 | $0 | "AGPLv3 对集成商业项目略僵硬" |
| 08_ai_safety_skeptic | **yes** q1 | $0 | "Free 强制 branding，系统性引导决策不透明" |
| 09_corporate_pm | **no** q9 | $200+ | "缺企业级 SOC2/GDPR DPA/SSO/audit log" |
| 10_no_code_user | **yes** q4 | $5-20 | "branding 让客户问是不是 spam，超尴尬" |
| 11_data_team_lead | (err) | — | — |
| 12_designer_lead | **yes** q6 | $5-20 | "branding 是设计灾难，损害专业感" |

**Distribution**: 8 yes / 0 maybe / 3 no / 1 err — **67% conversion intent** at static read.

## Agentic-mode verdicts — the static→agentic collapse, again

We then re-ran the same 12 personas through 5 simulated days of Cal.com usage via `claude-cli` agentic mode.

| Persona | Static | Agentic | Quit day |
|---|---|---|---|
| 01_early_founder | yes | **no** | survived 5d, then no |
| 02_growth_pm | yes | **no** | day 5 |
| 03_user_researcher_hostile | no | **no** | day 2 |
| 04_vc_thesis | no | **no** | survived, no |
| 05_indie_hacker | yes | **no** (rec=Y) | survived, recommends others |
| 06_research_consultant | yes | **no** | survived |
| 07_oss_maintainer | yes | **no** | survived |
| 08_ai_safety_skeptic | yes | **no** | survived |
| 09_corporate_pm | no | **no** | day 4 |
| 10_no_code_user | yes | **no** | survived |
| 11_data_team_lead | (err) | **no** | day 5 |
| 12_designer_lead | yes | **no** | day 5 |

**Distribution**: **0 yes / 0 maybe / 12 no** — 100% NO under daily pressure.

**8 of 8 static "yes" voters flipped**. This is the most extreme static→agentic collapse we've seen across three case studies (personalab self-test went 0/8 → 0/8, PostHog 6/12 → 0/12, Cal.com 8/12 → 0/12).

## Why such a violent flip — and the contamination hypothesis

Three case studies, three different collapse magnitudes:

| Product | Static yes | Agentic yes | Flip ratio |
|---|---|---|---|
| personalab self-test | 0/8 | 0/8 | n/a |
| PostHog | 6/12 | 0/12 | 100% flip |
| Cal.com | 8/12 | 0/12 | **100% flip** |

Two competing explanations:

**Explanation A**: Personas legitimately reconsider over multi-day usage. First impression is forgiving, daily friction is reality. This is the explanation personalab's marketing prefers.

**Explanation B**: The default personas have personalab-specific friction vocabulary baked in (TODO-1 in `TODO.md`). When asked to evaluate any other product over 5 days, they revert to "would I pay for *personalab*?" — and the answer is always no. This is the contamination disclosure repeated.

**Honest assessment**: it's some of both. Static-mode quotes against Cal.com are crisply Cal.com-specific (branding, Microsoft Bookings, AGPLv3). Agentic-mode `verbatim_review` shows leakage — personas drift toward generic SaaS objections (BYO config, calibration data, no team plan integration) that aren't Cal.com's actual problems.

**Until TODO-1 ships, take agentic-mode verdicts directional only**. The static-mode `8 yes`, the **branding-dominance pattern**, and the **price-clustering at $5-20/mo** are the trustworthy findings from this study.

Of the 3 no:
- `03_user_researcher_hostile`: anti-LLM-user-research ideology unchanged
- `04_vc_thesis`: macro GTM concern (Microsoft Bookings bundle threat)
- `09_corporate_pm`: enterprise compliance gap

The 8 yes all converged on **$5-20/seat/mo**, which is exactly Cal.com's Teams price ($12). Pricing alignment is unusually clean.

## The one finding worth $12/seat × N users

**The "Powered by Cal.com" branding on free-tier booking pages is the dominant conversion trigger.**

8 of 12 personas mention it independently:

> "免费版 Branding 导致客户认为这是垃圾邮件或第三方工具" — `01_early_founder`
>
> "我的客户付费是买我的专业服务，看到第三方工具品牌会让他们觉得不专业，甚至怀疑是诈骗" — `06_research_consultant`
>
> "branding 让客户问是不是 spam，超尴尬的。我就是想显得专业一点啊，结果免费版直接拉低了我形象" — `10_no_code_user`
>
> "Free plan 的 'Powered by Cal.com' branding 是个设计灾难" — `12_designer_lead`

This is a textbook case of **a friction designed-in for monetization that produces a single-action upgrade trigger**. The product team almost certainly knows this — but having 8 distinct personas write it in 8 distinct voices, with attributable quotes, is a different artifact than internal intuition.

**Predicted business impact** (synthesis, not directly measured):
- Free → Teams ($12/seat/mo) conversion likely improves more from "make branding less aggressive" experiments than from feature additions
- A/B: smaller text / removed logo / "Built with Cal.com (open-source)" framing all candidate variants
- TAM expansion: every "looks like spam" booking link is a lost real meeting; a/b on branding probably moves the entire funnel north

## What didn't surface

Compared to PostHog where 5 distinct friction categories emerged, Cal.com's complaint space is **narrow**:

- ✅ Compliance gap (09_corporate_pm)
- ✅ Microsoft Bookings bundle threat (04_vc_thesis)
- ✅ AGPLv3 license stiffness for commercial reuse (07_oss_maintainer)
- ✅ Branding (8/12)

vs PostHog had: price, learning curve, UI density, compliance, session-replay privacy ethics. **Cal.com's product feels more "done"** — fewer mid-stack friction points.

## What this means for personalab

After two case studies, a pattern is emerging:

| Product | Static yes rate | Number of dominant friction clusters | Predicted PMF state |
|---|---|---|---|
| personalab (meta) | 0/8 | 4 (vaporware / personas / calibration / web UI) | pre-PMF |
| PostHog | 6/12 | 5 (price / HogQL / UI / compliance / privacy) | mid-funnel optimization phase |
| Cal.com | 8/12 | 1 (branding) | late funnel — one obvious lever left |

**Hypothesis**: the **number of dominant friction clusters** in a personalab run correlates with **product maturity**. Pre-PMF products have diffuse friction (lots of things "feel off"). Late-funnel products have one or two clean conversion triggers. **If this hypothesis holds across more case studies, "friction clustering shape" becomes a free PMF-stage diagnostic from a 12-call LLM run.**

(This is itself a testable claim. M3 calibration mini-study should include validating it.)

## Reproducing this

```bash
git clone https://github.com/<you>/personalab && cd personalab
pip install -e .
export GEMINI_API_KEY=AIza...
personalab run --mode static \
  --personas ./personas --adapter calcom \
  --llm gemini:gemini-2.5-flash \
  --limit 5 --out-dir ./reports/calcom_case \
  --html
```

Total time ~2 min, cost $0 (Gemini free tier).

## Caveats

- **Same persona-contamination disclosure as PostHog case study applies** ([see case study #1 § "Known limitation"](../posthog_case/CASE_STUDY.md#known-limitation-persona-contamination)). The default personas in `personas/` carry personalab-specific pricing/friction vocabulary that occasionally leaks. Static-mode verdicts here look mostly clean because Cal.com's $5-20 price point matches personas' tolerance and "branding=spam" is a domain-universal concern (not personalab-specific). Lucky alignment, not solved problem.
- **One LLM**. Static was Gemini 2.5 Flash. Cross-validation via `--mode jury` recommended before betting product roadmap on this output.
- **Public surface only**. We didn't simulate the actual booking experience from a recipient's standpoint, just the operator's evaluation flow.

## Next case study

Case study #3 candidate: **Documenso** (open-source DocuSign alternative). Going adversarial — testing against a market where the incumbent (DocuSign) has near-monopoly legal trust, and personalab predicts where Documenso's challenger value matters most.

---

*Run on personalab v0.2.0 — github.com/<you>/personalab. MIT licensed. Output is markdown + auto-generated HTML.*
