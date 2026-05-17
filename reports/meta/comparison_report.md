# personalab-meta 双轨人格测试对比

**生成**: 2026-05-18 00:24 UTC+8  ·  static events: 7  ·  agentic events: 7  ·  days: 5

## 方法对比

| 维度 | Static（Tier 2）| Agentic（Tier 4）|
|---|---|---|
| 输入 | 一次性 transcript | N 个虚拟日分段流，每日决策一次 |
| 人格 | 8 | 8 |
| LLM 调用 | 8 | ~48 |
| 决策点 | 1 次（看完即评） | N+1 次/人格（每日 + 最终verdict）|
| 可观察行为 | "如果是我，我会..." | 实际切配置 / mute / 退订 |
| LLM | anthropic-api/claude-sonnet-4-6 | anthropic-api/claude-sonnet-4-6 |

## 总结果对比

| 人格 | Static | Agentic | 一致性 |
|---|---|---|---|
| 01_early_founder | maybe q7 | **no** $0 day4退 | ⬇️ 行为更严 |
| 02_growth_pm | maybe q7 | **no** $0 day4退 | ⬇️ 行为更严 |
| 03_user_researcher_hostile | no q9 | **no** $0 day1退 | ✅ 一致 |
| 04_vc_thesis | no q8 | **no** $0 day4退 | ✅ 一致 |
| 05_indie_hacker | maybe q7 | **no** $0 day4退 | ⬇️ 行为更严 |
| 06_research_consultant | maybe q4 | **no** $0 day5退 | ⬇️ 行为更严 |
| 07_oss_maintainer | maybe q6 | **no** $0 day4退 | ⬇️ 行为更严 |
| 08_ai_safety_skeptic | no q8 | **no** $0 day5退 | ✅ 一致 |

**Verdict count**:
- Static:  0 yes / 5 maybe / 3 no / 0 err
- Agentic: 0 yes / 0 maybe / 8 no / 0 err

**Agentic 把 5 个 'maybe' 打回原形成 NO** —— 一次性印象比多日体验宽容。

## Top 痛点关键词（agentic top_friction，≥2 人格）

（无关键词被 ≥2 个人格提到）

## 方法学结论

**Static 测试有用但乐观偏移**：一次性 transcript 给了产品 benefit of doubt；Agentic 把 "maybe 我可能会试试" 转化成 "试过了，不行"。

**最具决定性的差距：跨日行为**：短 transcript 中只是 1-2 条异常的问题，多日运行就成 pattern。

## 💰 月费意愿分布（agentic verdict）

| 价位 | 人格 |
|---|---|
| $0 | 01_early_founder, 02_growth_pm, 03_user_researcher_hostile, 04_vc_thesis, 05_indie_hacker, 06_research_consultant, 07_oss_maintainer, 08_ai_safety_skeptic |

