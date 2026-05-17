"""Shared time-zone helpers (CST = Asia/Shanghai = UTC+8)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

CST = timezone(timedelta(hours=8))


def now_cst_str(fmt: str = "%Y-%m-%d %H:%M UTC+8") -> str:
    return datetime.now(CST).strftime(fmt)


def ts_to_cst(ts: float, fmt: str = "%H:%M") -> str:
    return datetime.fromtimestamp(ts, CST).strftime(fmt)
