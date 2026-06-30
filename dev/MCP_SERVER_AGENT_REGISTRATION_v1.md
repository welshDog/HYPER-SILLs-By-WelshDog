# 🔌 DS-020 — MCP SERVER AGENT REGISTRATION — Make Your Agents Discoverable by Claude and Cursor

---
skill_id: DS-020
hero_name: "MCP SERVER AGENT REGISTRATION"
emoji: "🔌"
version: v1.0.0
status: ACTIVE
category: dev
depends_on:
  - DS-019  # FASTAPI_AGENT_API_STANDARDS
  - HS-009  # HYPER_AGENT_ROSTER
provides:
  - mcp-server-setup
  - agent-registration-protocol
  - tool-discovery
  - claude-cursor-integration
related:
  - DS-026  # HYPERCODE_SDK_MASTER
  - HS-008  # BROSKI_ORCHESTRATOR_PATTERN
  - HS-007  # HYPERFOCUS_AGENT_SWARM_CORE
graph_notes: "MCP server setup for making all swarm agents discoverable by Claude Code, Cursor, and Gemini CLI."
problem_keywords:
  - mcp server
  - register tools
  - expose to claude
  - tool discovery
  - agent registration

---

**Category:** `dev/`
**Version:** v1

## 📋 THE PROMPT
```text
Use skill DS-020 MCP SERVER AGENT REGISTRATION. Register agent [AGENT_NAME] with the MCP server — provide tool schema and handler.
```
