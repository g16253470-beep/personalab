"""Reporter: render a ModeResult into a markdown string."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from personalab.core.mode import ModeResult


class Reporter(ABC):
    """Render one ModeResult (or several) into markdown."""

    name: str = "base"

    @abstractmethod
    def render(self, result: ModeResult, **opts: Any) -> str:
        ...

    def render_to_file(self, result: ModeResult, path, **opts: Any) -> None:
        from pathlib import Path
        text = self.render(result, **opts)
        Path(path).write_text(text, encoding="utf-8")
