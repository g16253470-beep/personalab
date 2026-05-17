# signalstream — Jury Mode（多模型评委）

生成: 2026-05-17 23:39 UTC+8 · 事件: 25 · 陪审团: 2 个模型

模型列表:

- `anthropic-api/claude-sonnet-4-6`
- `anthropic-api/claude-haiku-4-5`

## 订阅意愿矩阵

| 人格 | anthropic-api/claude-sonnet-4-6 | anthropic-api/claude-haiku-4-5 | overall_agree |
|---|---|---|---|
| 01_burnt_veteran | ⚠ maybe q7 | ❌ no q9 | **0.67** |
| 02_junior_quant | ❌ no q9 | ❌ no q9 | **1.0** |
| 03_scalper | ⚠ maybe q7 | ❌ no q9 | **0.67** |
| 04_swing_trader | ❌ no q9 | ❌ no q9 | **1.0** |
| 05_anxious_beginner | ❌ no q9 | ❌ no q9 | **1.0** |
| 06_signal_reseller | ⚠ maybe q7 | ❌ no q9 | **0.67** |
| 07_noise_allergic_manager | ❌ no q10 | ❌ no q10 | **1.0** |
| 08_skeptical_tech | ❌ no q9 | ❌ no q9 | **1.0** |
| 09_competitor_ceo | ❌ no q10 | ❌ no q10 | **1.0** |
| 10_compliance_officer | ❌ no q10 | ❌ no q9 | **1.0** |
| 11_twitter_troll | ERR | ✅ yes q9 | **0.0** |
| 12_yc_partner | ❌ no q8 | ❌ no q8 | **1.0** |

## 月费意愿矩阵

| 人格 | anthropic-api/claude-sonnet-4-6 | anthropic-api/claude-haiku-4-5 | agree |
|---|---|---|---|
| 01_burnt_veteran | 5-20 | 0 | 0.5 |
| 02_junior_quant | 0 | 0 | 1.0 |
| 03_scalper | 20-50 | 0 | 0.5 |
| 04_swing_trader | 0 | 0 | 1.0 |
| 05_anxious_beginner | 0 | 0 | 1.0 |
| 06_signal_reseller | 50-200 | 0 | 0.5 |
| 07_noise_allergic_manager | 0 | 0 | 1.0 |
| 08_skeptical_tech | 0 | 0 | 1.0 |
| 09_competitor_ceo | 0 | 0 | 1.0 |
| 10_compliance_officer | 0 | 0 | 1.0 |
| 11_twitter_troll | — | 0 | ? |
| 12_yc_partner | 0 | 0 | 1.0 |

## ⚠️ 低一致性人格（overall_agree < 0.66）

这些人格在不同 LLM 间分歧大 —— 不要据其单一结论决策。

### 11_twitter_troll (agree=0.0)
- **anthropic-api/claude-sonnet-4-6**: ERROR — Expecting ',' delimiter: line 4 column 34 (char 90)
- **anthropic-api/claude-haiku-4-5**: yes / q9 / $0

