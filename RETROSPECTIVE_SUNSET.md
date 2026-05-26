# personalab — Sunset Retrospective

> 2026-05-26. 项目方向：**封版关停**（hard sunset）。
> 仓库标 archive，autoreply / monitor 计划任务 disable，所有公开 launch anchor 不再维护。
> 这份文档不是营销稿，是写给一年后自己看的诚实复盘。

## 一句话总结

> **9 天里把 framework 做完、case study 做完、三方 audit 都做完、launch 也发完，唯独 manual MVP 卡在「人类按 5 分钟物理键」这一步 8 天没动 — 这本身就是答案。**

---

## 时间线骨架

| 日期 | 事件 |
|---|---|
| 2026-05-17 | 从 okx_pulse `persona_test.py` 抽出独立 framework，命名 personalab |
| 2026-05-18 | v0.2.0 ship + PostHog/Cal.com case study + GitHub/Gist/IH/Reddit/dev.to launch + 三方 audit reject SaaS + 启动 manual-first Gap Discovery 10 天计划 |
| 2026-05-18→22 | OOO 5 天，autoreply bot 全程 0 real action（只拦 1 条 SEO spam + 1 次 SSL timeout）— dev.to 实际 0 评论积压 |
| 2026-05-25 | Gap Discovery Day 1-10 文件全部产出，5 个 HN reply READY_TO_SEND，0 sent |
| 2026-05-26 | Sunset 决策。9 天总产出：3,294 LOC + 3 case study + 16 commits + 0 buyer signal |

---

## 4 个根本错（按权重）

### 1. **Niche 选错了，而我用「文件产出」掩盖了它**（权重 40%）

dev tools 是 personalab 这把工具能用得最熟的 niche（personalab 自己就是 dev tool，personas 也是 dev 友好的）。**但 dev tools 这个 niche 对「LLM persona 测试」需求几乎为零** — 真正的 dev tool 创业者要么自己就是 ICP（直接试自己产品），要么直接发 HN/Reddit 看真人反馈，不需要 LLM 模拟一层。

我用「Day 1 / 2 / 3 / 4 / 5 / 6 / 9 / 10 文件交付」的节奏感掩盖了「这个 niche 没有人想付钱」的本质。**文件 = 进度幻觉**。Codex 在 D-11 已经预警过 "real_buyer_signal 0.20 权重才是决定的"，但我做的 Day 1-10 实际只在 Day 7-8（真 buyer outreach）那两天产生 buyer signal，其它 8 天都是 LLM 自循环。**LLM 自循环越多，对自己产品越自信，越不愿意停下问"有没有人买"**。

### 2. **三方 audit 一致 reject SaaS，我没有真的内化**（权重 25%）

D-10 三方 verdict 写在那里：Claude 🟡、Gemini ❌、Codex 🟡。三个独立模型一致说"不要做 SaaS"。我嘴上接受了，做了 manual MVP，但同一天就写 D-13 把 v1.0 北极星定成 7-level autonomy + W6 self-improvement loop（AUTONOMY_VISION.md 至今还挂着）。

这是**情绪对冲**：reject 太痛 → 立刻给自己画一个更大的饼。"我现在做 manual 是策略，长远还是要做 autonomous"。结果两边都没真的执行：manual 卡 8 天，autonomous gate 永远没解锁。

### 3. **Launch 时机选在 OOO 前一天**（权重 20%）

2026-05-18 launch，5-18→5-22 OOO 5 天。launch 第一周是 organic engagement 黄金窗口，我用 autoreply bot 兜底，但 bot 实际只能反应（reply 评论），不能主动（发新 thread / 回 HN / 跟 IH commenter 私聊）。**launch 周本来就需要人类高频在场**，OOO 把这个窗口烧掉了。

回来后 dev.to 6 天 0 评论，IH 没新 like，HN 没发出，**所有 anchor 进入死水**。这时候再"补"任何动作，cold start 难度 ×3。

### 4. **「manual MVP 心理 friction」我低估了**（权重 15%）

5 个 HN reply 物理上是 5 分钟。准备工作 AI 全做完，targets 选好、文案写好、AI tell 评分过、路径 A/B/C 对比给好、HN URL 一个个贴在 READY_TO_SEND.md 里。然后我**8 天没发**。

为什么？因为 HN reply 是**身份暴露 + 公开成败**。文件交付是"我做了"，HN reply 是"看看会不会有人回我"。这两件事的心理代价不在一个数量级。AI 把所有"做"的成本压到 0，但**身份暴露成本只有人能承担**，AI 帮不上 — 而身份暴露成本恰好是 manual MVP 真正的 gate。

这条对未来项目最有用：**任何 "AI 把准备工作做完，剩下 5 分钟物理操作交给你" 的设计本身就是错的**。如果 5 分钟物理操作能完成，AI 不需要做那么多准备；如果做了那么多准备还卡着，那 5 分钟根本不是物理问题。下次设计 manual MVP 要把"人类身份暴露"当一等公民列入成本表。

---

## 学到什么（带走的东西）

### 框架 / 代码层面
- **6 mode × 4 adapter × 12 persona 这个框架本身能跑**（6/6 smoke pass）。如果未来另一个 niche 用得上 LLM persona 测试，把代码 fork 出来直接用，**不要再叫 personalab**。
- **TODO-1 (persona contamination)** 是真问题，但已经写进 README disclaimer 自首了 — 在 OSS 上"已知问题已自首"的可信度高于"全声明 PMF"。
- **persona-as-rebuttal-not-vote**（D-11）这个 frame 是对的：LLM persona 当反驳器（"找我们没想到的反对意见"）远比当投票器（"算 yes/no 比例"）有用。这个 frame 值得带去任何"LLM 模拟用户"场景。

### 决策机制
- **三方独立 audit（Claude / Gemini / Codex）verdict 一致时，必须立刻砍方向**。我 D-10 拿到 3/3 reject SaaS 没砍方向，是这次最贵的一个迟疑。下次再拿到 3/3 一致负向 verdict，立刻 sunset / pivot，不要"manual MVP 探索"。
- **"文件产出节奏" 不是进度指标**。下次任何项目，进度指标只看 buyer signal（付费 / 真人回复 / signup conversion），不看"今天写了几个 .md"。
- **9 天里写了 16 commits 但没拿到 1 条真人外部反馈，这就是失败**。commit 数 / loc / 文件数都不算。

### 项目运作
- **launch 前不要 OOO 5 天**，废话。
- **AI 兜底不能替代人类在场**，特别是冷启动期。autoreply bot 只能反应不能主动，在 0 inbound 的世界里它是死代码。
- **manual MVP 的设计要先验 5 分钟动作的心理代价**，不要假设"准备工作 AI 做完就万事大吉"。
- **OSS 公开发布前先把 owner 账户最终化**。`g16253470-beep` 账户在 launch 后被改名为 `weiseer`，所有 IH/dev.to/Reddit 文章里的 Gist URL 现在 404，repo URL 301 redirect — 这是 trust 漏点。下次注册账户名要一步到位。

---

## 不带走的东西

- **personalab 这个名字** — 已经有 KTKyle/PersonaLab 和 IV-Archi/PersonaLab 两个同名（虽然 0 star），niche 拥挤，没有继承价值
- **Gap Discovery 10-day MVP 框架本身** — 是 Codex 的 frame，没问题，但跟 personalab 解耦，未来用别的项目套
- **AUTONOMY_VISION.md 的 7-level autonomy** — 是情绪对冲产物，不是真的设计
- **autoreply bot 这种 OOO 兜底设计** — 已经验证在 0 inbound 场景没用

---

## 关停 checklist（执行记录）

- [x] `personalab_autoreply` scheduled task → Disabled
- [x] `personalab_monitor` scheduled task → Disabled
- [x] RETROSPECTIVE_SUNSET.md 写完
- [x] README.md 顶部加 sunset header
- [x] STATE.md 改写成只剩 sunset notice
- [x] git remote 更新到 weiseer + commit + push
- [x] `gh repo archive weiseer/personalab` → repo 标 archived (read-only)
- [x] memory 写 sunset 决策替换原 project_personalab.md

## 仍存在但不维护

- 公开 anchor：IH launch post / dev.to / Reddit / Gist — 不删（删了反而显得 sketchy），但不再回复评论、不再追指标
- 老 GitHub 账户 `g16253470-beep` 已经 404；新账户 `weiseer` 下 repo + gist 都还能访问，repo archived
- v0.2.0 PyPI 包 **没 publish**（dist/ 下的 wheel 不上传），节省删除回收的麻烦

---

_文档作者：本人（与 Claude 协作起草）。诚实是写给一年后自己看的，不是给招聘官看的。_
