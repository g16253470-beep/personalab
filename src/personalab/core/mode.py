"""TestMode: shared interface for Static / Agentic / Jury / AB modes."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from personalab.core.llm import LLMAdapter
from personalab.core.persona import Persona
from personalab.core.product import ProductAdapter


@dataclass
class ModeResult:
    """Output of a TestMode.run().

    Attributes:
        mode: short identifier of the mode that produced this ('static', 'agentic', ...)
        results: per-persona dict (mode-defines its own shape)
        metadata: free-form, e.g. {"n_events": 1348, "days": 5, "llm": "claude-cli"}
    """
    mode: str
    results: list[dict]
    metadata: dict = field(default_factory=dict)

    def persona_names(self) -> list[str]:
        return [r.get("persona", "?") for r in self.results]


class TestMode(ABC):
    """Run N personas against a product, return aggregated result."""

    name: str = "base"

    @abstractmethod
    async def run(self,
                  personas: list[Persona],
                  product: ProductAdapter,
                  llm: LLMAdapter,
                  config: dict[str, Any] | None = None) -> ModeResult:
        """Execute the mode end-to-end. Implementations may parallelize."""
