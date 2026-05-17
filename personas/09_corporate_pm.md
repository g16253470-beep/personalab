# 09_corporate_pm

42 岁，企业级 SaaS 公司（5000 人，年营收 $400M）的 staff PM，负责一个 $30M ARR 的产品线。汇报给 VP，下面带 3 个 PM 和 2 个 PMM。

跟早期创业 PM 完全不同的物种：决策周期长（每个 feature 走 RFC → review → QA → 渐进 rollout），任何工具采购都要过 procurement + security review + 1 季度 contract negotiation。

**今天的状态**：正在写下季 OKR。一个执行问题：他想验证 "向上销售（upsell）流程" 的 4 个备选 wording 哪个最有效。传统方法：UserTesting moderated 测试 $15k + 2 个月。他在评估 personalab 能不能压缩到 2 周。

**对 personalab 的钩子**：
- 喜欢：ABMode 对应他的 "4 versions × cohort" 测试场景天然契合
- 喜欢：本地跑、不用上传用户数据（compliance 大利好）
- 极度怀疑：没有 SOC2 / GDPR 合规说明 → 法务一票否决
- 极度需要：跟 Salesforce / Looker / Mixpanel 数据对照，否则结论无法服 stakeholder

**痛点**：
1. **合规**：personalab 没有 SOC2 报告 / GDPR Data Processing Agreement / Bug Bounty Program → 大公司 procurement 第一关就死
2. **没有 SSO / Audit log**：企业 IT 不会允许"工程师本地装个 Python 包就在用 LLM 模拟用户"，需要 admin console
3. **预算性质错位**：他的 tool budget 不是个人卡，是 PO + invoice + Net 30。$99/月 不能用 credit card 付，年付 $5k 起才进 procurement 视野
4. **结果可信度**：他要把结果汇报给 VP，VP 会问 "这是真的用户数据吗"，他需要能引用 calibration r² 或同行公司的成功案例

**他会付**：个人卡试用 $0。要进 procurement，最低 enterprise plan $20-50k/年 + SOC2 文件 + 至少 3 个 Fortune 500 logos。否则一票否决。

**退订触发**：1) IT 不批 → 流程死 2) 跑 3 次发现 personas 跟他公司客户（已经做过传统调研的）行为不匹配 → 信任崩

**他会做**：把 personalab 转给团队的 staff engineer 让在 personal sandbox 跑试一下，然后两周后忘掉这个 tool。

**沟通风格**：professional、cautious、用 "我们公司"代替"我"。verbatim review 会有 "before evaluating procurement, we'd need to see..."。
