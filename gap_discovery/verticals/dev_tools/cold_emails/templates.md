# Cold email templates — dev tools vertical

3 个 variant 测试不同 angle。每个 ≤120 词。发送时间：周二/三 上午 10am 收件人当地时区。

---

## Variant A — "quote your pain back to you"

**Subject**: re: your <date> r/<sub> post about <pain point>

> Hey <first_name>,
>
> Saw your <date> post on r/<sub> about <one-line specific pain>. I'm currently mapping unmet needs in dev tools — your post is one of <N> independent complaints I've found mentioning <specific friction>.
>
> Two quick questions, will use them to focus next month's research:
>
> 1. Did you ever find a tool that fixed this? If yes, what's the gap that's still there?
> 2. If someone shipped <hypothetical solution>, what would you pay per month, honestly?
>
> Not selling anything. I'll publish the synthesis publicly in 2 weeks and send you the report.
>
> Thanks,
> <name>

**Optimization hypothesis**：refer back to their post = high open rate + felt-seen. Best for people with strong specific complaints.

---

## Variant B — "I built a thing, found 12 people who'd pay, are you the 13th?"

**Subject**: 12 devs said they'd pay for <X> — wanted to check with one more

> Hi <first_name>,
>
> Quick context: I run a small open-source thing called personalab that simulates user reactions to product ideas. Last week I mapped <N> dev complaints from <sub/forum>. One cluster stood out: <specific pain>.
>
> I'm trying to find out if real money would actually move for this. 12 devs in my simulation said they'd pay $30-80/mo to fix it.
>
> Could you tell me in one line:
>
> - Is this actually a problem for you, or just for "those guys"?
> - At $X/mo, would you click "subscribe"?
>
> No deck, no demo. Just calibrating my model against real humans. I'll share the data once I have 30 responses.
>
> <name>

**Optimization hypothesis**：concrete numbers + tool reference create credibility. Best for engineering manager / senior dev who want hard data.

---

## Variant C — "harshest critic" (for hostile personas like OSS maintainers / VCs)

**Subject**: short, brutal question about <vertical>

> <first_name>,
>
> Short question, brutal welcome:
>
> I've been collecting complaints in <vertical> for 2 weeks. The pattern I keep seeing is <specific cluster>. Multiple people say this; multiple companies say they "addressed" it; nobody actually fixed it.
>
> Am I missing something obvious? Tell me what's wrong with the framing, what you'd buy or not, and at what price.
>
> Reply length: ≤3 lines. I'll send back what I find.
>
> <name>

**Optimization hypothesis**：respect for time + acknowledgment they know more than you = unlocks high-quality short reply from senior people. Best for staff/principal eng or VC partners.

---

## Tracking sheet (`targets.csv`)

```csv
email,first_name,role,company,source_quote_id,variant_sent,sent_date,replied,reply_quality_1_5,wtp_quote
alice@xxx.com,Alice,Staff Eng,AcmeCo,reddit_r_devops_xyz,A,2026-05-25,Y,4,"$50/mo for sure"
```

## Compliance / ethics

- 全部 public-source email (GitHub bio / blog signature / public Twitter)
- 第一封邮件 + 后续最多 1 封 follow-up（7 天后）
- 收件人 reply unsubscribe 立即移除
- 公开发布时所有 quote 默认匿名（first name + role only）
- GDPR / CAN-SPAM 合规：明确 unsubscribe 路径 + 真实发件人身份

## 预期 reply rate

| Variant | 期望 open | 期望 reply | 期望高质 reply (3-5 stars) |
|---|---|---|---|
| A (quote back) | 50% | 12-18% | 6-8% |
| B (data) | 40% | 8-12% | 4-6% |
| C (brutal) | 35% | 5-10% | 3-5% |

30 emails × 平均 10% reply = **3 个有意义对话**。20 emails 跑 4 周 → 6-10 对话 → 2-3 个意愿付费明确。

## 测试 A/B 协议

- 30 emails 总数
- 每个 variant 10 封
- 4 周收集 reply
- 算每个 variant 的 reply rate + WTP signal
- Day 9 brief 内公开

---

**注**：所有模板写完先**手动 review 全过一遍**再发，避免任何 LLM 痕迹（"I hope this email finds you well"等套话直接 spam folder）。
