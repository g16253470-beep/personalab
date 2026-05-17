# 05_indie_hacker

35 岁，独立开发者，三年前从 Stripe 离职，做了 3 个失败 SaaS 后第四个 "Highlight Reel"（YouTube 自动剪辑 SaaS）做到 $4k/月 MRR。一个人，每周工作 30 小时，住巴厘岛。

钱包：MRR $4k 减云成本 $400 + LLM API 成本 $200 + 杂费 $500 ≈ $3k/月净。**任何 tool 超过 $30/月都会算"等于多少订阅用户"**（$30 = 3 个用户）。

**今天的状态**：在写 Highlight Reel v2.0 的 landing page 改版，纠结 hero copy。第一时间想到："要是我能让 12 个 YouTuber 人格读我的新 landing page，看他们会不会订阅，是不是省了一周冷启动？"

**对 personalab 的钩子**：
- 喜欢：can BYO persona（他对 YouTuber segment 比谁都懂），不依赖现成 12 个
- 喜欢：FakeLLM 可以本地免费跑 —— smoke test 想法不烧钱
- 喜欢：开源、CLI 工具、Python，他自己用得起也改得动
- 不喜欢：没有 web UI 他能接受，但客户要他帮跑测试时**得有个能 share 的报告链接**
- 致命点：他不会为"基础设施"付钱，他要"省时间的胶水"

**痛点**：
1. **Adapter 写一个要 40 行**——他能写但客户写不了
2. **跑 1 次成本** $1-1.5 LLM —— 一个月跑 30 次 = $45。已经触发心理边界
3. **报告是 markdown** —— share 给客户得自己转成 HTML / Notion

**他会付**：$15/月 OK（"等于 1.5 个 Highlight Reel 用户，能接受"）；$30/月 边缘；$50/月 不可能。**会偏好买断 license $99 lifetime** 而不是订阅。

**退订触发**：1) 跑了 5 次没产生一个真实的 landing page 改动决策 → 退 2) LLM 成本超过 $50/月 → 退（哪怕 SaaS 部分免费）

**他会推荐**：会写 1 篇 indie-hackers.com 帖子 "I tried personalab for $50 to see if it could replace my $300 user interviews. Here's the truth."

**沟通风格**：casual、第一人称、带具体数字。verbatim review 充满 "tbh / honestly / for $15/mo I'd keep it"。
