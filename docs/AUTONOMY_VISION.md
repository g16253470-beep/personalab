# personalab v1.0 — Autonomy Vision

> 项目北极星文档。当前在 v0.3 manual MVP，v1.0 终态是 7 级 autonomous loop。
> 来源：与 Codex 三方 audit 后的深度反思（DECISIONS.md D-13）。

## 核心区别

**Automation**：按脚本执行，无人干预 → 99% 项目所谓"自动化"。
**Autonomy**：感知 + 决策 + 学习 + 自改 → 真正的 AI 杠杆。

personalab v1.0 目标是 autonomy，不是 automation。

---

## 7 级 Autonomy 阶梯

每升一级 = leverage × 10，但风险 × 5。**绝不跳级**，每级配独立 guardrail。

```
Level 0  全 manual                  ← Day 1-10 (Codex 推荐, v0.3)
Level 1  工具自动                    ← scrape / annotate 脚本可跑（已实现）
Level 2  Pipeline 自动               ← 12-stage cron 串起来
Level 3  决策自动                    ← signup > 阈值 → push 通知
Level 4  行动自动                    ★ AI 自动 deploy landing + 发 cold email
Level 5  资源分配自动                ← AI 自己决定 $ 怎么分
Level 6  战略自动                    ← AI 自己决定 pivot 换 vertical
Level 7  进化自动                    ← AI 自己改自己 pipeline + auto-merge
```

---

## 每级 mechanism + Guardrails

### Level 1：工具自动（已实现）

**Mechanism**：脚本 idempotent + resume。
**已实现**：`scrape_hn.py`、`scrape_reddit.py`、`annotate.py`（含 resume support）。

### Level 2：Pipeline 自动（W1-W2）

**Mechanism**：GitHub Actions cron 每日跑 12-stage pipeline。

```yaml
# .github/workflows/gap_discovery_daily.yml
schedule: { cron: '0 6 * * *' }  # 06:00 UTC daily
jobs:
  daily:
    - scrape (HN + Reddit + GitHub Issues, 24h window)
    - annotate (Gemini Flash)
    - cluster + cross-source dedupe
    - persona rebuttal (personalab)
    - incumbent audit
    - retrospective backtest
    - confidence ranking
    - write Top 5 brief → git commit + discord webhook
```

**Guardrails**：
- 每 stage 独立 try/except，单点失败不卡全 pipeline
- Cost cap：单次跑总 LLM calls < 1000
- JSON schema validation 所有 LLM 输出

### Level 3：决策自动（W2-W3）

```python
def auto_rank(briefs):
    for b in briefs:
        if b.confidence > 0.65:
            promote_to_action(b)     # 进 Level 4
        elif b.confidence < 0.3:
            archive(b)
        else:
            queue_for_human_review(b)
```

**Guardrails**：
- 阈值参数 git tracked，调整要 PR
- Human review 队列 24h 超时 → 默认 archive
- 每个 promotion 立即 discord webhook

### Level 4：行动自动（W3-W4）★ 最高 ROI

```python
async def autonomous_validate(gap):
    html = await llm_generate_landing(gap)
    url = await cloudflare_pages_deploy(slug=gap.slug, html=html)
    add_plausible_tracking(url) + add_waitlist_form(url)
    
    emails = await hunter_io_find(query=gap.icp, limit=50)
    for email in emails:
        body = await llm_write_personal_email(gap, email.context)
        critic_score = await llm_critic(body)  # 反 spam guardrail
        if critic_score < 7: continue
        await resend_send(email, body, footer_unsubscribe=True)
    
    await sleep(86400)
    return {
        "signup_rate": get_signup_rate(url),
        "reply_rate": get_reply_rate(),
        "real_pmf_signal": signup > 0.005 and reply > 0.05
    }
```

**Guardrails**（最关键一层）：

| 风险 | Guardrail |
|---|---|
| Spam 误判 | < 50 emails/day total；每邮件必含 unsubscribe；3 天 follow-up 最多 1 次 |
| Brand damage | LLM critic 评分 ≥ 7/10 才发；< 7 丢弃 |
| Hallucination | Landing page 数字 / 引用 / claim 都需 source |
| GDPR / CAN-SPAM | footer 标准化 + 公司地址 + opt-out |
| 声誉一次受伤 | Sub-domain rotation：每周新 sub-domain，主域名永不发 cold email |

### Level 5：资源分配自动（W4-W5）

```python
class BudgetManager:
    monthly_cap = 200  # hard, override via PR only
    
    def allocate(self, gaps):
        spent = stripe_get_month_to_date()
        remaining = self.monthly_cap - spent
        if remaining < 20: return "stop"
        
        for gap in sorted(gaps, key=lambda g: g.roi, reverse=True):
            if remaining < gap.next_step_cost: break
            allocate_budget(gap, gap.next_step_cost)
            remaining -= gap.next_step_cost
```

**Guardrails**：
- Hard cap $200/月，超了 Stripe webhook 自动 freeze API keys
- Per-vertical cap ≤ 40% monthly
- 日支出 > $20 自动 discord 报警

### Level 6：战略自动（W5-W6）

```python
def weekly_strategy_review():
    last_4w = get_metrics()
    proposals = []
    
    best = max(last_4w.verticals, key=lambda v: v.real_pmf_signals)
    if best.signal_count >= 2:
        proposals.append(f"Double budget on {best.name}")
    
    dead = [v for v in last_4w.verticals if v.signal_count == 0]
    for v in dead[:2]:
        proposals.append(f"Kill {v.name}")
    
    if len(active_verticals) < 5:
        proposals.append(f"Add new vertical: {scan_trending()[0]}")
    
    create_pr(proposals, auto_approve=False, expiry_24h=True)
```

**Guardrails**：
- 24h 反悔窗：所有战略变更 24h 后才执行
- Pivot 上限：4 周内最多换 1 vertical
- Burn-rate check：超 cap 自动 reject

### Level 7：进化自动（W6+）★ 最危险

```python
class SelfImprovementAgent:
    async def daily_self_review(self):
        errors = last_24h_errors()
        analysis = await claude.analyze_root_cause(errors)
        patch = await claude.write_patch(analysis)
        
        if not run_smoke_tests(patch): return
        if not run_mini_pipeline(patch): return
        
        git_apply(patch)
        git_commit(f"self-fix: {analysis.summary}")
        schedule_auto_revert_check(patch, after=24h)
```

**Guardrails（最严密）**：
- Test 100% 通过 gate
- 24h metrics 不能回退 > 5%，否则 auto-revert
- **绝不能改 guardrail 代码自己**（hardcoded blacklist file path）
- **绝不能改财务 cap**（DB read-only）
- 任何 self-modify 都 git commit，human 可任意 revert

---

## Stack（2026 最佳工具）

| 阶段 | 工具 |
|---|---|
| 数据 | HN Algolia / GitHub API / Apify / Bright Data |
| LLM 标注 | Gemini Flash（免费）+ Claude Haiku（fallback）|
| Embedding | sentence-transformers (local) + HDBSCAN |
| Persona | personalab |
| 非 LLM 信号 | Google Trends / SerpAPI / LinkedIn (Bright Data) / Crunchbase |
| Landing | v0.dev API / Lovable / Claude Code 写静态 HTML |
| Deploy | Cloudflare Pages / Vercel free tier |
| Analytics | Plausible / GA4 |
| Email send | Resend / SendGrid |
| Email 找地址 | Hunter.io / Apollo.io |
| Schedule | GitHub Actions / Cloudflare Workers Cron |
| Storage | SQLite → Supabase / Cloudflare D1 |
| Agent loop | Claude Agent SDK / LangGraph |
| Self-modify | Claude Code / Aider |
| Cost monitor | Stripe webhook + 自写 |

---

## 6 周实施路径

| 周 | Level | 工作 | 投入 |
|---|---|---|---|
| W1 | 0→2 | manual MVP + cron pipeline | 15h |
| W2 | 2→3 | confidence ranking + push 通知 | 8h |
| W3 | 3→4 | ★ landing page 自动 + cold email 自动 | 20h |
| W4 | 4→5 | Budget manager + Stripe + Hard cap | 10h |
| W5 | 5→6 | 战略 weekly review + vertical 切换 | 8h |
| W6 | 6→7 | Self-improvement agent | 15h |

**总 ~76h ≈ 2 周 FT 等价（part-time 6 周）**。

---

## 商业意义

**Manual 模式**：1 founder × 10 天 / vertical = 5 vertical / 8 周
**Autonomous (Level 7)**：100 vertical 同时 24/7，每周自动产 5+ brief

**单人 founder 能 monitor 100+ vertical** —— 这是真正"算力代时间代真人调研"的形态。

---

## 真实陷阱（按概率排序）

| 风险 | 概率 | 后果 | 缓解 |
|---|---|---|---|
| Cold email 被识别 spam | 高 | Domain blacklist | Sub-domain rotation + LLM critic + 限频 |
| Budget 失控 | 中 | $5k 一夜烧光 | Stripe hard cap + DB read-only |
| Landing page 误导法律 | 中 | Lawsuit | LLM fact-check + "validation experiment" footer |
| Self-improvement 改坏 | 中 | Pipeline 挂 3 天 | Test gate + auto-revert + git history |
| Hallucinated need | 高 | Build 不存在市场 | 必须有非 LLM 硬信号（GitHub / Trends / CPC） |
| Anthropic / OpenAI 复刻 | 高 | 卷不过 | Calibration ledger + 公开 transparency |
| Distribution 饱和 | 中 | Auto cold email 到上限 | Organic content（HN/Twitter）需 human+AI |

---

## 决策原则（关机也不能丢）

1. **不跳级**。Level 0→7 一次跳过去 = AI 失控 + 财务破产
2. **每级独立 guardrail**。Level 越高 guardrail 越严
3. **Level 4 是最高 ROI**（自动 landing + 自动 cold email = 真正 PMF 自动化）
4. **Level 7 必须 human-revertible**（git history + auto-revert + DB read-only 财务 cap）
5. **Calibration ledger 必须从 Level 2 就开始累积**（不能等 Level 7 才补）—— 这是真正的 moat

---

## 跟当前 v0.3 manual MVP 的关系

**v0.3 不是浪费**。它是 mechanism 验证 gate：

- **如果 Day 5-10 manual MVP gate 过了**（2 付费客户）→ 立刻投 6 周做 v1.0
- **如果 gate 没过** → autonomous 化只是把错误规模化，**不做 v1.0**，把 personalab 当 portfolio

**Codex 警告的本质**：先用最小代价验证 mechanism，再投入算力规模化。这跟 autonomous vision 不矛盾，是 sequential。
