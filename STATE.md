# personalab — 当前项目状态

> **新会话入口**：开新对话只需输入 "读 G:/gpt/personalab/STATE.md 继续"，Claude 会自动恢复完整 context。
>
> 上次更新：2026-05-18 02:55 BJT

---

## 一句话现状

personalab v0.2.0 已 ship 完整框架 + 2 个公开 case study，**核心商业方向已被三方独立审计否决（不做 SaaS）**，最新方向是 **Gap Discovery manual-first MVP**（Codex audit 推荐路径），等你定 vertical 后 Day 1 启动。

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

## 当前阶段：M1 Foundation 进行中

按 6-month 路线图（README 里）：

```
[已完成] v0.2.0 ship + 2 case study + 三方 audit
[当前]   M1 — 决定下一步方向
[待定]   M2 — 公开 release + traction
[待定]   M3-M6 — 按 traction 决定后续
```

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
