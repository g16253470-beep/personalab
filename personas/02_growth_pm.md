# 02_growth_pm

29 岁，Series-B SaaS 公司的增长 PM。年 OKR 是把 Free → Paid conversion 从 3.2% 拉到 4.5%。手下管 2 个工程师 + 1 个设计师 + 1 个数据分析师。

每周做 3 个 A/B 测试，结果出来通常 2 周后才有统计显著性。对"加快迭代速度"这件事的执念是宗教级的。今天早上刚跟 CMO 吵了一架——CMO 想直接上新 pricing page，PM 坚持要先 A/B。

**对 personalab 的钩子**：
- 兴奋点：用 personalab 在真实 A/B 之前跑一遍，**让 12 personas 预演 conversion impact**，能砍掉 30% 注定失败的实验
- ABMode 是杀手特性 —— "v1 pricing page" vs "v2 pricing page"，让人格自动 diff
- 报告自动生成 P0 issue list 可以直接丢给设计师，省一次会议

**痛点**：
1. 他需要的是**signed-up users**的反馈，不是泛泛"trader"或"researcher"——能不能 import 自己公司的 ICP 文档生成 personas？
2. 12 个 SignalStream 加密人格对他**完全无用**；如果不能 BYO persona，1 周后弃用
3. integration with Amplitude / Mixpanel？让 prediction 自动跟真实 conversion 数据对照

**价格敏感度**：他个人的 tool budget 是 $300/月（公司每张 SaaS 卡上限）。$99 还在 friction-free 区间。$199 要写 case 给 boss。但他能为公司挪出最多 $1500/月，如果是"team plan + Slack integration + history"。

**退订触发**：跑了 5 次 ABMode，发现 personas 的 diff predictions 跟真实 A/B 结果相关性 < 0.4 → 立刻退。

**他会付**：个人 $99/月 OK；team plan $499/月 OK 如果有 calibration 数据。

**沟通风格**：精炼，爱用 framework / 2x2 矩阵。verbatim review 会是一段 "I evaluated personalab on 3 axes: speed, quality, ICP fit. 7/10/4."
