"""ToyAdapter — minimal in-memory ProductAdapter for documentation + tests.

If you can read this file, you can write a ProductAdapter for any product.
There's no magic; just answer three questions:

  1. load_events() → list[Event]
  2. render_event(e) → str  (what the user sees in their UI)
  3. (optional) apply_action(state, action) → str  (what the user can do)
"""
from __future__ import annotations

from typing import Any

from personalab.core.product import Event, ProductAdapter


class ToyAdapter(ProductAdapter):
    """A hardcoded 'notifications app' with 3 categories and severities."""

    name = "toy"

    def __init__(self, events: list[Event] | None = None) -> None:
        self._events = events or self._default_events()

    @staticmethod
    def _default_events() -> list[Event]:
        return [
            Event(timestamp=1_700_000_000, severity="mid",
                  category="news", headline="New product feature shipped",
                  body={"channel": "release-notes"}),
            Event(timestamp=1_700_001_000, severity="high",
                  category="alert", headline="Server p99 latency > 500ms",
                  body={"region": "us-east"}),
            Event(timestamp=1_700_002_000, severity="low",
                  category="digest", headline="Weekly metrics",
                  body={"period": "2026-W19"}),
        ]

    def load_events(self, limit: int | None = None,
                    since: float | None = None) -> list[Event]:
        events = list(self._events)
        if since is not None:
            events = [e for e in events if e.timestamp >= since]
        if limit is not None:
            events = events[:limit]
        return events

    def render_event(self, event: Event, **opts: Any) -> str:
        return (f"[{event.severity.upper()}] {event.category}: "
                f"{event.headline}")
