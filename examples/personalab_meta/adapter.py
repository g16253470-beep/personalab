"""PersonaLabSelfAdapter — meta-test: personalab as a commercial SaaS product.

Treats personalab itself as the product under test. Each event = one chapter
of a user's 5-day evaluation journey (install → first run → cost reveal →
share with team → renew decision). Personas read these and judge whether
they'd pay for it.

Default pricing assumption: $99/month individual, $499/month team.
"""
from __future__ import annotations

from typing import Any

from personalab.core.product import Event, ProductAdapter, SubscriptionState


PRICING_CONTEXT = """
**pricing on the landing page**:

| plan | $/month | includes |
|------|--------|----------|
| Free | $0     | FakeLLM only (smoke test), 100 personas/month, no real LLM |
| Indie | $29   | BYO LLM key, unlimited runs, single-user |
| Team  | $99   | + Slack share, Notion export, version history, 3 seats |
| Scale | $499  | + SOC2, SSO, white-label reports, calibration import, 25 seats |

competitors mentioned on the page:
- Maze ($0 / $50 / $150/mo) — usability testing with real recruited users
- Sprig (call for pricing, ~$1000/mo enterprise) — in-product surveys + AI summaries
- UserTesting ($49/session, $20k/yr team) — recorded real user sessions
- "ChatGPT custom GPT" — DIY, free, no framework

The README brags about: 5 test modes, multi-LLM jury, A/B mode, calibration,
40-line custom adapter, MIT license, ~3800 LOC, 6 passing smoke tests.
""".strip()


def _day_events() -> list[Event]:
    """7 events covering Day 1-7 of a prospective user evaluating personalab."""
    base_ts = 1_730_000_000
    day = 86400
    return [
        Event(
            timestamp=base_ts + 0 * day,
            severity="high",
            category="onboarding",
            headline="Day 1 — landing page + install",
            body={"narrative": (
                "你打开 personalab 的 landing page，看到 hero copy："
                "'让 12 个 AI 用户在你 ship 之前先试一周'。"
                "右上角 Pricing 链接。GitHub README 顶部写 'Evolved from "
                "SignalStream (an okx_pulse crypto signal product)'.\n\n"
                "你 pip install -e .（没有 PyPI 包，开发版）。\n"
                "运行 personalab version → 'personalab 0.1.0'。\n\n"
                "5 分钟过去了，你还没找到 docs/QUICKSTART.md，"
                "只有 ARCHITECTURE.md / ADAPTER_GUIDE.md / PERSONA_WRITING.md "
                "三份开发者风格文档。\n\n"
                + PRICING_CONTEXT
            )},
        ),
        Event(
            timestamp=base_ts + 1 * day,
            severity="high",
            category="first-run",
            headline="Day 2 — 第一次 `personalab run --mode static`",
            body={"narrative": (
                "你按 ADAPTER_GUIDE 写了 40 行的 SimpleAdapter，"
                "把你产品的 5 个 feature 描述作为 events。\n"
                "personalab run --mode static --llm anthropic-api:claude-sonnet-4-6 \n"
                "  --personas ./personas --adapter your_adapter --limit 10\n\n"
                "等了 35 秒，输出 static_report.md。\n"
                "12 个 SignalStream 加密人格在评论你的产品——\n"
                "  - 01_burnt_veteran: '推送密度过高'（你产品根本没推送）\n"
                "  - 09_competitor_ceo: '没有 hit rate 公布'（你不是金融产品）\n"
                "  - troll: 'Ctrl+C Bot'\n"
                "你意识到必须 BYO persona。再花 4 小时写自己的 12 个。\n\n"
                "成本：本次 Anthropic API 调用 ~$0.45。"
            )},
        ),
        Event(
            timestamp=base_ts + 2 * day,
            severity="mid",
            category="agentic-mode",
            headline="Day 3 — 跑 `--mode both` 看完整对比",
            body={"narrative": (
                "你写好 BYO personas 后跑 mode=both --days 3。\n"
                "139 秒后拿到 4 份报告：\n"
                "  static_report.md / agentic_report.md /\n"
                "  comparison_report.md / action_loop.md\n\n"
                "comparison 显示 3 个 'maybe' 被 agentic 打成 'no'，跟你直觉一致。\n"
                "action_loop.md 自动给出 P0/P1/P2 issue 列表，每条引用 ≥2 人格原话。\n\n"
                "成本：本次 Sonnet API ~$1.10。\n"
                "心算：每周跑 2 次 = $8.80 LLM + $99 SaaS = $475/月。\n"
                "对比 Maze Pro $150/月 + 真实用户 recruiting $300/月 = $450/月。\n"
                "区别：Maze 用真实用户（n=20-50），personalab 用 LLM（n=12）。"
            )},
        ),
        Event(
            timestamp=base_ts + 3 * day,
            severity="mid",
            category="jury-mode",
            headline="Day 4 — jury 模式跨模型验证",
            body={"narrative": (
                "你听说 jury mode 能检测单模型偏差，跑：\n"
                "personalab run --mode jury \n"
                "  --llm 'claude-cli,anthropic-api:claude-sonnet-4-6,gemini:gemini-2.5-pro'\n\n"
                "120 秒后报告显示：\n"
                "  - 8/12 personas 三模型完全一致（trust ✅）\n"
                "  - 3/12 部分分歧（Haiku 比 Sonnet 严苛）\n"
                "  - 1/12 troll persona Sonnet JSON 解析失败\n\n"
                "你第一次相信这个工具不是 'Claude 自己跟自己说话'。\n"
                "但你也注意到价格不便宜：jury 模式一次 24 调用 ~$0.35。"
            )},
        ),
        Event(
            timestamp=base_ts + 4 * day,
            severity="high",
            category="share",
            headline="Day 5 — 你想 share 给团队",
            body={"narrative": (
                "你把 comparison_report.md 复制粘贴到 Slack #product 频道。\n"
                "team lead 问：'这怎么自动化？能看 history 吗？能 link 到 PRD 吗？'\n"
                "你看了下 personalab：\n"
                "  - 没有 web UI\n"
                "  - 没有 share link\n"
                "  - 没有 history / cohort 跨时间对比\n"
                "  - 没有 Notion / Linear / Slack integration\n"
                "  - 没有 team collaboration\n\n"
                "你说：'当前只能你自己跑出来手动 share'。\n"
                "team lead 说：'那只是你个人 productivity tool。'\n\n"
                "$99 Team plan 标的是 'Slack share + Notion export + version history'\n"
                "但你 inspect 了 source code —— 这些功能尚未实现。"
            )},
        ),
        Event(
            timestamp=base_ts + 5 * day,
            severity="high",
            category="calibration",
            headline="Day 6 — 你想验证准确度",
            body={"narrative": (
                "你跑了 4 次 mode=both 一共烧了 $5.40。\n"
                "你查 personalab calibrate 子命令，发现需要：\n"
                "  - 真实用户行为 CSV (user_id, persona_match, subscribed, churned_at, paid_$)\n"
                "  - 你得手动把每个真实用户 label 到某个 persona\n"
                "  - 至少 30+ 真实用户才能算出有意义的 accuracy/F1\n\n"
                "你现在没有 30 个真实用户行为数据。\n"
                "也就是：你**没办法**回答 '这个工具准不准'。\n\n"
                "在 GitHub Issues 搜 'calibration data'，0 hits。\n"
                "作者在 ARCHITECTURE.md 写 '预测准 → 继续用；预测不准 → 改 personas'。\n"
                "但没人告诉你**怎么知道**预测准不准。"
            )},
        ),
        Event(
            timestamp=base_ts + 6 * day,
            severity="high",
            category="renewal",
            headline="Day 7 — 续费决定",
            body={"narrative": (
                "一周用下来：\n"
                "  - 价值：跑了 7 次，每次确实生成不一样的 insight，文字犀利\n"
                "  - 痛点：没团队功能、没 calibration 数据、CLI-only、需写自己的 personas\n"
                "  - 成本：$99 SaaS + ~$30/月 LLM API ≈ $130/月\n"
                "  - 替代：Maze Free + ChatGPT 自己写 prompts ≈ $0 但更慢\n\n"
                "你看 personalab 的定价页面，免费版只能跑 FakeLLM "
                "（fake output, 你试过，没用）。\n\n"
                "现在你要决定：\n"
                "1. UNSUBSCRIBE 完全弃用\n"
                "2. /profile downgrade — 降到 free 备着，偶尔本地跑\n"
                "3. /severity high — 只在重大产品决策前跑，每月 1-2 次\n"
                "4. /coin BYO — 继续付 $29 indie plan，不上 team plan\n"
                "5. DO_NOTHING 续 $99 team plan 等团队功能"
            )},
        ),
    ]


class PersonaLabSelfAdapter(ProductAdapter):
    """ProductAdapter that exposes personalab itself as the product under test."""

    name = "personalab-meta"

    def __init__(self) -> None:
        self._events = _day_events()

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

    # Use base default_state / split_by_day / matches_filter (severity gate only).

    def available_actions(self) -> list[str]:
        return [
            "/profile downgrade",       # 降级到 free
            "/profile upgrade-team",    # 升 $99
            "/severity high",           # 只在重大决策跑
            "/coin BYO",                # 继续 $29 indie
            "DO_NOTHING",
            "UNSUBSCRIBE",
        ]

    def actions_help(self) -> str:
        return (
            "- `/profile upgrade-team` — 升 $99 team plan\n"
            "- `/profile downgrade` — 降到 free（FakeLLM 占位）\n"
            "- `/coin BYO` — 续 $29 indie plan，自带 LLM key\n"
            "- `/severity high` — 只在重大产品决策跑，每月 1-2 次\n"
            "- `DO_NOTHING` — 今天不动\n"
            "- `UNSUBSCRIBE` — 完全弃用"
        )

    def apply_action(self, state: SubscriptionState, action: str) -> str:
        action = action.strip()
        if action.startswith("/profile "):
            tier = action.split(" ", 1)[1].strip()
            state.profile = tier
            return f"profile -> {tier}"
        if action == "/coin BYO":
            state.profile = "indie-byo-llm"
            return "indie BYO LLM tier active ($29/mo)"
        if action.startswith("/severity "):
            sev = action.split(" ", 1)[1].strip()
            state.min_severity = sev
            return f"severity={sev}"
        return super().apply_action(state, action)
