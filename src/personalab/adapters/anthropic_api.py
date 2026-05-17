"""Anthropic API LLMAdapter (optional, requires `anthropic` package)."""
from __future__ import annotations

import asyncio
import importlib.util
import os

from personalab.core.llm import LLMAdapter


class AnthropicAPIAdapter(LLMAdapter):
    """Call the Anthropic Messages API directly (no CLI subprocess)."""

    name = "anthropic-api"

    def __init__(self, model: str = "claude-sonnet-4-6",
                 api_key: str | None = None,
                 max_tokens: int = 4096) -> None:
        if importlib.util.find_spec("anthropic") is None:  # pragma: no cover
            raise RuntimeError(
                "AnthropicAPIAdapter needs `pip install anthropic` "
                "(personalab[anthropic-api])"
            )
        self.model = model
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY env var not set")
        self.max_tokens = max_tokens
        self.name = f"anthropic-api/{model}"

    async def complete(self, prompt: str, timeout: float = 180.0) -> str:
        import anthropic

        def _call() -> str:
            client = anthropic.Anthropic(api_key=self.api_key, timeout=timeout)
            resp = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            parts = []
            for block in resp.content:
                if getattr(block, "type", None) == "text":
                    parts.append(block.text)
            return "".join(parts)

        return await asyncio.to_thread(_call)
