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

## 待决策

- D-13: 启动 Gap Discovery Day 1（选 vertical）— 等用户定 vertical
- D-14: 是否先发 LAUNCH.md Show HN — 等用户决定先发还是先 Day 1 拿到 cold email 数据
- D-15: git init + PyPI publish — 等用户 PyPI token / 决定要不要 GitHub
- D-16: Manual Gap Diligence Service 商业模式 — 等 Day 7-8 cold email 回复率验证后再定

---

## 已被推翻的旧决策（保留作历史）

- ~~"做 SaaS $99/mo"~~ → D-10 三方 reject
- ~~"做 19h 8-stage 自动化 MarketGapMode"~~ → D-11 reject by Codex
- ~~"卖 personalab $30-80k"~~ → D-10 估值修正到 $2-8k，且非最优解
