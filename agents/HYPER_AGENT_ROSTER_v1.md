# HS-009 — 📋 HYPER AGENT ROSTER — The Full Register of Every Agent in the Swarm

---
skill_id: HS-009
hero_name: "HYPER AGENT ROSTER"
emoji: "📋"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-001  # ANATOMY_OF_AN_AGENT — each roster entry follows anatomy spec
provides:
  - agent-registry
  - agent-discovery
  - swarm-inventory
  - agent-capability-map
related:
  - HS-007  # HYPERFOCUS_AGENT_SWARM_CORE
  - HS-008  # BROSKI_ORCHESTRATOR_PATTERN
  - HS-010  # SPECIALIST_AGENT_ROLES
graph_notes: "Master registry of all 39+ agents — name, role, tier, tools, and status. Single source of truth for orchestrators and skill discovery."
problem_keywords:
  - agent roster
  - list of agents
  - which agents exist
  - agent inventory

---

**Category:** `agents/`
**Version:** v1

---

## 🔗 Related Skills

- [[HS-007]] HYPERFOCUS_AGENT_SWARM_CORE — swarm reads from the roster
- [[HS-008]] BROSKI_ORCHESTRATOR_PATTERN — orchestrator queries the roster to route tasks
- [[HS-010]] SPECIALIST_AGENT_ROLES — roster entries reference role definitions

---

## 📋 THE PROMPT

```text
Use skill HS-009 HYPER AGENT ROSTER. Find the best agent for task: [TASK]. Return agent name, tier, and tools.
```
