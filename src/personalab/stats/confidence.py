"""Tiny stats helpers — mean/stdev/CI95 without scipy."""
from __future__ import annotations

import math
import statistics
from collections import Counter
from typing import Iterable


# Approximate t-distribution critical values for 95% confidence
# (n_samples → t for n-1 df). Beyond 30 ≈ 1.96.
_T95 = {
    2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571, 7: 2.447,
    8: 2.365, 9: 2.306, 10: 2.262, 15: 2.131, 20: 2.086,
    25: 2.064, 30: 2.042,
}


def t95(n: int) -> float:
    if n in _T95:
        return _T95[n]
    keys = sorted(_T95)
    for k in keys:
        if k > n:
            return _T95[k]
    return 1.96


def summarize(values: Iterable[float]) -> dict:
    vals = [float(v) for v in values if v is not None]
    if not vals:
        return {"n": 0}
    if len(vals) == 1:
        v = vals[0]
        return {"n": 1, "mean": v, "std": 0.0, "ci95": [v, v],
                "min": v, "max": v}
    mean = statistics.mean(vals)
    std = statistics.stdev(vals)
    se = std / math.sqrt(len(vals))
    half = t95(len(vals)) * se
    return {
        "n": len(vals),
        "mean": round(mean, 2),
        "std": round(std, 2),
        "ci95": [round(mean - half, 2), round(mean + half, 2)],
        "min": min(vals),
        "max": max(vals),
    }


def majority_vote(values: Iterable[str]) -> tuple[str | None, float]:
    """Return (modal_value, fraction). Empty input → (None, 0.0)."""
    vs = [v for v in values if v is not None]
    if not vs:
        return None, 0.0
    counts = Counter(vs)
    top, n = counts.most_common(1)[0]
    return top, n / len(vs)


def is_noisy(summary: dict, threshold_cv: float = 0.25) -> bool:
    """Coefficient-of-variation > threshold → call the field 'noisy'."""
    if summary.get("n", 0) < 2:
        return False
    mean = summary.get("mean", 0)
    std = summary.get("std", 0)
    if mean == 0:
        return std > 0
    return abs(std / mean) > threshold_cv
