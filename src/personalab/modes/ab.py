"""ABMode — same personas, same LLM, two ProductAdapters → diff verdicts.

Use case: validate that v12.7 fixes actually move persona behavior in the
desired direction. Run the same Static (or Agentic) mode against both
product versions, then compute per-persona delta:

- did subscribe verdict change? (no → maybe = improvement)
- did quit_trigger_score drop?
- did pricing willingness increase?
- did the top_friction change category?

The diff is the headline metric for "fix effectiveness".
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from personalab.core.llm import LLMAdapter
from personalab.core.mode import ModeResult, TestMode
from personalab.core.persona import Persona
from personalab.core.product import ProductAdapter

log = logging.getLogger(__name__)


_SUB_RANK = {"no": 0, "maybe": 1, "yes": 2}
_PRICE_RANK = {"0": 0, "5-20": 1, "20-50": 2, "50-200": 3, "200+": 4}


def _norm_sub(r: dict) -> str | None:
    v = r.get("verdict")
    if v and isinstance(v, dict):
        return v.get("final_subscribe") or v.get("would_subscribe")
    return r.get("would_subscribe") or r.get("final_subscribe")


def _norm_price(r: dict) -> str | None:
    v = r.get("verdict")
    if v and isinstance(v, dict):
        return v.get("pricing_willingness_usd_month")
    return r.get("pricing_willingness_usd_month")


def _diff(a: dict, b: dict) -> dict:
    """Compute meaningful deltas between two per-persona verdicts."""
    sub_a, sub_b = _norm_sub(a), _norm_sub(b)
    sub_delta = (_SUB_RANK.get(str(sub_b), -1)
                 - _SUB_RANK.get(str(sub_a), -1)
                 if sub_a and sub_b else None)
    price_a, price_b = _norm_price(a), _norm_price(b)
    price_delta = (_PRICE_RANK.get(str(price_b), -1)
                   - _PRICE_RANK.get(str(price_a), -1)
                   if price_a and price_b else None)
    # quit_score (static) or engagement avg (agentic)
    qa = a.get("quit_trigger_score")
    qb = b.get("quit_trigger_score")
    score_delta = (qb - qa) if isinstance(qa, (int, float)) \
        and isinstance(qb, (int, float)) else None
    return {
        "subscribe_a": sub_a, "subscribe_b": sub_b, "sub_delta": sub_delta,
        "price_a": price_a, "price_b": price_b, "price_delta": price_delta,
        "quit_score_a": qa, "quit_score_b": qb, "quit_score_delta": score_delta,
    }


class ABMode(TestMode):
    """Run a base mode against two products, return per-persona diff."""

    name = "ab"

    def __init__(self, inner: TestMode,
                 product_a: ProductAdapter,
                 product_b: ProductAdapter,
                 label_a: str = "A", label_b: str = "B") -> None:
        if product_a.name == product_b.name and label_a == label_b:
            log.warning("ABMode given two adapters with the same name and "
                        "label — diff will be meaningless")
        self.inner = inner
        self.product_a = product_a
        self.product_b = product_b
        self.label_a = label_a
        self.label_b = label_b

    async def run(self, personas: list[Persona],
                  product: ProductAdapter,  # ignored
                  llm: LLMAdapter,
                  config: dict[str, Any] | None = None) -> ModeResult:
        log.info("AB: running '%s' mode on '%s' vs '%s'",
                 self.inner.name, self.product_a.name, self.product_b.name)

        a_result, b_result = await asyncio.gather(
            self.inner.run(personas, self.product_a, llm, config),
            self.inner.run(personas, self.product_b, llm, config),
        )
        a_by_name = {r["persona"]: r for r in a_result.results}
        b_by_name = {r["persona"]: r for r in b_result.results}

        diffs: list[dict] = []
        for p in personas:
            a = a_by_name.get(p.name, {})
            b = b_by_name.get(p.name, {})
            diffs.append({
                "persona": p.name,
                "a": a, "b": b,
                "diff": _diff(a, b),
            })

        return ModeResult(
            mode=self.name,
            results=diffs,
            metadata={
                "inner_mode": self.inner.name,
                "product_a": self.product_a.name,
                "product_b": self.product_b.name,
                "label_a": self.label_a,
                "label_b": self.label_b,
                "a_metadata": a_result.metadata,
                "b_metadata": b_result.metadata,
                "llm": llm.name,
                "config": config or {},
            },
        )
