"""SignalStream / okx_pulse ProductAdapter.

Concrete reference implementation showing how to plug a real product into
personalab. Reads from the okx_pulse sqlite schema and supports all the
TG-bot commands the v12.6 bot exposed.

This file is the SOLE place SignalStream knowledge lives — personalab.core
remains fully product-agnostic.
"""
from __future__ import annotations

import json
import re
import sqlite3
import time
from typing import Any

from personalab.core.product import Event, ProductAdapter, SubscriptionState
from personalab.core.timeutil import ts_to_cst


PROFILES: dict[str, dict] = {
    "scalper": {"categories": {"price", "volume", "taker", "liq"},
                "min_severity": "high", "hourly_cap": 15, "ccys": set()},
    "swing":   {"categories": {"funding", "oi", "long_short", "premium", "macro"},
                "min_severity": "mid", "hourly_cap": 8, "ccys": set()},
    "whale":   {"categories": {"price", "volume", "funding", "oi", "liq",
                                 "long_short", "premium", "taker", "macro",
                                 "fng", "news", "cross_ex"},
                "min_severity": "high", "hourly_cap": 5,
                "ccys": {"BTC", "ETH", "SOL", "BNB"}},
    "active":  {"categories": {"price", "volume", "funding", "oi", "liq",
                                 "long_short", "premium", "taker", "macro",
                                 "fng", "news", "cross_ex"},
                "min_severity": "mid", "hourly_cap": 15, "ccys": set()},
    "quiet":   {"categories": {"price", "volume", "funding", "oi", "liq",
                                 "long_short", "premium", "taker", "macro",
                                 "fng", "news", "cross_ex"},
                "min_severity": "high", "hourly_cap": 2,
                "ccys": {"BTC", "ETH"}},
}

COIN_PRESETS: dict[str, set[str]] = {
    "majors": {"BTC", "ETH", "BNB", "SOL", "XRP"},
    "meme":   {"DOGE", "SHIB", "PEPE", "WIF", "BONK", "FLOKI", "TRUMP"},
    "btceth": {"BTC", "ETH"},
}


_SEV_RANK = {"low": 0, "mid": 1, "high": 2}
_SEV_ICON = {"low": "🟢", "mid": "🟡", "high": "🔴"}


class SignalStreamAdapter(ProductAdapter):
    """ProductAdapter reading events from an okx_pulse sqlite db."""

    name = "signalstream"

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    # ------------------------------------------------------------------
    # Event loading
    # ------------------------------------------------------------------

    def load_events(self, limit: int | None = None,
                    since: float | None = None) -> list[Event]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        where: list[str] = []
        params: list[Any] = []
        if since is not None:
            where.append("pushed_at >= ?")
            params.append(since)
        sql = """
            SELECT pushed_at, ccy, market, max_severity, primary_indicator,
                   primary_category, primary_headline, triggers_json,
                   ai_confidence, ai_evidence_used, ai_root_cause
            FROM events
        """
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY pushed_at ASC"
        if limit is not None:
            sql += " LIMIT ?"
            params.append(int(limit))
        cur = conn.execute(sql, tuple(params))
        rows = cur.fetchall()
        conn.close()
        out: list[Event] = []
        for r in rows:
            d = dict(r)
            out.append(Event(
                timestamp=float(d.get("pushed_at") or 0),
                severity=d.get("max_severity") or "low",
                category=d.get("primary_category") or "unknown",
                headline=d.get("primary_headline") or "",
                body=d,
            ))
        return out

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render_event(self, event: Event, **opts: Any) -> str:
        b = event.body
        sev_icon = _SEV_ICON.get(event.severity, "⚪")
        if opts.get("compact"):
            rc = (b.get("ai_root_cause") or "")[:80]
            return (f"{sev_icon} {b.get('ccy', '?')}/{b.get('market', '?')} "
                    f"{b.get('primary_indicator', '?')}: "
                    f"{event.headline[:70]} | AI: {rc}")
        # Full TG-card render
        ts = ts_to_cst(event.timestamp, "%H:%M")
        try:
            triggers = json.loads(b.get("triggers_json") or "[]")
        except (ValueError, TypeError):
            triggers = []
        lines = [
            f"{sev_icon} {b.get('ccy', '?')}/{b.get('market', '?')} · "
            f"{event.severity.upper()}",
            f"  primary: {b.get('primary_indicator', '?')} → "
            f"{event.headline}",
        ]
        if len(triggers) > 1:
            lines.append("  并发触发 " + str(len(triggers)) + ": " + ", ".join(
                f"[{t.get('severity', '?')}]{t.get('category', '?')}"
                for t in triggers))
        rc = b.get("ai_root_cause", "")
        if rc:
            lines.append(f"  💡 根因: {rc[:140]}")
        conf = b.get("ai_confidence") or "?"
        evi = (b.get("ai_evidence_used") or "").split(",")
        lines.append(
            f"  🧠 conf={conf} evidence={','.join(evi) if evi[0] else '-'}"
        )
        lines.append(f"  ⏱ {ts}\n")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # State / filtering
    # ------------------------------------------------------------------

    def default_state(self) -> SubscriptionState:
        # whale, same as /start in the v12.6 bot
        p = PROFILES["whale"]
        return SubscriptionState(
            profile="whale",
            categories=set(p["categories"]),
            min_severity=p["min_severity"],
            filters={"ccys": set(p["ccys"])},
            hourly_cap=p["hourly_cap"],
        )

    def matches_filter(self, event: Event,
                         state: SubscriptionState) -> bool:
        if _SEV_RANK.get(event.severity, 0) < \
                _SEV_RANK.get(state.min_severity, 1):
            return False
        if state.categories and event.category not in state.categories:
            return False
        ccys = state.filters.get("ccys") or set()
        if ccys and event.body.get("ccy") not in ccys:
            return False
        return True

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def available_actions(self) -> list[str]:
        return [
            "/profile X", "/coin X Y", "/coin -", "/coinset X",
            "/severity X", "/mute Nh", "/quietnight HH:MM-HH:MM",
            "DO_NOTHING", "UNSUBSCRIBE",
        ]

    def actions_help(self) -> str:
        return (
            "- `/profile whale|scalper|swing|active|quiet` — 切换预设\n"
            "- `/coin BTC ETH SOL` 或 `/coin -`（清空）\n"
            "- `/coinset majors|meme|btceth` — 套用币种组\n"
            "- `/severity low|mid|high`\n"
            "- `/mute 1h|6h|24h|off` — 临时静音\n"
            "- `/quietnight 23:00-08:00` — 每日静音段\n"
            "- `DO_NOTHING` — 今天不动\n"
            "- `UNSUBSCRIBE` — 完全退订（永久离开）"
        )

    def apply_action(self, state: SubscriptionState, action: str) -> str:
        action = action.strip()
        if action.startswith("/profile "):
            name = action.split(" ", 1)[1].strip().lower()
            if name in PROFILES:
                p = PROFILES[name]
                state.categories = set(p["categories"])
                state.min_severity = p["min_severity"]
                state.filters["ccys"] = set(p["ccys"])
                state.hourly_cap = p["hourly_cap"]
                state.profile = name
                return f"profile=>{name} (cap={state.hourly_cap})"
            return f"unknown profile {name}"
        if action.startswith("/coin "):
            rest = action.split(" ", 1)[1].strip()
            if rest == "-":
                state.filters["ccys"] = set()
                return "coin cleared (all)"
            state.filters["ccys"] = {x.upper() for x in rest.split()}
            return f"coin={state.filters['ccys']}"
        if action.startswith("/coinset "):
            name = action.split(" ", 1)[1].strip().lower()
            if name in COIN_PRESETS:
                state.filters["ccys"] = set(COIN_PRESETS[name])
                return f"coinset {name}={state.filters['ccys']}"
            return f"unknown coinset {name}"
        if action.startswith("/mute "):
            rest = action.split(" ", 1)[1].strip()
            m = re.match(r"^(\d+)([hd])$", rest)
            if m:
                n, u = int(m.group(1)), m.group(2)
                mins = n * (60 if u == "h" else 1440)
                state.muted_until = time.time() + mins * 60
                return f"muted {n}{u}"
            if rest == "off":
                state.muted_until = 0.0
                return "mute off"
            return "bad mute syntax"
        if action.startswith("/quietnight "):
            state.quiet_hours = action.split(" ", 1)[1].strip()
            return f"quietnight={state.quiet_hours}"
        if action.startswith("/severity "):
            sev = action.split(" ", 1)[1].strip()
            if sev in ("low", "mid", "high"):
                state.min_severity = sev
                return f"severity={sev}"
            return f"bad severity {sev}"
        # fall back to base universal commands
        return super().apply_action(state, action)
