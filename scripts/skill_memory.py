#!/usr/bin/env python3
"""
skill_memory.py — HYPER-SILLs usage learning loop.

Skills get smarter the more they're used. This appends lightweight, git-tracked
usage events to `.skill-memory/` and analyses them for:
  - which skills are used most / never (drift candidates)
  - which skills are used TOGETHER (co-occurrence → super-pack suggestions)
  - dependency gaps (a skill repeatedly used right before another)

Public API:
  record(skill_ids, task="", success=True)   # append a usage event
  analyze() -> str                            # human-readable report

Zero external dependencies. Storage is JSONL so appends are cheap and conflict-free.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
MEM_DIR = VAULT_ROOT / ".skill-memory"
USAGE_LOG = MEM_DIR / "usage-log.jsonl"
REGISTRY_PATH = VAULT_ROOT / "skills-registry.json"


def record(skill_ids: list[str] | str, task: str = "", success: bool = True) -> None:
    """Append one usage event. `skill_ids` may be a list or comma-separated string."""
    if isinstance(skill_ids, str):
        skill_ids = [s.strip().upper() for s in skill_ids.split(",") if s.strip()]
    if not skill_ids:
        return
    MEM_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "skills": skill_ids,
        "task": task[:200],
        "success": bool(success),
    }
    with USAGE_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _load_events() -> list[dict]:
    if not USAGE_LOG.exists():
        return []
    out = []
    for line in USAGE_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _all_skill_ids() -> set[str]:
    try:
        reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        return {s["id"].upper() for s in reg.get("skills", [])}
    except Exception:  # noqa: BLE001
        return set()


def analyze() -> str:
    events = _load_events()
    if not events:
        return ("No usage recorded yet. The loop fills as skills get used "
                "(session-end hook records automatically, or call "
                "skill_memory.record([...])).")

    usage = Counter()
    cooc = Counter()
    fails = Counter()
    for e in events:
        skills = [s.upper() for s in e.get("skills", [])]
        for s in skills:
            usage[s] += 1
            if not e.get("success", True):
                fails[s] += 1
        for a, b in combinations(sorted(set(skills)), 2):
            cooc[(a, b)] += 1

    known = _all_skill_ids()
    never = sorted(known - set(usage)) if known else []

    lines = [f"🧠 Skill-memory report — {len(events)} sessions\n"]
    lines.append("Most used:")
    for sid, n in usage.most_common(5):
        flag = f"  ⚠️ {fails[sid]} fails" if fails[sid] else ""
        lines.append(f"  {sid}: {n}{flag}")

    if cooc:
        lines.append("\nUsed together (super-pack candidates):")
        for (a, b), n in cooc.most_common(5):
            if n >= 2:
                lines.append(f"  {a} + {b}: {n}x  → consider bundling")

    if never:
        lines.append(f"\nNever used ({len(never)}) — drift/review candidates:")
        lines.append("  " + ", ".join(never[:15]) + ("  ..." if len(never) > 15 else ""))

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "record":
        record(sys.argv[2] if len(sys.argv) > 2 else "", task=" ".join(sys.argv[3:]))
        print("recorded.")
    else:
        print(analyze())
