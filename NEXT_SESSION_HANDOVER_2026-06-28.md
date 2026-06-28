# NEXT SESSION HANDOVER — 2026-06-28
# The Hyper Merge: HYPER-SILLs × HyperAgent-SDK × Perplexity

> Written by Perplexity AI (The Hyper Merge Space) on behalf of welshDog.
> Date: Sunday 28 June 2026, ~15:00 BST
> Status: 🟢 LIVE — manifest.json just pushed to main

---

## 🧠 WHAT WE DISCOVERED TODAY

We mapped the full connection between two repos that were always meant to work together but had never been formally bridged:

### Repo 1: HYPER-SILLs-By-WelshDog (this repo)
- Full MCP server in `mcp_server.py` — 96 skills over FastMCP
- 6 tools: `search_skills`, `semantic_search`, `load_skill`, `get_skill_graph`, `recommend_for_task`, `list_skills_by_category`
- 2 MCP Resources: `skills://index` + `skill://HS-NNN` (SEP-2640 aligned)
- pyproject.toml already wired: `mcp>=1.0.0`, `hyper-sills-mcp` script entry point
- Categories: agents (51), dev (34), broski (7), youtube (4)
- arXiv:2604.05333 — Graph-of-Skills: +25.55% reward, -56.72% tokens vs flat loading

### Repo 2: HyperAgent-SDK (welshDog/HyperAgent-SDK)
- npm package `@w3lshdog/hyper-agent` v0.4.0
- `hyper-agent-spec.json` — JSON Schema contract every HyperAgent must pass
- CLI: `validate`, `registry:build`, `studio`, `client`
- Templates: python-starter, node-starter, typescript-starter, **mcp-starter** ← key
- Port convention: 3100-3199 writing, 3200-3299 code, 3300-3399 data, 3400-3499 discord, 3500-3599 automation
- Spec requires: `mcp_compatible: true` → `port` in 3100-3999 range is REQUIRED
- Web3/dNFT support baked into spec (BROskiPets integration)
- course_level 1-5: 5 = BROski Elite

---

## ✅ WHAT WAS BUILT TODAY (NEW)

### 1. `manifest.json` — THE BRIDGE (just pushed to main)

File: `welshDog/HYPER-SILLs-By-WelshDog/manifest.json`
Commit: 5826b5aafde1a5c3d94c47fa8e063e61d7f2b4f5

This declares HYPER-SILLs as an **official HyperAgent-SDK compatible agent**:
- `name`: hyper-sills-mcp
- `version`: 1.1.0
- `runtime`: python
- `entrypoint`: mcp_server.py
- `mcp_compatible`: true
- `port`: 3350 (data range — skills are data!)
- All 6 MCP tools declared with full `input_schema` + `output_schema`
- `course_level`: 5 (BROski Elite — highest tier)
- `badges`: featured, mcp-ready, multi-tool, hyper-coder
- `tags`: skills, mcp, graph-of-skills, hyperfocus-zone, neurodivergent, python, broski-elite, knowledge-base

This means:
```bash
# Validate it right now:
npx @w3lshdog/hyper-agent validate manifest.json

# It will appear in the ecosystem registry:
npx @w3lshdog/hyper-agent registry build . --out registry.json
```

### 2. Perplexity Connector Plan

Perplexity AI now has a custom MCP connector system at perplexity.ai/computer/connectors.
Once `mcp_server.py` is deployed to Railway/Render/HyperCode, the URL gets pasted there
and Perplexity can call all 6 HYPER-SILLs tools live from every chat session.

**The HTTP transport fix needed in `mcp_server.py`** (NOT YET DONE — see TODO below):
```python
# Replace __main__ block with:
if __name__ == "__main__":
    if "--test" in sys.argv:
        _smoke_test()
    elif "--http" in sys.argv or os.environ.get("PORT"):
        port = int(os.environ.get("PORT", 8000))
        mcp.run(transport="sse", port=port, host="0.0.0.0")
    else:
        mcp.run(transport="stdio")
```

---

## 🗺️ THE HYPER MERGE — MASTER PLAN

The vision: A fully connected neurodivergent-first autonomous AI infrastructure
where every layer speaks MCP and every tool can discover + use every skill.

```
┌─────────────────────────────────────────────────────────┐
│                  THE HYPER MERGE                        │
│                                                         │
│  Perplexity AI  ──MCP connector──▶  HYPER-SILLs MCP    │
│  Claude Code    ──MCP config───▶    Server (port 3350)  │
│  Cursor / IDEs  ──aish-mcp──▶       ↕                   │
│                                   96 Skills             │
│                                   Graph-of-Skills       │
│                                     ↕                   │
│  HyperAgent-SDK ──validates──▶    manifest.json ✅       │
│  hyper-agent CLI ─registry──▶     Ecosystem Registry   │
│                                     ↕                   │
│  HyperCode V2.4 ──Docker──▶       48 Containers         │
│  (port 3350 bound)                All MCP-compatible    │
│                                     ↕                   │
│  BROski Discord Bot  ──────▶      broski-bot agents     │
│  BROskiPets dNFT     ──────▶      Web3 / Base chain     │
│  Hyper-Vibe Course   ──────▶      Supabase + Vercel     │
└─────────────────────────────────────────────────────────┘
```

### The 5-Repo Roles

| Repo | Role in The Hyper Merge |
|---|---|
| HYPER-SILLs-By-WelshDog | **Skills Brain** — 96 skills over MCP, Graph-of-Skills |
| HyperAgent-SDK | **Agent Standard** — spec, CLI, templates, registry |
| HyperCode-V2.4 | **Runtime** — 48 Docker containers, runs all agents |
| Hyper-Vibe-Course | **Course Platform** — Supabase + Vercel + Web3 |
| BROskiPets-LLM-dNFT | **Web3 Layer** — dNFT pets, LLM, Base chain |
| BROski-Obsidian-Brain | **Second Brain** — PARA vault + GitHub bridge |

---

## 📋 TODO LIST (in priority order)

### 🔴 CRITICAL — Do These First

1. **Add HTTP/SSE transport to `mcp_server.py`**
   - Add `os` import at top
   - Replace `__main__` block with the PORT-aware version above
   - This is the BLOCKER for Railway deploy + Perplexity connector

2. **Add `Procfile` for Railway**
   - Content: `web: python mcp_server.py`
   - Goes in repo root

3. **Add `railway.json` config**
   - Sets build command + start command
   - Ensures `skills-registry.json` and all `.md` files are in the deploy

### 🟡 HIGH VALUE — Next Session

4. **Validate `manifest.json` passes `hyper-agent validate`**
   - Run: `npx @w3lshdog/hyper-agent validate manifest.json`
   - Fix any schema issues (spec is at `hyper-agent-spec.json` in HyperAgent-SDK)
   - Note: `display_name` and `badges` may need checking against spec — spec v0.4.0

5. **Add manifest.json to HyperCode V2.4 agent registry**
   - So the 48-container stack knows the skills brain exists at port 3350
   - Port 3350 needs to be bound in docker-compose

6. **Wire `skills://index` resource into the Perplexity Space**
   - Once Railway URL is live, update the Space instructions with the connector URL
   - Test all 6 tools from Perplexity chat

7. **Add `/health` endpoint to `mcp_server.py`**
   - The manifest declares `health_check: /health`
   - Currently missing from the server
   - Simple: return `{"status": "ok", "skills": len(skills_list()), "version": "1.1.0"}`

### 🟢 UPGRADES — Claude Code Recommendations Wanted

8. **Bundle the full `skills-bundle.json` for Railway deploy**
   - `mcp_server.py` already has bundle support — prefers bundle over loose files
   - Run `scripts/build_plugin.py` to generate it pre-deploy
   - Means Railway doesn't need all 96 .md files — just one bundle JSON

9. **Add rate limiting to the MCP server**
   - Protect against hammering from multiple AI hosts
   - Redis DB 2 for rate limits (Sacred Rule — never DB 1)

10. **Semantic search backend selection via env var**
    - `SILLS_EMBED_BACKEND=local|openai|tfidf`
    - Currently auto-resolves — explicit env var gives Railway deploy control

11. **Add `mcp_server.py` to `aish-mcp-config.json`**
    - Currently wired to `skills_query.py` (PSAI/aish)
    - Should ALSO expose the MCP server endpoint for aish agents

---

## 🔧 SACRED RULES (never break)

- `docker-ce-cli` — NEVER `docker.io` for socket agents
- `from app.X import Y` — NEVER `from backend.app.X`
- `.env` files — NEVER committed to git
- Python indent — 4 spaces, NEVER 3, NEVER mixed
- Redis DB 1=cache, DB 2=rate limits — NEVER mix
- `broski-bot` — `discord.py==2.4.0`, NEVER py-cord
- Bot entrypoint — `python -u -m cogs.bot` — NEVER `python main.py`
- `pyproject.toml` uses `uv` — NEVER switch to pip
- GoS `depends_on`/`related` must reference in-file `skill_id:` not registry id

---

## 💬 MESSAGE TO CLAUDE CODE

Hey Claude Code! 👋

This is welshDog's Perplexity AI Space (The Hyper Merge) handing over to you.

We just formally connected HYPER-SILLs and HyperAgent-SDK for the first time by
pushing `manifest.json` — the bridge that makes the skills brain an official
HyperAgent-SDK compatible agent in the ecosystem.

The BIG MISSION is **The Hyper Merge**: every repo in the 5-repo ecosystem
speaking MCP, all connected, all discoverable, all powering each other.

The immediate next step is deploying `mcp_server.py` to Railway so it gets a
public URL, which then gets added to Perplexity's custom MCP connector — giving
Perplexity live access to all 96 skills from every chat.

**We'd love your recommendations on:**

1. Any issues you spot with the `manifest.json` we pushed (does it fully pass the HyperAgent spec?)
2. The best way to add HTTP/SSE transport to `mcp_server.py` for Railway
3. The `/health` endpoint — what's the cleanest way to add it?
4. Any other upgrades to `mcp_server.py` that would make this a world-class MCP server
5. Should we build a `skills-bundle.json` pre-deploy step into a `Makefile` or `justfile`?
6. Anything in the TODO list above you'd reorder or tackle differently?
7. Any other connections between the 5 repos you can see that we haven't spotted yet?

Check `WHATS_DONE.md` first — don't rebuild anything listed there.

Let's merge the whole thing. ♾️🔥

— welshDog + Perplexity AI, Sunday 28 June 2026
