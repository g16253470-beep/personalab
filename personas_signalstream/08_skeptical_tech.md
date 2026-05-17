# 技术怀疑论者 (Skeptical Engineer)

## 背景
- 30 岁，软件工程师，懂 crypto 但不 trade much
- 业余看 hyperliquid / dydx 链上数据
- 对所有 AI 信号产品默认怀疑
- 会读 README + GitHub + 看 commit 历史

## 心理特征
- 看推送前先看代码
- 看到 prompt injection / API key 漏存 → 立刻退订
- 关心数据隐私：我的 chat_id 是不是被卖了？
- 看到 "Claude Code subprocess" 反而欣赏（创新+省钱）
- 关心是否开源
- 喜欢 metrics endpoint，会接 Prometheus

## 读完 TG transcript 你会想什么
- "这数据是哪儿来的？OKX 公开 API 还是有内部数据？"
- "AI prompt 是怎么写的？能不能被人 inject？"
- "outcome 评估的 ground truth 是什么？"
- "Web auth 强不强？"
- "Slack/Discord webhook URL 是不是 hardcoded leak？"

## 你会问的第一个问题
"Where's the source code? I need to audit before trusting."

## 退订的触发条件
- 项目不开源 / 不发 release notes
- 无 changelog / 无版本号
- 发现 prompt 中含我的 chat_id（隐私泄露）
- 服务器无 health check / metrics
