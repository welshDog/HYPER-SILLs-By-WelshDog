#!/usr/bin/env python3
"""
HYPER-SILLs MCP Server
Exposes the 120-skill vault via Model Context Protocol.
Works with Claude Code, Cursor, Gemini CLI, Copilot, and any MCP-compatible IDE,
plus remote hosts (Railway/Render) and the Perplexity MCP connector over HTTP.

Usage:
    python mcp_server.py          # stdio (for local mcp config wiring)
    python mcp_server.py --http   # streamable-HTTP on $PORT (default 8000) for remote hosts
    python mcp_server.py --test   # smoke-test all tools and exit

Health: GET /health -> {"status":"ok",...} (served when running over HTTP).

Backed by arXiv:2604.05333 — Graph-of-Skills yields +25.55% reward,
-56.72% tokens vs flat skill loading.
"""

import json
import os
import re
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse

SERVER_VERSION = "1.1.0"

VAULT_ROOT = Path(__file__).parent
REGISTRY_PATH = VAULT_ROOT / "skills-registry.json"
# Self-contained bundle (built by scripts/build_plugin.py for the Claude Code
# plugin). When present, skill `content` + `gos` are embedded, so the server
# needs no loose .md files — this is what makes the bundled plugin work after a
# github install (where only the plugin dir is cached). Repo runs fine without it.
BUNDLE_PATH = VAULT_ROOT / "skills-bundle.json"

mcp = FastMCP(
    "hyper-sills",
    instructions=(
        "HYPER-SILLs — 120-skill AI vault with Graph-of-Skills. "
        "Tools: search_skills, semantic_search, load_skill, get_skill_graph, recommend_for_task, list_skills_by_category. "
        "Resources (SEP-2640 Skills-over-MCP): skills://index, skill://HS-NNN. "
        "Categories: agents (51), dev (39), hypercode (12), broski (7), web3 (7), youtube (4)."
    ),
)

# ── Registry cache ────────────────────────────────────────────────────────────

_registry: dict | None = None
_gos_index: dict | None = None  # skill_id → Path, for vault-only skills


def get_registry() -> dict:
    global _registry
    if _registry is None:
        # Prefer the self-contained bundle (skills carry embedded content + gos).
        src = BUNDLE_PATH if BUNDLE_PATH.exists() else REGISTRY_PATH
        _registry = json.loads(src.read_text(encoding="utf-8"))
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
        category: filter to one of: agents, dev, hypercode, broski, web3, youtube
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
def semantic_search(query: str, limit: int = 5) -> str:
    """Find skills by describing the problem in natural language (meaning, not keywords).

    Ranks skills by semantic similarity to your description — use this when you
    don't know the hero name or ID. Falls back to keyword search if the vector
    index is unavailable.

    Args:
        query: natural-language description, e.g. "auto-restart a crashed agent"
        limit: max results (default 5)

    Examples:
        semantic_search("publish my skills so other tools can use them")
        semantic_search("stop my agents spawning forever")
    """
    if not query.strip():
        return json.dumps({"error": "Describe what you need in a sentence."})
    try:
        sys.path.insert(0, str(VAULT_ROOT / "scripts"))
        from search_skills import semantic_search as _ss  # type: ignore
        hits = _ss(query, limit=limit)
        if hits:
            return json.dumps({"query": query, "backend": "semantic",
                               "count": len(hits), "results": hits},
                              ensure_ascii=False, indent=2)
    except Exception as e:  # noqa: BLE001 — degrade gracefully to keyword search
        pass
    # Fallback: keyword search never leaves the user stuck (Mercy Message ethos).
    return search_skills(query=query, limit=limit)


def _content_and_gos(meta: dict) -> tuple[str | None, dict]:
    """Return (content, gos) for a skill — preferring the bundle's embedded
    fields, else reading the loose .md file. content is None if neither exists."""
    if meta.get("content"):
        return meta["content"], (meta.get("gos") or parse_gos(meta["content"]))
    fp = VAULT_ROOT / meta.get("file", "")
    if fp.exists():
        c = fp.read_text(encoding="utf-8", errors="replace")
        return c, parse_gos(c)
    return None, (meta.get("gos") or {})


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
        return _mercy_not_found(skill_id)

    content, gos = _content_and_gos(meta)
    if content is None:
        return json.dumps({"error": f"Content unavailable for {meta.get('file')}"})

    return json.dumps({
        "id":          meta["id"],
        "hero_name":   meta["hero_name"],
        "description": meta.get("description", ""),
        "category":    meta.get("category"),
        "file":        meta.get("file"),
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
        return _mercy_not_found(skill_id)

    _content, gos = _content_and_gos(meta)

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
        category: 'agents', 'dev', 'hypercode', 'broski', 'web3', or 'youtube'. Leave blank for overview.
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


# ── Resources (Skills-over-MCP / SEP-2640 alignment) ───────────────────────────
# The "Skills over MCP" working group (SEP-2640, Extensions Track) standardises
# exposing skills via MCP *Resources* rather than bespoke tools. We add a
# Resources surface alongside the existing tools so SEP-2640-aware hosts can
# discover and read skills natively, while keeping the tools for back-compat.

def _skill_uri(skill_id: str) -> str:
    return f"skill://{skill_id.upper()}"


@mcp.resource("skills://index")
def skills_index() -> str:
    """Browseable index of every skill as a Resource (skill://HS-NNN)."""
    items = [
        {
            "uri":       _skill_uri(s["id"]),
            "id":        s["id"],
            "hero_name": s.get("hero_name"),
            "category":  s.get("category"),
            "description": s.get("description", ""),
        }
        for s in skills_list()
        if s.get("status", "").lower() != "archived"
    ]
    return json.dumps({"count": len(items), "skills": items},
                      ensure_ascii=False, indent=2)


@mcp.resource("skill://{skill_id}")
def skill_resource(skill_id: str) -> str:
    """Read a single skill's full markdown by ID, e.g. resource skill://HS-100."""
    meta = find_by_id(skill_id)
    if not meta:
        return _mercy_not_found(skill_id)
    content, _gos = _content_and_gos(meta)
    if content is None:
        return f"# {skill_id}\n\nNo stress — this skill is registered but its content isn't bundled yet ({meta.get('file')})."
    return content


# ── Health check ───────────────────────────────────────────────────────────────
# The manifest.json declares `health_check: /health`. Served on the HTTP app
# (streamable-http / sse). Lets Railway/Render and the Perplexity connector probe
# liveness without speaking MCP.

@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    try:
        skills = len(skills_list())
        meta = get_registry().get("_meta", {})
        return JSONResponse({
            "status": "ok",
            "service": "hyper-sills-mcp",
            "version": SERVER_VERSION,
            "skills": skills,
            "categories": meta.get("categories", {}),
        })
    except Exception as exc:  # never let a probe crash the server
        return JSONResponse({"status": "degraded", "error": str(exc)}, status_code=503)


# ── Mercy messages (HS-069) ────────────────────────────────────────────────────
# Apply the vault's own ND-first error ethos to the server: never blame, always
# offer the next step.

def _mercy_not_found(skill_id: str) -> str:
    near = []
    sid = skill_id.upper().strip()
    digits = re.sub(r"\D", "", sid)
    for s in skills_list():
        if digits and digits in re.sub(r"\D", "", s.get("id", "")):
            near.append(f'{s["id"]} {s.get("hero_name","")}')
        if len(near) >= 3:
            break
    hint = ("Closest matches: " + "; ".join(near)) if near else \
        'Try search_skills("<keywords>") to find it by topic.'
    return json.dumps({
        "ok": False,
        "message": f"No stress — '{skill_id}' isn't in the vault yet. {hint}",
        "next_step": 'search_skills(query="...") or recommend_for_task(task="...")',
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

    print("6. resources: skills://index + skill://HS-100")
    idx = json.loads(skills_index())
    print(f"   index count={idx['count']}  first={idx['skills'][0]['uri'] if idx['skills'] else 'none'}")
    res = skill_resource("HS-100")
    print(f"   skill://HS-100 -> {len(res)} chars, starts: {res.splitlines()[0][:50] if res else '(empty)'}")
    print()

    print("7. mercy: load_skill('HS-9999')")
    r = json.loads(load_skill("HS-9999"))
    print(f"   ok={r.get('ok')}  message={r.get('message','')[:60]}")
    print()

    print("All tools + resources OK.")


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--test" in sys.argv:
        _smoke_test()
    elif "--http" in sys.argv or os.environ.get("PORT"):
        # HTTP transport for remote hosts (Railway/Render) + the Perplexity MCP
        # connector. Streamable-HTTP is the current standard (SSE is deprecated).
        mcp.settings.host = os.environ.get("HOST", "0.0.0.0")
        mcp.settings.port = int(os.environ.get("PORT", "8000"))

        # DNS-rebinding protection rejects any Host header not in allowed_hosts
        # (default: localhost only) -> "Invalid Host header" / 421 behind a proxy.
        # Allow this deployment's public host so MCP clients (e.g. Perplexity) connect.
        if os.environ.get("MCP_DISABLE_HOST_CHECK"):
            mcp.settings.transport_security = TransportSecuritySettings(
                enable_dns_rebinding_protection=False,
            )
        else:
            hosts = ["localhost", "localhost:*", "127.0.0.1", "127.0.0.1:*"]
            origins: list[str] = []
            # Railway / Render inject the public hostname automatically.
            domain = (os.environ.get("RAILWAY_PUBLIC_DOMAIN")
                      or os.environ.get("RENDER_EXTERNAL_HOSTNAME") or "").strip()
            if domain:
                hosts += [domain, f"{domain}:*"]
                origins += [f"https://{domain}", f"http://{domain}"]
            # Manual overrides (comma-separated) for any other public host/origin.
            hosts += [h.strip() for h in os.environ.get("MCP_ALLOWED_HOSTS", "").split(",") if h.strip()]
            origins += [o.strip() for o in os.environ.get("MCP_ALLOWED_ORIGINS", "").split(",") if o.strip()]
            mcp.settings.transport_security = TransportSecuritySettings(
                enable_dns_rebinding_protection=True,
                allowed_hosts=hosts,
                allowed_origins=origins,
            )

        transport = "sse" if "--sse" in sys.argv else "streamable-http"
        _ts = mcp.settings.transport_security
        print(
            f"HYPER-SILLs MCP serving {len(skills_list())} skills over {transport} "
            f"on {mcp.settings.host}:{mcp.settings.port} (health: /health, "
            f"allowed_hosts: {_ts.allowed_hosts or 'ALL — host check disabled'})",
            file=sys.stderr,
        )
        mcp.run(transport=transport)
    else:
        mcp.run(transport="stdio")
