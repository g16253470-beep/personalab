"""OpenAI LLMAdapter (optional, requires `openai` package)."""
from __future__ import annotations

import asyncio
import importlib.util
import os

from personalab.core.llm import LLMAdapter


class OpenAIAdapter(LLMAdapter):
    """Call the OpenAI Chat Completions API."""

    name = "openai"

    def __init__(self, model: str = "gpt-4o",
                 api_key: str | None = None,
                 max_tokens: int = 4096) -> None:
        if importlib.util.find_spec("openai") is None:  # pragma: no cover
            raise RuntimeError(
                "OpenAIAdapter needs `pip install openai` "
                "(personalab[openai])"
            )
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY env var not set")
        self.max_tokens = max_tokens
        self.name = f"openai/{model}"

    async def complete(self, prompt: str, timeout: float = 180.0) -> str:
        import openai

        def _call() -> str:
            client = openai.OpenAI(api_key=self.api_key, timeout=timeout)
            resp = client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content or ""

        return await asyncio.to_thread(_call)
