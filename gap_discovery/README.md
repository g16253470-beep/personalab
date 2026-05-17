# Gap Discovery — Manual-first MVP

> **决策来源**：Codex audit (`shared/codex-gap-audit.txt`) D-11，拒绝 19h 自动化 8-stage pipeline，按 10-day manual-first 方案执行。

## 哲学

**LLM 是信息压缩器，不是事实裁判**。Persona 是反驳器（说哪些 cluster 不靠谱），不是投票器（说哪些 cluster 靠谱）。最终信号是 **真实 buyer 的 cold email 回复率**。

## 10-day MVP 流程

| Day | 工作 | 已完成？ |
|---|---|---|
| 1 | 选 vertical + 设计 cold email 模板 + scrape 脚本 | ✅ 启动 |
| 2-3 | 手抓 100-300 raw quote（Reddit / HN / G2 / GitHub Issues） | ⏳ |
| 4 | LLM 标注 + cluster（LLM 只压缩，不裁判） | ⏳ |
| 5 | personalab 12 personas 作反驳器 | ⏳ |
| 6 | 5 个 incumbent teardown | ⏳ |
| 7-8 | 10 封 cold email 给真实 buyer | ⏳ |
| 9 | 等回复 + 整理 Top 3 gap brief | ⏳ |
| 10 | 公开发布 + 邀请付费客户 $1-3k report | ⏳ |

## 30 天 PMF 验证 gate

**2 个付费客户**（$1-3k 一次报告）= 验证通过 → 自动化 + scale → 转 Manual Gap Diligence Service 商业模式。
**0-1 个**= 这方向也不行 → 停手，把 personalab 当 portfolio + 用搜到的 gap 自己 build 一个项目。

## 第一个 vertical：dev tools

理由：
- 目标客户（dev / PM / OSS maintainer）跟 personalab 现有 personas 重叠最多
- HN / Reddit r/programming / r/devops / r/webdev / GitHub Issues 数据可得性最高
- Cold email 渠道：dev community 公开邮箱多（GitHub bio / blog signature）
- Show HN 受众一致：dev tools gap report 会被 HN 自然消费
- 个人 expertise：能写 incumbent teardown 不靠 LLM 编

详见 `verticals/dev_tools/plan.md`。

## 关键设计原则

1. **手工先，自动化后** —— 不要在 mechanism 错前固化它
2. **LLM 4 重 bias 必须打破** —— 加非 LLM 信号（GitHub issue reopen 数 / job posts / cold email reply）
3. **persona 作反驳器** —— 输出"这 gap 不靠谱因为..."，不是"这 gap 靠谱因为..."
4. **每个 brief 附可执行验证包** —— 50 lead + 10 cold email template + landing copy + 预期回复率
5. **Retrospective backtest 是更快的 trust** —— 用 2024 历史预测 2025 已知结果，比等 6 月 calibration 快 10×

## 文件层次

```
gap_discovery/
├── README.md                       # 本文件
├── verticals/
│   └── dev_tools/                  # 第一个 vertical
│       ├── plan.md                 # 完整 10-day 工作清单 + 决策
│       ├── data/
│       │   └── raw_quotes.jsonl    # 抓的原始 quote 数据
│       ├── cold_emails/
│       │   ├── templates.md        # 3 个 cold email variant
│       │   └── targets.csv         # 真实 buyer 名单（Day 7 填）
│       ├── personas_rebuttal.md    # personas 作反驳器输出
│       ├── incumbent_teardown.md   # 5 个 incumbent 手工拆解
│       └── gap_brief.md            # 最终 Top 3 brief
├── scripts/
│   ├── scrape_reddit.py            # Reddit JSON API
│   └── scrape_hn.py                # HN Algolia API
```
