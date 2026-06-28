#!/usr/bin/env python3
"""
generate_skill_map.py — Visual skill constellation (Mermaid).

ADHD brains process spatial/visual structure faster than text lists. This emits
a Mermaid dependency graph of the vault — nodes colored by category, edges from
`depends_on`, and (optionally) node emphasis by usage heat from .skill-memory.

    python scripts/generate_skill_map.py                       # -> docs/skill-map.md
    python scripts/generate_skill_map.py --category agents      # one category
    python scripts/generate_skill_map.py --out ../BROski-Obsidian-Brain/Skills/MAP.md

Renders in Obsidian, GitHub, and any Mermaid viewer. No external deps.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = VAULT_ROOT / "skills-registry.json"
USAGE_LOG = VAULT_ROOT / ".skill-memory" / "usage-log.jsonl"
DEFAULT_OUT = VAULT_ROOT / "docs" / "skill-map.md"

CATEGORY_COLOR = {
    "agents":  "#3b82f6",   # blue
    "dev":     "#22c55e",   # green
    "broski":  "#a855f7",   # purple
    "youtube": "#ef4444",   # red
}


def safe_id(skill_id: str) -> str:
    return skill_id.replace("-", "_")


def parse_depends_on(path: Path) -> list[str]:
    """Pull depends_on skill IDs from a skill file's GoS block."""
    if not path.exists():
        return []
    txt = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^depends_on:(.*?)(?=^\w|\Z)", txt, re.MULTILINE | re.DOTALL)
    if not m:
        return []
    ids = re.findall(r"-\s*((?:HS|DS)-\d+)", m.group(1))
    return ids


def usage_counts() -> Counter:
    c: Counter = Counter()
    if USAGE_LOG.exists():
        for line in USAGE_LOG.read_text(encoding="utf-8").splitlines():
            try:
                for sid in json.loads(line).get("skills", []):
                    c[sid.upper()] += 1
            except Exception:  # noqa: BLE001
                continue
    return c


def build_mermaid(category: str = "") -> str:
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    skills = [s for s in reg.get("skills", []) if s.get("status", "").lower() != "archived"]
    if category:
        skills = [s for s in skills if s.get("category", "").lower().rstrip("/") == category.lower()]

    # Map both registry id and in-file skill_id -> node, so edges resolve across aliases.
    by_id = {s["id"].upper(): s for s in skills}
    file_id_to_reg = {}
    for s in skills:
        fp = VAULT_ROOT / s.get("file", "")
        if fp.exists():
            fm = re.search(r"^skill_id:\s*(\S+)", fp.read_text(encoding="utf-8", errors="replace"), re.MULTILINE)
            if fm:
                file_id_to_reg[fm.group(1).upper()] = s["id"].upper()

    usage = usage_counts()
    lines = ["```mermaid", "graph TD"]

    for s in skills:
        sid = s["id"].upper()
        hero = (s.get("hero_name") or sid).replace('"', "'")
        emoji = s.get("emoji", "")
        n = usage.get(sid, 0)
        label = f'{emoji} {hero}'.strip()
        if n:
            label += f' ⚡{n}'
        lines.append(f'    {safe_id(sid)}["{label}"]')

    # Edges: depends_on -> this skill.
    seen_edges = set()
    for s in skills:
        sid = s["id"].upper()
        fp = VAULT_ROOT / s.get("file", "")
        for dep in parse_depends_on(fp):
            dep = dep.upper()
            target = file_id_to_reg.get(dep, dep if dep in by_id else None)
            if target and target in by_id:
                edge = (target, sid)
                if edge not in seen_edges:
                    seen_edges.add(edge)
                    lines.append(f"    {safe_id(target)} --> {safe_id(sid)}")

    # Category colors.
    for s in skills:
        cat = s.get("category", "").lower().rstrip("/")
        color = CATEGORY_COLOR.get(cat)
        if color:
            lines.append(f"    style {safe_id(s['id'].upper())} fill:{color},color:#fff,stroke:#1e293b")

    lines.append("```")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a Mermaid skill constellation.")
    ap.add_argument("--category", default="", help="agents/dev/broski/youtube (default: all)")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    mermaid = build_mermaid(args.category)
    title = f"# 🌌 HYPER-SILLs Skill Constellation{(' — ' + args.category) if args.category else ''}\n"
    legend = (
        "\n> Nodes colored by category: 🔵 agents · 🟢 dev · 🟣 broski · 🔴 youtube. "
        "Edges = `depends_on`. ⚡N = times used (from .skill-memory).\n\n"
    )
    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(title + legend + mermaid + "\n", encoding="utf-8")
    edges = mermaid.count("-->")
    nodes = mermaid.count('["')
    print(f"wrote {out}  ({nodes} nodes, {edges} edges)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
