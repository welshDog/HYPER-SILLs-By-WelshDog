#!/usr/bin/env python3
"""
trigger_engine.py — Auto-suggest HYPER-SILLs skill packs from context.

The best skill system loads skills BEFORE you ask. This scores each pack's
trigger conditions (keywords / file_patterns / context_signals, minus
exclusions) against the current task text and open files, returning ranked
pack suggestions.

    python scripts/trigger_engine.py --context "build a fastapi agent" --files Dockerfile main.py
    python scripts/trigger_engine.py --context "edit my youtube thumbnail" --json

Reads packs/<pack>/manifest.yaml. No external deps (tiny built-in YAML reader
for the simple 2-level manifest shape we control).
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = VAULT_ROOT / "packs"
REGISTRY_PATH = VAULT_ROOT / "skills-registry.json"


def read_manifest(path: Path) -> dict:
    """Minimal YAML reader for our manifest shape: scalars, `key:` lists of `- item`."""
    data: dict = {}
    cur_top: str | None = None
    cur_sub: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if line.startswith("- "):
            item = line[2:].strip().strip('"\'')
            if indent <= 2 and cur_top:
                data.setdefault(cur_top, []).append(item)
            elif cur_top and cur_sub is not None:
                data[cur_top].setdefault(cur_sub, []).append(item)
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"\'')
            if indent == 0:
                cur_top, cur_sub = key, None
                data[cur_top] = val if val else {}
            else:
                cur_sub = key
                if not isinstance(data.get(cur_top), dict):
                    data[cur_top] = {}
                data[cur_top][cur_sub] = val if val else []
    return data


def load_packs() -> list[dict]:
    packs = []
    if not PACKS_DIR.exists():
        return packs
    for mf in sorted(PACKS_DIR.glob("*/manifest.yaml")):
        try:
            packs.append(read_manifest(mf))
        except Exception:  # noqa: BLE001
            continue
    return packs


def pack_skill_ids(pack_name: str) -> list[str]:
    try:
        reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        return reg.get("packs", {}).get(pack_name, [])
    except Exception:  # noqa: BLE001
        return []


def score_pack(pack: dict, context: str, files: list[str]) -> tuple[float, list[str]]:
    ctx = context.lower()
    why: list[str] = []
    score = 0.0
    trig = pack.get("triggers", {}) or {}

    for kw in trig.get("keywords", []):
        if kw.lower() in ctx:
            score += 2.0
            why.append(f"keyword '{kw}'")
    for sig in trig.get("context_signals", []):
        # loose match: any 3+ char word from the signal present
        words = [w for w in re.split(r"\W+", sig.lower()) if len(w) > 3]
        if words and sum(w in ctx for w in words) >= max(1, len(words) // 2):
            score += 1.0
            why.append(f"signal '{sig}'")
    for pat in trig.get("file_patterns", []):
        if any(fnmatch.fnmatch(f, pat) or fnmatch.fnmatch(f, f"*/{pat}") for f in files):
            score += 1.5
            why.append(f"file ~ '{pat}'")

    # Exclusions zero it out — wrong pack for this context.
    for ex in trig.get("exclusions", []):
        if ex.lower() in ctx:
            return 0.0, [f"excluded by '{ex}'"]

    return score, why


def suggest(context: str, files: list[str]) -> list[dict]:
    out = []
    for pack in load_packs():
        score, why = score_pack(pack, context, files)
        if score > 0:
            name = pack.get("name", "?")
            out.append({
                "pack": name,
                "score": round(score, 2),
                "skills": len(pack_skill_ids(name)),
                "why": why,
                "auto_load": str(pack.get("auto_load", "false")).lower() == "true",
            })
    out.sort(key=lambda x: x["score"], reverse=True)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Suggest skill packs from context.")
    ap.add_argument("--context", default="", help="Task description / current context")
    ap.add_argument("--files", nargs="*", default=[], help="Open/changed file paths")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    hits = suggest(args.context, args.files)
    if args.json:
        print(json.dumps({"suggestions": hits}, ensure_ascii=False, indent=2))
        return 0
    if not hits:
        print("No pack triggered — use semantic search or /skill-find instead.")
        return 0
    print("\nSuggested packs:\n")
    for h in hits:
        tag = " (auto-load)" if h["auto_load"] else ""
        print(f"  {h['pack']}{tag}  — score {h['score']}, {h['skills']} skills")
        print(f"      because: {', '.join(h['why'][:4])}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
