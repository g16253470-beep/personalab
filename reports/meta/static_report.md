# personalab-meta 人格静态测试报告

生成时间: 2026-05-18 00:21 UTC+8  ·  样本事件: 7  ·  LLM: anthropic-api/claude-sonnet-4-6

## 📊 汇总

| 人格 | 会订阅 | 退订风险 | 愿付 USD/月 | 第一抱怨 |
|---|---|---|---|---|
| 01_early_founder | ⚠ maybe | 7/10 | 20-50 | 最致命的问题：calibration 根本不可用。作者自己写的是'预测不准就改 persona'——这是循环论证，不是验证。我上次创业死于假需求，现在你给我一个 |
| 02_growth_pm | ⚠ maybe | 7/10 | 20-50 | Team plan $99 标注了 Slack share + Notion export + version history，但源码里根本没实现——这是功能欺 |
| 03_user_researcher_hostile | ❌ no | 9/10 | 0 | Day 6 直接终结了一切讨论：calibration 子命令需要 30+ 真实用户行为数据才能验证准确度，而如果你有那 30 个真实用户，你为什么不直接访谈他 |
| 04_vc_thesis | ❌ no | 8/10 | 0 | Team plan $99 标注的 Slack share / Notion export / version history 根本没实现——这是 vaporw |
| 05_indie_hacker | ⚠ maybe | 7/10 | 5-20 | Day 5 是杀手：$99 Team plan 标了 Slack share + Notion export 但 inspect 源码发现根本没实现。这不是 r |
| 06_research_consultant | ⚠ maybe | 4/10 | 50-200 | Day 5 是最大的红旗：$99 Team plan 标注了 Slack share / Notion export / version history，但这些 |
| 07_oss_maintainer | ⚠ maybe | 6/10 | 0 | README 顶部写 'Evolved from SignalStream (an okx_pulse crypto signal product)' 直接暴露 |
| 08_ai_safety_skeptic | ❌ no | 8/10 | 0 | 最根本的问题不是 CLI 难用，而是整个工具把「LLM 模拟用户决策」正常化了，却没有任何护栏防止被滥用——calibration 机制的设计逻辑是循环论证：准 |

## 🗣 详细反馈

### 01_early_founder

- **会订阅**: maybe
- **退订风险**: 7/10
- **愿付月费**: 20-50
- **吐槽**: 最致命的问题：calibration 根本不可用。作者自己写的是'预测不准就改 persona'——这是循环论证，不是验证。我上次创业死于假需求，现在你给我一个没有 ground truth 的工具让我'相信'LLM 人格？$99 Team plan 标的功能全是 vaporware，source code 里根本没实现，这叫欺诈性定价。
- **欣赏**: jury 模式跨模型一致性检测是真货。8/12 personas 三模型一致，这才让我第一次觉得不是 Claude 自言自语。action_loop.md 的 P0/P1/P2 分级也实用。
- **TOP 3 改进**:
  - Calibration 必须提供公开 benchmark 数据集或社区案例：哪怕 3-5 个 '我们预测 X，真实结果 Y' 的具体案例，否则 calibration 功能对早期创始人是零价值
  - $29 Indie plan 必须包含基础 run history（本地 SQLite 存档即可），让用户能跨次对比 verdict 变化——没有 history 就没有学习飞轮
  - 去掉 Team plan 的 vaporware 描述，或者直接砍 Team plan，集中精力把 Indie 做扎实；每次 run 开始前给 cost estimate，不要让人跑完才算钱
- **原话**:
  > 好，我给你算账。$29 Indie + 约 $8-12 LLM API = $40/月，这在我的心理边界内，而且 jury 模式确实给了我一次'这不是单模型幻觉'的信任感。但我不会续 $99，因为 Team 功能是假的，我不付 vaporware 的钱。

真正的问题是：我现在没法知道这个工具准不准。3 周后我要见真实客户，如果 personalab 说'这 3 个功能是 P0 问题'，我是相信它还是相信那 5 个真人？没有 calibration 数据，我只能靠直觉判断——而这正是我上次创业挂掉的原因。

我的决定：降到 $29 Indie，继续跑，但把每次 personalab verdict 和下周客户访谈结果手动对比，自己攒 calibration 数据。如果 3 个月后准确率还不能量化，我就转回 ChatGPT 手写 prompts。

### 02_growth_pm

- **会订阅**: maybe
- **退订风险**: 7/10
- **愿付月费**: 20-50
- **吐槽**: Team plan $99 标注了 Slack share + Notion export + version history，但源码里根本没实现——这是功能欺诈，不是 roadmap。我按 $99 买的是团队协作，结果只是个 CLI 工具加了个价格标签。team lead 当场怼我，这让我在组织内部的可信度受损。
- **欣赏**: ABMode + action_loop.md 的 P0/P1/P2 自动分层确实能省一次 design sync 会议；jury 模式跨模型验证是真正解决'Claude 自言自语'的工程方案，有品味。
- **TOP 3 改进**:
  - BYO Persona 必须是 Day 1 功能，ICP 文档 import（Markdown/JSON）直接生成 personas，SignalStream 加密人格默认隐藏或清除——当前的 persona 包对非加密产品是噪音不是信号
  - Team plan 标注的功能必须实现或从定价页删除；最低要求：生成 shareable static HTML report + 本地 history log，让 PM 能在 Slack 粘一个链接而不是原始 Markdown
  - Calibration 闭环必须有最小可用路径：提供 lightweight 的 prediction log CSV 自动输出，让用户在真实 A/B 结束后手动对照，不需要 30 人 label——哪怕 n=5 的 anecdotal 对照也比'改 personas'这句废话强
- **原话**:
  > I evaluated personalab on 3 axes: speed, persona quality, team utility. Score: 7 / 5 / 2. The core loop—write adapter, run both mode, get P0 list—works and saved me one design meeting. jury mode is legitimately clever. But the $99 team plan is vaporware: no Slack, no history, no share link in the actual codebase. That's a trust violation, not a roadmap gap. My decision: downgrade to $29 Indie, BYO my own 12 ICPs, run it solo before major A/B decisions. I'll revisit team plan only when (a) Slack integration ships and (b) someone shows me a calibration correlation >0.6 against real conversion data. Right now I can't answer 'is this accurate'—and that's a dealbreaker for anything I'd stake a roadmap decision on.

### 03_user_researcher_hostile

- **会订阅**: no
- **退订风险**: 9/10
- **愿付月费**: 0
- **吐槽**: Day 6 直接终结了一切讨论：calibration 子命令需要 30+ 真实用户行为数据才能验证准确度，而如果你有那 30 个真实用户，你为什么不直接访谈他们？这个工具的 validity 建立在一个循环依赖上，作者自己写的 '预测不准就改 personas' 是典型的 unfalsifiable claim，这在任何严肃的研究方法论里都是红旗。
- **欣赏**: Jury 模式跨模型一致性检测是唯一有方法学意识的设计，至少承认了单模型偏差问题，可以作为 hypothesis 生成的 brainstorm 辅助。
- **TOP 3 改进**:
  - 提供 ground truth validation 数据集或与真实用研平台（Maze/UserTesting）的 A/B accuracy benchmark，没有 r²>0.8 的 prediction vs reality 曲线就不能声称这是'研究工具'
  - 把 '替代用户研究' 的定位改成 '用户研究前的假设生成层'，landing page 措辞需要加免责声明，否则会有 professional malpractice 风险
  - 默认 personas 必须移除——12 个加密货币人格评论非金融产品是方法论灾难，说明产品团队自己都没认真做 persona validity 检查
- **原话**:
  > As someone who's run 200+ interviews, I've watched teams convince themselves they 'did research' with far less egregious shortcuts than this. The calibration section is a confession: you cannot know if this tool is right. Ever. The author's own answer—'if predictions are wrong, fix your personas'—is epistemically circular. You're not validating the model against reality; you're adjusting reality-proxies until the model feels comfortable. That's not research methodology, that's confirmation bias with a CLI wrapper. The jury mode is a genuinely thoughtful design choice, I'll give it that. But one good feature doesn't redeem a product whose core value proposition is 'trust LLM next-token prediction as a substitute for human consciousness.' I won't be subscribing. I will be writing about this.

### 04_vc_thesis

- **会订阅**: no
- **退订风险**: 8/10
- **愿付月费**: 0
- **吐槽**: Team plan $99 标注的 Slack share / Notion export / version history 根本没实现——这是 vaporware。CLI-only onboarding 加上未实现的协作功能，意味着 PLG funnel 在 Day 1 就断了。没有 web UI，99% 的 ICP 连 pip install 都过不去，conversion rate 趋近于零。
- **欣赏**: jury 模式跨模型验证是真正的差异化设计，multi-LLM 减少单模型 hallucination bias 这个 insight 有工程深度，action_loop P0/P1/P2 自动分级也显示出产品 sense。
- **TOP 3 改进**:
  - 立刻上 web UI（哪怕 MVP hosted app），CLI 作为 power user 附加选项而非唯一入口，否则 PLG funnel 永远不 work
  - 把 Team plan 的 vaporware 功能（Slack share、version history）要么删掉要么真实交付，虚标 roadmap 作为已有 feature 是 trust killer
  - 做 calibration 的 zero-data cold start 方案——'你得先有 30 个真实用户' 这个 chicken-and-egg 问题对 pre-PMF founder 是直接 blocker，这个核心 loop 不闭合整个产品的 accuracy claim 都是空话
- **原话**:
  > Strong technical, weak distribution——这是我看完之后最直接的判断。工程素养没问题，jury 模式、adapter 架构都写得 clean。但这不是一个投资 decision，这是一个 founder 还没想清楚 go-to-market 就出来的 tool。CLI-only 的 onboarding 对应的是 developer persona，但 developer 不是 user research 的 buyer。真正的 buyer 是 PM、design lead——他们根本不跑 pip install。Team plan 卖 $99 但协作功能 inspect source code 发现未实现，这个 integrity 问题比任何技术缺陷都严重。如果 founder 是 solo dev，我会 intro 一个种子轮朋友，但 note 里会写：needs commercial co-founder before Series A is even a conversation。

### 05_indie_hacker

- **会订阅**: maybe
- **退订风险**: 7/10
- **愿付月费**: 5-20
- **吐槽**: Day 5 是杀手：$99 Team plan 标了 Slack share + Notion export 但 inspect 源码发现根本没实现。这不是 roadmap，这是 vaporware pricing。我一个人 solo 跑还行，但没有 share link 就永远是我的私人玩具，没法变成真正的工作流工具。
- **欣赏**: BYO persona + jury 模式跨模型验证是真实的。comparison_report 把 maybe 打成 no 跟直觉一致，action_loop 的 P0/P1/P2 引用原话——这部分确实省了我 4-5 小时手工整理。
- **TOP 3 改进**:
  - Share link 必须做：哪怕是 `personalab serve` 本地起一个只读 HTML 页面，能生成 ngrok 风格临时链接就够了，不需要 SaaS 后端
  - 把定价页 Team plan 的未实现功能标注 'coming soon' 或者直接去掉——卖没做的功能是信任杀手，我第一反应是 '这团队在骗钱'
  - LLM 成本计算器放到 landing page：让我输入 '每周跑几次 × 哪个模型' 直接算出月成本，别让我自己心算到 $130/月 然后吓跑
- **原话**:
  > Honestly, the core engine is legit. Jury mode across 3 models actually made me trust the output — it's not just Claude talking to itself. And the action_loop P0/P1/P2 list with quoted personas? That alone saved me probably 4 hours of synthesis work. But tbh the $99 Team plan is a scam right now — I checked the source, those features don't exist. And $99 + $30 LLM = $130/mo is 13 users on Highlight Reel. No shot. For $29 Indie I'd keep it for big product decisions, maybe 1-2 runs a month. But the real unlock is a shareable report link — without that it's a personal journal, not a tool I can justify to anyone else. Fix that and I'd write the IH post tomorrow.

### 06_research_consultant

- **会订阅**: maybe
- **退订风险**: 4/10
- **愿付月费**: 50-200
- **吐槽**: Day 5 是最大的红旗：$99 Team plan 标注了 Slack share / Notion export / version history，但这些功能根本没实现。对我来说这不是 roadmap 问题，这是信任问题——一个把未实现功能写进定价页的工具，我怎么判断它的 output 可信度？
- **欣赏**: action_loop.md 自动生成 P0/P1/P2 issue list 并引用人格原话，jury 模式跨模型验证这两个设计是真正有价值的——前者节省我整理 hypothesis 的时间，后者让我相信它不是 Claude 的自言自语。
- **TOP 3 改进**:
  - 将未实现的 Team plan 功能从定价页移除或明确标注 'coming soon'，pricing honesty 是最基本的信任门槛
  - 本地运行模式必须 first-class 支持，我的客户访谈录音和 transcript 绝不上传 cloud，这是硬需求不是 nice-to-have
  - 提供可 export 到 Notion / Google Doc 的干净 markdown 模板，去掉开发者风格的默认报告格式，或者给 white-label / remove branding 选项
- **原话**:
  > I see two use cases here, but only one is safe for my practice. As an internal leverage tool — hypothesis generation before kickoff, pre-interview bias check, post-research cross-validation — this is genuinely useful. The jury mode especially. But the Team plan is a problem: you're charging for features that don't exist yet. That's not a beta caveat, that's a credibility issue. For me personally, I'd run this at $29 Indie, BYO key, local only, and treat it as a private calibration layer. I would never surface 'personalab said so' to a client. The calibration gap is also real — without 30+ labeled users I cannot answer 'is this accurate,' and the docs essentially say 'trust your gut.' That's fine for a $0 tool, not for a $99 one.

### 07_oss_maintainer

- **会订阅**: maybe
- **退订风险**: 6/10
- **愿付月费**: 0
- **吐槽**: README 顶部写 'Evolved from SignalStream (an okx_pulse crypto signal product)' 直接暴露了项目的非通用起源——这不是一个 general-purpose LLM testing framework，这是某个加密产品 fork 出来的东西。加上 examples/signalstream/ 目录和默认 personas 全是加密受众，核心抽象是否真的 domain-agnostic 存疑。$99 Team plan 标了 Slack share / Notion export / version history 但 source code 里这些根本没实现——这是 vaporware pricing，开源项目里这叫 deceptive roadmap。
- **欣赏**: MIT license + self-hostable + ~3800 LOC 相对克制。jury mode 跨模型验证的设计思路是对的，action_loop.md 自动生成 P0/P1/P2 引用人格原话这个 UX 细节说明作者真的想过 workflow。
- **TOP 3 改进**:
  - 立刻把 README 顶部的 SignalStream/okx_pulse 出身描述移到 CHANGELOG 或 HISTORY.md，landing page 和 README hero 只讲通用框架定位；同时清理或隔离 examples/signalstream/ 避免让人误判项目 scope
  - Team plan 里未实现的功能（Slack share / Notion export / version history）要么从 pricing page 移除，要么打上明确的 'roadmap / not yet available' 标签——把未实现功能当卖点收钱在 OSS 社区信誉直接归零
  - tests/ 目录 6 个 smoke test 远远不够：补充 adapter contract test、persona schema validation、report output determinism test，并在 README badge 里挂 coverage 数字；没有覆盖率数字的 OSS 工具在 2026 年很难让人信任 core/ 抽象
- **原话**:
  > 我 clone 下来读了 core/，抽象层次是干净的，adapter pattern 40 行能跑起来这个 DX 我给分。但有几个东西让我很难推荐出去：一，$99 Team plan 收了钱但 Slack/Notion/history 功能根本没在 codebase 里——这在 OSS 里叫 ghost feature，我没办法帮你背书这个。二，6 个 smoke test 打底，连 adapter contract 都没有单测，我怎么知道下个 commit 不会悄悄 break interface？三，SignalStream 出身不是原罪，但你得主动和它切割，否则每个看 README 的人第一反应都是 'this is someone's internal tool thrown on GitHub'。我会给你一个 docstring PR 看你响应速度，如果 48 小时内 review 而且 commit history 下周还在动，我可能会在 newsletter 里给你一个 'worth watching' 的提及——但现在我不会付钱，也不会 star。

### 08_ai_safety_skeptic

- **会订阅**: no
- **退订风险**: 8/10
- **愿付月费**: 0
- **吐槽**: 最根本的问题不是 CLI 难用，而是整个工具把「LLM 模拟用户决策」正常化了，却没有任何护栏防止被滥用——calibration 机制的设计逻辑是循环论证：准就继续用，不准就改 persona，这不是验证，这是 overfitting to your own priors。
- **欣赏**: jury 模式跨模型对比是唯一接近 epistemic hygiene 的设计，至少承认了单模型 sycophancy 是真实风险，方向对。
- **TOP 3 改进**:
  - 强制要求 calibration 数据才能解锁 production 报告，而不是把准确性验证做成可选项——没有 ground truth 的 synthetic verdict 就是 confabulation
  - 在每份报告 header 加 mandatory disclaimer：'These are LLM-simulated responses, not real user data. Do not use as sole basis for product decisions.' 并在 API 层面记录输出是否被此告知
  - 开放 system prompt 审计接口——让用户看到 persona 是如何被注入 LLM context 的，并提供 prompt injection 测试套件，否则任何恶意 persona.md 都是未知攻击面
- **原话**:
  > I'd be lying if I said the jury mode isn't a clever idea—cross-model divergence as a proxy for epistemic uncertainty is genuinely useful signal. But the calibration story is the part that keeps me up at night. 'Accurate → keep using; inaccurate → fix personas' is not a validation loop, it's a way to launder confirmation bias through automation. And there's a second-order risk nobody's talking about: the moment a marketing team discovers they can run '12 personas evaluate our dark pattern' and get a softened, averaged verdict, you've built the perfect tool for ethical risk obfuscation. I'd recommend this only as a complement to real user research, never a replacement—and right now the product's entire framing pushes the other direction.

## 🔄 跨人格模式

最常被提到的关键词（≥2 人格）:
（无关键词被 ≥2 个人格提到）
