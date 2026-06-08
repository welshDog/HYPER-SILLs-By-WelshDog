# HS-017 — 🧠 MIND CORE — Hyper Brain Core Manifest

---
skill_id: HS-017
hero_name: "MIND CORE"
emoji: "🧠"
version: v1.0
category: agents
depends_on:
  - HS-016  # BRAIN PRIMER — orientation required before calling the core
provides:
  - brain-query-api
  - brain-state-update
  - mcp-compatible-brain-interface
related:
  - HS-018  # BRIDGE KEEPER — MCP bridge routes calls to this core
  - HS-011  # MIND BLOCKS — module map for this core's endpoints
  - HS-125  # THE GRAND CODEX — master context loads before the core
graph_notes: "Core brain agent manifest — MCP-compatible; Claude/Cursor can call it directly for knowledge queries and state updates."
---
**Category:** Agents / MCP-Compatible
**Version:** 1.0.0
**Runtime:** Python
**Entrypoint:** `hyper_brain_core.py`
**MCP Compatible:** ✅ YES
**Rescued From:** [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) — `.agents/hyper-brain-core/manifest.json`

> Core brain logic for the BROski HyperFocus ecosystem. MCP-compatible — Claude/Cursor can call it directly.

---

## 🛠️ Tools

### `query_brain`
Query the BROski brain for context, decisions, and knowledge.
```json
{ "query": "string" }
```

### `update_brain`
Update brain state with new knowledge or sprint wins.
```json
{ "key": "string", "value": "string" }
```

---

## ⚡ Usage

```python
# Query
result = query_brain(query="What is the current sprint focus?")

# Update after a win
update_brain(key="last_shipped", value="Level 17 — HyperSplit")
```

---

## 🔗 Related
- `agents/HYPER_BRAIN_MODULES_v1.md` (HS-011) — full API surface
- `agents/AGENT_MANIFEST_MCP_BRIDGE_v1.md` — routes calls through the mesh

*Rescued from BROski-Obsidian-Brain-for-HyperFocus-z0ne — HYPER-SKILLs Vault by WelshDog 🐕⚡*
