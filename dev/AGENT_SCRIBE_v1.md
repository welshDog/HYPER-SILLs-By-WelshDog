# HS-136 — 📜 AGENT SCRIBE — Docker Agent YAML Declaration Pattern

---
skill_id: HS-136
hero_name: "AGENT SCRIBE"
emoji: "📜"
version: v1.0.0
status: ACTIVE
category: dev
depends_on:
  - HS-028  # SDK PRIMER — HyperAgent SDK Agents README (interface standard)
  - HS-079  # THE CREW CHARTER — Specialist Agent Role Definitions
  - HS-009  # HYPER AGENT ROSTER — 22 Hyper Agents
provides:
  - docker-agent-yaml-pattern
  - multi-agent-hierarchy-config
  - model-swap-pattern
  - mcp-toolset-wiring
  - oci-agent-distribution
related:
  - HS-135  # GATEWAY SOVEREIGN — MCP Toolkit (pair skill)
  - HS-008  # THE CONDUCTOR — BROski Orchestrator Pattern
  - HS-067  # THE THRONE LADDER — Agent Role Hierarchy
  - HS-060  # FLEET ADMIRAL — Container Stack Reference
  - HS-002  # SIX LAWS OF AGENTS — the 6 laws every agent obeys
graph_notes: "Maps the HyperFocus Z0ne agent roster + HYPER-SILLs skill interface standard onto Docker Agent YAML. Config-not-code pattern: declare agents in YAML, swap model per profile, wire MCP tools, share via OCI registry."
problem_keywords:
  - docker agent yaml
  - agent.yaml
  - docker agent run
  - multi-agent delegation
  - swap model no code change
  - docker agent push pull
  - agent toolset
  - sub-agent hierarchy
  - hyper agent to docker agent

---

**Category:** `dev/`
**Version:** v1.0.0
**Born from:** Docker Agent v1.44.0 · docker-agent open-source
**The pattern:** Stop writing Python/TS glue to wire LLMs + tools. Declare it in YAML. Run with one command.

---

## 🧠 What It Does

**Config, not code. Declare once, run everywhere.**

Docker Agent takes a YAML (or HCL) file that describes:
- Which model the agent uses
- What its instructions/personality are
- Which tools it can call (built-in + MCP)
- Which sub-agents it can delegate to

Then `docker agent run agent.yaml` handles the entire LLM loop, tool execution, multi-agent delegation, and streaming output.

**Why this matters for HyperFocus Z0ne:**
Your 22-agent roster (HS-089) + HYPER-SILLs skill interface standard (HS-028) map directly onto Docker Agent YAML. The agent contracts you already have = the `instruction:` + `toolsets:` blocks.

---

## ⚡ THE PROMPT

```text
Use skill HS-136 AGENT SCRIBE.
Write a Docker Agent YAML for agent [AGENT_NAME] from the HyperFocus roster.
Role: [role from HS-089].
Model: [claude-sonnet-4-5 | llama3.2-local | gpt-4o].
Tools: [filesystem | shell | mcp:github | mcp:supabase | ...].
Sub-agents: [list if hierarchical].
```

---

## 🔧 YAML Structure — Full Reference

```yaml
# agent.yaml — Docker Agent config schema (version 10)
version: 10

metadata:
  author: welshDog
  description: "Brief description — used by Docker Hub registry"
  version: "1.0.0"

# ── MODELS ──────────────────────────────────────────────
# Define once, reference by name. Swap model = change one line.
models:
  cloud:
    provider: anthropic
    model: claude-sonnet-4-5
    max_tokens: 64000
  local:
    provider: dockermodelrunner   # Docker Model Runner — no API key
    model: ai/llama3.2
  fast:
    provider: anthropic
    model: claude-haiku-4-5       # Haiku for cheap tasks per Cost Awareness rule

# ── AGENTS ──────────────────────────────────────────────
agents:
  root:
    model: cloud                  # reference model by name
    description: "Orchestrator — routes tasks to specialist agents"
    instruction: |
      You are the BROski Orchestrator for HyperFocus Z0ne.
      Short sentences. Bold key info. Celebrate wins.
      Route complex tasks to specialist sub-agents.
      Never rebuild what WHATS_DONE.md says is done.
    toolsets:
      - type: think               # chain-of-thought reasoning
      - type: filesystem          # read/write files
      - type: mcp
        ref: docker:github        # via MCP Gateway (HS-135 GATEWAY SOVEREIGN)
    agents:
      - backend-specialist
      - frontend-specialist

  backend-specialist:
    model: cloud
    description: "FastAPI + Python backend expert"
    instruction: |
      You are a backend specialist for HyperCode-V2.4.
      Rules: from app.X import Y — NEVER from backend.app.X.
      FastAPI routing: public routes BEFORE auth-gated.
      Alembic up to 009.
    toolsets:
      - type: filesystem
      - type: shell
      - type: mcp
        ref: docker:supabase      # query yhtmuibgdnxhbgboajhc

  frontend-specialist:
    model: fast                   # cheaper model for UI tasks
    description: "Vite + React + TypeScript frontend expert"
    instruction: |
      You are a frontend specialist.
      Course dev: npm run dev:frontend (NOT npm run dev).
      MC dev: npm run dev:full.
      Web3/wagmi stays in /pets ONLY.
    toolsets:
      - type: filesystem
      - type: shell

# ── MCP SERVER DEFINITIONS ──────────────────────────────
# Reusable — reference with `ref:` in toolsets above
mcps:
  github:
    remote:
      url: docker:github          # resolved via MCP Gateway
  supabase:
    remote:
      url: docker:supabase

# ── PERMISSIONS ─────────────────────────────────────────
permissions:
  allow:
    - "read_*"
    - "filesystem:*"
    - "shell:cmd=npm*"
    - "shell:cmd=docker*"
    - "shell:cmd=git*"
  deny:
    - "shell:cmd=sudo*"
    - "shell:cmd=rm -rf*"         # sacred rule: never destroy
```

---

## 🔧 Minimal Starter — BROski Morning Briefing Agent

```yaml
# morning-briefing.yaml
version: 10
metadata:
  author: welshDog
  description: "HS-013 DAWN HERALD — Morning Briefing AI for HyperFocus Z0ne"

models:
  claude:
    provider: anthropic
    model: claude-haiku-4-5       # cheap — runs every morning
    max_tokens: 4096

agents:
  root:
    model: claude
    description: "Daily morning briefing agent"
    instruction: |
      You are DAWN HERALD. Every morning, produce a HyperFocus Z0ne briefing.
      Format: short bullets. Bold blockers. Celebrate wins from yesterday.
      Check GitHub for open PRs. Check Supabase for payment events.
      End with: ONE next task for Lyndz.
    toolsets:
      - type: think
      - type: mcp
        ref: docker:github
      - type: mcp
        ref: docker:supabase
```

Run it:
```bash
docker agent run morning-briefing.yaml
```

---

## 🔧 HyperFocus Roster → Docker Agent Mapping

| HS-089 Roster Agent | Docker Agent role | Suggested model | Key toolsets |
|---|---|---|---|
| BROski Orchestrator | `root` agent | claude-sonnet-4-5 | think + mcp:github + sub-agents |
| Backend Specialist | sub-agent | claude-sonnet-4-5 | filesystem + shell + mcp:supabase |
| Frontend Specialist | sub-agent | claude-haiku-4-5 | filesystem + shell |
| Healer Agent | sub-agent | claude-haiku-4-5 | shell + docker inspect |
| Morning Briefing | standalone agent | claude-haiku-4-5 | mcp:github + mcp:supabase |
| Session Snapshot | standalone agent | claude-haiku-4-5 | filesystem (write HANDOVER) |
| BROskiPets Bridge | sub-agent | local (llama3.2) | mcp:github + filesystem |

> 💡 **Cost Awareness rule from CLAUDE_CONTEXT.md**: use `claude-haiku-4-5` for drafts + single tasks. Escalate to `claude-sonnet-4-5` only for multi-step reasoning. Keep sessions under $5.

---

## 🚀 Build, Push, Share (OCI Distribution)

```bash
# Build agent as OCI artifact
docker agent build --tag welshdog/broski-orchestrator:latest .

# Push to Docker Hub — share like an image
docker agent push welshdog/broski-orchestrator:latest

# Pull + run anywhere
docker agent run welshdog/broski-orchestrator:latest
```

Your HYPER-SILLs skills can be bundled INTO the agent image — the skill vault becomes part of the OCI artifact.

---

## 🔧 Run Modes

```bash
# Interactive TUI (default)
docker agent run agent.yaml

# Single prompt, non-interactive
docker agent run agent.yaml --prompt "List open PRs on welshDog/HyperCode-V2.4"

# API mode (for hyper-agents-ide integration)
docker agent run agent.yaml --mode api --port 8099

# MCP mode (expose THIS agent as an MCP tool for Claude Code)
docker agent run agent.yaml --mode mcp
```

> 🔥 `--mode mcp` turns your Docker Agent into an MCP server — then Claude Code can call *your* agents as tools. HS-135 GATEWAY SOVEREIGN + this = full loop.

---

## 🪤 Gotchas

| Trap | Fix |
|---|---|
| `model:` references undefined key | Model must be defined in `models:` block first |
| Sub-agent not found | Sub-agent name in `agents:` list must exactly match a key in `agents:` section |
| `docker:github` ref fails | MCP Gateway not running — run HS-135 GATEWAY SOVEREIGN first |
| Token costs explode | Use `claude-haiku-4-5` for sub-agents; only root needs Sonnet |
| Agent loop never exits | Add `max_iterations: 10` under the agent to cap runaway loops |
| Windows path in `instruction:` | Use forward slashes or escape backslashes in YAML strings |

---

## 🔗 Related Skills

- **HS-135 GATEWAY SOVEREIGN** — Must run first if using `ref: docker:*` MCP toolsets
- **HS-028 SDK PRIMER** — HyperAgent SDK interface standard — agent contracts map here
- **HS-089 THE GRAND ROSTER** — 22 confirmed Hyper Agents — your casting list for this YAML
- **HS-008 THE CONDUCTOR** — BROski Orchestrator pattern — maps to `root` agent + sub-agents
- **HS-067 THE THRONE LADDER** — Role hierarchy — maps to `agents:` nesting depth
- **HS-098 THE SACRED SIX** — 6 Laws of Agents — should live in every `instruction:` block

---

*HS-136 AGENT SCRIBE — HYPER-SKILLs Vault by WelshDog 🐕⚡ — Born 2026-06-28*
*Docker Agent docs: docs.docker.com/ai/docker-agent/*
*Docker Agent GitHub: github.com/docker/docker-agent*
