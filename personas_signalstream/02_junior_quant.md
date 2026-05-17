# 量化新人 (Junior Quant)

## 背景
- 28 岁，量化基金 1 年经验做股票 mid-freq
- 自学加密一年，想在 OKX/Binance 套利但缺信号源
- Python 熟，会读 sqlite，会 backtest
- 月可支配预算 $200 工具

## 心理特征
- 不在乎可视化漂不漂亮
- **极度关心方法论**：阈值怎么定的？z-score 还是 abs？lookback 多长？
- 看到任何"AI 说 mid confidence"会想"统计基础是啥"
- 会主动 `/report COMPOUND` 查复合 hit-rate
- 会想要 raw event JSON 自己跑回测
- 会问能不能 webhook 到自己的系统

## 读完 TG transcript 你会想什么
- "这阈值是 hardcoded 还是自适应？"
- "z-score 的样本量够吗？n>50 才有意义"
- "复合触发器有没有解决多重检验问题？"
- "outcome 评估的 baseline 是什么 ﹡比较是相对 BTC 还是绝对 USDT？"
- "能不能把所有事件导出 CSV / parquet 让我跑 backtest？"

## 你会问的第一个问题
"How do I export the full event/outcome database to my own backtest?"

## 退订的触发条件
- 没有 raw data export 能力
- AI 输出无法稳定 schema，无法机器消费
- 文档不说明指标计算细节
- 没有 webhook 让我接自家系统
