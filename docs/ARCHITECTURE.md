# personalab — Architecture

## 一句话

把"AI 模拟用户"做成可复用的框架：给我一组人格 + 一个产品适配器，我给你诚实到刺耳的反馈。

## 五大抽象

```
┌─────────────┐    ┌──────────────┐    ┌───────────────┐
│   Persona   │    │ ProductAdapter│    │  LLMAdapter   │
│  (.md 文件) │    │  (你写的)    │    │ (Claude/GPT/G)│
└──────┬──────┘    └──────┬───────┘    └──────┬────────┘
       │                  │                   │
       └──────┬───────────┴───────────┬───────┘
              │                       │
              ▼                       ▼
       ┌─────────────┐         ┌─────────────┐
       │  TestMode   │ ──────► │  ModeResult │
       │ (策略选择)  │         │  (per-persona│
       │             │         │   dict 数组)│
       └─────────────┘         └──────┬──────┘
                                      │
                                      ▼
                               ┌──────────────┐
                               │   Reporter   │
                               │   (markdown) │
                               └──────────────┘
```

| 抽象 | 接口 | 实现 |
|---|---|---|
| **Persona** | `Persona`, `load_personas(dir)` | 12 个 SaaS dev-tool 默认人格 + 12 个 SignalStream 示例人格（对照组） |
| **LLMAdapter** | `LLMAdapter.complete(prompt)` | ClaudeCLI（内置）、AnthropicAPI、OpenAI、Gemini |
| **ProductAdapter** | `ProductAdapter.load_events / render_event / apply_action / ...` | PostHog case study（SaaS 模板）、SignalStream（事件流模板）、Toy（40-行最小演示）、personalab-meta（自测） |
| **TestMode** | `TestMode.run(personas, product, llm)` → `ModeResult` | Static、Agentic、Jury、AB、Stats |
| **Reporter** | `Reporter.render(result)` → markdown | Static、Agentic、Comparison、ActionLoop、Jury、AB、Stats、Calibration |

## 数据流

```
personas/*.md  ──► load_personas() ──► list[Persona]
                                         │
ProductAdapter ──► load_events() ─────► list[Event] ──┐
                                                       ▼
                                               TestMode.run() ──► ModeResult
                                                       ▲           │
LLMAdapter ──► parse_json_with_retry() ───────────────┘            ▼
                                                              Reporter.render()
                                                                   │
                                                                   ▼
                                                              markdown 报告
```

## 测试模式（L1-L5）

每个 mode 是 `TestMode` 的子类。可以叠加包装（`StatsMode(inner=StaticMode(...))`）。

| Mode | LLM 调用数 | 何时用 |
|---|---|---|
| **Static** | N（一人格一次） | 第一印象筛查，快速 |
| **Agentic** | N × (days + 1) | 多日行为，揭示 onboarding / 退订路径 |
| **Jury** | N × M（M 个 LLM） | 检测单模型偏差 |
| **AB** | 2 × inner_mode 总数 | 验证修复有效性 |
| **Stats** | N × repeats | 区分人格偏好 vs LLM 抖动 |

可以**嵌套**：`ABMode(inner=StatsMode(inner=AgenticMode(days=5), repeats=3), product_a=v126, product_b=v127)` 跑两版产品 × 多日 × 3 次重复。

## 报告与行动闭环（L2 + L7）

`ActionLoopReporter` 把所有人格的 `top_friction` 聚类成 P0/P1/P2 issue list，每条引用 ≥2 个人格的原话作为依据。这是从"研究"到"工程"的桥。

`CalibrationReporter`（L6）反过来：用真实用户行为做 ground truth，量化人格预测准确度。预测准 → 继续用；预测不准 → 改 personas 或限制使用范围。

## 目录结构

```
personalab/
├── src/personalab/
│   ├── core/              # 五大抽象 + 公共工具（产品无关）
│   │   ├── persona.py
│   │   ├── llm.py
│   │   ├── product.py     # ProductAdapter + Event + SubscriptionState
│   │   ├── mode.py
│   │   ├── reporter.py
│   │   ├── parsing.py     # JSON 重试解析
│   │   └── timeutil.py    # CST 时区
│   ├── adapters/          # LLM 后端（optional extras）
│   │   ├── anthropic_api.py
│   │   ├── openai_api.py
│   │   └── gemini_api.py
│   ├── modes/             # 测试模式
│   │   ├── static.py
│   │   ├── agentic.py
│   │   ├── jury.py
│   │   ├── ab.py
│   │   └── stats.py
│   ├── reports/           # 报告渲染
│   │   ├── static.py
│   │   ├── agentic.py
│   │   ├── comparison.py
│   │   ├── action_loop.py
│   │   ├── jury.py
│   │   ├── ab.py
│   │   ├── stats.py
│   │   └── calibration.py
│   ├── stats/             # 统计工具
│   │   └── confidence.py
│   ├── calibration/       # L6 真实对照
│   │   ├── dataset.py
│   │   └── metrics.py
│   └── cli.py             # personalab CLI 入口
├── examples/
│   ├── posthog_case/      # SaaS 模板：PostHog 7-day 评估
│   ├── signalstream/      # 事件流模板（SignalStream / okx_pulse）
│   ├── personalab_meta/   # personalab 自测的元 adapter
│   └── toy/               # 40 行最小演示
├── personas/              # 12 个示例人格
├── tests/                 # FakeLLM + in-memory db 的 smoke tests
└── docs/                  # 你正在读这个文件
```

## 解耦原则

- `core/` **永远** 不依赖 `examples/`、`adapters/`、外部产品代码
- `examples/<x>/` 是 ProductAdapter 的实现，**只** 反向依赖 `core/`
- `adapters/` 是 LLM 后端，依赖 `core/`，互不依赖
- `modes/` 和 `reports/` 互不依赖（reports 读 `ModeResult`，modes 不知道 reports 存在）

测试 `core/` 解耦：`grep -r "signalstream\|sqlite\|SignalStream" src/personalab/core/` 必须返回空。

## CLI 命令

```
personalab version
personalab run --mode {static,agentic,both,jury} --personas DIR --adapter NAME --db PATH [...]
personalab calibrate --predictions JSON --truth CSV
```

run 子命令的 `--llm` 接逗号分隔多个模型 spec，jury 模式下作为陪审团：

```
personalab run --mode jury --llm "claude-cli,openai:gpt-4o,gemini:gemini-2.5-pro" ...
```

## 扩展点

| 想加什么 | 在哪写 |
|---|---|
| 新 LLM 后端 | `adapters/<name>.py`，加 `LLMAdapter` 子类，更新 `adapters/__init__.py: build_llm()` |
| 新产品支持 | `examples/<your_product>/adapter.py`，实现 `ProductAdapter` |
| 新测试模式 | `modes/<name>.py`，加 `TestMode` 子类 |
| 新报告样式 | `reports/<name>.py`，加 `Reporter` 子类 |
| 新人格 | `personas/<NN_name>.md`（可选 YAML frontmatter） |

详见 [ADAPTER_GUIDE.md](ADAPTER_GUIDE.md) 和 [PERSONA_WRITING.md](PERSONA_WRITING.md)。
