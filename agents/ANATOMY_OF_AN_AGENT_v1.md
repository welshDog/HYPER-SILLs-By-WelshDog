# HS-001 — 🦴 ANATOMY OF AN AGENT — The Core Structure Every Agent Needs

---
skill_id: HS-001
hero_name: "ANATOMY OF AN AGENT"
emoji: "🦴"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - none  # Root skill — foundational, no upstream deps
provides:
  - agent-structure-pattern
  - agent-anatomy-reference
  - agent-build-checklist
related:
  - HS-002  # SIX_LAWS_OF_AGENTS
  - HS-003  # AGENT_LIFECYCLE_STATE_MACHINE
  - HS-010  # SPECIALIST_AGENT_ROLES
graph_notes: "Root node of the agent graph — defines the canonical anatomy every agent in the swarm must implement."
---

**Category:** `agents/`
**Version:** v1

---

## 🤔 What It Does

Defines the canonical anatomy of an agent: the required components, structure, and interface every agent in the HyperFocus swarm must have. The foundation everything else builds on.

---

## 🎯 Purpose

- **Who uses it:** Agent builders, orchestrators, onboarding new AI sessions
- **When to use it:** First thing you read before building any new agent
- **What it unlocks:** A consistent, interoperable agent architecture across all 39+ agents

---

## 📥 Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `agent_name` | `string` | ✅ | Name of the agent being built |
| `role` | `string` | ✅ | What the agent does |

---

## 📤 Output Format

```json
{
  "agent": {
    "name": "string",
    "role": "string",
    "tools": [],
    "memory": {},
    "output_format": {}
  }
}
```

---

## 🔮 Prompt Block

```
You are an agent architect for the HyperFocus Zone.

Build a new agent following the canonical anatomy:
1. Identity (name, role, tier)
2. Tools (what it can call)
3. Memory (what it retains)
4. Output contract (what it returns)
5. Guardrails (what it must never do)

Agent to build: [AGENT_NAME]
Role: [ROLE]
```

---

## 💡 Example Usage

```python
# Load this skill when spinning up a new agent definition
agent = {
    "name": "MORNING_BRIEFING",
    "role": "Delivers daily system status to Discord",
    "tier": 2,
    "tools": ["docker_check", "discord_webhook", "github_issues"],
    "memory": {"last_run": None, "failure_count": 0},
    "output_format": "discord_embed"
}
```

---

## 🚨 Anti-patterns

- **Don't build agents without an output contract** — downstream agents can't consume undefined output
- **Don't skip the guardrails section** — every agent needs at least one hard stop

---

## 🔗 Related Skills

- [[HS-002]] SIX_LAWS_OF_AGENTS — the rules every agent obeys
- [[HS-003]] AGENT_LIFECYCLE_STATE_MACHINE — how agents move through states
- [[HS-010]] SPECIALIST_AGENT_ROLES — which roles exist in the swarm

---

## 📋 THE PROMPT

> Copy this block into any AI session to activate the skill:

```text
Use skill HS-001 ANATOMY OF AN AGENT. Build a new agent following the canonical HyperFocus structure: identity, tools, memory, output contract, guardrails.
```
