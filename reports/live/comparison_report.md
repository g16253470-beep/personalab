# signalstream 双轨人格测试对比

**生成**: 2026-05-17 23:37 UTC+8  ·  static events: 25  ·  agentic events: 200  ·  days: 3

## 方法对比

| 维度 | Static（Tier 2）| Agentic（Tier 4）|
|---|---|---|
| 输入 | 一次性 transcript | N 个虚拟日分段流，每日决策一次 |
| 人格 | 12 | 12 |
| LLM 调用 | 12 | ~48 |
| 决策点 | 1 次（看完即评） | N+1 次/人格（每日 + 最终verdict）|
| 可观察行为 | "如果是我，我会..." | 实际切配置 / mute / 退订 |
| LLM | anthropic-api/claude-sonnet-4-6 | anthropic-api/claude-sonnet-4-6 |

## 总结果对比

| 人格 | Static | Agentic | 一致性 |
|---|---|---|---|
| 01_burnt_veteran | maybe q7 | **no** $0 day2退 | ⬇️ 行为更严 |
| 02_junior_quant | no q9 | **no** $0 day2退 | ✅ 一致 |
| 03_scalper | maybe q7 | **no** $0 day3退 | ⬇️ 行为更严 |
| 04_swing_trader | no q9 | **no** $0 day2退 | ✅ 一致 |
| 05_anxious_beginner | no q9 | **no** $0 day1退 | ✅ 一致 |
| 06_signal_reseller | maybe q7 | **no** $0 day3退 | ⬇️ 行为更严 |
| 07_noise_allergic_manager | no q10 | **no** $0 day1退 | ✅ 一致 |
| 08_skeptical_tech | no q9 | **no** $0 day2退 | ✅ 一致 |
| 09_competitor_ceo | no q10 | **no** $0 day2退 | ✅ 一致 |
| 10_compliance_officer | no q10 | **no** $0 day3退 | ✅ 一致 |
| 11_twitter_troll | yes q2 | **no** $0 day2退 | ⚠️ 矛盾 |
| 12_yc_partner | no q8 | **no** $0 day2退 | ✅ 一致 |

**Verdict count**:
- Static:  1 yes / 3 maybe / 8 no / 0 err
- Agentic: 0 yes / 0 maybe / 12 no / 0 err

**Agentic 把 3 个 'maybe' 打回原形成 NO** —— 一次性印象比多日体验宽容。

## Top 痛点关键词（agentic top_friction，≥2 人格）

- `AI` × 6 — 01_burnt_veteran, 02_junior_quant, 04_swing_trader, 08_skeptical_tech, 09_competitor_ceo, 12_yc_partner
- `噪声` × 2 — 04_swing_trader, 07_noise_allergic_manager

## 方法学结论

**Static 测试有用但乐观偏移**：一次性 transcript 给了产品 benefit of doubt；Agentic 把 "maybe 我可能会试试" 转化成 "试过了，不行"。

**最具决定性的差距：跨日行为**：短 transcript 中只是 1-2 条异常的问题，多日运行就成 pattern。

## 💰 月费意愿分布（agentic verdict）

| 价位 | 人格 |
|---|---|
| $0 | 01_burnt_veteran, 02_junior_quant, 03_scalper, 04_swing_trader, 05_anxious_beginner, 06_signal_reseller, 07_noise_allergic_manager, 08_skeptical_tech, 09_competitor_ceo, 10_compliance_officer, 11_twitter_troll, 12_yc_partner |

