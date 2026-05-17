"""Real-user behavior dataset.

Schema (CSV or JSON list):
    real_user_id     str   unique id
    persona_match    str   stem of the persona archetype they map to
                            (e.g. "03_scalper") — human-labeled by product team
    subscribed       bool  did they subscribe at all?
    churned_at       iso8601 or null  when did they leave (null if still active)
    pricing_paid_usd float monthly USD paid (0 if free / unsubscribed)
    actions          comma-separated list of commands they actually issued
                       (optional, for agentic action-sequence comparison)

CSV example (header required):
    real_user_id,persona_match,subscribed,churned_at,pricing_paid_usd,actions
    u_001,01_burnt_veteran,true,,10,/profile swing,/mute 6h
    u_002,07_noise_allergic_manager,false,2026-01-15,0,UNSUBSCRIBE
"""
from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class RealUser:
    real_user_id: str
    persona_match: str
    subscribed: bool
    churned_at: str | None = None
    pricing_paid_usd: float = 0.0
    actions: list[str] = field(default_factory=list)

    @classmethod
    def from_row(cls, row: dict) -> "RealUser":
        actions = row.get("actions") or ""
        if isinstance(actions, str):
            actions = [a.strip() for a in actions.split(",") if a.strip()]
        sub = row.get("subscribed")
        if isinstance(sub, str):
            sub = sub.strip().lower() in ("1", "true", "yes", "y", "t")
        price = row.get("pricing_paid_usd") or 0
        try:
            price = float(price)
        except (ValueError, TypeError):
            price = 0.0
        return cls(
            real_user_id=str(row["real_user_id"]),
            persona_match=str(row["persona_match"]),
            subscribed=bool(sub),
            churned_at=(row.get("churned_at") or None) or None,
            pricing_paid_usd=price,
            actions=list(actions),
        )


def load_real_users(path: Path | str) -> list[RealUser]:
    """Load truth dataset from CSV or JSON."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [RealUser.from_row(row) for row in reader]
    if path.suffix.lower() in (".json", ".jsonl"):
        text = path.read_text("utf-8")
        if path.suffix.lower() == ".jsonl":
            return [RealUser.from_row(json.loads(line))
                    for line in text.splitlines() if line.strip()]
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError(f"{path} must contain a list of dicts")
        return [RealUser.from_row(r) for r in data]
    raise ValueError(f"unsupported real-users file format: {path.suffix}")


def save_real_users(users: list[RealUser], path: Path | str) -> None:
    path = Path(path)
    if path.suffix.lower() == ".csv":
        rows = [asdict(u) for u in users]
        for r in rows:
            r["actions"] = ",".join(r["actions"])
        with path.open("w", encoding="utf-8", newline="") as f:
            if not rows:
                return
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        return
    path.write_text(
        json.dumps([asdict(u) for u in users], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
