# 写一个人格

人格是 personalab 的输入数据。写得好 = 测试有用；写得糙 = 12 份"客观、中立、感谢分享"。

## 文件位置 & 格式

```
personas/
├── 01_first_persona.md
├── 02_second_persona.md
└── ...
```

文件名 stem（不含 `.md`）就是 persona 的 ID。建议数字前缀方便排序。

可选 YAML frontmatter 用于结构化标签（不影响 LLM 阅读，但供报告分类）：

```markdown
---
segment: trader
archetype: scalper
hostility: friendly
---

# 03_scalper

35 岁的高频日内交易员，每天 10 小时盯盘...
```

## 一个人格 = 三层信息

### 1. 身份背景（who & why）

具体到刺痛感的程度。避免泛泛的 "He is a trader who wants to make money."

✅ **好**: "37 岁，金融工程出身，前对冲基金 quant，去年自营，今年靠 BTC 永续套利吃饭。账户里 12 万 USD，每天交易 30-80 次。"

❌ **差**: "He is a professional trader interested in crypto signals."

### 2. 心理钩子（what they care about）

人格的"过敏点"——什么会让他立刻退订？

✅ **好**: "对 noise 极度过敏。一次假信号毁三次成功带来的信任。看到中文/英文混排会觉得不专业。"

❌ **差**: "He values accuracy."

### 3. 行为习惯（how they act）

具体的使用模式 + 决策风格。

✅ **好**: "永远先看推送时间戳和数据来源，再看结论。如果引用源不明就直接划过去。每天 10 点和 22 点会集中看 TG 总结。"

❌ **差**: "He likes to read carefully."

## 必备 8 项检查表

每个人格 `.md` 至少要回答：

- [ ] **名字 + 年龄 + 一句话身份**（context anchor）
- [ ] **当前在用什么竞品**（mental anchor for comparison）
- [ ] **3-5 个具体痛点**（kill triggers）
- [ ] **愿付价位区间**（pricing realism）
- [ ] **退订触发条件**（≥1 个具体场景：连续几条假信号 / 推送某种内容 / 看到某句话）
- [ ] **欣赏什么**（avoid 100% negative — 否则 LLM 退化成"否定一切"）
- [ ] **沟通风格**（决定 verbatim_review 的语气：刻薄 / 礼貌 / 沉默 / 在 Twitter 写 thread）
- [ ] **任何反向偏见**（competitor CEO 会刻意找茬；compliance 会盯合规）

## 推荐人格组合（12 人）

参考 `personas/` 目录的 12 个 SaaS dev-tool 人格，结构上：

| 类别 | 数量 | 例子 |
|---|---|---|
| 友善目标用户 | 4-5 | early founder, growth PM, indie hacker, designer lead |
| 友善但挑剔 | 2-3 | research consultant, data team lead, corporate PM |
| 对抗 / 敌意 | 3-4 | user researcher hostile, VC thesis, OSS maintainer, AI safety skeptic |
| 边缘 / 非典型 | 1-2 | no-code user |

对照参考：`personas_signalstream/` 目录是另一组 12 加密交易者人格，用于 SignalStream 这种领域特定产品。

**对抗人格至少 25%**——它们独立指出的问题等于"工程必修课"。友善人格的反馈容易过宽（"听上去不错可以试试"）。

## 反模式（不要这么写）

### 1. 复合人格
"既是 scalper 又是合规专家又是 troll 的资深用户。"
→ LLM 会发疯调和这些特质，verdict 不稳定。**一人格一身份**。

### 2. 上帝视角描述
"He represents the segment of users who want X."
→ LLM 会去满足这种"代表性"，给出 product-team-flavored feedback 而不是真实反应。**第一人称侧写**。

### 3. 全负面
"Hates everything about UX, finds it ugly, will never pay."
→ LLM 给的 verbatim 全是骂街，没有信息量。**至少给 1 个欣赏点**，哪怕是"data 还行"。

### 4. 缺少 kill trigger
没写"什么情况下退订"。
→ Agentic 模式下人格会一直磨磨蹭蹭，N 天结束都不退订，数据不真实。

## 长度建议

- **min**: 800 字（中文）/ 250 词（英文）
- **max**: 2000 字 / 700 词
- 超过 2000 字 LLM 容易抓不到重点，verdict 变成对人格本身的总结，不是对产品的反应。

默认 12 SaaS 人格平均 ~1000 字，是 sweet spot。

## 写完后验证

跑一次 StaticMode（FakeLLM 即可，零成本）：

```bash
python tests/test_e2e_smoke.py
```

打开生成的 `static_report.md` 看：

- 每人的 `first_complaint` 是否反映他独特视角？还是 12 个人吐槽同样话题？（→ 后者说明人格区分度不够）
- `verbatim_reaction` 的语气是否符合人格？（→ 不符合说明性格描述不够具体）
- 价格分布是否合理？所有人都 $0 → 价格设定可能写得太悲观

## 让人格"演技"更稳的小技巧

1. **第一段写"今天早上的状态"**：让 LLM 立刻进入此刻视角
2. **引一句他的"口头禅"**：LLM 会在 verbatim 里复用
3. **写他的"今晚要做什么"**：让 verdict 时间线感更强
4. **加 1 个不重要的细节**：比如"养着一只 7 岁的柴犬叫 Mochi"，让 LLM 感到这是一个人不是一个 spec

最后：写完读一遍出声，能想象出这个人坐你对面骂你产品的样子，就成了。
