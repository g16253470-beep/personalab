# posthog Agentic 行为仿真报告

生成: 2026-05-18 01:31 UTC+8 · 仿真 5 天 · 12 个人格 · 事件: 7 · LLM: claude-cli

## 📊 汇总

| 人格 | 完成天数 | 退订日 | 累计收到 | 最终 | 月费 | 推荐? |
|---|---|---|---|---|---|---|
| 01_early_founder | 5/5 | 5 | 7 | ❌ no | 0 | ❌ |
| 02_growth_pm | 5/5 | - | 7 | ❌ no | 20-50 | ❌ |
| 03_user_researcher_hostile | 1/5 | 1 | 2 | ❌ no | 0 | ❌ |
| 04_vc_thesis | 5/5 | - | 7 | ❌ no | 0 | ❌ |
| 05_indie_hacker | 5/5 | 5 | 6 | ❌ no | 5-20 | ❌ |
| 06_research_consultant | 4/5 | 4 | 5 | ❌ no | 0 | ❌ |
| 07_oss_maintainer | 5/5 | - | 7 | ❌ no | 0 | ✅ |
| 08_ai_safety_skeptic | 5/5 | 5 | 7 | ❌ no | 0 | ❌ |
| 09_corporate_pm | 4/5 | 4 | 5 | ❌ no | 0 | ❌ |
| 10_no_code_user | 1/5 | 1 | 2 | ❌ no | 0 | ❌ |
| 11_data_team_lead | 4/5 | 4 | 5 | ❌ no | 0 | ❌ |
| 12_designer_lead | 5/5 | - | 7 | ⚠ maybe | 20-50 | ❌ |

## 🎬 每人格行动序列

### 01_early_founder

- **day 1** (收 2 条, mood: *curious*, engage 7/10) → `DO_NOTHING` — 刚装上才发第一条 event，funnel 还没建出来，现在调配置太早
- **day 2** (收 1 条, mood: *annoyed*, engage 4/10) → `DO_NOTHING` — funnel 都没搭，看 replay 是噱头，先把 ICP 写完
- **day 3** (收 1 条, mood: *annoyed*, engage 4/10) → `DO_NOTHING` — funnel还没建完，A/B test对pre-seed没意义，先聚焦ICP和客户访谈
- **day 4** (收 1 条, mood: *considering_quit*, engage 4/10) → `/coin analytics-only` — replay有用，flags对pre-seed没意义，砍掉省钱
- **day 5** (收 2 条, mood: *considering_quit*, engage 3/10) → `UNSUBSCRIBE` — $140/月吃掉1%跑道，7个产品用2个，GA+Hotjar够用

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: $140/月吃掉1%跑道，7条推送只有replay对我有用。没看到任何'persona预测 vs 真实用户行为'的对照数据，我不敢拿这个骗自己第二次。
- 欣赏: Session replay 是真的有价值——day4我差点为了它单独留下。12 personas 提前压测 pitch 的想法听起来诱人，但5天里没一条推送证明它真比我自己脑补强。
- 原话:
  > Tried personalab for a week as a pre-seed founder. Verdict: not for us. 7个推送5天，funnel都没搭起来就在推A/B test和flags——典型的'功能堆砌型'SaaS，没考虑用户实际处在哪个阶段。Session replay确实有用，但$99/月就为这个？GA+Hotjar白嫖能搞定80%。真正的killer是calibration缺失：'LLM假扮12个persona帮你压测pitch'听起来很性感，但没有任何'预测vs真实结果'的backtest数据。我上次创业就死在'假需求'上，这次不会再为没验证过的东西付费。如果他们能拿出'用过personalab的团队 vs 没用的，6个月后产品/市场契合度差异'的数据，再聊。在那之前，$300做5个真人访谈更踏实。

### 02_growth_pm

- **day 1** (收 2 条, mood: *curious*, engage 7/10) → `DO_NOTHING` — Day 1 顺，先跑 funnel 看 ICP fit 再调配置
- **day 2** (收 1 条, mood: *curious*, engage 7/10) → `DO_NOTHING` — 录像功能有兴趣,但要先看funnel+ICP fit再调,别急着开新模块
- **day 3** (收 1 条, mood: *curious*, engage 7/10) → `DO_NOTHING` — PostHog AB体验顺，先跑两周看数据相关性再调配置
- **day 4** (收 1 条, mood: *considering_quit*, engage 6/10) → `DO_NOTHING` — $140在$300预算内,先跑满月看ICP fit再决,别急着切栈
- **day 5** (收 2 条, mood: *considering_quit*, engage 6/10) → `/coin analytics-only` — 7产品里只analytics+replay真用上,砍冗余降成本聚焦conversion

**最终判定**:
- 续订: no
- 月费意愿: 20-50
- 最大阻力: 12 个固定 SignalStream 人格跟我 SaaS ICP 零重合，无法 BYO persona、无法导 ICP 文档，ABMode 跑出来的 diff 没有 calibration 数据证明跟真实 A/B 相关性 >0.4。
- 欣赏: ABMode 思路对——v1 vs v2 自动 diff + P0 issue list 确实能省一次设计评审会。Analytics + replay 两个模块真的用上了，比看 Hotjar 录像快。
- 原话:
  > I evaluated personalab on 3 axes: speed 8, quality 5, ICP fit 3. ABMode 的产品直觉是对的——pre-A/B 跑一遍 personas、自动 diff 出 P0 issues，理论上能砍 30% 注定失败的实验。但落地两个硬伤：一是 12 个加密人格全是 trader/researcher，跟 SaaS funnel 用户零重合，又不能 import 自家 ICP doc 生成 persona；二是没有跟 Amplitude/Mixpanel 的回测数据，我没法证明 prediction 跟真实 conversion 相关性 >0.4。$140/月在预算内但买的是信仰。给我 BYO persona + calibration report，team plan $499 我立刻签。现在状态：analytics-only $29 续着，主功能砍了。

### 03_user_researcher_hostile

- **day 1** (收 2 条, mood: *done*, engage 1/10) → `UNSUBSCRIBE` — Synthetic users are professional malpractice; no ground truth validation shown.

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 零 ground truth validation。没有 r²、没有 prediction vs reality 曲线、没有 calibration 报告。方法学层面就是 next-token prediction 冒充用户研究。
- 欣赏: 作为 brainstorm 工具列出'我们可能漏掉的 segment'尚可，可以当成会议前的便签——但仅此而已，绝不进入决策链路。
- 原话:
  > As someone who's run 200+ interviews: personalab 是 synthetic users 这个伪学科的又一个标本。Day 1 我就退订了，剩下 4 天没回头看。问题不在 UI、不在 persona 文案写得漂不漂亮——问题在于他们从不展示 ground truth validation。没有 r²、没有 prediction-vs-reality 曲线、没有 calibration 数据，凭什么让我把 12 个 RLHF-flattened 的'人格'当成用户洞察？Jakob Nielsen 不会同意，Steve Krug 不会同意，任何在真实访谈室里坐过的人都不会同意。更危险的是政治后果：团队用了它，procurement 就再也不批真实用户研究预算了，你以为省了 $99/月，实际上失去了发现 unknown unknowns 的能力。Medium 长文在路上了,标题已经想好:《Why I won't be using AI synthetic users in 2026》。

### 04_vc_thesis

- **day 1** (收 2 条, mood: *curious*, engage 7/10) → `DO_NOTHING` — Day 1 评估期，feature set 还没看完，先观察 PLG funnel 自己跑通没
- **day 2** (收 1 条, mood: *calm*, engage 3/10) → `DO_NOTHING` — Not my workflow—I evaluate founders, not run session replay on my own site.
- **day 3** (收 1 条, mood: *calm*, engage 3/10) → `DO_NOTHING` — Not a buyer. Evaluating PLG funnel signals, not implementing.
- **day 4** (收 1 条, mood: *calm*, engage 3/10) → `DO_NOTHING` — Not a buyer. Evaluating as deal, not user—pricing irrelevant to thesis.
- **day 5** (收 2 条, mood: *calm*, engage 3/10) → `DO_NOTHING` — Not a buyer—evaluating as deal. No subscription decision to make.

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: CLI-only + pip install onboarding，没有 web UI、没有团队协作、没有 SOC2，PLG funnel 第一步就漏 99% 用户。
- 欣赏: Framework 工程素养在线，prompt 编排和 persona 抽象 clean，作为 pre-seed feasibility 工具能跑通核心循环。
- 原话:
  > Strong technical, weak distribution. 看了 5 天，founder 把 framework 写得很干净，能看出 engineering chops，但这不是 fundable product。TAM 在 AI-for-research 撑死 $50M/年 long-tail，moat 一周可复刻，Anthropic 一个 feature 就秒了。GTM 更要命：CLI + pip install 的 onboarding 在 PLG 漏斗第一步就死，没有 web UI、没有 SSO、没有 SOC2，enterprise 进不去，$99/mo 又撑不起 sales team，$5M ARR 要 4200 客户，不现实。Pre-seed only if founder 全职 + 招 commercial co-founder。Personal use 我不会订阅，这是 funding decision 不是 subscription decision。

### 05_indie_hacker

- **day 1** (收 2 条, mood: *curious*, engage 7/10) → `/coin analytics-only` — 先砍到只用 analytics+replay，funnel 那 8 个 tab 我用不上还烧钱
- **day 2** (收 1 条, mood: *calm*, engage 7/10) → `DO_NOTHING` — 昨天刚砍到 analytics-only，replay 1 行启用，先跑两天看 MAU 600 够不够
- **day 3** (收 1 条, mood: *calm*, engage 7/10) → `DO_NOTHING` — feature flag 免费够用，A/B 已跑，没必要动配置
- **day 4** (收 1 条, mood: *considering_quit*, engage 4/10) → `/severity high` — $140/月=14个用户，太贵。日常砍到只在launch时开，平时GA+免费层够用
- **day 5** (收 1 条, mood: *done*, engage 3/10) → `UNSUBSCRIBE` — $140/月=14用户，7个产品只用2个，GA+Hotjar够，省下钱给LLM API

**最终判定**:
- 续订: no
- 月费意愿: 5-20
- 最大阻力: $140/月 = 14 个 Highlight Reel 用户。7 个产品我只真用 2 个，剩下 5 个在烧我钱。订阅模型对 indie 不友好，价值/价格曲线第三天就断了。
- 欣赏: Analytics + session replay 这两个组合确实救过我一次 landing page 转化诊断，比纯 GA 看得清。免费层和 BYO 配置思路对独立开发者算友好。
- 原话:
  > tbh 试了 5 天就退了。产品本身不烂，analytics + replay 那两个 tab 真能用，第二天就帮我看出 hero CTA 下面的滚动断点。但 $140/月 = 我 14 个付费用户，而我七个工具里只真用两个，剩下 funnel/heatmap/A-B 那堆 launch 完就吃灰。最致命的是订阅 —— 我宁可 $99 买断也不要每月扣 $140。indie 的钱包逻辑：每一刀都得换回 ARR。砍到 analytics-only 套餐都 $50+ 的话我可能还会回来，现在这样一刀切 bundle 等于强制我替没用的 5 个工具付费。honestly for $15/mo analytics+replay only I'd keep it。已经退了，省下的钱去续 Claude API。

### 06_research_consultant

- **day 1** (收 2 条, mood: *considering_quit*, engage 6/10) → `DO_NOTHING` — 才第2天，SDK装好了funnel还没建，先摸清8个tab再说
- **day 2** (收 1 条, mood: *considering_quit*, engage 3/10) → `DO_NOTHING` — 客户访谈录像绝不能上云，session replay 直接踩隐私红线
- **day 3** (收 1 条, mood: *calm*, engage 4/10) → `DO_NOTHING` — A/B 测试与我的咨询交付无关，且仍未解决本地部署/隐私问题
- **day 4** (收 1 条, mood: *considering_quit*, engage 2/10) → `UNSUBSCRIBE` — 客户访谈数据不能上云，4天没解决本地部署，付费没意义

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 客户访谈数据涉及 NDA 和录音 transcript，4 天没看到任何 local-first 或 on-prem 部署选项，云端 SaaS 形态从根本上不适用于咨询场景。
- 欣赏: hypothesis 生成的角度还算有启发，作为项目立项前的 brainstorm 替代品有潜力，能省下几小时从零脑暴的时间。
- 原话:
  > I see two use cases here, but only one is safe. As a leverage tool for hypothesis generation before client interviews — promising, could save me half a day of solo brainstorming. As anything that touches actual client transcripts or recordings — absolutely not, and they don't offer local deployment. Five days in, the product kept pushing session replay, A/B testing, funnel analytics — none of which map to consulting workflows. The privacy posture is a non-starter for anyone under NDA. If they ship a local-first or self-hosted option I'd retest. Until then it's a PM tool dressed up as a research tool. Skip.

### 07_oss_maintainer

- **day 1** (收 2 条, mood: *curious*, engage 7/10) → `DO_NOTHING` — Day1 装 SDK 体验顺，self-host 路径已确认，先观察 Insight UI 学习曲线
- **day 2** (收 1 条, mood: *curious*, engage 6/10) → `DO_NOTHING` — self-host 路径已确认，session replay 先观望，不急着开
- **day 3** (收 1 条, mood: *calm*, engage 5/10) → `DO_NOTHING` — feature flag 是 SaaS 玩具,我维护 OSS 库不需要 A/B 测 hero copy
- **day 4** (收 1 条, mood: *calm*, engage 4/10) → `/profile self-host` — $140/月+SaaS锁定，self-host PostHog本来就是OSS维护者的默认路径
- **day 5** (收 2 条, mood: *calm*, engage 4/10) → `/profile self-host` — OSS维护者本能选self-host，$140/月+SaaS锁定违背原则

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: $140/月 SaaS 锁定 + 推送内容偏 SaaS 玩具（feature flag、session replay、hero copy A/B），完全不是 OSS 维护者的语境
- 欣赏: self-host 路径真实可跑，不依赖任何 cloud service；SDK 装上 Day1 就顺；core/ 抽象比预期干净
- 原话:
  > 5 天试用结论：personalab 作为 OSS 库本身还行——self-host 完整可跑，pyproject.toml 没有 100 个 transitive deps，core/ 抽象读起来不脏。但它的 SaaS 推送策略完全跑偏：7 条里塞 feature flag A/B、session replay、hero copy 优化，这是给 growth PM 的玩具，不是给维护者的工具。$140/月更是直接劝退——同价位我自己 docker-compose 拉一个就完了。我会 star，会在 newsletter 里推给我那 50+ founder 订户（他们才是付费目标），但我自己永远 self-host。建议作者把 OSS 和 SaaS 文案彻底分流，别用同一套 onboarding 喂两种人。examples/signalstream/ 那个目录也建议删掉或重命名，看着像加密产品 fork。

### 08_ai_safety_skeptic

- **day 1** (收 2 条, mood: *curious*, engage 6/10) → `DO_NOTHING` — Day 1 仅观察；先评估数据流与 prompt injection 面，再决定配置
- **day 2** (收 1 条, mood: *considering_quit*, engage 4/10) → `DO_NOTHING` — session replay 涉及 PII 与第三方持有，需先评估合规与数据流再启用
- **day 3** (收 1 条, mood: *calm*, engage 4/10) → `DO_NOTHING` — A/B 推送与我的 AI safety 关注无交集；继续观察 prompt injection 面
- **day 4** (收 1 条, mood: *calm*, engage 4/10) → `DO_NOTHING` — 成本与我的 alignment/隐私担忧无关；账单页不解决 prompt injection 与数据流问题
- **day 5** (收 2 条, mood: *done*, engage 2/10) → `UNSUBSCRIBE` — 五天无任何隐私/注入面回应；继续使用即默许

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 五天推送零字提及 prompt injection、数据流、第三方 logs 留存；persona md 作为输入面完全没有防御层讨论，作者似乎不把 AI safety 当一等问题。
- 欣赏: 把'让 LLM 扮演用户跑产品决策'这件事产品化，至少给了 AI safety 社区一个可解剖的、representative 的 case study——批评它需要它先存在。
- 原话:
  > Spent 5 days with personalab. The premise—synthetic users as a product-research surrogate—is exactly the kind of tool that normalizes AI-mediated decisions without real humans in the loop, and that's the structural concern, not a feature gap. Three unresolved failure modes after a week: (1) RLHF sycophancy bias softens 12 personas into 12 variants of 'interesting but…', hiding fat-tail objections; (2) persona markdown is an untrusted input surface with no visible prompt-injection defense; (3) transcripts ship to third-party LLM APIs with no data-flow disclosure I could find. Jury mode using three Anthropic models isn't cross-vendor—it's an echo chamber with extra steps. I'd recommend this tool only if used alongside, not instead of, real user research, and only after the author publishes a threat model. Until then I'd rather fork it and add a red-team suite than pay for it. Writing it up on LessWrong.

### 09_corporate_pm

- **day 1** (收 2 条, mood: *considering_quit*, engage 4/10) → `DO_NOTHING` — Day 1 评估期，先看合规与企业能力再决定，不急着配置
- **day 2** (收 1 条, mood: *annoyed*, engage 3/10) → `DO_NOTHING` — 推送内容跑题（PostHog 非 personalab），且企业合规未解，不动
- **day 3** (收 1 条, mood: *annoyed*, engage 3/10) → `DO_NOTHING` — 推送又跑题PostHog，与personalab企业合规评估无关，继续观望
- **day 4** (收 1 条, mood: *done*, engage 2/10) → `UNSUBSCRIBE` — 推送全是PostHog跑题，与personalab企业合规评估无关，弃用

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 推送5条全跑题PostHog，与personalab无关；更致命的是无SOC2/GDPR/SSO/audit log，procurement与法务第一关就毙，企业根本无法采购。
- 欣赏: ABMode对4版本×cohort测试场景天然契合，本地跑不上传用户数据这点对compliance友好，理论上可把UserTesting的两个月压缩到两周。
- 原话:
  > Before evaluating procurement, we'd need to see SOC2 Type II、GDPR DPA、SSO/audit log、至少3个Fortune 500 reference logos，以及calibration r²或同行成功案例——目前一个都没有。产品方向（ABMode + 本地跑）我们公司其实很想要，能压缩upsell wording测试周期。但5天试用收到的5条推送全在讲PostHog，跟personalab自身能力无关，连产品团队自己都没在认真run这个channel。个人卡$0试用尚可，进我们采购流程最低$20-50k/年起，目前条件不具备，一票否决。等他们拿到企业合规材料和参考客户再聊。

### 10_no_code_user

- **day 1** (收 2 条, mood: *annoyed*, engage 2/10) → `UNSUBSCRIBE` — 看到 SDK 要嵌 JS + 8 个 tab 的 funnel 界面，立刻劝退，我只想 paste 邮件拿反馈

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: Day 1 就让我嵌 JS SDK + 看 8 tab 的 funnel dashboard，我是 marketing 不是 dev，连 demo 都没体验到就被技术栈劝退，根本不是给我这种人用的产品 😩
- 欣赏: 理念真的好 —— AI 模拟 6 种人格预测我的 onboarding 效果，这正是我想要的；如果有 web playground 让我 paste 邮件就出报告，我立刻付 $99
- 原话:
  > ok so I tried personalab for like a day and honestly? the IDEA is amazing — imagine getting feedback from 6 different user personas on your onboarding emails BEFORE you send them?? 🤯 but the second I opened it they wanted me to install an SDK and embed JS into my funnel and I was like…. babe. I write copy in Notion. I'm not touching code 😭 there's literally no way to just paste my emails and get a verdict. felt 100% built for devs, not for marketers like me. unsubscribed day 1. if they ever ship a 'drag your URL / paste your copy' web version I'd pay $50/mo tomorrow but until then it's a hard no from the no-code girlies ✌️

### 11_data_team_lead

- **day 1** (收 2 条, mood: *curious*, engage 6/10) → `DO_NOTHING` — SDK 跑通了，但还没看到 stats rigor 和 calibration，先观察 funnel 再判
- **day 2** (收 1 条, mood: *calm*, engage 4/10) → `DO_NOTHING` — session replay 是定性数据，与我要的 stats rigor / calibration 无关
- **day 3** (收 1 条, mood: *calm*, engage 4/10) → `DO_NOTHING` — feature flag 与我要的 stats rigor / calibration 无关，继续观望
- **day 4** (收 1 条, mood: *considering_quit*, engage 3/10) → `UNSUBSCRIBE` — 无 deterministic seeding/Cohen's kappa/calibration plot，stats rigor 不达标，回 in-house

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 无 deterministic seeding、无 Cohen's kappa、无 calibration plot；persona = .md text 不具可重复性，Anthropic 3 模型不算 cross-validation，stats rigor 完全不达标。
- 欣赏: Stats mode 重复 N 次 + CI95 的思路方向是对的，calibration framework 概念上有学术价值，是唯一不会被我直接鄙视的部分。
- 原话:
  > Tried personalab for 5 days as a potential addition to our offline eval pipeline. Conceptually interesting — stats mode with CI95 and a calibration scaffold show the authors have read the right papers. But the methodology is not publishable or sellable to data-driven teams as-is: persona files are free-form .md (no deterministic seeding, no version pinning, temperature not locked), so reproducibility is unverifiable. The 'multi-LLM jury' is three Anthropic models — that's not cross-architecture validation, and there's no Cohen's kappa reported. top_friction is unstructured free text, and ActionLoopReporter still buckets by keywords instead of embedding clustering (HDBSCAN/UMAP). I'd recommend tightening the methodology — deterministic seeding, cross-vendor jury with IRR, auto-generated calibration plots, tagged categorical outputs — before this is ready for serious evaluation work. Back to in-house for now.

### 12_designer_lead

- **day 1** (收 2 条, mood: *curious*, engage 6/10) → `DO_NOTHING` — 刚装完SDK，8个tab的界面像IRC客户端，先消化再说
- **day 2** (收 1 条, mood: *curious*, engage 6/10) → `DO_NOTHING` — session replay 听着像金矿，但 IRC 风界面还没消化完，先观望
- **day 3** (收 1 条, mood: *calm*, engage 5/10) → `DO_NOTHING` — feature flag不是我设计师的菜，但PostHog比LD便宜这点mark一下
- **day 4** (收 1 条, mood: *considering_quit*, engage 5/10) → `/coin analytics-only` — flag用不上，replay是金矿，砍掉省钱保核心
- **day 5** (收 2 条, mood: *calm*, engage 7/10) → `/coin analytics-only` — replay+funnel救过我，HogQL和7产品我用不上，保核心砍杂项续费

**最终判定**:
- 续订: maybe
- 月费意愿: 20-50
- 最大阻力: Markdown 报告像 1998 IRC 客户端，截图给 stakeholder 看不专业；persona 全是文字没头像没 quote card，design review 不能直接展示
- 欣赏: Session replay + funnel 是真金矿——比 Maze 等 72h 快，比 UserTesting $1500 便宜。第 5 天救过我一次，让我看到 version B 的 hover 路径完全断了
- 原话:
  > The idea is gorgeous but the experience feels like a 1998 IRC client. Replay 和 funnel 真的能用，我跑 ABMode 比 Maze 快 70 倍、比 UserTesting 便宜 30 倍，这是核心价值。但报告输出是 git log 风格的 markdown，我没法 screenshot 进 Figma 给 stakeholder 看——persona 没头像、没 quote card、没 tag cloud，全是 wall of text。HogQL 和 feature flag 这些我用不上，砍掉。我会留 analytics-only 档继续观望，但不会推给 design community——除非他们出 Figma plugin + visual report + persona portrait，那一天我会写 Medium 长文吹爆。现在？只能算 promising beta。

