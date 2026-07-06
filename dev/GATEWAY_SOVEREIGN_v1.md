# HS-135 — 🐳 GATEWAY SOVEREIGN — Docker MCP Toolkit Profile Setup + Claude Code Wiring

---
skill_id: HS-135
hero_name: "GATEWAY SOVEREIGN"
emoji: "🐳"
version: v1.0.0
status: ACTIVE
category: dev
depends_on:
  - HS-081  # PORTAL FORGE — MCP Server + Agent Registration (upstream pattern)
  - HS-129  # SKILLS-OVER-MCP — Expose Skills as MCP Resources
provides:
  - docker-mcp-toolkit-setup
  - hyperfocus-profile-wiring
  - claude-code-mcp-connection
  - per-project-mcp-profile
  - mcp-gateway-run
related:
  - HS-136  # AGENT SCRIBE — Docker Agent YAML Pattern (sibling skill)
  - HS-060  # FLEET ADMIRAL — Container Stack Reference
  - HS-037  # GRID MASTER — Architecture Quick Ref
  - HS-080  # THE TOOL BELT — Universal Agent Tools API
graph_notes: "Concrete Docker MCP Toolkit implementation for HyperFocus Z0ne. Replaces per-client MCP config hell with one profile, one gateway, all clients. Direct upgrade path from HS-081 PORTAL FORGE."
problem_keywords:
  - docker mcp toolkit
  - mcp profile
  - claude code tools
  - mcp gateway
  - github stripe supabase tools
  - docker desktop beta features
  - mcp server add
  - client connect

---

**Category:** `dev/`
**Version:** v1.0.0
**Born from:** Docker Desktop 4.40+ · Docker Agent v1.44.0 · Compose v5.1.3
**Replaces the pain of:** configuring every MCP server separately for every AI client (Claude Code, Cursor, Zed) on every machine.

---

## 🧠 What It Does

**One gateway. All tools. Every client.**

Docker MCP Toolkit creates a **profile** — a named bundle of containerised MCP servers.
Connect that profile to any AI client once. Every tool in the profile is immediately available.

No more:
- Per-client `mcp_config.json` files
- Installing MCP server deps locally
- Re-configuring when you add a new tool
- Dependency conflicts between servers

The MCP Gateway (a single `docker mcp gateway run` process) routes all tool calls to the right containerised server, handles auth, and manages lifecycle.

---

## ⚡ THE PROMPT

```text
Use skill HS-135 GATEWAY SOVEREIGN.
Set up Docker MCP Toolkit with a hyperfocus profile.
Wire Claude Code to the gateway.
Add servers: [github | stripe | supabase | postgres | <other>].
```

---

## 🔧 Phase 0 — Preconditions

| Requirement | Check |
|---|---|
| Docker Desktop 4.40+ | `docker --version` → 29.4.x+ |
| Docker Compose v5.1.x | `docker compose version` |
| Claude Code installed | `claude --version` |
| Windows 11 + WSL2 (HyperFocus primary) | PowerShell or WSL2 terminal |

---

## 🔧 Phase 1 — Enable MCP Toolkit in Docker Desktop

```
Docker Desktop → Settings → Beta features → Enable Docker MCP Toolkit → Apply
```

This activates:
- MCP Toolkit UI under the left sidebar
- `docker mcp` CLI subcommands
- MCP Gateway process management

> ⚠️ **Requires restart of Docker Desktop after enabling.**

---

## 🔧 Phase 2 — Create `hyperfocus` Profile (PowerShell)

```powershell
# Create the named profile
docker mcp profile create hyperfocus

# Add core servers for HyperFocus Z0ne
docker mcp server add github     --profile hyperfocus   # PRs, issues, commits
docker mcp server add stripe     --profile hyperfocus   # refunds, payments, webhooks
docker mcp server add supabase   --profile hyperfocus   # DB, auth, edge functions
```

**What each server unlocks in your sessions:**

| Server | What Gordon can do |
|---|---|
| `github` | List PRs, create issues, read files, trigger workflows on welshDog/* repos |
| `stripe` | Look up payments, check webhook events, verify price IDs TEST vs LIVE |
| `supabase` | Query `yhtmuibgdnxhbgboajhc` directly — missions, tokens, enrollments |

> 💡 Browse 300+ available servers: `docker mcp server list` or Docker Hub → MCP catalog

---

## 🔧 Phase 3 — Connect Claude Code

### Option A — Global (user-wide, persists across all projects):
```bash
claude mcp add MCP_DOCKER -s user -- docker mcp gateway run
```

### Option B — Docker Desktop UI:
```
MCP Toolkit sidebar → Clients tab → Claude Code → Connect
```

### Option C — Per-project (preferred for HyperFocus repos):

Drop this in your repo root at `.claude/mcp.json`:
```json
{
  "servers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run", "--profile", "hyperfocus"],
      "type": "stdio"
    }
  }
}
```

> Use Option C for `HyperCode-V2.4` and `hyper-agents-ide` — keeps the profile scoped to the project, not global.

---

## ✅ Phase 4 — Verify

```bash
# Check Claude Code sees the gateway
claude mcp list
# Expected output:
# MCP_DOCKER: docker mcp gateway run - ✓ Connected

# Live test — real tool invocation
claude "Use the GitHub MCP server to list open PRs on welshDog/HyperCode-V2.4"
claude "Use the Stripe MCP server to check the last 3 payment events"
```

---

## 🏗️ Per-Repo Rollout Map

| Repo | Profile approach | Servers needed |
|---|---|---|
| `HyperCode-V2.4` | `.claude/mcp.json` per-project | github + stripe + supabase |
| `hyper-agents-ide` | `.claude/mcp.json` per-project | github + supabase |
| `Hyper-Vibe-Coding-Course` | `.claude/mcp.json` per-project | stripe + supabase |
| `WelshDog-Mission-Control` | `.claude/mcp.json` per-project | github + supabase |
| `BROskiPets-LLM-dNFT` | global `-s user` is fine | github |

---

## 🪤 Gotchas

| Trap | Fix |
|---|---|
| `docker mcp` command not found | MCP Toolkit not enabled yet — go back to Phase 1 |
| Gateway starts but tools show as disconnected | Check Docker Desktop is running before Claude Code session starts |
| Supabase server needs project URL | Set `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` as Docker secrets or env |
| Profile not found on `gateway run` | Profile name is case-sensitive — `hyperfocus` not `Hyperfocus` |
| WSL2 path issues | Run `docker mcp` from PowerShell, not WSL2 terminal for Desktop-managed gateway |

---

## 🔗 Related Skills

- **HS-081 PORTAL FORGE** — Original MCP registration pattern (FastAPI-based, pre-Toolkit)
- **HS-129 SKILLS-OVER-MCP** — Expose HYPER-SILLs skills themselves as MCP resources
- **HS-136 AGENT SCRIBE** — Docker Agent YAML — pair with this for full declarative agent stack
- **HS-080 THE TOOL BELT** — Universal Agent Tools API — conceptual upstream of this skill

---

*HS-135 GATEWAY SOVEREIGN — HYPER-SKILLs Vault by WelshDog 🐕⚡ — Born 2026-06-28*
*Docker MCP Toolkit: docs.docker.com/ai/mcp-catalog-and-toolkit/*
*MCP Gateway: github.com/docker/mcp-gateway*
