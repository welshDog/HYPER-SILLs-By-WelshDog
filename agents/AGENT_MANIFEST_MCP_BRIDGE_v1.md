# HS-018 — 🌉 BRIDGE KEEPER — MCP Bridge Manifest

---
skill_id: HS-018
hero_name: "BRIDGE KEEPER"
emoji: "🌉"
version: v1.0
category: agents
depends_on:
  - HS-017  # MIND CORE — bridge routes to the brain core
  - HS-016  # BRAIN PRIMER — ecosystem orientation required
provides:
  - mcp-bridge-api
  - tool-call-routing
  - brain-cluster-access
related:
  - DS-020  # MCP_SERVER_AGENT_REGISTRATION — registration pattern for this bridge
graph_notes: "MCP protocol bridge manifest — entry point for any AI IDE (Claude Code, Cursor) to reach the BROski brain cluster."
---
**Category:** Agents / MCP-Compatible
**Version:** 1.0.0
**Runtime:** Python
**Entrypoint:** `mcp_bridge.py`
**MCP Compatible:** ✅ YES
**Rescued From:** [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) — `.agents/mcp-bridge/manifest.json`

> MCP protocol bridge — lets Claude/Cursor talk to the Brain cluster. Routes any MCP tool call through the hyper-brain network.

---

## 🛠️ Tools

### `bridge_call`
Route an MCP tool call through the hyper-brain network.
```json
{ "tool": "string", "args": "object" }
```

---

## ⚡ Usage

```python
# Route a tool call through the bridge
result = bridge_call(
  tool="query_brain",
  args={"query": "What containers are running?"}
)
```

---

## 🌐 Port
- Brain API: `http://localhost:8100`
- MCP Gateway: port `8820`

---

## 🔗 Related
- `agents/HYPER_BRAIN_MODULES_v1.md` (HS-011) — `/mcp/status` `/mcp/query`
- `agents/AGENT_MANIFEST_HYPER_BRAIN_CORE_v1.md` — what it bridges to

*Rescued from BROski-Obsidian-Brain-for-HyperFocus-z0ne — HYPER-SKILLs Vault by WelshDog 🐕⚡*
