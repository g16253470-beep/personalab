"""PostHogAdapter — case study #1 for personalab.

Material drawn from public PostHog assets (posthog.com, docs.posthog.com,
github.com/PostHog/posthog README, pricing page) as of 2026-05-18. All
verbatim brand content remains property of PostHog Inc.; this adapter only
restructures the public marketing surface into a 7-day evaluation journey.

Use:
    personalab run --mode both \\
      --personas ./personas \\
      --adapter posthog \\
      --llm claude-cli \\
      --days 5 --limit 7 --out-dir ./reports/posthog_case
"""
from __future__ import annotations

from typing import Any

from personalab.core.product import Event, ProductAdapter, SubscriptionState


PRICING_CONTEXT = """
**PostHog pricing (cloud, as of 2026-05-18, public)**:

| product surface | free tier | paid usage |
|---|---|---|
| Product Analytics | 1M events/mo free | $0.00005 / event after |
| Session Replay | 5k recordings/mo | $0.005 / recording |
| Feature Flags | 1M requests/mo | $0.0001 / request |
| Experiments | bundled with feature flags | same |
| Surveys | 250 responses/mo | $0.20 / response |
| Web Analytics | 1M pageviews/mo | $0.00005 / pageview |
| Data Warehouse | 1M rows/mo | $0.000015 / row |

Self-host: free forever (MIT license, you run it on your own infra).

vs competitors mentioned by Posthog:
- Mixpanel: bundled pricing, more enterprise, no session replay built-in
- Amplitude: similar tier, more focus on analytics depth
- LogRocket: session replay specialist, no analytics/feature flags
- Heap: auto-capture analytics, expensive at scale
- LaunchDarkly: feature flags specialist, expensive
""".strip()


def _journey_events() -> list[Event]:
    """7 events: Day 1-7 of a prospective PostHog user evaluating it."""
    base_ts = 1_731_000_000
    day = 86400
    return [
        Event(
            timestamp=base_ts + 0 * day,
            severity="high",
            category="onboarding",
            headline="Day 1 — landing page + 'Get started for free'",
            body={"narrative": (
                "你在 Twitter 看到 PostHog 的推文：'Stop renting your analytics. "
                "Self-host PostHog and own your data.' 点进 posthog.com，看到 hero："
                "'How developers build successful products' + 8 个产品 logo "
                "(Product Analytics / Session Replay / Feature Flags / "
                "Experiments / Surveys / Web Analytics / LLM observability / "
                "Data Warehouse)。\n\n"
                "右上角'Get started — free'按钮。点了，进入 sign-up：邮箱 + 密码 + "
                "工作邮箱推荐。没有 SSO / Google login。\n\n"
                "5 分钟后进入 dashboard，看到一个 onboarding wizard："
                "'1. Install SDK / 2. Send first event / 3. Build your first insight'。\n\n"
                + PRICING_CONTEXT
            )},
        ),
        Event(
            timestamp=base_ts + 1 * day,
            severity="high",
            category="install",
            headline="Day 2 — 装 SDK + 发出第一条 event",
            body={"narrative": (
                "你按 wizard 装 posthog-js。是 11 行 JS 嵌入 + 一个 project key。\n"
                "5 分钟后 Live Events 面板里看到你刚才点击的事件流。\n\n"
                "感觉：很顺。\n\n"
                "试图建第一个 Insight（funnel），界面有 8 个 tab "
                "(Trends / Funnels / Retention / Paths / Lifecycle / Stickiness / SQL Editor / HogQL)，"
                "信息密度很高，需要点 6 次才搞清楚 'Funnel'在哪。\n\n"
                "Free tier 限额：1M events/月。你查 docs 说目前 8k events/月，"
                "免费层够用很久。"
            )},
        ),
        Event(
            timestamp=base_ts + 2 * day,
            severity="mid",
            category="session-replay",
            headline="Day 3 — 启用 session replay",
            body={"narrative": (
                "session replay 是 PostHog 的 selling point。1 行代码启用，"
                "5 分钟后看到第一段真实用户操作录像。\n\n"
                "你看到一个用户在 checkout 页面卡 30 秒，"
                "鼠标在 'Apply Discount' 上反复 hover —— 这是金矿数据。\n\n"
                "免费层：5k 录像/月。你的 site MAU 600，估算够用。\n\n"
                "但 Storage 用量上来后：'After free tier, $0.005/recording'。"
                "心算：10k MAU 平均 3 sessions/月 = 30k recordings = $150/月。\n"
                "不便宜，但比 LogRocket 便宜（$199/月起，10k sessions）。"
            )},
        ),
        Event(
            timestamp=base_ts + 3 * day,
            severity="mid",
            category="feature-flags",
            headline="Day 4 — feature flags + experiments",
            body={"narrative": (
                "你用 feature flag 上了第一个 A/B：homepage hero copy 改两版。\n"
                "PostHog UI 4 步配置完：targeting / split / metric / launch。\n\n"
                "比 LaunchDarkly 简单（LaunchDarkly $20/seat/月 + per-event 收费），"
                "PostHog 1M requests 免费。\n\n"
                "experiment 结果 5 天后跑出来，statistical significance 自动算，"
                "支持 Bayesian + frequentist 两种。\n\n"
                "踩坑：你想看 'experiment x analytics 交叉表'，发现要写 HogQL（PostHog 自家 SQL）。"
                "你不熟 HogQL，看了 docs 30 分钟才搞定。"
            )},
        ),
        Event(
            timestamp=base_ts + 4 * day,
            severity="high",
            category="cost-shock",
            headline="Day 5 — 账单页面打开",
            body={"narrative": (
                "你查 Billing。免费层快用完了：events 92% / sessions 75%。"
                "下个月会撞免费层。\n\n"
                "你预估月成本：events $50 + session replay $80 + flags $10 = ~$140/月。\n\n"
                "对比备选：\n"
                "- 自建 PostHog（self-host）：服务器 ~$80/月 + 维护时间无价\n"
                "- Mixpanel：似类档位 $200+/月，没有 session replay\n"
                "- 各家 unbundled：Mixpanel $100 + LogRocket $200 + LaunchDarkly $80 = $380/月\n\n"
                "PostHog 的 bundle 是真省钱，但 $140/月你也得签 procurement。\n"
                "你公司 8 个人，没有正式 procurement，CFO 是 founder 自己。"
            )},
        ),
        Event(
            timestamp=base_ts + 5 * day,
            severity="mid",
            category="self-host-question",
            headline="Day 6 — 'self-host 还是 cloud？'",
            body={"narrative": (
                "你纠结 self-host：'free forever' 听上去诱人，但你看 docs："
                "'PostHog Self-Hosted: K8s deploy, 8 vCPU + 16GB RAM minimum, "
                "managed Postgres + ClickHouse + Redis + Kafka + 5 services'。\n\n"
                "Hetzner CCX23 (8 vCPU/32GB) = $50/月，但要你自己维护 ClickHouse 升级。\n"
                "你的工程师不会 ClickHouse。\n\n"
                "结论：self-host 适合 5000 events/sec 以上的中型公司，"
                "对你 600 MAU 等级是 overkill。\n\n"
                "继续看 PostHog Cloud。"
            )},
        ),
        Event(
            timestamp=base_ts + 6 * day,
            severity="high",
            category="decision",
            headline="Day 7 — 是否续费 / 升级",
            body={"narrative": (
                "一周用下来：\n"
                "- ✅ session replay 救了你一次 checkout bug\n"
                "- ✅ funnel insight 让你发现 sign-up 75% drop-off 在某一步\n"
                "- ✅ feature flag A/B 跑完得到清晰统计结果\n"
                "- ⚠️ HogQL 学习曲线\n"
                "- ⚠️ $140/月 不便宜\n"
                "- ⚠️ 7 个产品太多，多数用不上\n\n"
                "你的选项：\n"
                "1. UNSUBSCRIBE 完全不用，回到 Google Analytics + Hotjar\n"
                "2. /coin 只用 product analytics + session replay 两个 surface，关其他\n"
                "3. /profile self-host 转自建（前提：找一个 ClickHouse 熟手）\n"
                "4. /severity high 只在 launch 重要 feature 时启用 experiments\n"
                "5. DO_NOTHING 续 cloud，吃 $140/月"
            )},
        ),
    ]


class PostHogAdapter(ProductAdapter):
    """ProductAdapter exposing public PostHog evaluation journey to personas."""

    name = "posthog"

    def __init__(self) -> None:
        self._events = _journey_events()

    def load_events(self, limit: int | None = None,
                    since: float | None = None) -> list[Event]:
        events = list(self._events)
        if since is not None:
            events = [e for e in events if e.timestamp >= since]
        if limit is not None:
            events = events[:limit]
        return events

    def render_event(self, event: Event, **opts: Any) -> str:
        sev_icon = {"low": "🟢", "mid": "🟡", "high": "🔴"}.get(event.severity, "⚪")
        if opts.get("compact"):
            return (f"{sev_icon} {event.headline}\n"
                    f"   {event.body.get('narrative', '')[:200]}...")
        return (f"## {sev_icon} {event.headline}\n\n"
                f"{event.body.get('narrative', '')}\n")

    def available_actions(self) -> list[str]:
        return [
            "/profile self-host",       # 转自建
            "/coin analytics-only",     # 只用 product analytics + session replay
            "/severity high",           # 只在重大 launch 用
            "DO_NOTHING",
            "UNSUBSCRIBE",
        ]

    def actions_help(self) -> str:
        return (
            "- `/profile self-host` — 转自建（前提是有 ClickHouse 熟手）\n"
            "- `/coin analytics-only` — 只开 product analytics + session replay\n"
            "- `/severity high` — 只在重大 feature launch 时启用\n"
            "- `DO_NOTHING` — 今天不动\n"
            "- `UNSUBSCRIBE` — 完全弃用回到 GA + Hotjar"
        )

    def apply_action(self, state: SubscriptionState, action: str) -> str:
        action = action.strip()
        if action.startswith("/profile "):
            state.profile = action.split(" ", 1)[1].strip()
            return f"profile -> {state.profile}"
        if action == "/coin analytics-only":
            state.profile = "analytics-only"
            return "subset: analytics + session replay only"
        if action.startswith("/severity "):
            sev = action.split(" ", 1)[1].strip()
            state.min_severity = sev
            return f"severity={sev}"
        return super().apply_action(state, action)
