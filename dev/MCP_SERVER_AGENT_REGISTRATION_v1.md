# HS-081 — MCP Server + Agent Registration Pattern 🔌

**Category:** `dev/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §3
**Version:** v1

---

## 🤔 What It Does

How to expose a HyperCode service as an MCP (Model Context Protocol) server, and how an agent registers as an MCP client to discover and call those tools. This is the wiring that lets Claude (and any other MCP-aware LLM) see every HyperCode capability as a callable tool.

---

## 🛠️ Server Side — register a tool

```python
from mcp import MCPServer

server = MCPServer(name="my_service")

@server.tool
async def my_tool(param: str) -> dict:
    """Tool description for agent discovery — keep it crisp.
    LLM clients read this verbatim to decide when to call you."""
    return {"result": "value"}
```

**Discovery rules:**
- Docstring = tool description shown to the LLM. Be explicit about purpose, inputs, side effects.
- Type hints on params become the JSON schema. No hints = no schema = LLM can't call you reliably.
- Return type should be JSON-serialisable.

---

## 🤖 Client Side — agent registers + calls

```python
from mcp_agent import Agent

agent = Agent(
    name="MyAgent",
    server_names=["hypercode_execution", "hypercode_memory"]
)

# Agent discovers tools automatically and can call them:
result = await agent.call_tool("run_hypercode", source="...")
```

---

## 📋 Naming Convention

| Surface | Convention | Example |
|---|---|---|
| Server name | `hypercode_<service>` (snake_case) | `hypercode_execution` |
| Tool name | verb-first, snake_case | `run_hypercode`, `search_memory` |
| Description | starts with imperative verb | "Execute HyperCode source and return stdout/stderr." |

---

## 🧪 Local Smoke Test

```bash
# List exposed tools
mcp list-tools hypercode_execution

# Call one
mcp call hypercode_execution run_hypercode --param source='print("hi")'
```

---

## 🚧 Gotchas

- **Untyped params = silent fail.** Without type hints the LLM client gets no schema and either skips the tool or guesses wrong args.
- **Don't expose state-changing tools without an approval flag.** Server-side, every write tool should respect a `require_approval` kwarg that ties back into [[HS-077]].
- **Keep tool surface small per server.** One server = one bounded service. Don't dump everything into a god-server — the LLM picks worse tools as the menu grows.

---

## 🧩 Related Skills

- [[HS-080]] Universal Agent Tools API — what every agent exposes
- [[HS-074]] FastAPI Agent API Standards — REST counterpart
- [[HS-077]] User Agency Approval Gate
