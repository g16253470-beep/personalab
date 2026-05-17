"""JuryMode — same persona × multiple LLM judges, measure agreement.

For each persona, JuryMode runs the static-style verdict prompt against every
LLM in the panel concurrently. Output includes per-LLM verdicts plus an
agreement score per field (1.0 = unanimous, lower = divergent).

Purpose: detect when single-model bias is steering a verdict. A persona where
3 models all say "no" is trustworthy; one where Claude says yes / GPT says no
is a coin-flip and should be flagged.
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
from personalab.modes.static import PROMPT_TEMPLATE as STATIC_PROMPT

log = logging.getLogger(__name__)


def _field_agreement(values: list) -> float:
    """1.0 if all values agree, else fraction of mode count."""
    if not values:
        return 0.0
    counts: dict = {}
    for v in values:
        key = str(v)
        counts[key] = counts.get(key, 0) + 1
    return max(counts.values()) / len(values)


def _compute_agreement(per_llm: list[dict]) -> dict:
    """Field-level agreement scores across multiple LLM verdicts."""
    good = [r for r in per_llm if "error" not in r]
    if len(good) < 2:
        return {"_n_good": len(good), "_overall": 0.0}
    fields = ["would_subscribe", "pricing_willingness_usd_month"]
    field_scores = {f: _field_agreement([r.get(f) for r in good])
                    for f in fields}
    # numeric: bucket quit_trigger_score into low(1-3)/mid(4-6)/high(7-10)
    def bucket(x):
        try:
            x = int(x)
        except (TypeError, ValueError):
            return "?"
        return "low" if x <= 3 else "mid" if x <= 6 else "high"
    field_scores["quit_trigger_bucket"] = _field_agreement(
        [bucket(r.get("quit_trigger_score")) for r in good])
    overall = sum(field_scores.values()) / len(field_scores)
    return {**field_scores, "_n_good": len(good),
            "_overall": round(overall, 2)}


class JuryMode(TestMode):
    """Run static-style verdict across a jury of LLMs for each persona."""

    name = "jury"

    def __init__(self, jury: list[LLMAdapter],
                 concurrency: int = 4, retries: int = 3,
                 timeout: float = 180.0) -> None:
        if not jury:
            raise ValueError("JuryMode needs at least one LLM in the jury")
        self.jury = jury
        self.concurrency = concurrency
        self.retries = retries
        self.timeout = timeout

    async def _run_one_llm(self, persona: Persona, transcript: str,
                             llm: LLMAdapter) -> dict:
        prompt = STATIC_PROMPT.format(persona_body=persona.body,
                                       transcript=transcript)
        t0 = time.time()
        try:
            data = await parse_json_with_retry(
                llm, prompt,
                retries=self.retries, timeout=self.timeout,
                label=f"jury/{persona.name}/{llm.name}",
            )
            return {"llm": llm.name,
                    "elapsed_sec": round(time.time() - t0, 1), **data}
        except Exception as e:
            return {"llm": llm.name, "error": str(e)[:200]}

    async def _run_one_persona(self, persona: Persona, transcript: str) -> dict:
        per_llm = await asyncio.gather(
            *(self._run_one_llm(persona, transcript, j) for j in self.jury)
        )
        agreement = _compute_agreement(per_llm)
        log.info("[jury %s] %d/%d good, overall_agree=%s",
                 persona.name, agreement.get("_n_good", 0), len(self.jury),
                 agreement.get("_overall"))
        return {"persona": persona.name,
                "per_llm": per_llm,
                "agreement": agreement}

    async def run(self, personas: list[Persona], product: ProductAdapter,
                  llm: LLMAdapter,  # ignored — jury uses self.jury
                  config: dict[str, Any] | None = None) -> ModeResult:
        cfg = config or {}
        events = product.load_events(limit=cfg.get("limit", 30))
        transcript = product.render_transcript(events)
        log.info("jury: %d personas × %d LLMs (%s), %d events",
                 len(personas), len(self.jury),
                 [j.name for j in self.jury], len(events))

        sem = asyncio.Semaphore(self.concurrency)

        async def _bounded(p: Persona) -> dict:
            async with sem:
                return await self._run_one_persona(p, transcript)

        results = await asyncio.gather(*(_bounded(p) for p in personas))
        return ModeResult(
            mode=self.name,
            results=list(results),
            metadata={
                "n_events": len(events),
                "jury": [j.name for j in self.jury],
                "product": product.name,
                "config": cfg,
            },
        )
