"""StatsMode — wrap another TestMode and run it N times for robustness.

Returns a ModeResult whose per-persona dict contains:
  - "runs": raw results from each repetition
  - "aggregated": majority votes + mean/std/CI95 for numeric fields
  - "noisy": list of fields whose CoV exceeds threshold

Use this to distinguish "persona has stable preference" (low variance across
runs) from "LLM is flipping a coin" (high variance, model artefact).
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from personalab.core.llm import LLMAdapter
from personalab.core.mode import ModeResult, TestMode
from personalab.core.persona import Persona
from personalab.core.product import ProductAdapter
from personalab.stats.confidence import is_noisy, majority_vote, summarize

log = logging.getLogger(__name__)


_NUMERIC_FIELDS_STATIC = ["quit_trigger_score"]
_NUMERIC_FIELDS_AGENTIC = []  # verdict has no built-in numeric; deltas computed elsewhere
_CATEGORICAL_FIELDS = ["would_subscribe", "final_subscribe",
                        "pricing_willingness_usd_month"]


def _extract_field(r: dict, field: str):
    if field in r:
        return r.get(field)
    v = r.get("verdict")
    if v and isinstance(v, dict):
        return v.get(field)
    return None


def _aggregate(persona: str, runs: list[dict]) -> dict:
    out: dict = {"persona": persona, "n_runs": len(runs), "runs": runs}
    agg: dict = {}
    noisy: list[str] = []

    for field in _CATEGORICAL_FIELDS:
        values = [_extract_field(r, field) for r in runs]
        modal, frac = majority_vote(values)
        if modal is not None:
            agg[f"{field}_modal"] = modal
            agg[f"{field}_agreement"] = round(frac, 2)

    for field in _NUMERIC_FIELDS_STATIC + _NUMERIC_FIELDS_AGENTIC:
        values = [_extract_field(r, field) for r in runs]
        # filter numeric
        nums = [v for v in values if isinstance(v, (int, float))]
        if nums:
            s = summarize(nums)
            agg[field] = s
            if is_noisy(s):
                noisy.append(field)

    # Mark categorical fields as noisy when agreement < 0.5
    for field in _CATEGORICAL_FIELDS:
        ag = agg.get(f"{field}_agreement")
        if isinstance(ag, (int, float)) and ag < 0.5:
            noisy.append(field)

    out["aggregated"] = agg
    out["noisy"] = noisy
    # Use latest run as "representative" copy (verdict + decisions for agentic)
    if runs:
        last = runs[-1]
        for k in ("verdict", "decisions", "days_completed", "quit_day",
                  "total_received", "final_state", "first_complaint",
                  "verbatim_reaction", "top_3_changes", "what_works"):
            if k in last:
                out[k] = last[k]
    return out


class StatsMode(TestMode):
    """Run `inner` mode `repeats` times, aggregate per-persona stats."""

    name = "stats"

    def __init__(self, inner: TestMode, repeats: int = 3,
                 parallel_runs: bool = True) -> None:
        if repeats < 2:
            raise ValueError("StatsMode needs repeats >= 2")
        self.inner = inner
        self.repeats = repeats
        self.parallel_runs = parallel_runs

    async def run(self, personas: list[Persona],
                  product: ProductAdapter, llm: LLMAdapter,
                  config: dict[str, Any] | None = None) -> ModeResult:
        log.info("stats: %s × %d repeats × %d personas",
                 self.inner.name, self.repeats, len(personas))

        if self.parallel_runs:
            run_results = await asyncio.gather(*(
                self.inner.run(personas, product, llm, config)
                for _ in range(self.repeats)
            ))
        else:
            run_results = []
            for _ in range(self.repeats):
                run_results.append(
                    await self.inner.run(personas, product, llm, config))

        # Reorganize: per persona, collect their results across runs
        by_persona: dict[str, list[dict]] = {p.name: [] for p in personas}
        for rr in run_results:
            for r in rr.results:
                name = r.get("persona")
                if name in by_persona:
                    by_persona[name].append(r)

        aggregated = [_aggregate(p.name, by_persona[p.name]) for p in personas]

        return ModeResult(
            mode=self.name,
            results=aggregated,
            metadata={
                "inner_mode": self.inner.name,
                "repeats": self.repeats,
                "llm": llm.name,
                "product": product.name,
                "config": config or {},
            },
        )
