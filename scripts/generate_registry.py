#!/usr/bin/env python3
"""
HYPER-SKILLs Registry Generator
Parses vault-index.md and outputs skills-registry.json
Usage: python scripts/generate_registry.py
       python scripts/generate_registry.py --output path/to/output.json
"""

import re
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

# ── Category → tags + pack mapping ──────────────────────────────────────────
CATEGORY_META = {
    "agents/":    {"tags": ["agents", "orchestration", "ai"],        "pack": "Agent Builder Pack"},
    "dev/":       {"tags": ["coding", "dev", "tooling"],             "pack": "ND-Friendly Coding Pack"},
    "broski/":    {"tags": ["broski", "ND-friendly", "hyperfocus"],  "pack": "ND-Friendly Coding Pack"},
    "youtube/":   {"tags": ["youtube", "content", "analytics"],      "pack": "YouTube Growth Pack"},
    "content/":   {"tags": ["content", "writing", "scripts"],        "pack": "YouTube Growth Pack"},
    "hypercode/": {"tags": ["hypercode", "system", "architecture"],  "pack": None},
    "web3/":      {"tags": ["web3", "nft", "blockchain"],            "pack": None},
}

# ── Parse a skill hero name from the vault-index name cell ───────────────────
HERO_RE = re.compile(r'\*\*(.+?)\*\*')

def extract_hero_name(raw_name: str) -> str:
    """Pull the hero name from '📊 **SIGNAL HUNTER** — YT Analytics Debugger'"""
    match = HERO_RE.search(raw_name)
    return match.group(1).strip() if match else raw_name.strip()

def extract_description(raw_name: str) -> str:
    """Pull the subtitle from after the em-dash"""
    if '—' in raw_name:
        return raw_name.split('—', 1)[1].strip()
    return ""

def extract_emoji(raw_name: str) -> str:
    """Grab the leading emoji if present"""
    # Emoji are the first character(s) before the space+bold
    parts = raw_name.split('**', 1)
    return parts[0].strip() if parts else ""

def parse_file_path(raw_path: str) -> str | None:
    """Extract file path from markdown link like [`youtube/YT_DEBUGGER_v1.md`](youtube/...)"""
    match = re.search(r'\(([^)]+\.md)\)', raw_path)
    return match.group(1).strip() if match else None

def parse_vault_index(vault_path: Path) -> list[dict]:
    content = vault_path.read_text(encoding="utf-8")

    # ── Rescued skills section ────────────────────────────────────────────
    rescued_section = ""
    in_rescued = False
    for line in content.splitlines():
        if "## ✅ RESCUED SKILLS" in line:
            in_rescued = True
        elif line.startswith("## ") and in_rescued:
            break
        if in_rescued:
            rescued_section += line + "\n"

    skills = []
    # Match table rows: | HS-NNN | name cell | file cell | source | category |
    row_re = re.compile(r'^\|\s*(HS-\d+)\s*\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|\s*$')

    for line in rescued_section.splitlines():
        m = row_re.match(line.strip())
        if not m:
            continue
        raw_id, raw_name, raw_file, raw_source, raw_cat = [
            x.strip() for x in m.groups()
        ]
        if raw_id == "ID":  # header row
            continue

        file_path = parse_file_path(raw_file)
        if not file_path:
            continue

        category_key = raw_cat.strip('`').strip()
        meta = CATEGORY_META.get(category_key, {"tags": [], "pack": None})
        hero = extract_hero_name(raw_name)
        description = extract_description(raw_name)
        emoji = extract_emoji(raw_name)

        # Derive version from filename (e.g. _v1.md → v1.0)
        ver_match = re.search(r'_v(\d+)\.md$', file_path)
        version = f"v{ver_match.group(1)}.0" if ver_match else "v1.0"

        skills.append({
            "id":          raw_id,
            "hero_name":   hero,
            "emoji":       emoji,
            "description": description,
            "category":    category_key.rstrip('/'),
            "version":     version,
            "file":        file_path,
            "source_repo": raw_source.strip(),
            "tags":        meta["tags"],
            "pack":        meta["pack"],
            "status":      "rescued",
        })

    return skills


def build_registry(skills: list[dict]) -> dict:
    categories = {}
    packs = {}
    for s in skills:
        cat = s["category"]
        categories[cat] = categories.get(cat, 0) + 1
        if s["pack"]:
            packs.setdefault(s["pack"], []).append(s["id"])

    return {
        "_meta": {
            "name":         "HYPER-SKILLs Registry",
            "repo":         "welshDog/HYPER-SILLs-By-WelshDog",
            "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total_skills": len(skills),
            "categories":   categories,
        },
        "packs": packs,
        "skills": skills,
    }


def main():
    parser = argparse.ArgumentParser(description="Generate HYPER-SKILLs registry JSON")
    parser.add_argument("--vault",  default="vault-index.md",        help="Path to vault-index.md")
    parser.add_argument("--output", default="skills-registry.json",  help="Output JSON path")
    parser.add_argument("--pretty", action="store_true", default=True, help="Pretty-print JSON")
    args = parser.parse_args()

    vault_path  = Path(args.vault)
    output_path = Path(args.output)

    if not vault_path.exists():
        print(f"❌ vault-index.md not found at: {vault_path}")
        sys.exit(1)

    print(f"\n🔍 Parsing {vault_path}...")
    skills = parse_vault_index(vault_path)
    print(f"✅ Found {len(skills)} rescued skills")

    registry = build_registry(skills)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    indent = 2 if args.pretty else None
    output_path.write_text(json.dumps(registry, indent=indent, ensure_ascii=False), encoding="utf-8")

    print(f"\n📦 Registry written → {output_path}")
    print(f"   Skills:     {registry['_meta']['total_skills']}")
    print(f"   Categories: {json.dumps(registry['_meta']['categories'], indent=6)}")
    print(f"   Packs:      {list(registry['packs'].keys())}")
    print(f"\n🏆 Done! BROski approved ♾️\n")


if __name__ == "__main__":
    main()
