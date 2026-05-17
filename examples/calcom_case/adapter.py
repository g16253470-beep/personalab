"""CalComAdapter — case study #2: Cal.com (open-source scheduling) eval.

Material drawn from cal.com / cal.com/pricing / docs.cal.com as of 2026-05-18.
All verbatim brand content remains property of Cal.com Inc. Translates the
public surface into a 5-day evaluation journey.

Use:
    personalab run --mode both --personas ./personas \\
      --adapter calcom --llm gemini:gemini-2.5-flash \\
      --days 5 --limit 5 --out-dir ./reports/calcom_case
"""
from __future__ import annotations

from typing import Any

from personalab.core.product import Event, ProductAdapter, SubscriptionState


PRICING_CONTEXT = """
**Cal.com pricing (cloud, 2026-05-18, public)**:

| plan | $/seat/month | features |
|---|---|---|
| Free | $0  | unlimited 1:1, basic integrations, Cal.com branding |
| Teams | $12 | round-robin, collective scheduling, no branding, workflows |
| Organizations | $37 | SAML SSO, admin API, sub-teams, white-label |
| Platform | usage-based | Atoms (embeddable React components), white-label dev platform |

Self-host: free forever, AGPLv3 license. Run your own Cal.com instance,
own your data.

Competitors:
- Calendly ($10/$15/$20/seat/month + $25 admin): closed source, biggest brand
- SavvyCal ($12-20/seat): mid-market, less features
- Microsoft Bookings: bundled with M365, lower friction inside org
- Google Appointment Schedules: bundled with Google Workspace, free-ish
- HubSpot Meetings: bundled with HubSpot CRM
""".strip()


def _journey_events() -> list[Event]:
    """5 events covering the prospective Cal.com user's evaluation."""
    base_ts = 1_732_000_000
    day = 86400
    return [
        Event(
            timestamp=base_ts + 0 * day,
            severity="high",
            category="onboarding",
            headline="Day 1 — landing page + 'Get started for free'",
            body={"narrative": (
                "你被同行推荐看 Cal.com，hero："
                "'The scheduling infrastructure for absolutely everyone'。\n\n"
                "右上角 Sign up 按钮。提供 Google / Microsoft / Apple / 邮箱"
                "4 种登录方式。\n\n"
                "Onboarding wizard："
                "1) Connect a calendar (Google / Outlook / Office365) "
                "2) Set availability "
                "3) Configure first event type "
                "4) Get your booking link\n\n"
                "10 分钟搞定。booking link 是 `cal.com/yourname/30min`，"
                "默认带 Cal.com branding。\n\n"
                + PRICING_CONTEXT
            )},
        ),
        Event(
            timestamp=base_ts + 1 * day,
            severity="mid",
            category="first-use",
            headline="Day 2 — 第一次发链接给客户",
            body={"narrative": (
                "你把 cal.com/yourname/30min 发给一个潜在客户。\n"
                "他点开看到 Cal.com branding（'Powered by Cal.com'），"
                "犹豫了一下：'这是个 third-party tool 还是 spam？'\n\n"
                "他还是预约了。15 分钟内：\n"
                "- 你的 calendar 自动加了事件\n"
                "- 双方收到确认邮件\n"
                "- Cal.com 自动检查 Zoom 链接（默认没装，要你手动配置）\n\n"
                "你查 Free plan 限制：1 calendar / 不能去 branding / "
                "无 round-robin。要去 branding 必须升到 Teams $12/seat/月。\n\n"
                "你一个人用：$12 × 1 = $12/月。可接受。"
            )},
        ),
        Event(
            timestamp=base_ts + 2 * day,
            severity="mid",
            category="integration",
            headline="Day 3 — Zoom / Stripe / workflows 配置",
            body={"narrative": (
                "你装了 Zoom integration（10 秒）+ Stripe 收预付款"
                "（needs Teams plan，但 Free 也能跑过）。\n"
                "试了 workflow：'预约前 1 小时自动发 SMS 提醒' —— Teams plan 才能用。\n\n"
                "对比 Calendly：Calendly Free 不能去 branding，"
                "$10/seat 才能去 + 加 workflows，跟 Cal.com $12/seat 差不多。\n\n"
                "差异点：Cal.com 开源、self-host 可选；Calendly 老牌、"
                "用户认 brand（'send me Calendly link' 是 verb）。\n\n"
                "你犹豫：要不要 self-host？"
                "Cal.com Self-Host：Docker compose + Postgres + 你的域名。"
                "估算 $20/月 server，但需要你会维护。"
            )},
        ),
        Event(
            timestamp=base_ts + 3 * day,
            severity="high",
            category="team-pricing",
            headline="Day 4 — 推荐给团队，遇到合算账问题",
            body={"narrative": (
                "你想推荐给整个 5 人 sales team。\n"
                "Cal.com Teams $12 × 5 = $60/月，年付 $720。\n"
                "对比：\n"
                "- Calendly Standard $12 × 5 = $60/月（差不多）\n"
                "- Calendly Teams $20 × 5 = $100/月（有 round-robin）\n"
                "- Microsoft Bookings: $0（你们已经付 M365 E3 $32/user/月）\n\n"
                "Sales 老板问：'我们已经付 M365 了，为什么不用 Bookings？'\n"
                "你: 'Bookings 是基础款，没 round-robin、UI 简陋、"
                "无 workflows、无 Stripe 收预付'。\n"
                "老板：'我们 sales 不需要这些。给客户能预约就行。'\n\n"
                "你妥协：自己用 Cal.com Free，team 用 Bookings。"
                "Cal.com 把你从用户变成 indie evangelist。"
            )},
        ),
        Event(
            timestamp=base_ts + 4 * day,
            severity="high",
            category="decision",
            headline="Day 5 — 决策",
            body={"narrative": (
                "5 天用下来：\n"
                "- ✅ 个人 scheduling 流程清爽，open source 心态加分\n"
                "- ✅ self-host 选项有 dignity\n"
                "- ✅ 跟 Calendly 同价位但更多 feature (workflows / Stripe / SAML)\n"
                "- ⚠️ Free 必带 branding，单人用不爽\n"
                "- ⚠️ team 卖给老板时被 'we already have Bookings' 顶回\n"
                "- ⚠️ 跟 Calendly 比无品牌优势，朋友/客户不熟 Cal.com\n\n"
                "你的选择：\n"
                "1. UNSUBSCRIBE 完全弃用回到 manual schedule\n"
                "2. /coin self-host 自建（前提是你会 Docker）\n"
                "3. /profile free 长期免费用，吃 branding\n"
                "4. /severity high 升 Teams $12 去 branding\n"
                "5. DO_NOTHING 续 Free"
            )},
        ),
    ]


class CalComAdapter(ProductAdapter):
    """ProductAdapter exposing Cal.com public evaluation journey to personas."""

    name = "calcom"

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
            "/profile free",
            "/coin self-host",
            "/severity high",  # 升 Teams $12 去 branding
            "DO_NOTHING",
            "UNSUBSCRIBE",
        ]

    def actions_help(self) -> str:
        return (
            "- `/profile free` — 长期 Free，吃 branding\n"
            "- `/coin self-host` — 自建 Cal.com Docker（前提：会维护）\n"
            "- `/severity high` — 升 Teams $12/seat 去 branding + workflows\n"
            "- `DO_NOTHING` — 今天不动\n"
            "- `UNSUBSCRIBE` — 弃用回到 manual schedule"
        )

    def apply_action(self, state: SubscriptionState, action: str) -> str:
        action = action.strip()
        if action.startswith("/profile "):
            state.profile = action.split(" ", 1)[1].strip()
            return f"profile -> {state.profile}"
        if action == "/coin self-host":
            state.profile = "self-host"
            return "self-host: Docker + Postgres + your domain"
        if action.startswith("/severity "):
            sev = action.split(" ", 1)[1].strip()
            state.min_severity = sev
            return f"severity={sev}"
        return super().apply_action(state, action)
