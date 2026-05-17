# Vertical #1: Dev Tools — 10-day plan

> Started 2026-05-18. Owner: solo founder + Claude as research / synthesis assistant.

## 目标

10 天内手工 + personalab 找出 dev tools 市场 **Top 3 unmet need**，公开发布 + 10 封 cold email 真实 buyer outreach，**30 天内 2 个付费客户**为 PMF gate。

## Day 1 — 启动（今天）

- [x] 选 vertical = dev tools
- [x] 写 cold email 3 个 variant 模板
- [x] 写 Reddit scrape 脚本（subreddit 列表 + JSON API）
- [x] 写 HN Algolia scrape 脚本
- [ ] 抓第一批 sample 数据（50-100 quotes）作 sanity check
- [ ] 检查数据质量 + 修脚本

## Day 2-3 — 大规模抓取 100-300 quotes

**Subreddit 列表（dev 抱怨/痛点最集中）**：
- r/programming
- r/devops
- r/webdev
- r/Python / r/golang / r/rust / r/javascript（语言社区，工具抱怨多）
- r/sideproject
- r/SaaS（工具购买者视角）
- r/cscareerquestions（工程师工作流痛点）
- r/ExperiencedDevs（资深视角，质量高）

**HN 搜索 query**：
- `"I wish" OR "frustrated" OR "annoying" OR "broken"` filter type:comment
- `"better than" alternative tool`
- `"why is there no"`
- 限制最近 12 个月

**GitHub Issues**（更精准但慢）：
- 重点 repo issues with `bug:` / `feature-request:` / 100+ reactions
- 大 OSS 项目的 abandoned PRs

**目标**：300 条 quote，去重后 ~200 条进 Day 4 标注。

## Day 4 — LLM 标注 + cluster（不裁判，只压缩）

每条 quote → JSON：
```json
{
  "id": "...",
  "source": "reddit/r/devops",
  "url": "...",
  "timestamp": "...",
  "raw_text": "...",
  "unmet_need_one_line": "...",  // LLM 压缩 1 句话
  "severity_1_5": 4,             // LLM 估 1-5
  "segment": "junior dev / staff eng / OSS maint / indie hacker",
  "willingness_to_pay_clue": "..." // 引用 quote 内任何 $ 数字
}
```

LLM 用 Gemini 2.5 Flash（免费层够 300 quote × 1 call）。

简单聚类：embedding 后 KMeans k=15-20，或手工 review tag → bucket。

## Day 5 — Persona 反驳器

把 Top 10 cluster 喂给 personalab 12 personas，prompt 改成：

> "下面这 10 个 cluster 是从 200 条真实 dev 抱怨中提取的。**你作为 [persona] 视角**，告诉我哪几个 cluster 不靠谱（reasons: 抱怨者不是真买家 / 已有产品已解决 / 不会有人付钱 / 抱怨太分散）。"

**反驳器 output**：每个 cluster 收到 0-12 个 "不靠谱" 票数。
**最终保留**：得票 ≤ 4 的 cluster（reasonably defensible）。

## Day 6 — Incumbent teardown

针对 Day 5 保留的每个 cluster，手工 + 部分 personalab 拆 3-5 个 incumbent：

| Cluster | Incumbent | URL | Pricing | 解决程度 (1-5) | 缺什么 |
|---|---|---|---|---|---|

5 个 incumbent / cluster = 至多 ~25 个 teardown entries。手工写，**personalab 只作 sanity check**（"你这 incumbent 真的没解决 cluster 吗？"）。

## Day 7-8 — Cold email 真实 buyer

按 Day 6 保留的 cluster，每个 cluster 找 10 个真实 buyer：
- GitHub 高活跃 contributor 的 public email
- 大 OSS 项目 maintainer 的 blog/Twitter signature
- r/SaaS / IndieHackers 帖主公开邮箱
- 不能是公司一线员工 — 必须是有 buy authority 的 founder / lead / dir

**1 个 cluster 10 emails × 3 cluster ≈ 30 cold emails**。

发件人：以个人身份（不是 corporate），引用具体的 quote，**问"如果有 X 工具你会付 $Y 一份 quarterly report 吗？"**。

期望回复率：5-15%（dev community 已知 cold email 友善），即 1-5 个有意义回复。

## Day 9 — 综合 Top 3 brief

每个 brief 一页：

```
GAP: <1 句话>
CLUSTER 出处: <数据频率 + 增长率>
PERSONA 反驳分数: <得票 / 12>
INCUMBENT 覆盖度: <%>
COLD EMAIL 反馈: <实际回复 quotes>
ICP: <精确 segment + day-in-the-life>
PRICING 锚: <$/月，参考竞品 + WTP signal>
TAM 估算: <现有市场 × 假设 share>
6 周路径: <solo dev 可执行 milestone>
致命风险: <regulatory / technical / market timing / Anthropic absorb>
```

## Day 10 — 公开发布

- 把 3 个 brief 渲染成 HTML（用 personalab html_renderer）
- 写 blog post：`"我用 personalab 找了 dev tools 市场 3 个未填需求 — 这是数据"`
- 发：Show HN + Twitter thread + Indie Hackers
- 邀请付费客户：$1k 一份 deep brief（含 raw data + cold email 反馈），$3k 一份 vertical 综合（含 6 周建造计划）

## 30 天 gate

| 结果 | 决策 |
|---|---|
| **2+ 付费客户** | 验证通过，跑下个 vertical（no-code/fintech），转 Manual Gap Diligence Service 商业模式 |
| **1 付费客户** | 边缘，再做 1 个 vertical 看是否能重复 |
| **0 付费客户** | 这方向不行，停手。挑保留的 cluster 之一自己 build |

## 关键风险

1. **抓 300 quote 后发现 dev tools 抱怨太分散** — 切窄 vertical（如"DevOps observability"或"frontend testing"）
2. **Cold email 回复率 < 3%** — 邮件文案 / segment 错位，加做 LinkedIn DM
3. **Persona 反驳器输出还是 LLM bias** — 加 contrarian persona，加 GitHub issue reopen 数据
4. **3 个 gap 全是 incumbent 已经在做** — 这恰好是好信号，证明 mechanism 工作
