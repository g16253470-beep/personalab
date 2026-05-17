# signalstream 人格静态测试报告

生成时间: 2026-05-17 23:35 UTC+8  ·  样本事件: 25  ·  LLM: anthropic-api/claude-sonnet-4-6

## 📊 汇总

| 人格 | 会订阅 | 退订风险 | 愿付 USD/月 | 第一抱怨 |
|---|---|---|---|---|
| 01_burnt_veteran | ⚠ maybe | 7/10 | 0 | 25条推送里每一条的「根因」全是同一句话「量价背离 / 资金费率倒挂」，这是复制粘贴的假分析还是系统bug？conf=low的信号凭什么发出来，LOW prio |
| 02_junior_quant | ❌ no | 9/10 | 0 | 每条信号的 conf 标签和 primary trigger 完全没有统计定义——vol_breakout 的阈值是什么？z-score 还是绝对值？lookb |
| 03_scalper | ⚠ maybe | 7/10 | 20-50 | HIGH信号里混着BNB/PEPE/DOGE/SOL，我只要BTC和ETH。25条推送里真正有用的只有3条（BTC HIGH x3，ETH HIGH x1），其 |
| 04_swing_trader | ❌ no | 9/10 | 0 | 90分钟内轰炸25条推送，全是分钟级噪声，没有一条给我24h OI趋势或funding连续变化天数。conf=low的信号占一半，历史命中率完全缺失，这些信号对 |
| 05_anxious_beginner | ❌ no | 9/10 | 0 | 从11点到1点，25条消息轰炸过来，每条都是funding_flip、oi_spike、taker_imbalance……我一个都看不懂！这到底是让我买还是卖？ |
| 06_signal_reseller | ⚠ maybe | 7/10 | 50-200 | 信号频率还行，一小时20多条够填群了。但他妈的没有止损价、没有入场点、没有「做多/做空」的明确动作指令——就给我个🔴🟢颜色和conf=low？我客户要的是「BT |
| 07_noise_allergic_manager | ❌ no | 10/10 | 0 | 从11:33到13:00不到两小时就轰炸了25条，第一条就是DOGE LOW级别，我连BTC的第一条都还没看到就已经想静音了。DOGE、PEPE、BNB这些跟我 |
| 08_skeptical_tech | ❌ no | 9/10 | 0 | 所有根因都是同一句话 'fake root cause #N: 量价背离 / 资金费率倒挂'——这是模板占位符没替换干净，说明要么系统根本没有真正的根因分析，要 |
| 09_competitor_ceo | ❌ no | 10/10 | 0 | 每一条信号的根因全是'量价背离 / 资金费率倒挂'——这是复制粘贴的 placeholder，不是分析。20分钟内发25条信号，conf=low 的照发，没有一 |
| 10_compliance_officer | ❌ no | 10/10 | 0 | 这个系统对DOGE、BNB、BTC、ETH等永续合约资产持续输出方向性信号（红色=看空、绿色=看多）并标注置信度，这在法律实质上构成投资建议，而非中性信息。'仅 |
| 11_twitter_troll | ✅ yes | 2/10 | 0 | 每条信号的'根因'全都是'量价背离/资金费率倒挂'，一字不差复制粘贴了25次。这不是AI分析，这是Ctrl+C Ctrl+V Bot，连换个说法的功夫都省了，素 |
| 12_yc_partner | ❌ no | 8/10 | 0 | 这整个 transcript 就是一堆信号 noise，没有任何 outcome tracking——我怎么知道这些信号有没有用？所有根因都是同一句话'量价背离 |

## 🗣 详细反馈

### 01_burnt_veteran

- **会订阅**: maybe
- **退订风险**: 7/10
- **愿付月费**: 0
- **吐槽**: 25条推送里每一条的「根因」全是同一句话「量价背离 / 资金费率倒挂」，这是复制粘贴的假分析还是系统bug？conf=low的信号凭什么发出来，LOW priority的DOGE/PEPE占了一半，这噪音比我2021年那个骗局的群还多。
- **欣赏**: 有conf分级、有evidence字段、有🔴HIGH标识，至少没有出现「必涨」「稳赚」字样，格式克制没有乱用emoji。
- **TOP 3 改进**:
  - 每条信号的根因必须是真实差异化的文本，不能25条全写同一句，否则直接判定为ChatGPT套壳或数据mock
  - 提供可验证的历史命中率页面，包含原始timestamp+价格+结果，允许第三方审计，不接受截图
  - conf=low的信号默认静音或折叠，用户自选是否接收，2小时内25条推送已超出可接受阈值
- **原话**:
  > 好，先别急着退。格式还算干净，没跟我说'保证盈利'，这比那个Big Pump群强一点。但我翻了25条，根因全是同一行字——这要么是demo数据要么是系统没接真分析模块。你们的AI到底在做什么？vol和taker我懂，但为什么conf=low的信号还要推给我？我现在最想知道的是：给我一个链接，让我自己去查你们过去30天HIGH信号的hit rate，原始数据，不要截图。做不到这一点，我下周就退。

### 02_junior_quant

- **会订阅**: no
- **退订风险**: 9/10
- **愿付月费**: 0
- **吐槽**: 每条信号的 conf 标签和 primary trigger 完全没有统计定义——vol_breakout 的阈值是什么？z-score 还是绝对值？lookback window 多长？'conf=low' 但信号方向是 HIGH 这种矛盾出现了好几次，说明 confidence 和 direction 是两套独立逻辑，没有任何文档解释它们怎么合并。这根本没法机器消费。
- **欣赏**: 信号频率合理，primary trigger 分类（funding_flip / vol_breakout / oi_spike / taker_imbalance / premium_swing）有一定结构，至少说明底层用了多维度数据源。
- **TOP 3 改进**:
  - 提供 raw event JSON 或 CSV/parquet 导出接口，包含所有字段（trigger 原始值、阈值、lookback、timestamp），让我能自己跑 backtest
  - 公开每个 trigger 指标的计算方法文档：z-score 的 lookback n 是多少、funding_flip 的翻转幅度阈值是绝对值还是百分位、oi_spike 用的是什么基准窗口
  - 提供 webhook / REST API 输出稳定 schema，同时披露 outcome 评估的 hit-rate baseline（相对 BTC 还是绝对 USDT PnL，评估窗口多长）
- **原话**:
  > 看了半小时，最大的问题是这些信号完全是黑箱输出，我没有任何办法验证它。'conf=high' 是基于什么分布？样本量够吗？funding_flip 的触发条件是 hardcoded 阈值还是自适应的？更诡异的是信号 #16 是 HIGH direction 但 conf=low，信号 #3 是 HIGH direction 但 conf=mid——direction 和 confidence 的关系完全不透明。我在股票那边任何因子上线前都要先跑 IC/IR，这里连 raw event 都导不出来让我怎么 backtest？没有 webhook，没有 schema 文档，没有指标计算细节，这对我来说就是不可用的产品，$0。

### 03_scalper

- **会订阅**: maybe
- **退订风险**: 7/10
- **愿付月费**: 20-50
- **吐槽**: HIGH信号里混着BNB/PEPE/DOGE/SOL，我只要BTC和ETH。25条推送里真正有用的只有3条（BTC HIGH x3，ETH HIGH x1），其他全是噪音。没有过滤功能的话这频道对我来说跟垃圾桶没区别。
- **欣赏**: BTC HIGH推送间隔约7-9分钟，格式极简，没有废话段落，扫一眼就知道是什么信号类型。
- **TOP 3 改进**:
  - 支持按 pair+level 订阅过滤：只推 BTC/ETH PERP · HIGH，其他全屏蔽
  - 每条信号加上触发时的实时价格和OI变化数值，没数字等于没信号
  - 删掉「根因」和「conf」字段，或折叠成可选项，正文只保留 pair / level / signal_type / price / timestamp
- **原话**:
  > OK格式还行，不啰嗦，这点给分。但25条里我能用的就BTC HIGH那几条，ETH HIGH一条。DOGE PEPE BNB HIGH我根本不交易，全是干扰。更大的问题：没有价格数字，只告诉我vol_breakout，我怎么知道当时BTC在哪？你这信号到我手里我还要自己去看盘，那你存在的意义是什么？如果能设置'只推BTC+ETH HIGH，附带触发价和OI变化%'，我愿意付钱。现在这个状态，maybe，等我看完一周延迟数据再说。

### 04_swing_trader

- **会订阅**: no
- **退订风险**: 9/10
- **愿付月费**: 0
- **吐槽**: 90分钟内轰炸25条推送，全是分钟级噪声，没有一条给我24h OI趋势或funding连续变化天数。conf=low的信号占一半，历史命中率完全缺失，这些信号对4h+持仓者毫无参考价值。
- **欣赏**: 信号涵盖funding_flip、oi_spike、taker_imbalance等衍生品维度，方向上有一定结构感。
- **TOP 3 改进**:
  - 提供每日/每周聚合摘要，合并同资产信号，给出24h维度的OI和funding趋势，而不是逐条实时推送
  - 每条信号附上历史命中率（要求n≥20样本），并注明该信号在1h/4h/1d多时间尺度上的一致性
  - 加入宏观背景标注（DXY/SPX方向）以及funding持续天数、long_short比率绝对值，不只列信号类型
- **原话**:
  > 我一打开频道，90分钟25条消息全堆在那里。DOGE LOW conf=low，PEPE HIGH conf=low，这种东西我连看都不想看。我需要的是：BTC的funding已经连续负3天了吗？ETH的OI过去24h是净增还是净减？现在DXY在反弹还是破位？一条都没有。更别说历史命中率，你给我推一个信号却不告诉我这类信号过去赢了几次，我凭什么动仓位？这产品明显是给刷单或5分钟scalper设计的，跟我的交易周期完全对不上。除非出一个专属的周报模式，否则我不会付一分钱。

### 05_anxious_beginner

- **会订阅**: no
- **退订风险**: 9/10
- **愿付月费**: 0
- **吐槽**: 从11点到1点，25条消息轰炸过来，每条都是funding_flip、oi_spike、taker_imbalance……我一个都看不懂！这到底是让我买还是卖？绿色是涨红色是跌吗？conf=low又是啥意思？我完全不知道该怎么办。
- **欣赏**: 红绿黄颜色区分还算直观，至少我知道红色可能是警告，绿色可能是好事，这个我勉强能猜到。
- **TOP 3 改进**:
  - 每条信号末尾加一句大白话结论，比如「建议观望，暂不操作」或「BTC短期风险上升，持有者注意」
  - 提供「新手模式」，隐藏所有技术术语（funding/OI/taker/premium），只显示币种+颜色+一句话建议
  - 消息数量太多，提供「仅看HIGH级别」或「每日汇总一条」的过滤选项，别把25条全推给我
- **原话**:
  > 我就看了第一条，DOGE/PERP，funding_flip，conf=low，evidence=vol,taker……我直接懵了。我不知道PERP是什么，我不知道funding_flip是什么，我甚至不知道这条消息是在告诉我好消息还是坏消息。然后我划下去，还有24条！都是这种格式！我朋友说这个很好用，但他玩了两年了，我才玩三个月。这个app根本不是给我这种人设计的。我现在就想知道：我手里的BTC和ETH，现在该拿着还是该卖掉？就这一个问题。能不能给我一个答案？

### 06_signal_reseller

- **会订阅**: maybe
- **退订风险**: 7/10
- **愿付月费**: 50-200
- **吐槽**: 信号频率还行，一小时20多条够填群了。但他妈的没有止损价、没有入场点、没有「做多/做空」的明确动作指令——就给我个🔴🟢颜色和conf=low？我客户要的是「BTC空 · 入场97200 · 止损97800 · 目标96000」这种格式，这玩意我没法直接转发，还得人工二次加工，那我买它干嘛？
- **欣赏**: 信号覆盖币种够多（BTC/ETH/SOL/DOGE/PEPE/BNB），频率高，每隔几分钟一条，能持续填充群内容节奏，不会冷场。
- **TOP 3 改进**:
  - 加入明确方向标签（做多/做空）+ 具体入场区间 + 止损/止盈价位，否则信号无法直接转发给零售客户
  - 提供B2B API接入 + 多chat_id转发 + 白标选项，隐藏SignalStream品牌，让我能以自己名义分发
  - 去掉或可配置'non-financial-advice'免责声明，或允许我在接入层自定义消息模板，不要强制附加干扰转售的免责文字
- **原话**:
  > OK频率我满意，一小时二十多条，我的群不会死。但这格式……conf=low、evidence=vol,taker——我他妈怎么转发给我1500个客户？他们要的是'现在买还是卖、在哪买、止损多少'，不是量化术语课。而且我看了半天没看到任何B2B入口，没API文档，没白标说明。如果这产品只卖给散户自用，那我就是错误客群。给我API+白标+可定制消息模板，我愿意付月费，不然我去找下一家。

### 07_noise_allergic_manager

- **会订阅**: no
- **退订风险**: 10/10
- **愿付月费**: 0
- **吐槽**: 从11:33到13:00不到两小时就轰炸了25条，第一条就是DOGE LOW级别，我连BTC的第一条都还没看到就已经想静音了。DOGE、PEPE、BNB这些跟我有什么关系？完全是噪音。
- **欣赏**: BTC/ETH HIGH级别的几条信号（#3、#5、#11、#21）理论上是我需要的，格式简洁，一眼能看出币种和级别。
- **TOP 3 改进**:
  - 必须支持白名单过滤：只推BTC和ETH，其他币种永远不出现在我的推送里
  - 每日上限1-2条，HIGH级别才推，MID和LOW直接丢进周报摘要
  - BTC/ETH要有实际价格变动幅度（比如'BTC -5.2%'），不要只给信号类型，让我一秒判断是不是真大事
- **原话**:
  > 这是什么？我打开手机看到25条通知，第一条是DOGE LOW，我当时就想直接退订。你们知道我一天被多少垃圾信息轰炸吗？我要的是：BTC或ETH出了真正的大事，一条推送告诉我。不是DOGE资金费率倒挂，不是PEPE什么鬼信号。就算BTC那几条HIGH级别有点价值，但它们被淹没在这堆垃圾里，我根本不想翻。这个产品现在对我来说价值是零，除非你们给我一个只看BTC/ETH、每天最多一条的模式，否则我不会付一分钱。

### 08_skeptical_tech

- **会订阅**: no
- **退订风险**: 9/10
- **愿付月费**: 0
- **吐槽**: 所有根因都是同一句话 'fake root cause #N: 量价背离 / 资金费率倒挂'——这是模板占位符没替换干净，说明要么系统根本没有真正的根因分析，要么是 prompt 输出直接 hardcoded，AI 推理是假的。这是最硬的 red flag。
- **欣赏**: 信号结构字段设计还算清晰：primary trigger + secondary signal + conf level + evidence tags，格式工程上有点想法。
- **TOP 3 改进**:
  - 根因分析必须是真实的、per-signal 差异化输出，不能是占位符；公开 prompt 模板和数据 pipeline 架构图供审计
  - 提供 GitHub repo 或至少发布 changelog + 版本号，说明数据来源（OKX public API？内部 feed？）及采集频率
  - 加 /metrics endpoint（Prometheus 格式），暴露信号准确率回测数据、outcome ground truth 评估方法，以及明确声明 chat_id 等用户数据的存储与使用政策
- **原话**:
  > 我一眼就看到了：25 条消息，根因全是 'fake root cause #N'，这不是 AI 分析，这是一个 f-string 没填好。要么是演示数据没清理就推给用户，要么系统根本没有根因模块，只是在格式上贴了个标签糊弄人。conf=high 但根因是假的，这 confidence score 有什么意义？源码在哪？数据从哪拉的？prompt 长什么样？在我审完这三件事之前，这东西我不会订阅，更不会用来做任何交易参考。

### 09_competitor_ceo

- **会订阅**: no
- **退订风险**: 10/10
- **愿付月费**: 0
- **吐槽**: 每一条信号的根因全是'量价背离 / 资金费率倒挂'——这是复制粘贴的 placeholder，不是分析。20分钟内发25条信号，conf=low 的照发，没有一条附 outcome。这不是信号平台，这是噪音生成器。
- **欣赏**: 格式结构清晰，conf 分级和 evidence 字段设计方向对，至少在装模作样这件事上做得比较整齐。
- **TOP 3 改进**:
  - 每条信号必须公开 outcome 回填，7天内无结果标 EXPIRED，不然conf=high是自封的，毫无意义
  - 根因字段不能是全局统一模板，25条信号25条一样的根因说明你的 AI 根本没有运行，或者 system prompt 只有一行
  - 公开 90 天全量信号的 P&L，包括亏损，按方向（多/空）分类，否则任何 hit-rate 声明都是操纵
- **原话**:
  > 好，我把这个截下来发 Twitter。看见没——25条信号，根因100%相同，全是'量价背离/资金费率倒挂'。这不是 AI，这是 for loop。conf=high 是谁评的？你自己？基于什么样本？n=几？然后 DOGE LOW 和 BTC HIGH 同时出现，方向矛盾你怎么解释？更妙的是没有一条 outcome，你永远不知道哪条对了哪条错了。这就是'诚实账本'？我运营平台8年，这套我见过太多次了——用格式感制造专业幻觉，把数据审计权留给自己。Thread 写完了，等着。

### 10_compliance_officer

- **会订阅**: no
- **退订风险**: 10/10
- **愿付月费**: 0
- **吐槽**: 这个系统对DOGE、BNB、BTC、ETH等永续合约资产持续输出方向性信号（红色=看空、绿色=看多）并标注置信度，这在法律实质上构成投资建议，而非中性信息。'仅供参考'免责声明在此场景下完全无效。
- **欣赏**: 信号标注了置信度等级（low/mid/high）和证据来源，说明系统有内部评估机制，若转型为纯数据展示工具尚有合规空间。
- **TOP 3 改进**:
  - 立即停止向用户推送方向性信号（红/绿/黄色 + HIGH/MID/LOW风险标签），改为中性数据流，不得暗示买卖方向
  - 申请所在司法管辖区的投资顾问牌照，或聘请持牌机构作为信号发布主体并承担合规责任
  - 删除或彻底隔离数据库中存储的 action: long_entry / short_entry 等意图性字段，防止被视为系统性交易建议的证据
- **原话**:
  > 我看完这份记录，结论非常清晰：这是一个未经注册的投资顾问服务。红色信号对应看空、绿色对应看多、置信度high加上永续合约标的——这不是'数据展示'，这是交易指令的变体。免责声明一行字挡不住实质认定。更严重的是，系统后端存有结构化信号字段，这在调查时会作为意图证据使用。我将发出正式警告函，要求7天内停止面向零售用户推送此类内容，并提交合规整改方案。逾期不整改，将启动罚款及强制下架程序。

### 11_twitter_troll

- **会订阅**: yes
- **退订风险**: 2/10
- **愿付月费**: 0
- **吐槽**: 每条信号的'根因'全都是'量价背离/资金费率倒挂'，一字不差复制粘贴了25次。这不是AI分析，这是Ctrl+C Ctrl+V Bot，连换个说法的功夫都省了，素材已经够我发三条thread了。
- **欣赏**: 推送频率够高、格式整齐，截图素材充足，反而帮我省了找料的时间，感谢。
- **TOP 3 改进**:
  - 根因描述至少别25条全一样，这太容易被截图dunk了
  - conf=low还要发出来？低置信度信号发出来等于承认自己在发噪音
  - 同一个币20分钟内发绿/红互相矛盾的信号（BNB 11:37红→11:40绿，DOGE一天内四种状态），能加个自动去重或冷却期吗
- **原话**:
  > bro我订了这个bot两小时，它给我发了25条信号，每一条的'根因'都是'量价背离/资金费率倒挂'。二十五条。一字不差。PEPE conf=high建议买，十分钟后PEPE conf=low建议卖，同一个bot同一个币。然后BNB今天拿到了🟢🟡🔴全套勋章。这不是信号，这是随机数生成器加了个中文模板。thread明天见，素材已经拉满，谢谢这个产品，真的，谢谢 💀🧵

### 12_yc_partner

- **会订阅**: no
- **退订风险**: 8/10
- **愿付月费**: 0
- **吐槽**: 这整个 transcript 就是一堆信号 noise，没有任何 outcome tracking——我怎么知道这些信号有没有用？所有根因都是同一句话'量价背离/资金费率倒挂'，这是 copy-paste 占位符还是真实分析？conf=low 的信号发出来有什么意义？没有胜率记录，没有 P&L，这不是产品，是个 alert spammer。
- **欣赏**: 信号分层（HIGH/MID/LOW）+ 多维 evidence 标注（vol, taker）的格式设计有一定结构感，工程执行看得出用心。
- **TOP 3 改进**:
  - 砍掉 80% 信号噪音，只推 conf=high 且有历史胜率背书的信号，并附带该类信号过去 30 天 hit rate（公开可审计账本）
  - 每条根因必须差异化——'量价背离/资金费率倒挂'出现在每一条信号是 credibility killer，用真实计算值替代占位符
  - 加入信号结果追踪闭环：信号发出后 X 分钟内价格变动自动回填，让用户能评估 ROI，这才是真正的 defensibility
- **原话**:
  > Okay, I skimmed this. Competent engineer, clearly knows how to pipe data and format a Telegram bot. But what am I looking at? 25 signals in 90 minutes, half of them conf=low, and every single root cause is the exact same string. That's a template bug, not an analysis engine. There's zero outcome data—did any of these signals make money? I have no idea. Coinglass is free. ChatGPT can explain funding rate divergence. What's the actual edge here? Until you show me a verified hit-rate ledger with 500+ signals tracked, and 100 traders who paid for it, this is a feature demo, not a business. Come back when you have that.

## 🔄 跨人格模式

最常被提到的关键词（≥2 人格）:
（无关键词被 ≥2 个人格提到）
