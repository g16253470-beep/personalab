# 写一个 ProductAdapter

让 personalab 测试你的产品，本质就是回答三个问题：

1. **用户能看见什么？** → `load_events()` 返回 `list[Event]`
2. **每个东西长什么样？** → `render_event(e)` 返回字符串
3. **(可选) 用户能做什么？** → `apply_action(state, action)` 修改订阅状态

## 最小可用版（约 40 行）

参考 `examples/toy/adapter.py`：

```python
from personalab.core.product import Event, ProductAdapter

class ToyAdapter(ProductAdapter):
    name = "toy"

    def __init__(self, events=None):
        self._events = events or self._default_events()

    def load_events(self, limit=None, since=None):
        events = list(self._events)
        if since is not None:
            events = [e for e in events if e.timestamp >= since]
        if limit is not None:
            events = events[:limit]
        return events

    def render_event(self, event, **opts):
        return f"[{event.severity.upper()}] {event.category}: {event.headline}"
```

这就够跑 **StaticMode**（人格读 transcript → verdict）。没了。

## 加 Agentic 支持（让人格"使用" N 天）

Agentic mode 让人格每天看一批消息、做一个动作。要补：

```python
def default_state(self) -> SubscriptionState:
    """初始订阅设定。默认 severity=mid，没有任何过滤。"""
    return SubscriptionState(profile="default", min_severity="mid")

def matches_filter(self, event, state) -> bool:
    """事件是否能"穿透"到用户当前的设定。"""
    rank = {"low": 0, "mid": 1, "high": 2}
    return rank.get(event.severity, 0) >= rank.get(state.min_severity, 1)

def apply_action(self, state, action) -> str:
    """处理人格发出的命令，返回 human-readable 结果。"""
    if action.startswith("/severity "):
        sev = action.split(" ", 1)[1].strip()
        if sev in ("low", "mid", "high"):
            state.min_severity = sev
            return f"severity={sev}"
    return super().apply_action(state, action)  # fallback to DO_NOTHING/UNSUBSCRIBE

def available_actions(self) -> list[str]:
    return ["/severity X", "DO_NOTHING", "UNSUBSCRIBE"]

def actions_help(self) -> str:
    return ("- `/severity low|mid|high` — 调整严重度门槛\n"
            "- `DO_NOTHING` — 今天不动\n"
            "- `UNSUBSCRIBE` — 退订")
```

`actions_help()` 直接进入 agentic prompt，让 LLM 知道有哪些动作可选。

`split_by_day()` 用基类默认实现就行（按时间均匀切片）。

## Real-product 完整版示例

仓库自带两个完整 ProductAdapter 作为参考：

**`examples/posthog_case/adapter.py`（~150 行）** —— 把 PostHog 公开 product surface
（landing page / signup / 各 product feature / pricing / billing）映射为
7-day evaluation journey。**最容易模仿的"非加密 SaaS"模板**。每个 day = 一个 Event，
body 含 narrative + 公开 pricing 表 + 竞品对比。`apply_action()` 处理 `/profile`、
`/coin analytics-only`、`/severity` 等用户决策。

**`examples/signalstream/adapter.py`（~220 行）** —— 从 sqlite 读真实事件流的
domain-specific adapter（okx_pulse 加密信号 bot），展示如何处理：

| 扩展 | 代码位置 |
|---|---|
| sqlite 读取真实事件 | `load_events()` 用 `sqlite3.connect` |
| TG 卡片样式渲染 | `render_event()` 含 emoji 和多行格式 |
| profile / coin presets | 顶部 dict + `apply_action()` 处理 `/profile`、`/coin`、`/coinset` |
| 严重度 + 类别 + 币种三重过滤 | `matches_filter()` |
| 静音 / quiet hours | `apply_action()` 处理 `/mute`、`/quietnight` |

## 校验 adapter

加一个 5 行测试，证明走通：

```python
def test_my_adapter():
    from your_module import YourAdapter
    from personalab.core.persona import load_personas
    from personalab.modes import StaticMode
    from tests.fakes import FakeLLM  # personalab 自带

    adapter = YourAdapter(...)
    personas = load_personas("personas/")[:3]
    result = asyncio.run(
        StaticMode().run(personas, adapter, FakeLLM(), {"limit": 5})
    )
    assert len(result.results) == 3
```

通了就 production-ready。

## 关键不变量

- `Event.severity ∈ {"low", "mid", "high"}`（personalab 的过滤逻辑依赖这个）
- `Event.timestamp` 是 unix epoch float（用于按时间分日）
- `Event.category` 是字符串（任意值，由你定义；用于 `matches_filter` 的可选过滤）
- `Event.body` 是 dict，存任何 render 时要用的字段
- `default_state()` 返回的 `SubscriptionState` 决定"新用户进来的初始体验"——**强烈影响**第一天的人格反应

## 该参考哪个 adapter 模板

- 你的产品是 **SaaS / web app**（有 landing page、pricing、N 个 feature surface）→ **复制 `posthog_case` adapter** 改 narrative
- 你的产品是**基于事件流的订阅式通知**（TG bot / push 通知 / 邮件订阅）→ 复制 `signalstream` adapter 改字段
- 你的产品形态完全不同（chat 应用、IDE 插件、CLI 工具）→ 从 `examples/toy/adapter.py` 起步重写
- 数据源不是 sqlite → 在 `__init__` 里改成你的数据源（API、Parquet、JSON、纯硬编码）

`core/` 不关心你的数据源，只要你输出 `list[Event]`。
