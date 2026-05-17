# Open issues / roadmap

Tracked here until a GitHub repo exists. Each item is a candidate issue body — copy-paste when filing.

---

## P0 — blocks credibility, not blocks release

### TODO-1: persona profile / product preference separation
Default `personas/` markdown files tangle two things that should be orthogonal:
- **User profile** — role, budget, working style, segment vocabulary
- **Product preferences** — what features they want, what triggers churn

Result: when a persona authored for product A is reused on product B, verbatim feedback contaminates. Confirmed in `reports/posthog_case/CASE_STUDY.md#known-limitation`.

**Fix shape**: split persona into `profile.yaml` (stable across products) + optional `<product>_preferences.md` (per-product overlay).

### TODO-2: agentic LLM-failure fabrication taints retention metric
`modes/agentic.py:171-176` silently emits `DO_NOTHING` when the LLM call retries are exhausted. This pollutes retention/engagement aggregation downstream — a quota error looks identical to a real "user didn't act today" signal.

**Fix shape**: emit `_llm_unavailable: true` flag in the day decision; reporter excludes these days from engagement averages and surfaces them as a footnote.

### TODO-3: contamination disclosure boilerplate
Reports need a "personas-product compatibility" disclaimer header. When a `posthog` adapter is run with the `personalab`-flavored default personas, the reporter should auto-detect and warn.

**Fix shape**: ProductAdapter declares `name` and `domain`; Persona frontmatter declares `target_products`; reporter cross-checks and prepends warning if mismatched.

---

## P1 — known code debt (Codex audit, 2026-05-18)

### TODO-4: SubscriptionState defaults are event-stream biased
`core/product.py:34-47` defaults to severity / category / mute / hourly_cap fields that are natural for push-notification products (SignalStream) but unnatural for IDE plugins, chat apps, design tools.

**Fix shape**: make `SubscriptionState` carry only `profile: str` and `filters: dict`; let ProductAdapter define its own state subclass. Update toy / posthog adapters to demonstrate clean usage.

### TODO-5: CLI doesn't expose mode nesting
SDK supports `ABMode(StatsMode(AgenticMode(...)))`, but `--mode` is a single string in `cli.py:182-184`. Users can't actually run "stats on top of A/B" from the CLI.

**Fix shape**: parse `--mode` as a comma-separated outer→inner stack (e.g. `--mode ab,stats,agentic --label-a v1 --label-b v2 --repeats 3 --days 5`).

### TODO-6: JSON parsing has no schema validation
`core/parsing.py:20-36` uses a greedy `{.*}` regex extraction. Malformed-but-near-JSON output (missing fields, wrong types) silently produces partial results.

**Fix shape**: define a `pydantic` (or `dataclasses`-only fallback) schema per mode; reject responses missing required fields; surface to retry loop.

### TODO-7: No global rate limiter
`modes/stats.py:101-105` and `modes/ab.py:93-96` multiply concurrent calls (Stats × Agentic = repeats × days × personas). With strict LLM quotas (Gemini free tier), this hits rate limits invisibly.

**Fix shape**: add a project-wide `asyncio.Semaphore` per `LLMAdapter` instance with documented defaults (e.g. 10 RPS for Gemini free, 50 RPS for paid).

### TODO-8: No prompt/version metadata in reports
Reports don't record which prompt template version generated them. When prompts evolve, old reports can't be re-interpreted.

**Fix shape**: `ModeResult.metadata` gains `prompt_version: str` and `personalab_version: str`; reporter renders these in the header.

### TODO-9: README claimed "HTML on roadmap" but 0.2.0 shipped it
Fixed in 0.2.0 README, leaving this here as a process reminder: keep CHANGELOG ↔ README in sync at every minor bump.

---

## P2 — nice-to-have

### TODO-10: ActionLoopReporter keyword buckets are SignalStream-biased
`reports/action_loop.py:25-39` has buckets like "AI 稳定性" / "小币 / 币种过滤" that are nonsense for non-crypto products. PostHog case study showed weak signal because of this.

**Fix shape**: replace keyword-bucket clustering with embedding-based clustering (sentence-transformers / OpenAI embeddings + HDBSCAN). Optional dependency. Fall back to keyword buckets if no embedding key.

### TODO-11: persona portrait + visual report
designer_lead persona wants persona portraits + visual report templates (see `personas/12_designer_lead.md`). HTML renderer is a first step; richer template (cards, color-coded sentiment) would close the gap.

### TODO-12: web playground for non-dev users
`personas/10_no_code_user.md` makes the case: 30% of evaluators bail at `pip install`. A streamlit/gradio playground at a hosted URL would let non-dev marketers/PMs try it.

### TODO-13: case study #2
Per `CASE_STUDY.md` close, next public study should be Cal.com (open-source scheduling, similar audience). Build adapter from public surface, run with cleaner non-`personalab`-contaminated personas (depends on TODO-1).

### TODO-14: SOC2 / GDPR DPA / SSO
`personas/09_corporate_pm` + `personas/04_vc_thesis` both call out enterprise compliance as a hard blocker. Real fix requires legal effort. Mark as "v1.x — not pursuing in v0.x".

### TODO-15: calibration mini-study with real users
Codex audit recommends: pick 5-10 real founders, run personalab predictions, then interview them, compute r². Without this number, the methodology objection (TODO-1 + persona authenticity) stays unresolved.

---

## Workstream sequencing (M1-M6 mapping)

| Roadmap | Critical items |
|---|---|
| M1 (Foundation) | TODO-1, TODO-2, TODO-3, TODO-9, TODO-13 case study #2, TODO-15 calibration mini-study |
| M2 (Public release) | Show HN + Twitter + Indie Hackers + 5-min demo video |
| M3 (Capture inbound) | TODO-10 embedding clustering, TODO-6 schema validation, paid pilot work |
| M4 (Web UI) | TODO-12 streamlit playground, TODO-11 visual report |
| M5 (Decision point) | TODO-5 CLI nesting, TODO-7 rate limiter (if paid customers report it) |
| M6 (Outcome) | TODO-4 SubscriptionState cleanup, TODO-8 prompt versioning, TODO-14 compliance (only if enterprise pursues) |

---

## v1.0 Autonomy Track — 6 周 7-级解锁（详见 docs/AUTONOMY_VISION.md）

**激活条件**：Day 5-10 manual MVP gate 过（2 付费客户 OR signup rate > threshold）

### W1 — Level 0→2: Pipeline 自动化（15h）
- TODO-A1: GitHub Actions cron `gap_discovery_daily.yml` 每日 06:00 UTC
- TODO-A2: 12-stage pipeline 串成单 entry point（Python `run_pipeline.py`）
- TODO-A3: 每 stage 独立 try/except + 错误日志到 discord webhook
- TODO-A4: Cost cap (LLM calls < 1000 / run)
- TODO-A5: JSON schema validation 所有 LLM output

### W2 — Level 2→3: 决策自动（8h）
- TODO-A6: confidence ranking 8-factor 加权打分
- TODO-A7: 阈值 (0.65 / 0.3) 参数化进 git config
- TODO-A8: human review queue + 24h 超时 archive
- TODO-A9: Discord webhook for promotions

### W3 — Level 3→4: ★ 行动自动（20h，最高 ROI）
- TODO-A10: `llm_generate_landing(gap) → html` (Claude / v0.dev API)
- TODO-A11: Cloudflare Pages auto-deploy via API
- TODO-A12: Sub-domain rotation：每周新 sub-domain，主域永不 cold email
- TODO-A13: Hunter.io / Apollo 邮箱抓取 50 个 / gap
- TODO-A14: LLM 写个性化 cold email + LLM critic（spam score ≥ 7/10 才发）
- TODO-A15: Resend / SendGrid 发送 + footer unsubscribe + GDPR / CAN-SPAM 合规
- TODO-A16: < 50 emails/day total 硬限
- TODO-A17: 24h 后 signup_rate / reply_rate 自动收集

### W4 — Level 4→5: 资源分配自动（10h）
- TODO-A18: BudgetManager class + Stripe webhook
- TODO-A19: monthly_cap $200 hardcoded，DB read-only
- TODO-A20: per-vertical cap ≤ 40%
- TODO-A21: 日支出 > $20 自动 discord 报警
- TODO-A22: 触发 emergency stop API key freeze

### W5 — Level 5→6: 战略自动（8h）
- TODO-A23: weekly_strategy_review() 周末跑
- TODO-A24: 自动 propose vertical 增加 / kill / budget shift
- TODO-A25: 24h 反悔窗，human 可 veto
- TODO-A26: 4 周内 pivot 上限 1 次

### W6 — Level 6→7: 进化自动（15h，最危险）
- TODO-A27: SelfImprovementAgent + Claude Agent SDK loop
- TODO-A28: 错误日志 → LLM root cause analysis → patch
- TODO-A29: 100% smoke test 通过 gate
- TODO-A30: 24h metrics 回退 > 5% → auto-revert
- TODO-A31: hardcoded blacklist：禁改 guardrail / 财务 cap / git auto-merge 规则
- TODO-A32: 所有 self-modify git commit，human 可任意 revert

### 持续 — Calibration ledger（v1.0 唯一真正 moat）
- TODO-A33: 每天预测 snapshot 到 `data/calibration_ledger/<date>.jsonl`
- TODO-A34: 3 月后 revisit script：预测对吗？
- TODO-A35: Quarterly 公开 prediction accuracy（成 niche 的 Gartner）
- TODO-A36: 用历史 accuracy 调整 prior probability，闭环
