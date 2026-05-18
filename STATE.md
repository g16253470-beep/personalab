# personalab — 当前项目状态

> **新会话入口**：开新对话只需输入 "读 G:/gpt/personalab/STATE.md 继续"，Claude 会自动恢复完整 context。
>
> 上次更新：2026-05-18 09:00 BJT

---

## 🎉 PUBLIC URLS (live as of 2026-05-18)

- **GitHub repo**: https://github.com/g16253470-beep/personalab
- **Public Gist (C11 brief)**: https://gist.github.com/g16253470-beep/689071000407ef83f1226896e77c2840
- **IH product page**: https://www.indiehackers.com/product/personalab
- **IH launch post** ⭐: https://www.indiehackers.com/post/launched-personalab-i-tested-it-on-posthog-cal-com-and-itself-every-persona-said-no-j766rC1WqI9mKEsvqCDi (live 2026-05-18 ~10:40 BJT, 1 LIKE at submit)
- **Reddit r/SideProject post**: https://www.reddit.com/r/SideProject/comments/1tgajyc/i_tested_my_ai_product_tester_on_3_real_saas/ ❌ auto-filtered (new account spam protection)
- **Reddit r/indiehackers**: ❌ same auto-filter
- **dev.to launch post** ⭐: https://dev.to/personalab/i-tested-my-ai-product-tester-on-3-real-saas-products-every-persona-said-no-26ci (live 2026-05-18 ~12:20 BJT, username `personalab`)
- **Autonomous monitor**: Windows scheduled task `personalab_monitor`, runs every 2h, dashboard at `gap_discovery/monitor/monitor_dashboard.md`
- **Active launch threads index**: `gap_discovery/monitor/threads_to_watch.txt`

**Show HN deferred**: new account anti-spam policy blocked submit. HN warm-up plan: comment + upvote 2-4 weeks on g16253470-beep then retry. Show HN draft text remains in `LAUNCH.md` Option B.

---

## 一句话现状

personalab v0.2.0 已 ship 完整框架 + 2 个公开 case study，**核心商业方向已被三方独立审计否决（不做 SaaS）**。Gap Discovery Day 1-9 完整跑通（dev tools vertical），找到 C11 (local-first DB GUI + cross-device sync) 为 winner，sibling 项目 `G:/gpt/personalab_db_sync/` W1 scaffold 已就绪。**2026-05-18 GitHub 公开发布 + autonomous monitor 启动**。

---

## 已完成（截至 2026-05-18）

### 代码 / 框架
- **v0.2.0 完整 release-ready**：6 个 mode（Static / Agentic / Jury / AB / Stats / Calibration）、4 个 LLM adapter（claude-cli / anthropic-api / openai / gemini）、8 个 reporter、HTML 渲染器、CLI 全 mode 支持
- **PyPI build done**：`dist/personalab-0.2.0-py3-none-any.whl` + `.tar.gz`，twine check PASSED，待你 publish（见 `RELEASE.md`）
- **6/6 smoke tests** 通过；pyflakes 0 warning
- 4 个 ProductAdapter：signalstream（历史）、posthog_case、calcom_case、personalab_meta、toy

### Case studies（3 份）
| Case | static | agentic | 关键发现 |
|---|---|---|---|
| **personalab 自测** | 0/8 yes | 0/8 yes | pre-PMF，自己的 P0 issue list 自动出 |
| **PostHog** | 6/12 yes | 0/12 yes | 5 类 friction，static→agentic 100% collapse |
| **Cal.com** | 8/12 yes | 0/12 yes | **1 个杀手发现**："Powered by Cal.com" branding 8/12 提及 |

### 文档（全套）
- README.md（已去 SignalStream 包袱，加 Honest disclaimers）
- CHANGELOG.md（0.2.0 完整）
- docs/QUICKSTART.md / ARCHITECTURE.md / ADAPTER_GUIDE.md / PERSONA_WRITING.md
- docs/MARKET_GAP_VISION.md（Gap Discovery 设计）
- TODO.md（15 项 P0/P1/P2 公开 issue）
- LAUNCH.md（Show HN 两版 + Twitter thread + Indie Hackers）
- RELEASE.md（PyPI publish 步骤）

### 独立审计（三方 verdict 一致）
- **Claude（我）**：🟡 OSS + 服务，不做 SaaS
- **Gemini 2.5 Flash**：❌ 放弃（最激进）
- **Codex（最新）**：🟡 **manual-first 10-day MVP，不做自动化** — 详见 `shared/codex-gap-audit.txt`

### 市场扫描
- **直接竞品 8 家**：Synthetic Users / Blok ($7.5M) / Artificial Societies (YC W25, $5.35M) / Microsoft TinyTroupe（开源同类）/ Cambium AI / Deepsona / Personaut / Toluna
- **市场需求方向竞品**：GapRadar ($14.99/月，**占位但市场认知 ≈ 0**)
- 结论：personalab 是这个 niche 的第 10 个 mover，**不是 SaaS 卖钱方向**

---

## 当前阶段：Gap Discovery Day 4 完成，Day 5 准备启动

按 6-month 路线图（README 里）+ v1.0 Autonomy Vision（docs/AUTONOMY_VISION.md）：

```
[已完成] v0.2.0 ship + 2 case study + 三方 audit
[已完成] Day 1-4 Gap Discovery dev tools (392 → 235 真实 unmet need)
[当前]   Day 5 personas 反驳器 + Day 6 incumbent teardown
[gate]   Day 7-8 cold email 真实 buyer outreach (PMF 信号验证)
[激活]   v1.0 W1-W6 7-level autonomy (gate 过才启动)
```

**v1.0 北极星**：详见 `docs/AUTONOMY_VISION.md`，7-level autonomous loop，6 周解锁，Level 4（auto landing + auto cold email）是最高 ROI 一级。

---

## Gap Discovery 进展（截至 2026-05-18 03:53 BJT）

| Day | 工作 | 状态 |
|---|---|---|
| 1 | 选 vertical = dev tools；写 cold email 3 variant；scrape 脚本 | ✅ |
| 2 | HN scrape **392 条 quotes**（2007-2026 date range）| ✅ |
| 3 | （并入 Day 2/4）| - |
| 4 | Gemini Flash 标注 **392/392 完成，0 错误，235 (59%) 真 dev-tool**；segment 主导 staff_eng 137 (58%) | ✅ |
| 5 | personas 反驳器 — **9 defensible / 9 rejected 出炉**，Top 4: C3/C4/C11/C14 | ✅ |
| 6 | incumbent teardown (C3/C4/C11/C14 各 3-5 incumbent) | ⏳ NEXT |
| 6 | incumbent teardown | ⏳ |
| 7-8 | cold email 30 封 | ⏳ |
| 9 | Top 3 brief | ⏳ |
| 10 | 公开发布 + 邀请付费客户 | ⏳ |

**关键文件**：
- `gap_discovery/README.md` — 流程
- `gap_discovery/verticals/dev_tools/plan.md` — Day 1-10 详细
- `gap_discovery/verticals/dev_tools/data/raw_quotes.jsonl` — 392 原始 HN
- `gap_discovery/verticals/dev_tools/data/tagged_quotes.jsonl` — Gemini 标注（50 已 sample / 392 后台中）
- `gap_discovery/verticals/dev_tools/cold_emails/templates.md` — 3 个 cold email variant + 跟踪 CSV schema
- `gap_discovery/scripts/scrape_hn.py` + `scrape_reddit.py` + `annotate.py`

**50 条 sample 已得高 sev unmet need**：
- "GitHub 内容审核透明度"（sev=4，跟 oss_maint persona 顾虑契合）
- "PHP 标准库现代化"
- "游戏开发入门门槛"
- "项目协作平台 contributor matching"

**Reddit scrape 失败原因**：Reddit 2023 API 政策变化，无 OAuth 403 Blocked。决定跳过 Reddit（不投入 OAuth 工作）→ Day 4 LLM 标注后如果数据不够，再补 GitHub Issues 或 Pushshift 历史档案。

---

## ⚠️ 下一个决策点（卡在这）

Codex audit 推荐的 **manual-first 10-day Gap Discovery MVP**（取代我原本的 19h 8-stage 自动化方案）：

| Day | 工作 |
|---|---|
| 1 | **选 1 vertical**（候选：dev tools / no-code / fintech / health tech / e-commerce）|
| 2-3 | 手抓 100-300 raw quote（Reddit / HN / G2） |
| 4 | LLM 标注 + cluster（LLM 只**压缩信息**，不裁判事实） |
| 5 | personalab 12 personas 作**反驳器**（不是投票器） |
| 6 | 5 个 incumbent teardown（手工 + 部分 personalab） |
| 7-8 | **10 封 cold email 给真实 buyer** ←Codex 强调这才是真实信号 |
| 9 | 等回复 + 整理 Top 3 gap brief |
| 10 | 公开发布 + 邀请付费客户 $1-3k report |

**30 天 gate**：2 个付费客户。
- 达成 → 自动化 + scale，可能转向 Manual Gap Diligence Service 商业模式
- 没达成 → 这方向也不行，停手，把 personalab 当 portfolio

**Codex 核心修订**：
- ① 加 `real_buyer_signal 0.20` 权重（我原方案没有这一项）
- ② persona_vote 降到 0.05（我隐含给很高，错了）
- ③ LLM 4 重 bias 叠加，必须加非 LLM 信号（GitHub issue / job posts / cold email reply）
- ④ Calibration 不是 sales asset 是 brand asset，6 月太久
- ⑤ 替代 trust：**Retrospective backtest**（用 2024 数据预测 2025 已知结果）

---

## 需要用户决定的 3 件事

1. **是否启动 Day 1**（选 vertical + 设计 cold email 模板）？
2. **是否先发 LAUNCH.md 的 Show HN**（narrative 改成 "我做了 personalab，正在用它找下一个项目"）？
3. **是否 git init + PyPI publish**（要你的 token / 决定）？

---

## 恢复入口（新会话怎么继续）

**最简方式**：开新对话输入这一句：

> 读 G:/gpt/personalab/STATE.md，继续推进 personalab 项目。

Claude 会读这文件 + DECISIONS.md + 关键 reports，5 分钟内恢复 full context。

**关键引用文件清单**：

| 文件 | 作用 |
|---|---|
| `STATE.md`（本文件）| 当前状态 + 下一步 |
| `DECISIONS.md` | 截至今天所有关键决策 log |
| `TODO.md` | 15 项 P0-P3 待办 |
| `CHANGELOG.md` | 已交付历史 |
| `LAUNCH.md` | Show HN / Twitter / IH 草稿（待发） |
| `RELEASE.md` | PyPI publish 步骤 |
| `docs/MARKET_GAP_VISION.md` | Gap Discovery 完整设计 |
| `reports/posthog_case/CASE_STUDY.md` | 第 1 份 case study |
| `reports/calcom_case/CASE_STUDY.md` | 第 2 份 case study |
| `reports/meta/` | personalab 自测报告 |
| `G:/gpt/shared/codex-gap-audit.txt` | Codex 三论 audit 全文 |
| `G:/gpt/shared/gemini-strategy.md` | Gemini 二论分析 |

**memory 文件**（自动加载）：
- `~/.claude/projects/G--gpt/memory/MEMORY.md`（含项目指针）
- `~/.claude/projects/G--gpt/memory/feedback_no_claude_api.md`（仍生效）
- `~/.claude/projects/G--gpt/memory/feedback_reply_timestamp.md`（每条回复打时间戳）

---

## 后台运行注意

- **Codex 任务**：已完成（codex-gap-audit.txt）
- **agentic 后台**：已完成（reports/posthog_case_claude/, reports/calcom_case/）
- **没有 in-flight 任务**会因关机丢失
