"""Calibration metrics: persona prediction vs real user behavior.

Three comparisons:

1. **Subscribe classification** — predicted (yes/maybe/no) vs actual (bool).
   Map maybe → subscribed=true (optimistic) for binary comparison.
   Output: precision/recall/F1 + confusion matrix.

2. **Pricing regression** — predicted bucket midpoint vs actual paid USD.
   Output: mean absolute error.

3. **Action-sequence Jaccard** (agentic only) — set of commands persona
   issued vs set of commands real user issued, share of overlap.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean
from typing import Iterable

from personalab.calibration.dataset import RealUser


# Bucket midpoints in USD/month
_PRICE_MIDPOINT = {"0": 0, "5-20": 12.5, "20-50": 35,
                   "50-200": 125, "200+": 300}


def _predicted_subscribe(pred: dict) -> str | None:
    if "would_subscribe" in pred:
        return pred["would_subscribe"]
    v = pred.get("verdict") or {}
    return v.get("final_subscribe")


def _predicted_price(pred: dict) -> str | None:
    if "pricing_willingness_usd_month" in pred:
        return pred["pricing_willingness_usd_month"]
    v = pred.get("verdict") or {}
    return v.get("pricing_willingness_usd_month")


def _predicted_actions(pred: dict) -> list[str]:
    return [d.get("action", "") for d in pred.get("decisions", [])]


@dataclass
class ConfusionMatrix:
    tp: int = 0  # predicted subscribe, real subscribed
    fp: int = 0  # predicted subscribe, real not
    fn: int = 0  # predicted no, real subscribed
    tn: int = 0  # predicted no, real not

    def precision(self) -> float:
        d = self.tp + self.fp
        return self.tp / d if d else 0.0

    def recall(self) -> float:
        d = self.tp + self.fn
        return self.tp / d if d else 0.0

    def f1(self) -> float:
        p, r = self.precision(), self.recall()
        return 2 * p * r / (p + r) if (p + r) else 0.0

    def accuracy(self) -> float:
        total = self.tp + self.fp + self.fn + self.tn
        return (self.tp + self.tn) / total if total else 0.0


@dataclass
class CalibrationResult:
    n: int
    subscribe: ConfusionMatrix = field(default_factory=ConfusionMatrix)
    price_mae: float | None = None
    action_jaccard_mean: float | None = None
    per_user: list[dict] = field(default_factory=list)
    matched_personas: list[str] = field(default_factory=list)


def _pred_sub_to_bool(pred: str | None, maybe_as: str = "yes") -> bool | None:
    if pred is None:
        return None
    pred = pred.lower()
    if pred == "yes":
        return True
    if pred == "no":
        return False
    if pred == "maybe":
        return maybe_as == "yes"
    return None


def compare_subscribe(pred_by_persona: dict[str, dict],
                       real_users: Iterable[RealUser],
                       maybe_as: str = "yes") -> ConfusionMatrix:
    cm = ConfusionMatrix()
    for u in real_users:
        pred = pred_by_persona.get(u.persona_match)
        if not pred:
            continue
        pb = _pred_sub_to_bool(_predicted_subscribe(pred), maybe_as=maybe_as)
        if pb is None:
            continue
        ab = bool(u.subscribed)
        if pb and ab:
            cm.tp += 1
        elif pb and not ab:
            cm.fp += 1
        elif not pb and ab:
            cm.fn += 1
        else:
            cm.tn += 1
    return cm


def compare_pricing(pred_by_persona: dict[str, dict],
                    real_users: Iterable[RealUser]) -> float | None:
    diffs: list[float] = []
    for u in real_users:
        pred = pred_by_persona.get(u.persona_match)
        if not pred:
            continue
        ph = _predicted_price(pred)
        if ph not in _PRICE_MIDPOINT:
            continue
        diffs.append(abs(_PRICE_MIDPOINT[ph] - u.pricing_paid_usd))
    return mean(diffs) if diffs else None


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def compare_actions(pred_by_persona: dict[str, dict],
                    real_users: Iterable[RealUser]) -> float | None:
    scores: list[float] = []
    for u in real_users:
        pred = pred_by_persona.get(u.persona_match)
        if not pred:
            continue
        # Compare the *command prefix* (first token) sets
        pred_acts = {a.split()[0] for a in _predicted_actions(pred) if a}
        real_acts = {a.split()[0] for a in u.actions if a}
        if not pred_acts and not real_acts:
            continue
        scores.append(_jaccard(pred_acts, real_acts))
    return mean(scores) if scores else None


def calibrate(predictions: list[dict],
              real_users: list[RealUser],
              maybe_as: str = "yes") -> CalibrationResult:
    """Compute all calibration metrics in one pass."""
    pred_by_persona = {p["persona"]: p for p in predictions}
    cm = compare_subscribe(pred_by_persona, real_users, maybe_as=maybe_as)
    mae = compare_pricing(pred_by_persona, real_users)
    jacc = compare_actions(pred_by_persona, real_users)

    per_user = []
    for u in real_users:
        pred = pred_by_persona.get(u.persona_match)
        if not pred:
            per_user.append({"real_user_id": u.real_user_id,
                             "match": u.persona_match,
                             "status": "no_prediction"})
            continue
        per_user.append({
            "real_user_id": u.real_user_id,
            "persona_match": u.persona_match,
            "real_subscribed": u.subscribed,
            "real_pricing": u.pricing_paid_usd,
            "pred_subscribe": _predicted_subscribe(pred),
            "pred_pricing": _predicted_price(pred),
        })

    matched = sorted({u.persona_match for u in real_users
                       if u.persona_match in pred_by_persona})

    return CalibrationResult(
        n=len(real_users),
        subscribe=cm,
        price_mae=mae,
        action_jaccard_mean=jacc,
        per_user=per_user,
        matched_personas=matched,
    )
