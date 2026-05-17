# calcom Agentic 行为仿真报告

生成: 2026-05-18 02:06 UTC+8 · 仿真 5 天 · 12 个人格 · 事件: 5 · LLM: claude-cli

## 📊 汇总

| 人格 | 完成天数 | 退订日 | 累计收到 | 最终 | 月费 | 推荐? |
|---|---|---|---|---|---|---|
| 01_early_founder | 5/5 | - | 5 | ❌ no | 0|5-20 | ❌ |
| 02_growth_pm | 5/5 | 5 | 5 | ❌ no | 0 | ❌ |
| 03_user_researcher_hostile | 2/5 | 2 | 2 | ❌ no | 0 | ❌ |
| 04_vc_thesis | 5/5 | - | 5 | ❌ no | 0 | ❌ |
| 05_indie_hacker | 5/5 | - | 5 | ❌ no | 0 | ✅ |
| 06_research_consultant | 5/5 | - | 5 | ❌ no | 0 | ❌ |
| 07_oss_maintainer | 5/5 | - | 5 | ❌ no | 0 | ❌ |
| 08_ai_safety_skeptic | 5/5 | - | 5 | ❌ no | 0 | ❌ |
| 09_corporate_pm | 4/5 | 4 | 4 | ❌ no | 0 | ❌ |
| 10_no_code_user | 5/5 | - | 5 | ❌ no | 0 | ❌ |
| 11_data_team_lead | 5/5 | 5 | 5 | ❌ no | 0 | ❌ |
| 12_designer_lead | 5/5 | 5 | 5 | ❌ no | 0 | ❌ |

## 🎬 每人格行动序列

### 01_early_founder

- **day 1** (收 1 条, mood: *curious*, engage 6/10) → `/profile free` — 先白嫖验证流程，$12/seat不值，钱要留给真访谈
- **day 2** (收 1 条, mood: *calm*, engage 6/10) → `/profile free` — 客户已预约，branding没挡路；$12/seat不值，钱留给真访谈
- **day 3** (收 1 条, mood: *calm*, engage 6/10) → `/profile free` — workflow是nice-to-have，$12/seat还是不值，钱留给真访谈
- **day 4** (收 1 条, mood: *annoyed*, engage 3/10) → `/profile free` — $60/月给sales工具不值，钱留给真客户访谈
- **day 5** (收 1 条, mood: *calm*, engage 6/10) → `/profile free` — Free够用,$12/seat不值,钱留给真客户访谈

**最终判定**:
- 续订: no
- 月费意愿: 0|5-20
- 最大阻力: 5 天 5 条推送全是 sales 工具升级话术，没有一条给我 calibration 证据：12 个 persona 的预测 vs 真实用户行为对照在哪？没有这个我不敢付费
- 欣赏: Free tier 真能跑 persona 压测，不强制升级；产品没把我当傻子，至少让我先用起来验证流程，这点比大多数 SaaS 良心
- 原话:
  > Tried personalab for a week before my customer interviews. TL;DR: free tier is genuinely usable, paid tier I don't trust yet. The 12 personas thing sounds great on paper—stress test your pitch before real users tear you apart. But after 5 days of upsell pushes I still have zero evidence the persona feedback predicts real user behavior. Where's the calibration data? 'LLM pretending to be my ICP' is exactly the failure mode that killed my last startup. At $12/seat I'd need to see 'past N predictions vs actual outcomes' before signing. Until then it's $1.5/run roleplay theater, not a research tool. Staying on free, spending the $300 on 5 real interviews next week. Talk to me again when you ship a track record.

### 02_growth_pm

- **day 1** (收 1 条, mood: *curious*, engage 7/10) → `DO_NOTHING` — Day 1 just landed; need to test ABMode before committing budget
- **day 2** (收 1 条, mood: *considering_quit*, engage 5/10) → `DO_NOTHING` — 客户已订上，branding 是噪音；先看 ABMode calibration 再决定付费
- **day 3** (收 1 条, mood: *annoyed*, engage 4/10) → `DO_NOTHING` — Cal.com 噪音，等 ABMode calibration 数据再决定
- **day 4** (收 1 条, mood: *annoyed*, engage 4/10) → `DO_NOTHING` — Cal.com 跟我核心 ABMode 验证无关；等 calibration 数据
- **day 5** (收 1 条, mood: *done*, engage 2/10) → `UNSUBSCRIBE` — 5天全是Cal.com噪音，ABMode calibration数据从未来过，核心钩子未验证

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 连续5天推送全是Cal.com无关噪音，ABMode calibration数据零交付，核心钩子从未验证；BYO persona和Amplitude对接更是无影。
- 欣赏: 12 personas + ABMode的概念本身击中我的痛点——A/B前预演conversion impact，理论上能砍掉一半失败实验。仅此而已。
- 原话:
  > I evaluated personalab on 3 axes: speed 6, quality 3, ICP fit 2. 概念是真的诱人——12 personas替我预演A/B、ABMode自动diff两版pricing page、报告直接生成P0 issue list——作为增长PM我愿意为这个掏$99/月。但5天试用我收到5条推送，5条全是某个Cal.com客户的branding流水，ABMode的calibration数据一次都没出过，跟我用例的相关性约等于零。SignalStream那12个加密人格对signed-up SaaS users的场景完全无用，BYO persona没影、Amplitude/Mixpanel集成没影、prediction vs真实conversion的对照没影。核心钩子一个都没验证，已退。等他们做出calibration数据再说，现在连$5都不值。

### 03_user_researcher_hostile

- **day 1** (收 1 条, mood: *annoyed*, engage 2/10) → `DO_NOTHING` — Cal.com 跟我职业无关，推送本身就是噪音；先观察这工具的信噪比
- **day 2** (收 1 条, mood: *done*, engage 1/10) → `UNSUBSCRIBE` — Cal.com 推送与我的UX研究业务无关，第2条噪音已足够，无ground truth价值

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 无 ground truth validation，无 r² 校准曲线，方法学站不住。LLM 做 next-token prediction，不是模拟用户意识，把这玩意当研究依据是 professional malpractice。
- 欣赏: 作为 brainstorm 工具问"我们漏掉哪个 segment"勉强可用。仅此而已，绝不能作为决策依据，且必须配真用户访谈做二次验证。
- 原话:
  > As someone who's run 200+ user interviews across 8 years at FAANG: synthetic users are professional malpractice. 试用 personalab 两天，收到的全是 Cal.com 推送噪音——连 onboarding 都没搞清楚我是 UX researcher，更别提它的 persona 输出能否对得上真实人类行为。没有 calibration report，没有 prediction vs ground truth 的 r² 曲线，没有任何方法学透明度。Jakob Nielsen 不会签字，Steve Krug 不会签字。最危险的不是它输出错答案，而是它输出 plausible-sounding 错答案——你甚至不知道它错在哪。RLHF politeness bias 让 12 个 persona 趋同成一个 LLM 声音。$99/月？procurement 会把它归类成 Slack 备忘录。我会写一篇 Medium 把它列为 2026 反面案例。Use it for hypothesis generation, then validate with real humans. 单独买？$0。

### 04_vc_thesis

- **day 1** (收 1 条, mood: *curious*, engage 6/10) → `DO_NOTHING` — Day 1 just landing page recon; need to see retention cohort + GTM motion before any commit.
- **day 2** (收 1 条, mood: *calm*, engage 4/10) → `DO_NOTHING` — Cal.com is ops noise, not my deal thesis. Branding is non-issue at this stage; keep watching, no spend.
- **day 3** (收 1 条, mood: *calm*, engage 2/10) → `DO_NOTHING` — Cal.com推送跟我的deal thesis无关,继续观察personalab自身指标
- **day 4** (收 1 条, mood: *calm*, engage 2/10) → `DO_NOTHING` — Cal.com 是 ops 噪音，跟我的 deal thesis 无关，继续观察 personalab
- **day 5** (收 1 条, mood: *calm*, engage 2/10) → `DO_NOTHING` — Cal.com是ops噪音,跟我的deal thesis无关,继续观察personalab

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 5 天 5 条推送全是 Cal.com ops 噪音，零产品 metric、零 cohort 数据、零 GTM 信号。CLI-only 没 web UI，PLG 根本跑不通。
- 欣赏: Framework 工程素养 clean，能看出 founder 技术功底；persona simulation 思路 directionally correct，作为 pre-seed feasibility check 工具有价值。
- 原话:
  > Strong technical, weak distribution. 跟了 5 天，推送全是 Cal.com 这种 ops 噪音，没看到任何 retention cohort 或 ARR signal——说明 founder 还在 build mode，没进入 GTM。CLI + pip install 的 onboarding 在 PLG 漏斗顶端直接 99% 流失，$99/mo 想做到 $5M ARR 要 4200 客户，数学不成立。Moat 也存疑：Anthropic 哪天上个 AI focus group feature 就秒了。赛道里 Maze 已经 $50M、UserTesting 上市，incumbent 抓 80% 市场，long-tail 留给 LLM 工具最多 $50M/年。Pre-seed only if founder commits full-time + 找个 commercial co-founder。我个人不会订阅，portco 有需要的话可以聊 enterprise license bundled with onboarding 支持。Pass for now，保持观察。

### 05_indie_hacker

- **day 1** (收 1 条, mood: *calm*, engage 6/10) → `/profile free` — tbh $12/seat 不划算，先免费吃 branding 看 booking 量再说
- **day 2** (收 1 条, mood: *calm*, engage 6/10) → `DO_NOTHING` — 客户还是预约了，branding 不致命，先观察几次再决定要不要 self-host
- **day 3** (收 1 条, mood: *considering_quit*, engage 4/10) → `DO_NOTHING` — workflows要$12/seat=1.2个用户，先继续吃Free，branding还没真痛到要付钱
- **day 4** (收 1 条, mood: *considering_quit*, engage 4/10) → `/coin self-host` — $60/月=6个用户，肉疼。我会维护Docker，自建省钱还能改
- **day 5** (收 1 条, mood: *calm*, engage 7/10) → `/coin self-host` — 昨天已决定自建，今天落地Docker，省$60/月=6用户，能改能审

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: $12/seat订阅模式不make sense，跑5次没产生一个真landing page改动决策，5天我都在算成本不在用产品，最后干脆自建省$60/月
- 欣赏: BYO persona + FakeLLM本地跑想法不烧钱，开源CLI Python我能改能审，self-host路径是真的存在不是PPT
- 原话:
  > tbh personalab 的核心想法我很喜欢 —— BYO persona + 本地 FakeLLM 跑 smoke test，这正是 indie hacker 需要的。但订阅定价完全错位：$12/seat 对我等于一个 Highlight Reel 用户，5 天试下来没产生一个真实的 landing page 改动决策，我凭啥付？最后第 4 天我就决定自建 Docker，第 5 天落地，省 $60/月 = 6 个用户的 MRR。honestly 这产品该卖 $99 lifetime license 而不是 SaaS 订阅，indie 用户买断会爽快得多。for $15/mo 我不会续，但开源 self-host 我会一直用，也会写一篇 indie-hackers 帖子推荐 —— 别为 hosted 付钱，自己跑。给团队的建议：把 adapter 那 40 行模板化，给个 share 链接功能，然后认真考虑 lifetime license。

### 06_research_consultant

- **day 1** (收 1 条, mood: *considering*, engage 6/10) → `DO_NOTHING` — Day 1 仅看 landing，需先评估隐私与本地化再决策
- **day 2** (收 1 条, mood: *considering_quit*, engage 5/10) → `DO_NOTHING` — Branding 是问题但客户已预约，先观察实际反馈再决策
- **day 3** (收 1 条, mood: *considering_quit*, engage 4/10) → `DO_NOTHING` — 隐私与品牌仍未解，先观察 workflow 实际价值
- **day 4** (收 1 条, mood: *considering_quit*, engage 4/10) → `DO_NOTHING` — 隐私/品牌未解，推团队前先自己再验一轮
- **day 5** (收 1 条, mood: *considering_quit*, engage 4/10) → `DO_NOTHING` — 隐私/白标未解，单人吃 branding 不爽，再观望

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 隐私与本地化未确认前不敢喂客户访谈数据；默认品牌外露，无 white-label，无法夹进 $45k deliverable
- 欣赏: 立项阶段批量生成 hypothesis 的脑暴效率确实省 4-6 小时，作为内部 pre-interview brief 工具方向是对的
- 原话:
  > Five days in and I'm not subscribing—yet. There are two use cases here, but only one is defensible. As a private leverage tool for hypothesis generation before client interviews, it genuinely saves me half a day of solo brainstorming. As anything that touches actual client transcripts or shows up in a deliverable, it's a non-starter until they ship first-class local execution and a white-label export. Right now the branding screams 'dev tool,' the privacy story is unclear, and the 'recommendations' occasionally argue against judgment calls I've already validated in real interviews. I'll revisit when local mode and white-label land. Until then I'd rather eat the 6 hours than risk a client finding LLM-simulated personas in my $45k report. As a leverage tool, maybe. As primary research, no.

### 07_oss_maintainer

- **day 1** (收 1 条, mood: *curious*, engage 7/10) → `/coin self-host` — OSS维护者本能：能self-host就不吃branding，Docker我熟
- **day 2** (收 1 条, mood: *calm*, engage 7/10) → `DO_NOTHING` — self-host Docker还没起，先把容器跑通再说，branding不是我痛点
- **day 3** (收 1 条, mood: *calm*, engage 6/10) → `DO_NOTHING` — Docker容器还在调，self-host没跑通前不评价产品本身
- **day 4** (收 1 条, mood: *calm*, engage 5/10) → `DO_NOTHING` — Docker还没跑通就别推销售队，self-host不验证完不掏团队钱
- **day 5** (收 1 条, mood: *considering_quit*, engage 4/10) → `/coin self-host` — Docker五天还没跑通就该今天搞定，self-host是我唯一会用的形态

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: self-host Docker 五天没跑通，README 缺最小 docker-compose 示例；examples/signalstream/ 业务感太强像加密产品 fork，core/ 抽象边界不清。
- 欣赏: license 不是 AGPL、能完整 self-host 不绑 cloud、pyproject.toml 依赖没失控，core/ 单独读还算干净，作者 commit 节奏在持续。
- 原话:
  > Spent 5 days kicking the tires on personalab — an OSS-friendly memory/agent framework out of the SignalStream lineage. Good news: MIT-ish, fully self-hostable, no mandatory cloud, pyproject is clean. Bad news: I still don't have it running in Docker after 5 days. There's no first-class docker-compose in the README, the examples/ dir leans heavily on a signalstream/ folder that reads like a crypto product fork, and core/ has a few abstractions whose 'why' isn't documented anywhere. Author is committing daily which is the only reason I haven't unstarred. I'm not paying — OSS infra should be free — and I won't push it to my newsletter until the self-host story is one `docker compose up` away and the examples stop looking like someone's day job. Watching, not endorsing. Will revisit in 2 weeks; if quickstart isn't fixed by then, quiet unstar.

### 08_ai_safety_skeptic

- **day 1** (收 1 条, mood: *curious*, engage 5/10) → `DO_NOTHING` — Day 1 仅评估 surface；先观察使用模式与数据流再决定。
- **day 2** (收 1 条, mood: *curious*, engage 5/10) → `DO_NOTHING` — Day 2 仍在观察 data flow 与 third-party trust model，未到决策点。
- **day 3** (收 1 条, mood: *calm*, engage 4/10) → `DO_NOTHING` — Day 3 推送是 Cal.com 选型，与我的 AI safety 关切无关；继续观察 data flow 与 prompt 透明度。
- **day 4** (收 1 条, mood: *calm*, engage 4/10) → `DO_NOTHING` — Cal.com 选型与我的 alignment/misuse 关切无关，继续观察 data flow 与 jailbreak 面。
- **day 5** (收 1 条, mood: *calm*, engage 4/10) → `DO_NOTHING` — Cal.com 选型与 AI safety 关切正交；继续观察 personalab 本体的数据流与 injection 面。

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 5 天推送全是 Cal.com 选型琐事，没看到 prompt injection 防御、数据留存策略、jury 跨厂商化等结构性问题的任何动静。
- 欣赏: 把 persona 显式建模、留下可审计的 trace，这个 artifact 本身比黑箱式 A/B 工具更适合做 red-team 研究对象。
- 原话:
  > Five days in, personalab feels like a clever artifact pointed at the wrong layer of the problem. 12 personas through Claude evaluating a product written with Claude is a closed loop — RLHF sycophancy will smooth the verdicts, fat-tail objections vanish, and cross-vendor jury is still aspirational. Worse, the data flow is opaque: persona markdown plus full product transcripts flow to a third-party API with no documented retention or injection hardening. I can already picture growth teams using this to launder dark-pattern decisions: 'the synthetic users didn't churn.' I'd recommend it only as a brainstorming aid alongside, never instead of, real user research — and only after the author ships a prompt-injection test suite and clarifies the data-retention story. I'll fork and write it up on LessWrong; I won't pay.

### 09_corporate_pm

- **day 1** (收 1 条, mood: *considering_quit*, engage 3/10) → `DO_NOTHING` — Day 1, evaluating compliance & procurement fit before any action
- **day 2** (收 1 条, mood: *considering_quit*, engage 3/10) → `DO_NOTHING` — Still in evaluation; need SOC2/SSO before any procurement move.
- **day 3** (收 1 条, mood: *annoyed*, engage 3/10) → `DO_NOTHING` — 推送内容跟我评估的 personalab 完全无关，且仍卡在 SOC2/SSO 合规前置
- **day 4** (收 1 条, mood: *done*, engage 1/10) → `UNSUBSCRIBE` — 推送全是Cal.com不相关内容，且核心合规阻塞未解，evaluation已死

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 无 SOC2/GDPR/SSO/Audit log，procurement 第一关就死；外加 4 天推送全是 Cal.com 等不相关内容，evaluation 直接崩盘。
- 欣赏: ABMode 对 4-version × cohort 测试场景天然契合，本地运行不上传用户数据，理论上对 compliance 友好。
- 原话:
  > Before evaluating procurement, we'd need to see SOC2 Type II, a GDPR DPA, SSO/SAML, audit logs, and at minimum 3 Fortune 500 reference logos — none of which personalab has today. The ABMode concept and local-execution story are genuinely interesting for upsell wording tests, and on paper it could compress a $15k UserTesting cycle. But the 5-day trial pushed me Cal.com scheduling content that had nothing to do with the product I was evaluating, which killed any remaining signal that this team understands enterprise buyers. For a solo PM or indie founder, maybe worth a look. For anyone reporting to a VP who'll ask 'is this real user data, and is legal okay with it?' — not ready. Revisit in 12-18 months once the compliance and integration story (Salesforce, Looker, Mixpanel) exists.

### 10_no_code_user

- **day 1** (收 1 条, mood: *curious*, engage 7/10) → `DO_NOTHING` — 第一天先看看，邮箱注册了再说，calendar 连接晚点弄
- **day 2** (收 1 条, mood: *considering_quit*, engage 5/10) → `DO_NOTHING` — 客户还是预约了，branding 没真挡到我，先观望
- **day 3** (收 1 条, mood: *considering_quit*, engage 5/10) → `DO_NOTHING` — workflows是nice-to-have，Free还够用，先不花钱也不折腾Docker
- **day 4** (收 1 条, mood: *considering_quit*, engage 4/10) → `DO_NOTHING` — 5人团队 $60/月不便宜，Bookings免费但要折腾，再观望一天
- **day 5** (收 1 条, mood: *calm*, engage 6/10) → `/profile free` — Free够用，branding忍一忍，省钱要紧，等真有团队再升

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 5 天根本没用上 😅 看到 pip install + CLI 我直接懵了，没有 web 入口让我 paste 邮件草稿，Free tier 我也碰不到。门槛 = 我永远不会真的上手。
- 欣赏: concept 真的 brilliant —— AI 用不同人格替我测 onboarding 邮件？这正是我每次发 sequence 前焦虑的事。如果能 5 分钟看到 demo 我立刻付 $50。
- 原话:
  > okay so I tried personalab for a week and honestly?? the idea is *chef's kiss* 👨‍🍳💋 —— AI personas testing your product before real users see it? YES please, this is exactly what I need for my onboarding emails 😍 BUT. it's built for devs. like, pip install, CLI commands, write your persona in markdown with frontmatter?? babe I run my whole business on Webflow + Zapier, I'm not opening a terminal 😭 5 days went by and I literally never used it once. if they ever ship a web playground where I can paste my email draft and get 6 persona reactions, take my $$$ immediately. until then it's a hard no from non-technical founders like me. 🥲 #builtForDevs

### 11_data_team_lead

- **day 1** (收 1 条, mood: *curious*, engage 5/10) → `DO_NOTHING` — 先看 stats mode 和 calibration 再判断，未到付费决策点
- **day 2** (收 1 条, mood: *calm*, engage 5/10) → `DO_NOTHING` — branding 是 UX 噪音，与我评估 stats/calibration 的核心 ROI 无关
- **day 3** (收 1 条, mood: *annoyed*, engage 2/10) → `DO_NOTHING` — Cal.com scheduling 与我评估 LLM stats/calibration 无关，今日推送 noise
- **day 4** (收 1 条, mood: *annoyed*, engage 3/10) → `DO_NOTHING` — Cal.com scheduling 与 LLM 模拟评估无关，等 stats/calibration 数据
- **day 5** (收 1 条, mood: *done*, engage 1/10) → `UNSUBSCRIBE` — 5天推送全是Cal.com scheduling，与我评估的LLM stats/calibration无关，错配产品

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 5 天推送全是 Cal.com scheduling 营销噪音，与我评估的 stats mode、calibration、jury IRR 完全错配，未触及核心 ROI
- 欣赏: Stats mode（N 次重复 + CI95）和 calibration framework 概念上是正确方向，jury 架构思路也对，是少数不会被我当成 prompt loop 鄙视的部分
- 原话:
  > Tried personalab for a week. The stats mode and calibration framework are the only parts I'd take seriously for an offline eval pipeline — everything else is a packaged prompt loop. But after 5 days of onboarding nudges all about Cal.com scheduling, I never saw deterministic seeding, Cohen's kappa across heterogeneous models, or proper calibration plots. Persona-as-markdown isn't reproducible; top_friction as free text isn't ML-processable; keyword bucketing in ActionLoopReporter is 2010-era TF-IDF, should be HDBSCAN over embeddings. I'd recommend tightening the methodology before this is publishable or sellable to data-driven teams. Unsubscribed.

### 12_designer_lead

- **day 1** (收 1 条, mood: *curious*, engage 6/10) → `DO_NOTHING` — 先看产品，Cal.com 跟我做的 design 工具无关，今天只观察
- **day 2** (收 1 条, mood: *calm*, engage 6/10) → `DO_NOTHING` — Cal.com branding 丑但不是我的痛点，还在观察 personalab 本体
- **day 3** (收 1 条, mood: *calm*, engage 4/10) → `DO_NOTHING` — Cal.com 推送跟我的 design review 痛点无关，第3天还在观望 personalab 的 visual report
- **day 4** (收 1 条, mood: *annoyed*, engage 3/10) → `DO_NOTHING` — Cal.com 跟我设计需求无关，4 天推送全跑题，懒得动
- **day 5** (收 1 条, mood: *done*, engage 1/10) → `UNSUBSCRIBE` — 5天全是Cal.com，跟我design review痛点零相关，弃

**最终判定**:
- 续订: no
- 月费意愿: 0
- 最大阻力: 5天5条全是Cal.com，跟我design review的visual report、Figma import、persona portrait痛点零相关，推送系统根本没读懂我是谁。
- 欣赏: ABMode让12 persona给design版本即时反馈的概念很性感，理论上能替代我买不起的UserTesting，但产品没把它端到我面前。
- 原话:
  > The idea is gorgeous but the experience feels like a 1998 IRC client。我是design lead，连续5天收到的全是Cal.com这种开发者工具推送，没有一条提到Figma、visual report、persona portrait——这些才是我会付$99/月的理由。底层多agent verbatim feedback的想法真的能颠覆user research，但他们的推送引擎完全不知道用户是谁，markdown输出像git log，我没法截图给stakeholder看。等他们出Figma plugin + 视觉化report再叫我，现在弃。

