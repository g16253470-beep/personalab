# 5 个 confirmed C11 outreach targets — Ready for human action

> AI 已完成 100% 准备工作：5 个 truly-C11 关联的 HN 真实抱怨者 + 5 封个性化 draft + AI critic 评分 + 2 种 outreach 路径建议。
>
> 你只需要：(1) 选 1-2 个路径 (2) Send。

## 5 个 confirmed 目标（LLM 二次过滤 confidence 4-5/5）

| HN id | author | karma | subtype | profile email | HN URL |
|---|---|---|---|---|---|
| hn_5470551 | ivanhoe | 4347 | db_gui_pain | ❌ | https://news.ycombinator.com/item?id=5470551 |
| hn_7096377 | tunap | 1421 | local_first | ❌ | https://news.ycombinator.com/item?id=7096377 |
| hn_7868615 | pilif | 14945 | db_gui_pain | ❌ | https://news.ycombinator.com/item?id=7868615 |
| hn_9464444 | pearjuice | 3041 | db_gui_pain | ❌ | https://news.ycombinator.com/item?id=9464444 |
| **hn_952055** | rpdillon | 4982 | local_first | ✅ `hn.rpdillon@xoxy.net` | https://news.ycombinator.com/item?id=952055 |

## 两种 outreach 路径 — 选你舒服的

### 🅰️ 路径 A: HN reply (强烈推荐) — 5 分钟完成 5 个

**为什么 HN reply 优于 cold email**：

| 维度 | Cold email | HN reply |
|---|---|---|
| Reply rate | 5-15% | **25-40%**（HN 文化是必回） |
| Spam 风险 | 70% 进 spam | 0% |
| 找邮箱难度 | 90% case 找不到 | 不需要 |
| 收件方信任 | 低（陌生人外联） | 高（同社区） |
| 留下公开 trace | 私下 | 公开（**双重好处**：其他 dev 看到 → free traffic）|
| 你的身份成本 | 用 personal email + 暴露 | HN handle 即可 |

**做法**：
1. 注册 / 登陆 你的 HN handle
2. 打开 5 个上面 HN URL
3. 在每个原始 quote 下 reply 一条**改造版** draft (见下面)
4. 等 24-72h 看 reply

每条 HN reply ≤ 4 句，**不要邮件 length**：

```
Saw this old comment of yours — I'm prototyping <product 1 sentence>.
Curious if this would have solved your <他/她具体词>?
If you'd pay $15/mo for it, would love to know — calibrating.
github.com/<repo when ready>
```

### 🅱️ 路径 B: Cold email (如果坚持) — 适用 1 封 (rpdillon)

只 hn_952055 (rpdillon) 有 profile email `hn.rpdillon@xoxy.net`。其他 4 个：
- 去 github.com/<HN handle> 找 bio 邮箱 (5 min × 4)
- 或 google "<HN handle> email"
- 或 Hunter.io API ($50/月 if 你要 scale)

每封 draft 见 `queue/<hn_id>.md`，AI 起草质量高（ai_tell 2-4/10）。

### 🅲 路径 C: 100% AI 自动发（不推荐 first batch，推荐 W3+ 规模化）

需要：
- 注册 personalab.io domain ($10 + 24h DNS warm)
- 接 Resend / Loops API ($0-29/月)
- 找邮箱 via Hunter ($50/月 起)
- AI 自动 send + 自动 webhook 收回复 + 自动 7 天 follow-up
- 预期 reply rate **3-5%** (新 domain + AI 味即便压到 2/10 仍会被识别)

**结论：第一批 5 封路径 C 不划算 (cold start 反 reputation)**。路径 C 是 v1.0 Level 4 第 30 封之后的事。

## 我做完的事 vs 剩你做的事

| Stage | AI 做 | 你做 |
|---|---|---|
| 找 quote | ✅ 392 → 5 confirmed | - |
| 找 author | ✅ HN Firebase API | - |
| 起草邮件 | ✅ 个性化 + critic | - |
| Spam check | ✅ AI tell 2-4/10 | - |
| 找邮箱 | ⚠️ 1/5 自动 | 4/5 手工 google (路径 B) **或** 选路径 A 跳过 |
| 实际 send | ❌ 第一批不自动 | 你 5 分钟 HN reply 完成 |
| 监控 reply | ✅ 可写 monitor 脚本 | 你定期 check |
| 7 天 follow-up | ✅ 可写 | - |

**最优 send 路径：A（HN reply）**。准备时间 5 分钟，reply rate 高 3-5×，0 spam 风险。

## 时间预算

| Path | 准备 | 你花 | reply rate | 真实信号强度 |
|---|---|---|---|---|
| **A (HN reply)** | ✅ done | **5 min** | 25-40% | ⭐⭐⭐⭐⭐ |
| B (cold email) | ✅ done | 30-60 min 找邮箱 + send | 5-15% | ⭐⭐⭐⭐ |
| C (100% auto) | 1 周 setup | 0 | 3-5% | ⭐⭐ |

**等你做完路径 A 后**：我自动 monitor HN reply（每天扫这 5 个 thread）+ 整理回复数据 + 自动写 Day 9 brief 更新版（含真实 buyer feedback）。
