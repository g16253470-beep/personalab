"""StaticMode — one-shot transcript reading test (Tier 2).

Each persona reads the entire transcript once and emits a single JSON verdict.
Cheap, fast, but biased optimistic (no behavioral pressure).

Migrated from okx_pulse v12.6 persona_test.py and de-coupled from SignalStream.
"""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

from personalab.core.llm import LLMAdapter
from personalab.core.mode import ModeResult, TestMode
from personalab.core.parsing import parse_json_with_retry
from personalab.core.persona import Persona
from personalab.core.product import ProductAdapter

log = logging.getLogger(__name__)


PROMPT_TEMPLATE = """你的任务：扮演下面的用户人格，读他们刚刚收到的产品 transcript，
基于这个人格的心理特征给出反应。

# 你扮演的人格

{persona_body}

---

# 这是产品 transcript（按时间顺序）

```
{transcript}
```

---

# 请输出严格 JSON（无 markdown 包裹）：

{{
  "would_subscribe": "yes" | "maybe" | "no",
  "quit_trigger_score": 1-10,
  "first_complaint": "30-80 字 这个人格读完最大的吐槽",
  "what_works": "20-50 字 这个人格欣赏的地方（如果有）",
  "top_3_changes": ["改进1", "改进2", "改进3"],
  "pricing_willingness_usd_month": "0 / 5-20 / 20-50 / 50-200 / 200+",
  "verbatim_reaction": "100-150 字，这个人格用自己的话说一段话"
}}

立即输出 JSON，不要任何前置说明。"""


class StaticMode(TestMode):
    """One-shot transcript → verdict for each persona, in parallel."""

    name = "static"

    def __init__(self, concurrency: int = 3, retries: int = 3,
                 timeout: float = 180.0) -> None:
        self.concurrency = concurrency
        self.retries = retries
        self.timeout = timeout

    async def _run_one(self, persona: Persona, transcript: str,
                       llm: LLMAdapter) -> dict:
        prompt = PROMPT_TEMPLATE.format(
            persona_body=persona.body,
            transcript=transcript,
        )
        t0 = time.time()
        try:
            data = await parse_json_with_retry(
                llm, prompt,
                retries=self.retries, timeout=self.timeout,
                label=f"static/{persona.name}",
            )
            elapsed = time.time() - t0
            log.info("[%s] static done in %.1fs (sub=%s score=%s)",
                     persona.name, elapsed,
                     data.get("would_subscribe"),
                     data.get("quit_trigger_score"))
            return {"persona": persona.name, "elapsed_sec": round(elapsed, 1),
                    **data}
        except Exception as e:
            log.exception("[%s] static failed: %s", persona.name, e)
            return {"persona": persona.name, "error": str(e)[:200]}

    async def run(self, personas: list[Persona], product: ProductAdapter,
                  llm: LLMAdapter,
                  config: dict[str, Any] | None = None) -> ModeResult:
        cfg = config or {}
        limit = cfg.get("limit", 30)
        events = product.load_events(limit=limit)
        transcript = product.render_transcript(events)
        log.info("static: %d events, transcript %d chars, %d personas, conc=%d",
                 len(events), len(transcript), len(personas), self.concurrency)

        sem = asyncio.Semaphore(self.concurrency)

        async def _bounded(p: Persona) -> dict:
            async with sem:
                return await self._run_one(p, transcript, llm)

        results = await asyncio.gather(*(_bounded(p) for p in personas))
        return ModeResult(
            mode=self.name,
            results=list(results),
            metadata={
                "n_events": len(events),
                "transcript_chars": len(transcript),
                "llm": llm.name,
                "product": product.name,
                "config": cfg,
            },
        )
