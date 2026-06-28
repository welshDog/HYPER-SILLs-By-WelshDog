#!/usr/bin/env python3
"""
body_double.py — ADHD body-double mode for HYPER-SILLs.

Body doubling is a low-stakes accountability practice: a quiet presence that
makes task-initiation easier. This script IS that presence — it holds your task
and loaded skills in view, nudges gently on an interval, then celebrates and
logs the session to the learning loop.

    python scripts/body_double.py --task "Wire the plugin marketplace" --skills HS-128,HS-129
    python scripts/body_double.py --task "..." --skills HS-128 --nudge 10   # nudge every 10 min
    python scripts/body_double.py --task "..." --skills HS-128 --once       # print one frame & exit

No external deps. Ctrl-C ends the session and records it.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NUDGES = [
    "Still here with you. One small step is plenty.",
    "No need to rush — progress, not perfection.",
    "Stuck? Shrink the next step until it's almost too easy.",
    "Hydrate, unclench your jaw, keep going. 💧",
    "You're doing the thing. That's the whole game.",
    "Lost the thread? Re-read your task line up top. No blame.",
]


def _banner(task: str, skills: list[str], started: datetime) -> str:
    mins = int((datetime.now() - started).total_seconds() // 60)
    bar = "─" * 48
    return (
        f"\n{bar}\n"
        f" 🧑‍🤝‍🧑 BODY DOUBLE — I'm here with you\n"
        f"{bar}\n"
        f"  Task:    {task}\n"
        f"  Skills:  {', '.join(skills) if skills else '(none loaded)'}\n"
        f"  Elapsed: {mins}m   Started: {started.strftime('%H:%M')}\n"
        f"  Next:    one small step. You pick it.\n"
        f"{bar}"
    )


def _record(skills: list[str], task: str) -> None:
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from skill_memory import record  # type: ignore
        if skills:
            record(skills, task=f"body-double: {task}", success=True)
    except Exception:  # noqa: BLE001
        pass


def main() -> int:
    ap = argparse.ArgumentParser(description="ADHD body-double mode.")
    ap.add_argument("--task", required=True, help="What you're working on")
    ap.add_argument("--skills", default="", help="Comma-separated skill IDs loaded")
    ap.add_argument("--nudge", type=int, default=15, help="Minutes between nudges (default 15)")
    ap.add_argument("--once", action="store_true", help="Print one frame and exit (no loop)")
    args = ap.parse_args()

    skills = [s.strip().upper() for s in args.skills.split(",") if s.strip()]
    started = datetime.now()

    print(_banner(args.task, skills, started))
    if args.once:
        _record(skills, args.task)
        print("\n  (--once) Frame shown. Session logged. Go get it. ⚡\n")
        return 0

    nudge_i = 0
    try:
        while True:
            time.sleep(max(1, args.nudge) * 60)
            print(_banner(args.task, skills, started))
            print(f"  💬 {NUDGES[nudge_i % len(NUDGES)]}")
            nudge_i += 1
    except KeyboardInterrupt:
        mins = int((datetime.now() - started).total_seconds() // 60)
        _record(skills, args.task)
        print(f"\n\n  ✅ BROski-approved. {mins}m of focus banked. Session logged.")
        print("     Rest is part of the work. Proud of you. 🐕⚡\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
