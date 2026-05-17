"""One-off: build a realistic synthetic okx_pulse-shaped sqlite db.

Used when no live okx_pulse.db is available for demo runs.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "src"))

from tests.fakes import make_in_memory_signalstream_db  # noqa: E402


def main(out: str = "demo.db", n_events: int = 200, seed: int = 1) -> None:
    src = make_in_memory_signalstream_db(n_events=n_events, seed=seed)
    dst = sqlite3.connect(out)
    src.backup(dst)
    src.close()
    dst.close()
    print(f"[OK] wrote {n_events} events to {Path(out).resolve()}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "demo.db"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    main(out, n)
