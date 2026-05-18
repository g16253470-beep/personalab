# personalab — 决策时间线

Append-only 决策日志。**永远不要删除条目**，新增在最下面。

---

## 2026-05-17

### D-1 项目命名 `personalab`
**决策**：从 okx_pulse 的 `persona_test.py` + `agentic_persona_test.py` 抽离成独立框架，命名 personalab，放 `G:/gpt/personalab/`。
**理由**：原项目封版（memory 标记 okx_pulse v12.6-final 关停），抽离成 product-agnostic framework 复用价值更高。

### D-2 L1-L7 全做完
**决策**：用户选"完整 L1-L7 含框架抽离（一周）"路径，完成 14 任务。
**理由**：framework 完整度 > 半成品。

### D-3 默认 LLM 限定 claude-cli
**决策**：`build_llm("anthropic-api:...")` 默认 raise RuntimeError，要 `PERSONALAB_ALLOW_CLAUDE_API=1` 解锁。
**理由**：用户已付 Claude 套餐，禁止重复烧 Anthropic API 钱。Memory `feedback_no_claude_api.md` 持久化。

---

## 2026-05-18

### D-4 personas 默认改为通用 SaaS dev-tool（去加密味）
**决策**：`personas/` 重命名为 `personas_signalstream/`，新建 12 个通用 SaaS personas 当默认。
**理由**：non-crypto 产品测试需要通用人格。但这埋下了 D-7 contamination 问题。

### D-5 PostHog 当 case study #1（不当 Documenso / Cal.com）
**决策**：先做 PostHog，因为主题契合（user research tool 测 product analytics tool）+ audience overlap 大 + 公开素材完整。
**理由**：见 LAUNCH.md narrative。

### D-6 找 + 验证 + 合并 Gemini API keys
**决策**：全盘搜 14 个 Gemini key 候选，验证 4 个有效（`AIzaSyArxx...` 主用），合并到 `G:/black/okx_agent/.env` + `C:/Users/19619/Desktop/api/keys.md`，删除 api.txt / tokey.txt。
**理由**：避免每次再扫盘 + 集中管理凭证。

### D-7 公开承认 persona contamination（不重跑修复）
**决策**：PostHog + Cal.com case study 都加 "Known limitation: persona contamination" 完整段，承认默认 personas 含 personalab-specific 词汇导致 verdict 漂移。
**理由**：Codex audit 指出（codex-audit.txt 行 7）`agentic_report` 多处 personas 评 personalab 不评 PostHog。**隐瞒 = 不诚实 + UX researcher hostile audience 必然发现 = 信任崩**。公开 = 反 hostile 防御 + transparency narrative。

### D-8 Cal.com case study #2 启动
**决策**：选 Cal.com 当 #2，跑 mode=both (Gemini Flash static + claude-cli agentic)。结果：8 yes / 0 maybe / 3 no / 1 err static → 0 yes / 0 maybe / 12 no agentic（100% flip）。
**关键发现**：8/12 personas 独立指认 "Powered by Cal.com" 免费版 branding 是 #1 转换障碍 —— 至今 personalab 最干净的 single-lever 发现。

### D-9 不做 case study #3 (Documenso)
**决策**：3 份 case（self + PostHog + Cal.com）已是 "minimum credible sample"，Documenso 留作 Show HN 后 community 投票决定。

### D-10 三方独立 audit 一致 verdict
**决策**：Claude / Gemini / Codex 三方独立审计 personalab 商业化，verdict：
- Claude（我）：🟡 OSS + 服务，不做 SaaS
- Gemini Flash：❌ 完全放弃
- Codex（最新）：🟡 manual-first，不做自动化

**理由**：3/3 都说不做 SaaS。**personalab 作为 standalone SaaS 商业化不可行**。

### D-11 reject 我自己的 8-stage 自动化 Gap Discovery 方案
**决策**：放弃 19h 自动化 pipeline，按 Codex 推荐做 10 天 manual-first MVP。
**理由**：Codex audit 五个关键缺陷（codex-gap-audit.txt）：
- ① 缺购买验证层（real buyer signal）
- ② LLM 4 重 bias 叠加（数据 + 标注 + persona + incumbent audit 都是 LLM）
- ③ Calibration 是 brand asset 不是 sales asset
- ④ Synthetic Users 两周可复制
- ⑤ 真实 cold email 回复率 > LLM persona vote 信号强 10 倍

**关键转向**：persona 从"投票器"降级到"反驳器"。权重表大改：
- 我原方案：persona_vote 隐含很重
- Codex 修订：data 0.30 / growth 0.25 / coverage -0.20 / **real_buyer_signal 0.20** / persona 0.05 / moat -0.10

### D-12 创建 STATE.md + DECISIONS.md 持续化机制
**决策**：写 `STATE.md`（当前状态快照）+ `DECISIONS.md`（本文件）+ memory 指针，关机/换设备后用户只需说"读 STATE.md 继续"。
**理由**：当前对话 context 关机后丢失最危险。代码留着但决策推演逻辑链丢了。需要文件化中间状态。

---

### D-13 v1.0 北极星定为 7-Level Autonomy
**决策**：v0.3 manual MVP（Codex 推荐）是 mechanism 验证 gate；**v1.0 真正终态是 7-level autonomous loop**（Level 0→7 在 6 周内逐级解锁）。
**理由**：
- Codex 提的 manual-first 不矛盾 autonomous，它是 sequential
- 不做 autonomous = 单人产能上限 5-10 vertical/季度
- 做 autonomous = 100+ vertical 同时 24/7，单 founder 真正杠杆
- Level 4（自动 landing + 自动 cold email）是最高 ROI 一级，**3-7 天就能 PMF 验证**
- Level 7（self-improvement）是最危险一级，必须严格 guardrail + human-revertible

详见 `docs/AUTONOMY_VISION.md`。

### D-14 Day 1-4 Gap Discovery dev tools 完成
**已实施**：
- HN scrape: 392 quotes (8 queries, 2007-2026)
- Reddit scrape 失败 (403 Blocked, 2023 API 政策), 跳过
- Gemini Flash annotate: 392/392 完成，0 错误，**59% (235 条) 真 dev-tool 相关**
- segment 主导：staff_eng 137 (58%) — ICP 跟现有 personas 高重合
- categories: framework 44 / collab 19 / build 15 / deploy 14 / api 9 / infra 8 / docs 7 / db 6

下一步：Day 5 personas 反驳器（用 235 真实 cluster）。

### D-16 公开发布完成（GitHub + Gist + IH + Reddit）2026-05-18
**已实施**：
- 9:00 BJT — GitHub public repo (`g16253470-beep/personalab`)，14 commits 推送
- 9:00 BJT — Public Gist 含 C11 bundle (16 KB)
- 9:00 BJT — Windows scheduled task `personalab_monitor` 每 2h 自动跑
- 10:40 BJT — IH product page (`/product/personalab`) + launch post live，**第 1 LIKE 在 submit 后 1 分钟内**
- 11:28 BJT — Reddit r/SideProject (38.7K members) launch post live

**HN 状态**：Show HN 被新账号 anti-spam 政策拦截（不是内容拒绝）。warm-up 计划 2-4 周后再试。

**LAUNCH narrative 选定**：诚实交底版 — "I tested my AI tool on PostHog/Cal.com, every persona said no"（HN/IH/Reddit 三处一致）。

**Identity barrier 物理瓶颈处理**：gh CLI 装一次（5 min OAuth）→ 后续 100% 自动化解锁所有 GitHub / Gist 操作。Reddit / IH / Show HN 仍需手工 submit（平台 anti-bot 政策无 API）。

下一步：等 24-72h organic engagement signal，monitor 自动追踪。

### D-15 Day 5 personas 反驳器完成，9 defensible cluster 入 Day 6
**已实施**：
- 235 dev-tool unmet need → LLM 聚类 18 cluster
- 12 personas 各反驳 6-8 cluster（**作为反驳器，不是投票器**）
- **9 defensible (≤ 4 down-vote) / 9 rejected**
- 成本：~14 Gemini Flash calls，~3 min

**Top 4 candidate**（按"提及频率 × 反对少 × severity"排）：
- **C3** 团队协作 / code review / contrib mgmt (members=**20**, down=2/12, sev=3.1)
- **C4** AI/LLM coding agent 精确性 + context (members=12, down=2/12, sev=3.67)
- **C11** 跨设备数据同步 + DB GUI (members=7, **down=1/12**, sev=3.57)
- **C14** SRE 用户级监控 + AI 性能可观测 (members=3, **down=1/12**, **sev=4.0**)

**Day 6 重点 teardown** 这 4 个 cluster 的 incumbents：
- C3: CodeRabbit / Sourcery / Linear / GitHub native review
- C4: Cursor / Copilot / Aider / Windsurf
- C11: TablePlus / DBeaver / Sequel Pro / iCloud sync
- C14: Datadog / Honeycomb / Sentry / LangSmith / Helicone

---

## 待决策

- D-15: 是否先发 LAUNCH.md Show HN — 等 Day 7-8 cold email 回复数据
- D-16: git push GitHub — 等仓库公开 readiness
- D-17: Manual Gap Diligence Service 商业模式 — 等 Day 7-8 cold email 回复率验证
- D-18: 是否跳到 W1 Level 2 自动化 — 等 Day 5-10 manual MVP gate 结果（2 付费客户）

---

## 已被推翻的旧决策（保留作历史）

- ~~"做 SaaS $99/mo"~~ → D-10 三方 reject
- ~~"做 19h 8-stage 自动化 MarketGapMode"~~ → D-11 reject by Codex
- ~~"卖 personalab $30-80k"~~ → D-10 估值修正到 $2-8k，且非最优解
