"""Google Gemini LLMAdapter (optional, requires `google-genai` package)."""
from __future__ import annotations

import asyncio
import importlib.util
import os

from personalab.core.llm import LLMAdapter


class GeminiAdapter(LLMAdapter):
    """Call Google Gemini via google-genai SDK."""

    name = "gemini"

    def __init__(self, model: str = "gemini-2.5-pro",
                 api_key: str | None = None) -> None:
        if importlib.util.find_spec("google.genai") is None:  # pragma: no cover
            raise RuntimeError(
                "GeminiAdapter needs `pip install google-genai` "
                "(personalab[gemini])"
            )
        self.model = model
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") \
            or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY env var not set")
        self.name = f"gemini/{model}"

    async def complete(self, prompt: str, timeout: float = 180.0) -> str:
        from google import genai

        def _call() -> str:
            client = genai.Client(api_key=self.api_key)
            resp = client.models.generate_content(
                model=self.model, contents=prompt,
            )
            return resp.text or ""

        return await asyncio.wait_for(asyncio.to_thread(_call), timeout=timeout)
