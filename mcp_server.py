#!/usr/bin/env python3
"""
HYPER-SILLs MCP Server
Exposes the HYPER-SILLs skill vault via Model Context Protocol.
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

import asyncio
import functools
import json
import logging
import os
import re
import sys
import time
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# ── Logging setup — fix Railway INFO-as-error noise ─────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s %(message)s",
    stream=sys.stdout,  # stdout = INFO severity in Railway, not error
)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("hyper-sills")

SERVER_VERSION = "1.2.0"

VAULT_ROOT = Path(__file__).parent
REGISTRY_PATH = VAULT_ROOT / "skills-registry.json"
# Self-contained bundle (built by scripts/build_plugin.py for the Claude Code
# plugin). When present, skill `content` + `gos` are embedded, so the server
# needs no loose .md files — this is what makes the bundled plugin work after a
# github install (where only the plugin dir is cached). Repo runs fine without it.
BUNDLE_PATH = VAULT_ROOT / "skills-bundle.json"


def _meta_summary() -> tuple[int, str]:
    """Read total + per-category counts from the bundle/registry `_meta` so the
    server instructions never go stale when skills are added (counts drift is a
    recurring papercut — keep this single source of truth)."""
    order = ["agents", "dev", "hypercode", "broski", "web3", "youtube"]
    for p in (BUNDLE_PATH, REGISTRY_PATH):
        try:
            meta = json.loads(p.read_text(encoding="utf-8"))["_meta"]
            cats = meta.get("categories", {})
            cat_str = ", ".join(f"{c} ({cats[c]})" for c in order if c in cats)
            return int(meta.get("total_skills", 0)), cat_str
        except Exception:
            continue
    return 0, ""


_TOTAL_SKILLS, _CATEGORY_SUMMARY = _meta_summary()

MODEL_PROFILES = {
    "claude": {
        "description": "Anthropic-style long-context, markdown-first, high-detail output.",
        "response_style": "markdown",
        "include_examples": True,
        "include_graph": True,
        "max_summary_chars": 1800,
        "max_payload_chars": 12000,
        "trim_content": False,
    },
    "gpt": {
        "description": "OpenAI-style concise, structured, action-first output.",
        "response_style": "json",
        "include_examples": True,
        "include_graph": True,
        "max_summary_chars": 900,
        "max_payload_chars": 8000,
        "trim_content": True,
    },
    "gemini": {
        "description": "Google-style structured reasoning blocks with clear sections.",
        "response_style": "structured_blocks",
        "include_examples": True,
        "include_graph": True,
        "max_summary_chars": 1200,
        "max_payload_chars": 9000,
        "trim_content": True,
    },
    "local": {
        "description": "Compact, low-token output for local or small open models.",
        "response_style": "minimal_json",
        "include_examples": False,
        "include_graph": False,
        "max_summary_chars": 600,
        "max_payload_chars": 5000,
        "trim_content": True,
    },
    "generic": {
        "description": "Safe default for unknown or mixed-model contexts.",
        "response_style": "balanced_json",
        "include_examples": True,
        "include_graph": True,
        "max_summary_chars": 1200,
        "max_payload_chars": 8000,
        "trim_content": True,
    },
}


def detect_model_profile(model_hint: str | None) -> str:
    """Map a user-provided model hint to a stable persona profile."""
    hint = (model_hint or "").lower()
    if not hint:
        return "generic"

    if any(token in hint for token in ("claude", "sonnet", "opus", "anthropic")):
        return "claude"
    if any(token in hint for token in ("gpt", "chatgpt", "openai", "o1", "o3", "4o", "4.1")):
        return "gpt"
    if any(token in hint for token in ("gemini", "google")):
        return "gemini"
    if any(token in hint for token in ("llama", "mistral", "qwen", "deepseek", "ollama", "local", "small-model")):
        return "local"
    return "generic"


def _truncate(text: str, limit: int) -> str:
    if limit <= 0 or len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def _build_model_optimized_payload(skill_meta: dict, gos: dict, content: str, profile_name: str, task_context: str = "") -> dict:
    profile = MODEL_PROFILES.get(profile_name, MODEL_PROFILES["generic"])
    parts = {
        "id": skill_meta.get("id"),
        "hero_name": skill_meta.get("hero_name"),
        "category": skill_meta.get("category"),
        "description": skill_meta.get("description", ""),
        "summary": _truncate((skill_meta.get("description") or "").strip() or (gos.get("graph_notes") or ""), profile["max_summary_chars"]),
        "depends_on": [ref.get("id") for ref in gos.get("depends_on", [])],
        "provides": gos.get("provides", []),
        "related": [ref.get("id") for ref in gos.get("related", [])],
        "profile": profile_name,
        "response_style": profile["response_style"],
    }

    excerpt = ""
    if content:
        excerpt = _truncate(content.strip(), profile["max_payload_chars"])

    if profile_name == "claude":
        parts["payload"] = {
            "role": "system",
            "format": "markdown",
            "use_when": "When this skill is the best fit for the task.",
            "what_it_does": parts["summary"],
            "prerequisites": parts["depends_on"],
            "related": parts["related"],
            "task_context": task_context,
            "content_excerpt": excerpt,
        }
    elif profile_name == "gpt":
        parts["payload"] = {
            "role": "assistant",
            "format": "json",
            "objective": parts["summary"],
            "prerequisites": parts["depends_on"],
            "next_steps": [
                f"load_skill(\"{skill_meta.get('id')}\")",
                "get_skill_graph(\"{skill_meta.get('id')}\")",
            ],
            "task_context": task_context,
            "content_excerpt": excerpt,
        }
    elif profile_name == "gemini":
        parts["payload"] = {
            "role": "reasoner",
            "format": "structured_blocks",
            "context": parts["summary"],
            "sections": {
                "why_this_skill": parts["summary"],
                "prerequisites": parts["depends_on"],
                "related": parts["related"],
                "task_context": task_context,
            },
            "content_excerpt": excerpt,
        }
    elif profile_name == "local":
        parts["payload"] = {
            "role": "tool",
            "format": "minimal_json",
            "goal": parts["summary"],
            "requires": parts["depends_on"],
            "task_context": task_context,
            "content_excerpt": excerpt,
        }
    else:
        parts["payload"] = {
            "role": "assistant",
            "format": "balanced_json",
            "summary": parts["summary"],
            "prerequisites": parts["depends_on"],
            "content_excerpt": excerpt,
            "task_context": task_context,
        }

    return parts


mcp = FastMCP(
    "hyper-sills",
    instructions=(
        f"HYPER-SILLs — {_TOTAL_SKILLS}-skill AI vault with Graph-of-Skills. "
        "Skill tools: search_skills, semantic_search, load_skill, get_skill_graph, recommend_for_task, list_skills_by_category. "
        "Model adaptation tools: get_model_profile, get_model_optimized_skill. "
        "Action tools: broski_agent (dispatch a task to the BROski orchestrator), brain_core_agent (query the Hyper Brain memory). "
        "Resources (SEP-2640 Skills-over-MCP): skills://index, skill://HS-NNN. "
        f"Categories: {_CATEGORY_SUMMARY}."
    ),
)

# ── Registry cache ──────────────────────────────────────────────────────────

_registry: dict | None = None
_gos_index: dict | None = None  # skill_id → Path, for vault-only skills


def get_registry() -> dict:
    global _registry
    if _registry is None:
        src = BUNDLE_PATH if BUNDLE_PATH.exists() else REGISTRY_PATH
        _registry = json.loads(src.read_text(encoding="utf-8"))
    return _registry


def skills_list() -> list[dict]:
    return get_registry().get("skills", [])


def _build_gos_index() -> dict:
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
    result = next((s for s in skills_list() if s.get("id", "").upper() == sid), None)
    if result:
        return result
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


# ── GoS frontmatter parser ──────────────────────────────────────────────────────

def _parse_list_section(block: str, key: str) -> list[str]:
    m = re.search(rf'^{key}:(.*?)(?=^\w|\Z)', block, re.MULTILINE | re.DOTALL)
    if not m:
        return []
    items = []
    for line in m.group(1).splitlines():
        item = re.match(r'\s*-\s*(.+)', line)
        if item:
            items.append(item.group(1).strip())
    return items


def _parse_ref_list(block: str, key: str) -> list[dict]:
    m = re.search(rf'^{key}:(.*?)(?=^\w|\Z)', block, re.MULTILINE | re.DOTALL)
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
    lines = content.splitlines()
    start = next((i for i, l in enumerate(lines) if l.strip() == "---"), None)
    if start is None:
        return {}
    end = next((i for i in range(start + 1, len(lines)) if lines[i].strip() == "---"), None)
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


# ── Tool call metrics ────────────────────────────────────────────────────────
TOOL_CALLS_TOTAL = Counter("mcp_tool_calls_total", "Total MCP tool invocations", ["tool", "status"])
TOOL_CALL_DURATION = Histogram("mcp_tool_call_duration_seconds", "MCP tool call duration in seconds", ["tool"])


def instrument_tool(func):
    name = func.__name__

    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            status = "success"
            try:
                return await func(*args, **kwargs)
            except Exception:
                status = "error"
                raise
            finally:
                TOOL_CALL_DURATION.labels(tool=name).observe(time.perf_counter() - start)
                TOOL_CALLS_TOTAL.labels(tool=name, status=status).inc()
        return async_wrapper

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.perf_counter()
        status = "success"
        try:
            return func(*args, **kwargs)
        except Exception:
            status = "error"
            raise
        finally:
            TOOL_CALL_DURATION.labels(tool=name).observe(time.perf_counter() - start)
            TOOL_CALLS_TOTAL.labels(tool=name, status=status).inc()
    return sync_wrapper


# ── Tools ────────────────────────────────────────────────────────────

@mcp.tool()
@instrument_tool
def get_model_profile(model_hint: str = "") -> str:
    """Return the active model persona profile used to format a skill for a specific LLM."""
    profile_name = detect_model_profile(model_hint)
    profile = MODEL_PROFILES.get(profile_name, MODEL_PROFILES["generic"]).copy()
    return json.dumps({
        "requested_hint": model_hint or "",
        "resolved_profile": profile_name,
        "settings": profile,
        "note": "Use this profile to choose the best skill payload format for the caller.",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
@instrument_tool
def get_model_optimized_skill(skill_id: str, model_hint: str = "", task_context: str = "") -> str:
    """Return a skill payload optimized for the caller's model persona.

    This adapts the same skill for Claude, GPT, Gemini, local models, and unknown callers
    without changing the underlying skill content or graph metadata.
    """
    meta = find_by_id(skill_id)
    if not meta:
        return _mercy_not_found(skill_id)

    content, gos = _content_and_gos(meta)
    if content is None:
        return json.dumps({"error": f"Content unavailable for {meta.get('file')}"})

    profile_name = detect_model_profile(model_hint)
    payload = _build_model_optimized_payload(meta, gos, content, profile_name, task_context)
    payload["requested_hint"] = model_hint or ""
    payload["profile_description"] = MODEL_PROFILES.get(profile_name, MODEL_PROFILES["generic"])["description"]

    return json.dumps(payload, ensure_ascii=False, indent=2)


@mcp.tool()
@instrument_tool
def search_skills(
    query: str = "",
    category: str = "",
    tag: str = "",
    limit: int = 10,
) -> str:
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
                " ".join(s.get("keywords", [])),
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
            "version":     s.get("version", ""),
            "category":    s.get("category"),
            "file":        s.get("file"),
            "tags":        s.get("tags", []),
            "pack":        s.get("pack"),
        })
        if len(results) >= limit:
            break

    return json.dumps({"count": len(results), "results": results}, ensure_ascii=False, indent=2)


@mcp.tool()
@instrument_tool
def semantic_search(query: str, limit: int = 5) -> str:
    if not query.strip():
        return json.dumps({"error": "Describe what you need in a sentence."})
    try:
        sys.path.insert(0, str(VAULT_ROOT / "scripts"))
        from search_skills import semantic_search as _ss, active_backend  # type: ignore
        hits = _ss(query, limit=limit)
        if hits:
            return json.dumps({"query": query, "backend": active_backend(), "count": len(hits), "results": hits}, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return search_skills(query=query, limit=limit)


def _content_and_gos(meta: dict) -> tuple[str | None, dict]:
    if meta.get("content"):
        return meta["content"], (meta.get("gos") or parse_gos(meta["content"]))
    fp = VAULT_ROOT / meta.get("file", "")
    if fp.exists():
        c = fp.read_text(encoding="utf-8", errors="replace")
        return c, parse_gos(c)
    return None, (meta.get("gos") or {})


@mcp.tool()
@instrument_tool
def load_skill(skill_id: str) -> str:
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
@instrument_tool
def get_skill_graph(skill_id: str) -> str:
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
        "load_order_hint": "Load depends_on skills first, then this skill, then optionally load related skills for context.",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
@instrument_tool
def recommend_for_task(task: str, limit: int = 5) -> str:
    if not task.strip():
        return json.dumps({
            "error": "Provide a task description.",
            "example": 'recommend_for_task("build a self-healing agent")',
        })

    backend = "keyword"
    hits: list[dict] = []
    try:
        sys.path.insert(0, str(VAULT_ROOT / "scripts"))
        from search_skills import semantic_search as _ss, active_backend  # type: ignore
        hits = _ss(task, limit=limit)
        if hits:
            backend = active_backend()
    except Exception:
        hits = []

    if hits:
        results = []
        for h in hits:
            meta = find_by_id(h["id"]) or {}
            results.append({
                "id":               h["id"],
                "hero_name":        h["hero_name"],
                "description":      h.get("description", ""),
                "category":         h.get("category"),
                "version":          meta.get("version", ""),
                "relevance_score":  round(float(h.get("score", 0.0)), 4),
                "tags":             meta.get("tags", []),
                "next_step":        f'load_skill("{h["id"]}")',
            })
    else:
        keywords = [w for w in re.split(r'\W+', task.lower()) if len(w) > 2]
        scored = []
        for s in skills_list():
            haystack = " ".join([
                s.get("id", ""), s.get("hero_name", ""), s.get("description", ""),
                s.get("category", ""), " ".join(s.get("tags", [])),
                " ".join(s.get("keywords", [])),
            ]).lower()
            hitcount = sum(1 for kw in keywords if kw in haystack)
            if hitcount:
                scored.append((hitcount, s))
        scored.sort(key=lambda x: x[0], reverse=True)
        denom = max(len(keywords), 1)
        results = [
            {
                "id":               s["id"],
                "hero_name":        s["hero_name"],
                "description":      s.get("description", ""),
                "category":         s.get("category"),
                "version":          s.get("version", ""),
                "relevance_score":  round(hitcount / denom, 3),
                "tags":             s.get("tags", []),
                "next_step":        f'load_skill("{s["id"]}")',
            }
            for hitcount, s in scored[:limit]
        ]

    return json.dumps({
        "task":        task,
        "backend":     backend,
        "count":       len(results),
        "recommended": results,
        "tip": "Run get_skill_graph(id) on the top result to find prerequisite skills to load first (GoS load-order).",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
@instrument_tool
def list_skills_by_category(category: str = "") -> str:
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
        {"id": s["id"], "hero_name": s["hero_name"], "description": s.get("description", ""), "tags": s.get("tags", [])}
        for s in skills_list()
        if s.get("category", "").lower().rstrip("/") == cat
    ]

    return json.dumps({"category": category, "count": len(skills), "skills": skills}, ensure_ascii=False, indent=2)


BROSKI_AGENT_URL = os.environ.get("BROSKI_AGENT_URL", "").strip().rstrip("/")
BRAIN_CORE_URL = os.environ.get("BRAIN_CORE_URL", "").strip().rstrip("/")


def _agent_unconfigured(tool: str, env: str) -> str:
    return json.dumps({
        "ok": False,
        "message": f"No stress — {tool} isn't wired up on this host yet. Set {env} to the agent's URL to enable it.",
        "next_step": f"Set env {env}=https://<your-agent-host> and redeploy.",
    }, ensure_ascii=False, indent=2)


async def _call_agent(tool: str, url: str, path: str, payload: dict, result_key: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(f"{url}{path}", json=payload)
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        return json.dumps({
            "ok": False,
            "message": f"{tool} couldn't reach its backend: {exc}",
            "next_step": "Check the backend URL is reachable from this host.",
        }, ensure_ascii=False, indent=2)
    return json.dumps({
        "ok": True,
        "tool": tool,
        "result": data.get(result_key, f"(no '{result_key}' field in response)"),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
@instrument_tool
async def broski_agent(task: str) -> str:
    if not task.strip():
        return json.dumps({"ok": False, "message": "Describe the task to run."})
    if not BROSKI_AGENT_URL:
        return _agent_unconfigured("broski_agent", "BROSKI_AGENT_URL")
    return await _call_agent("broski_agent", BROSKI_AGENT_URL, "/run", {"task": task}, "result")


@mcp.tool()
@instrument_tool
async def brain_core_agent(query: str) -> str:
    if not query.strip():
        return json.dumps({"ok": False, "message": "Describe what to look up."})
    if not BRAIN_CORE_URL:
        return _agent_unconfigured("brain_core_agent", "BRAIN_CORE_URL")
    return await _call_agent("brain_core_agent", BRAIN_CORE_URL, "/query", {"query": query}, "answer")


# ── Resources (Skills-over-MCP / SEP-2640 alignment) ──────────────────────────────────────────

def _skill_uri(skill_id: str) -> str:
    return f"skill://{skill_id.upper()}"


@mcp.resource("skills://index")
def skills_index() -> str:
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
    return json.dumps({"count": len(items), "skills": items}, ensure_ascii=False, indent=2)


@mcp.resource("skill://{skill_id}")
def skill_resource(skill_id: str) -> str:
    meta = find_by_id(skill_id)
    if not meta:
        return _mercy_not_found(skill_id)
    content, _gos = _content_and_gos(meta)
    if content is None:
        return f"# {skill_id}\n\nNo stress — this skill is registered but its content isn't bundled yet ({meta.get('file')})."
    return content


def _search_backend_report() -> dict:
    import importlib.util
    report = {"index": "unknown", "query": "tfidf", "dense_active": False}
    try:
        sys.path.insert(0, str(VAULT_ROOT / "scripts"))
        from search_skills import load_index  # type: ignore
        report["index"] = load_index().get("backend", "unknown")
    except Exception:
        return report
    if importlib.util.find_spec("sentence_transformers"):
        report["query"] = "local:sentence-transformers"
    elif os.environ.get("OPENAI_API_KEY"):
        report["query"] = "openai"
    report["dense_active"] = (report["index"] != "tfidf" and report["query"] != "tfidf")
    return report


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
            "search_backend": _search_backend_report(),
        })
    except Exception as exc:
        return JSONResponse({"status": "degraded", "error": str(exc)}, status_code=503)


@mcp.custom_route("/metrics", methods=["GET"])
async def metrics(request: Request) -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def _mercy_not_found(skill_id: str) -> str:
    near = []
    sid = skill_id.upper().strip()
    digits = re.sub(r"\D", "", sid)
    for s in skills_list():
        if digits and digits in re.sub(r"\D", "", s.get("id", "")):
            near.append(f'{s["id"]} {s.get("hero_name", "")}')
        if len(near) >= 3:
            break
    hint = ("Closest matches: " + "; ".join(near)) if near else 'Try search_skills("<keywords>") to find it by topic.'
    return json.dumps({
        "ok": False,
        "message": f"No stress — '{skill_id}' isn't in the vault yet. {hint}",
        "next_step": 'search_skills(query="...") or recommend_for_task(task="...")',
    }, ensure_ascii=False, indent=2)


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


if __name__ == "__main__":
    if "--test" in sys.argv:
        _smoke_test()
    elif "--http" in sys.argv or os.environ.get("PORT"):
        mcp.settings.host = os.environ.get("HOST", "0.0.0.0")
        mcp.settings.port = int(os.environ.get("PORT", "8000"))

        if os.environ.get("MCP_DISABLE_HOST_CHECK"):
            mcp.settings.transport_security = TransportSecuritySettings(
                enable_dns_rebinding_protection=False,
            )
        else:
            hosts = ["localhost", "localhost:*", "127.0.0.1", "127.0.0.1:*"]
            origins: list[str] = []
            domain = (os.environ.get("RAILWAY_PUBLIC_DOMAIN") or os.environ.get("RENDER_EXTERNAL_HOSTNAME") or "").strip()
            if domain:
                hosts += [domain, f"{domain}:*"]
                origins += [f"https://{domain}", f"http://{domain}"]
            hosts += [h.strip() for h in os.environ.get("MCP_ALLOWED_HOSTS", "").split(",") if h.strip()]
            origins += [o.strip() for o in os.environ.get("MCP_ALLOWED_ORIGINS", "").split(",") if o.strip()]
            mcp.settings.transport_security = TransportSecuritySettings(
                enable_dns_rebinding_protection=True,
                allowed_hosts=hosts,
                allowed_origins=origins,
            )

        transport = "sse" if "--sse" in sys.argv else "streamable-http"
        logger.info(
            "HYPER-SILLs MCP serving %d skills over %s on %s:%s (health: /health)",
            len(skills_list()), transport, mcp.settings.host, mcp.settings.port
        )
        mcp.run(transport=transport)
    else:
        mcp.run(transport="stdio")
