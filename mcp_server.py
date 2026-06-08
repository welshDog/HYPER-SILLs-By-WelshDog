#!/usr/bin/env python3
"""
HYPER-SILLs MCP Server
Exposes the 88-skill vault via Model Context Protocol (stdio transport).
Works with Claude Code, Cursor, Gemini CLI, Copilot, and any MCP-compatible IDE.

Usage:
    python mcp_server.py          # stdio (for mcp config wiring)
    python mcp_server.py --test   # smoke-test all tools and exit

Backed by arXiv:2604.05333 — Graph-of-Skills yields +25.55% reward,
-56.72% tokens vs flat skill loading.
"""

import json
import re
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

VAULT_ROOT = Path(__file__).parent
REGISTRY_PATH = VAULT_ROOT / "skills-registry.json"

mcp = FastMCP(
    "hyper-sills",
    instructions=(
        "HYPER-SILLs — 88-skill AI vault with Graph-of-Skills. "
        "Tools: search_skills, load_skill, get_skill_graph, recommend_for_task, list_skills_by_category. "
        "Categories: agents (49), dev (31), broski (7), youtube (1)."
    ),
)

# ── Registry cache ────────────────────────────────────────────────────────────

_registry: dict | None = None
_gos_index: dict | None = None  # skill_id → Path, for vault-only skills


def get_registry() -> dict:
    global _registry
    if _registry is None:
        _registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return _registry


def skills_list() -> list[dict]:
    return get_registry().get("skills", [])


def _build_gos_index() -> dict:
    """Build a lazy index of skill_id → file path from GoS blocks in vault files.
    Used as fallback for skills that are in files but not in the registry.
    """
    global _gos_index
    if _gos_index is not None:
        return _gos_index
    _gos_index = {}
    for fp in VAULT_ROOT.rglob("*.md"):
        try:
            txt = fp.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"^skill_id:\s*((?:HS|DS)-\d+)\s*$", txt, re.MULTILINE)
            if m:
                sid = m.group(1).strip().upper()
                _gos_index[sid] = fp
        except Exception:
            pass
    return _gos_index


def find_by_id(skill_id: str) -> dict | None:
    sid = skill_id.upper().strip()
    # Registry lookup first (fast path)
    result = next((s for s in skills_list() if s.get("id", "").upper() == sid), None)
    if result:
        return result
    # Fallback: scan GoS blocks in vault files (handles registry/file ID mismatches)
    idx = _build_gos_index()
    fp = idx.get(sid)
    if fp is None:
        return None
    try:
        content = fp.read_text(encoding="utf-8", errors="replace")
        gos = parse_gos(content)
        rel = fp.relative_to(VAULT_ROOT)
        return {
            "id":          gos.get("skill_id", sid),
            "hero_name":   gos.get("hero_name", sid),
            "emoji":       gos.get("emoji", ""),
            "description": gos.get("graph_notes", "")[:100],
            "category":    gos.get("category", ""),
            "version":     gos.get("version", ""),
            "file":        str(rel).replace("\\", "/"),
            "tags":        [],
            "pack":        "",
            "status":      "vault-only",
        }
    except Exception:
        return None


# ── GoS frontmatter parser ─────────────────────────────────────────────────────

def _parse_list_section(block: str, key: str) -> list[str]:
    """Pull a YAML list section by key name."""
    m = re.search(
        rf'^{key}:(.*?)(?=^\w|\Z)',
        block, re.MULTILINE | re.DOTALL
    )
    if not m:
        return []
    items = []
    for line in m.group(1).splitlines():
        item = re.match(r'\s*-\s*(.+)', line)
        if item:
            items.append(item.group(1).strip())
    return items


def _parse_ref_list(block: str, key: str) -> list[dict]:
    """Pull depends_on / related — list of '- HS-NNN  # comment' items."""
    m = re.search(
        rf'^{key}:(.*?)(?=^\w|\Z)',
        block, re.MULTILINE | re.DOTALL
    )
    if not m:
        return []
    refs = []
    for line in m.group(1).splitlines():
        item = re.match(r'\s*-\s*((?:HS|DS)-\d+|none)\s*(?:#\s*(.*))?', line)
        if item:
            ref_id = item.group(1).strip()
            note = (item.group(2) or "").strip()
            if ref_id.lower() != "none":
                refs.append({"id": ref_id, "note": note})
    return refs


def parse_gos(content: str) -> dict:
    """Extract GoS YAML block from the first --- ... --- pair in a skill file."""
    lines = content.splitlines()

    # Find opening ---
    start = next((i for i, l in enumerate(lines) if l.strip() == "---"), None)
    if start is None:
        return {}

    # Find closing ---
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].strip() == "---"),
        None,
    )
    if end is None:
        return {}

    block = "\n".join(lines[start + 1 : end])

    def scalar(pattern: str) -> str:
        m = re.search(pattern, block, re.MULTILINE)
        return m.group(1).strip().strip("\"'") if m else ""

    return {
        "skill_id":   scalar(r"^skill_id:\s*(.+)$"),
        "hero_name":  scalar(r'^hero_name:\s*["\']?(.+?)["\']?\s*$'),
        "emoji":      scalar(r'^emoji:\s*["\']?(.+?)["\']?\s*$'),
        "version":    scalar(r"^version:\s*(.+)$"),
        "category":   scalar(r"^category:\s*(.+)$"),
        "graph_notes": scalar(r'^graph_notes:\s*["\'](.+?)["\']'),
        "depends_on": _parse_ref_list(block, "depends_on"),
        "provides":   _parse_list_section(block, "provides"),
        "related":    _parse_ref_list(block, "related"),
    }


# ── Tools ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def search_skills(
    query: str = "",
    category: str = "",
    tag: str = "",
    limit: int = 10,
) -> str:
    """Search the HYPER-SILLs vault by keyword, category, or tag.

    Args:
        query: keyword matched against skill ID, hero name, description, and tags
        category: filter to one of: agents, dev, broski, youtube
        tag: filter by a specific tag (e.g. 'coding', 'orchestration', 'ND-friendly')
        limit: max results to return (default 10)

    Returns JSON with count and list of matching skills.
    """
    q = query.lower()
    cat = category.lower().rstrip("/")
    tg = tag.lower()

    tokens = q.split() if q else []
    results = []
    for s in skills_list():
        if tokens:
            haystack = " ".join([
                s.get("id", ""),
                s.get("hero_name", ""),
                s.get("description", ""),
                " ".join(s.get("tags", [])),
            ]).lower()
            if not all(t in haystack for t in tokens):
                continue
        if cat and s.get("category", "").lower().rstrip("/") != cat:
            continue
        if tg and tg not in [t.lower() for t in s.get("tags", [])]:
            continue
        results.append({
            "id":          s.get("id"),
            "hero_name":   s.get("hero_name"),
            "description": s.get("description"),
            "category":    s.get("category"),
            "file":        s.get("file"),
            "tags":        s.get("tags", []),
            "pack":        s.get("pack"),
        })
        if len(results) >= limit:
            break

    return json.dumps({"count": len(results), "results": results},
                      ensure_ascii=False, indent=2)


@mcp.tool()
def load_skill(skill_id: str) -> str:
    """Load the full content of a skill file by its ID (e.g. 'HS-042' or 'DS-028').

    Returns the complete markdown content plus parsed GoS metadata
    (depends_on, provides, related, graph_notes).

    Args:
        skill_id: the skill ID, e.g. 'HS-042', 'DS-009', 'HS-001'
    """
    meta = find_by_id(skill_id)
    if not meta:
        return json.dumps({
            "error": f"Skill '{skill_id}' not found in registry.",
            "hint": "Call search_skills() to find the right ID.",
        })

    fp = VAULT_ROOT / meta["file"]
    if not fp.exists():
        return json.dumps({"error": f"File not on disk: {meta['file']}"})

    content = fp.read_text(encoding="utf-8", errors="replace")
    gos = parse_gos(content)

    return json.dumps({
        "id":          meta["id"],
        "hero_name":   meta["hero_name"],
        "description": meta.get("description", ""),
        "category":    meta.get("category"),
        "file":        meta["file"],
        "tags":        meta.get("tags", []),
        "gos":         gos,
        "content":     content,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_skill_graph(skill_id: str) -> str:
    """Return the Graph-of-Skills dependency graph for a skill.

    Shows:
    - depends_on: skills to load BEFORE this one (prerequisites)
    - provides:   capability slugs this skill unlocks
    - related:    adjacent skills worth loading together

    Hero names are resolved for all referenced skills so you can
    chain-load the right pack without looking up IDs manually.

    Args:
        skill_id: the skill ID, e.g. 'HS-008', 'HS-042'
    """
    meta = find_by_id(skill_id)
    if not meta:
        return json.dumps({
            "error": f"Skill '{skill_id}' not found.",
            "hint": "Call search_skills() to find the right ID.",
        })

    fp = VAULT_ROOT / meta["file"]
    if not fp.exists():
        return json.dumps({"error": f"File not on disk: {meta['file']}"})

    content = fp.read_text(encoding="utf-8", errors="replace")
    gos = parse_gos(content)

    def resolve(refs: list[dict]) -> list[dict]:
        out = []
        for r in refs:
            ref_meta = find_by_id(r["id"])
            out.append({
                "id":          r["id"],
                "hero_name":   ref_meta["hero_name"] if ref_meta else "(not in registry)",
                "description": ref_meta.get("description", "") if ref_meta else "",
                "note":        r.get("note", ""),
            })
        return out

    return json.dumps({
        "id":          meta["id"],
        "hero_name":   meta["hero_name"],
        "emoji":       gos.get("emoji", ""),
        "graph_notes": gos.get("graph_notes", ""),
        "depends_on":  resolve(gos.get("depends_on", [])),
        "provides":    gos.get("provides", []),
        "related":     resolve(gos.get("related", [])),
        "load_order_hint": (
            "Load depends_on skills first, then this skill, "
            "then optionally load related skills for context."
        ),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def recommend_for_task(task: str, limit: int = 5) -> str:
    """Recommend the best skills for a given task description.

    Examples:
      "build a new agent from scratch"
      "add prometheus metrics to my FastAPI service"
      "write ND-friendly error messages"
      "set up a nightly self-improvement loop"
      "design an A/B test for agent behaviour"

    Args:
        task: natural-language description of what you're trying to do
        limit: max skills to return (default 5)
    """
    if not task.strip():
        return json.dumps({
            "error": "Provide a task description.",
            "example": 'recommend_for_task("build a self-healing agent")',
        })

    keywords = [w for w in re.split(r'\W+', task.lower()) if len(w) > 2]
    scored = []
    for s in skills_list():
        haystack = " ".join([
            s.get("id", ""),
            s.get("hero_name", ""),
            s.get("description", ""),
            s.get("category", ""),
            " ".join(s.get("tags", [])),
        ]).lower()
        score = sum(1 for kw in keywords if kw in haystack)
        if score > 0:
            scored.append((score, s))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = [
        {
            "id":               s["id"],
            "hero_name":        s["hero_name"],
            "description":      s.get("description", ""),
            "category":         s.get("category"),
            "relevance_score":  score,
            "tags":             s.get("tags", []),
            "next_step":        f'load_skill("{s["id"]}")',
        }
        for score, s in scored[:limit]
    ]

    return json.dumps({
        "task":        task,
        "count":       len(results),
        "recommended": results,
        "tip": (
            "Run get_skill_graph(id) on the top result to find "
            "prerequisite skills to load first (GoS load-order)."
        ),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def list_skills_by_category(category: str = "") -> str:
    """List all skills in a category, or show category overview if none given.

    Args:
        category: 'agents', 'dev', 'broski', or 'youtube'. Leave blank for overview.
    """
    if not category:
        meta = get_registry().get("_meta", {})
        packs = get_registry().get("packs", {})
        return json.dumps({
            "total_skills": meta.get("total_skills", 0),
            "categories":   meta.get("categories", {}),
            "packs": {pack: len(ids) for pack, ids in packs.items()},
            "hint": 'Call list_skills_by_category("agents") to see all agent skills.',
        }, ensure_ascii=False, indent=2)

    cat = category.lower().rstrip("/")
    skills = [
        {
            "id":          s["id"],
            "hero_name":   s["hero_name"],
            "description": s.get("description", ""),
            "tags":        s.get("tags", []),
        }
        for s in skills_list()
        if s.get("category", "").lower().rstrip("/") == cat
    ]

    return json.dumps({
        "category": category,
        "count":    len(skills),
        "skills":   skills,
    }, ensure_ascii=False, indent=2)


# ── Smoke test ─────────────────────────────────────────────────────────────────

def _smoke_test():
    print("HYPER-SILLs MCP Server — smoke test\n")

    print("1. list_skills_by_category()")
    r = json.loads(list_skills_by_category())
    print(f"   total={r['total_skills']} cats={r['categories']}\n")

    print("2. search_skills(query='agent')")
    r = json.loads(search_skills(query="agent", limit=3))
    print(f"   count={r['count']}  first={r['results'][0]['id'] if r['results'] else 'none'}\n")

    print("3. recommend_for_task('build a self-healing agent')")
    r = json.loads(recommend_for_task("build a self-healing agent", limit=3))
    for s in r["recommended"]:
        print(f"   {s['id']} {s['hero_name']} (score={s['relevance_score']})")
    print()

    print("4. get_skill_graph('HS-008')")
    r = json.loads(get_skill_graph("HS-008"))
    print(f"   {r['id']} {r['hero_name']}")
    print(f"   depends_on: {[d['id'] for d in r['depends_on']]}")
    print(f"   provides:   {r['provides'][:3]}")
    print()

    print("5. load_skill('HS-042')")
    r = json.loads(load_skill("HS-042"))
    print(f"   {r['id']} {r['hero_name']}")
    print(f"   content length: {len(r.get('content',''))} chars")
    gos = r.get("gos", {})
    print(f"   gos.graph_notes: {gos.get('graph_notes','(none)')[:60]}")
    print()

    print("All tools OK.")


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--test" in sys.argv:
        _smoke_test()
    else:
        mcp.run(transport="stdio")
