"""JSON parsing with codefence stripping + retry on LLM responses.

LLMs prompted for "strict JSON, no markdown" still emit ```json ...``` fences
roughly 10-20% of the time. This module wraps that messiness with a single
retry loop used by every TestMode.
"""
from __future__ import annotations

import asyncio
import json
import logging
import re

from personalab.core.llm import LLMAdapter

log = logging.getLogger(__name__)

_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```\s*$",
                        flags=re.IGNORECASE | re.MULTILINE)
_OBJECT_RE = re.compile(r"\{.*\}", flags=re.DOTALL)


def strip_fences(text: str) -> str:
    return _FENCE_RE.sub("", text.strip()).strip()


def extract_json(text: str) -> dict:
    """Try strict parse first; fall back to first `{...}` substring."""
    cleaned = strip_fences(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        m = _OBJECT_RE.search(cleaned)
        if not m:
            raise
        return json.loads(m.group(0))


async def parse_json_with_retry(llm: LLMAdapter, prompt: str,
                                  retries: int = 3,
                                  timeout: float = 180.0,
                                  backoff_base: float = 3.0,
                                  label: str = "") -> dict:
    """Call llm.complete + parse JSON, retrying on failure with linear backoff.

    Raises the last exception if all retries fail.
    """
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            raw = await llm.complete(prompt, timeout=timeout)
            return extract_json(raw)
        except Exception as e:
            last_exc = e
            wait = backoff_base * (attempt + 1)
            log.warning("[%s] attempt %d/%d failed: %s — retry in %.1fs",
                         label or llm.name, attempt + 1, retries,
                         str(e)[:120], wait)
            if attempt + 1 < retries:
                await asyncio.sleep(wait)
    assert last_exc is not None
    raise last_exc
