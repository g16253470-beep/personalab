"""ProductAdapter: how a real product is exposed to virtual users.

Implementing an adapter for a new product means answering 3 questions:

1. **What events does a user see?** → `load_events()`
2. **How does the user 'read' an event in their UI?** → `render_event()`
3. **What can the user *do* in response?** → `apply_action()` (optional)

Static mode needs only (1) + (2). Agentic mode also needs (3) plus
`split_by_day()` and `matches_filter()` for behavioral simulation.

See the examples/ directory for working reference implementations.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Event:
    """Product-agnostic event the user might receive.

    `body` is a free-form dict for product-specific fields the renderer needs.
    """
    timestamp: float
    severity: str  # 'low' | 'mid' | 'high' (or product-specific scale)
    category: str
    headline: str
    body: dict = field(default_factory=dict)


@dataclass
class SubscriptionState:
    """Mutable per-user state for agentic mode.

    Adapter is free to subclass / extend; the base shape covers severity gates,
    category filters, mute timers, profile labels.
    """
    profile: str = "default"
    categories: set[str] = field(default_factory=set)
    min_severity: str = "mid"
    filters: dict = field(default_factory=dict)  # adapter-defined, e.g. {ccys: {BTC,ETH}}
    hourly_cap: int = 0  # 0 = no cap
    muted_until: float = 0.0
    quiet_hours: str = ""


class ProductAdapter(ABC):
    """Translate a real product into events a persona can react to."""

    name: str = "base"

    @abstractmethod
    def load_events(self, limit: int | None = None,
                    since: float | None = None) -> list[Event]:
        """Return events oldest-first by default."""

    @abstractmethod
    def render_event(self, event: Event, **opts: Any) -> str:
        """Format a single event the way a real user would see it."""

    def render_transcript(self, events: list[Event], **opts: Any) -> str:
        """Default: join individual renders. Override for headers/separators."""
        return "\n".join(self.render_event(e, **opts) for e in events)

    # --- agentic-only (override to enable behavioral mode) -----------------

    def split_by_day(self, events: list[Event], days: int) -> list[list[Event]]:
        """Bucket events into `days` equal time slices (oldest → newest).

        Default: linear time-binning between min and max timestamp.
        """
        if not events or days <= 0:
            return [[] for _ in range(days)]
        events = sorted(events, key=lambda e: e.timestamp)
        t_min, t_max = events[0].timestamp, events[-1].timestamp
        span = max(t_max - t_min, 1.0)
        buckets: list[list[Event]] = [[] for _ in range(days)]
        for e in events:
            frac = (e.timestamp - t_min) / span
            idx = min(int(frac * days), days - 1)
            buckets[idx].append(e)
        return buckets

    def default_state(self) -> SubscriptionState:
        """Initial subscription state for a fresh persona. Override per product."""
        return SubscriptionState()

    def matches_filter(self, event: Event, state: SubscriptionState) -> bool:
        """Whether `event` reaches the user given their current state.

        Default: severity gate only. Override to add categories/filters/etc.
        """
        rank = {"low": 0, "mid": 1, "high": 2}
        return rank.get(event.severity, 0) >= rank.get(state.min_severity, 1)

    def apply_action(self, state: SubscriptionState, action: str) -> str:
        """Mutate state based on persona's chosen command. Return human result.

        Default: only handles UNSUBSCRIBE / DO_NOTHING universal commands.
        Override to add product-specific commands like /profile, /coin, etc.
        """
        action = action.strip()
        if action == "UNSUBSCRIBE":
            return "UNSUBSCRIBED"
        if action == "DO_NOTHING":
            return "no action"
        return f"unrecognized: {action}"

    def available_actions(self) -> list[str]:
        """List of commands the persona can issue. Override per product."""
        return ["DO_NOTHING", "UNSUBSCRIBE"]

    def actions_help(self) -> str:
        """Markdown bullet list describing available actions, injected into the
        agentic-mode prompt. Override per product when commands take arguments.
        """
        return "\n".join(f"- `{a}`" for a in self.available_actions())

    def render_state(self, state: SubscriptionState) -> str:
        """Human-readable summary of state for the agentic-mode prompt."""
        parts = [f"profile={state.profile}",
                 f"severity={state.min_severity}"]
        if state.categories:
            parts.append(f"categories={sorted(state.categories)[:6]}")
        if state.filters:
            parts.append(f"filters={state.filters}")
        if state.hourly_cap:
            parts.append(f"cap={state.hourly_cap}/h")
        if state.quiet_hours:
            parts.append(f"quiet={state.quiet_hours}")
        return " ".join(parts)
