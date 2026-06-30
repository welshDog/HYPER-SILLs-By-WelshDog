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
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone

# Repo root — skill file paths in vault-index.md are relative to this.
REPO_ROOT = Path(__file__).resolve().parent.parent

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

# ── Tag + keyword enrichment ────────────────────────────────────────────────
# Registry tags were generic per-category defaults (e.g. agents/orchestration/ai),
# so literal-term keyword search was blind ("docker" -> 0 hits). Enrich each skill
# with its frontmatter `provides` slugs (shown as tags) + content-frequency terms
# (hidden `keywords`, used by search_skills) so meaningful words actually match.
_STOP = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with", "is",
    "are", "be", "this", "that", "it", "as", "at", "by", "from", "you", "your",
    "my", "use", "uses", "using", "via", "when", "what", "which", "how", "do",
    "if", "not", "but", "can", "will", "all", "any", "one", "two", "its", "has",
    "skill", "skills", "prompt", "example", "agent", "agents", "hyper", "broski",
}


def parse_problem_keywords(fm_text: str) -> list[str]:
    """Curated `problem_keywords` YAML list from frontmatter (phrases may contain
    spaces, e.g. 'keeps crashing'), preserved verbatim for the dense embed doc."""
    bm = re.search(r'(?m)^problem_keywords:\s*\n((?:[ \t]*-[ \t]*.+\n?)+)', fm_text)
    if not bm:
        return []
    return [ln.strip() for ln in re.findall(r'(?m)^[ \t]*-[ \t]*(.+?)\s*$', bm.group(1))]


def enrich_tags_keywords(fm_text: str, base_tags: list[str]) -> tuple[list[str], list[str]]:
    """Return (display_tags, search_keywords) for one skill.

    tags     = category defaults + frontmatter `provides` slugs (curated, shown).
    keywords = top content-frequency terms + split provides (search-only, hidden).
    """
    tags = list(base_tags)
    provides: list[str] = []
    pm = re.search(r'(?m)^provides:\s*\n((?:[ \t]*-[ \t]*.+\n?)+)', fm_text)
    if pm:
        provides = [p.strip() for p in re.findall(r'-[ \t]*([A-Za-z0-9][\w\-]+)', pm.group(1))]
        for p in provides:
            if p and p not in tags:
                tags.append(p)

    # Body = everything outside the YAML frontmatter block.
    body = re.sub(r'(?ms)^---\s*$.*?^---\s*$', '', fm_text, count=1)
    freq = Counter(w for w in re.findall(r'[a-z][a-z0-9]{2,}', body.lower()) if w not in _STOP)
    keywords = {w for w, _ in freq.most_common(20)}
    for p in provides:                         # make slug words individually searchable
        keywords.update(w for w in p.split('-') if len(w) > 2 and w not in _STOP)
    keywords.update(t for t in tags if '-' not in t and len(t) > 2)
    return tags, sorted(keywords)


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
    # Match table rows: | HS-NNN | or | DS-NNN | name cell | file cell | source | category |
    row_re = re.compile(r'^\|\s*((?:HS|DS)-\d+)\s*\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|\s*$')

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
        status = "rescued"

        # Prefer richer in-file frontmatter when present (semver + lifecycle),
        # and enrich tags/keywords from the file content for real keyword search.
        tags, keywords, problem_keywords = list(meta["tags"]), [], []
        skill_fp = (REPO_ROOT / file_path)
        if skill_fp.exists():
            fm = skill_fp.read_text(encoding="utf-8", errors="replace")
            vm = re.search(r'^version:\s*["\']?(v\d+\.\d+(?:\.\d+)?)', fm, re.MULTILINE)
            if vm:
                version = vm.group(1)
            sm = re.search(r'^status:\s*["\']?([A-Za-z]+)', fm, re.MULTILINE)
            if sm:
                status = sm.group(1).upper() if sm.group(1).lower() != "rescued" else "rescued"
            tags, keywords = enrich_tags_keywords(fm, meta["tags"])
            problem_keywords = parse_problem_keywords(fm)
            # Fold curated phrase tokens into the literal-search keyword bag too.
            kw = set(keywords)
            for ph in problem_keywords:
                kw.update(w for w in re.split(r'[^a-z0-9]+', ph.lower())
                          if len(w) > 2 and w not in _STOP)
            keywords = sorted(kw)

        skills.append({
            "id":          raw_id,
            "hero_name":   hero,
            "emoji":       emoji,
            "description": description,
            "category":    category_key.rstrip('/'),
            "version":     version,
            "file":        file_path,
            "source_repo": raw_source.strip(),
            "tags":        tags,
            "keywords":    keywords,
            "problem_keywords": problem_keywords,
            "pack":        meta["pack"],
            "status":      status,
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
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total_skills": len(skills),
            "categories":   categories,
        },
        "packs": packs,
        "skills": skills,
    }


def reconcile_disk(skills: list[dict]) -> list[str]:
    """Safety net: find skill .md files on disk that the registry missed.

    The registry is generated from vault-index.md. If a skill file exists on
    disk but was never promoted to a RESCUED row, it silently vanishes from the
    registry, the MCP server, and the bridge manifest. This catches that.
    Returns the list of stranded file paths (relative to repo root).
    """
    header_re = re.compile(r'#\s*(?:\S+\s+)?(?:HS|DS)-\d+\s*[—-]')
    reg_files = {s["file"] for s in skills}
    stranded = []
    for folder in CATEGORY_META:  # only real skill folders
        for fp in sorted((REPO_ROOT / folder.rstrip("/")).glob("*.md")):
            head = fp.read_text(encoding="utf-8", errors="replace")[:200]
            if not header_re.search(head):
                continue  # not a skill file (template, readme, etc.)
            rel = fp.relative_to(REPO_ROOT).as_posix()
            if rel not in reg_files:
                stranded.append(rel)
    return stranded


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="Generate HYPER-SKILLs registry JSON")
    parser.add_argument("--vault",  default="vault-index.md",        help="Path to vault-index.md")
    parser.add_argument("--output", default="skills-registry.json",  help="Output JSON path")
    parser.add_argument("--pretty", action="store_true", default=True, help="Pretty-print JSON")
    args = parser.parse_args()

    vault_path  = Path(args.vault)
    output_path = Path(args.output)

    if not vault_path.exists():
        print(f"vault-index.md not found at: {vault_path}")
        sys.exit(1)

    print(f"\nParsing {vault_path}...")
    skills = parse_vault_index(vault_path)
    print(f"Found {len(skills)} rescued skills")

    registry = build_registry(skills)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    indent = 2 if args.pretty else None
    output_path.write_text(json.dumps(registry, indent=indent, ensure_ascii=False), encoding="utf-8")

    print(f"\nRegistry written -> {output_path}")
    print(f"   Skills:     {registry['_meta']['total_skills']}")
    print(f"   Categories: {json.dumps(registry['_meta']['categories'], indent=6)}")
    print(f"   Packs:      {list(registry['packs'].keys())}")

    # Safety net — warn loudly if any skill file on disk isn't in the registry.
    stranded = reconcile_disk(skills)
    if stranded:
        print(f"\n⚠️  {len(stranded)} skill file(s) on disk are MISSING from the registry")
        print("   (they exist on disk but have no RESCUED row in vault-index.md):")
        for s in stranded:
            print(f"     - {s}")
        print("   Add a RESCUED row for each in vault-index.md, then re-run.")
    else:
        print("\n✅ Disk reconciliation clean — every skill file on disk is registered.")


if __name__ == "__main__":
    main()
