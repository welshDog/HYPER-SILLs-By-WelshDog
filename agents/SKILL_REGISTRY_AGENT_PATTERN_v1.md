# HS-042 — 📋 REGISTRY LORD — SkillRegistry Agent Pattern
**Category:** agents
**Version:** 1.0


---
skill_id: HS-042
hero_name: "REGISTRY LORD"
emoji: "📋"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-008  # BROSKI ORCHESTRATOR PATTERN — orchestrator uses the registry for routing
  - HS-067  # THE THRONE LADDER — hierarchy determines registry authority
provides:
  - skill-registry-pattern
  - task-routing
  - agent-capability-index
  - yellow-pages-pattern
related:
  - HS-079  # THE CREW CHARTER — role definitions feed the registry
  - HS-125  # THE GRAND CODEX — codex is the source of truth for capabilities
graph_notes: "Central registry pattern for a 30+ agent swarm — the Yellow Pages that routes tasks to the best-matched agent."
problem_keywords:
  - skill registry
  - route to capability
  - yellow pages
  - find the right agent

---
> *"An agent that knows what every other agent can do — and routes tasks to the right one."*

---

## 🎯 What It Does
The SkillRegistry pattern — a central agent that maintains a live registry of all agent capabilities and routes incoming tasks to the best-matched agent automatically.

## 🌍 Why It Exists
In a 30+ agent swarm, without a registry, tasks get lost or duplicated. SkillRegistry is the Yellow Pages of the swarm.

## ⚙️ How To Use
1. Paste when building the orchestrator or adding a new agent to the swarm
2. Register new agent capabilities using the schema below
3. Route tasks via the registry — never hardcode agent targets

---

## 📋 THE PROMPT

```
Implement the SkillRegistry agent pattern for: [CONTEXT]

REGISTRY SCHEMA (per agent):
```json
{
  "agent_id": "[AGENT_NAME]",
  "capabilities": ["[SKILL_1]", "[SKILL_2]"],
  "endpoint": "http://[AGENT_NAME]:[PORT]",
  "health": "/health",
  "priority": 1,
  "tags": ["[TAG_1]", "[TAG_2]"]
}
```

ROUTING LOGIC:
1. Receive task with tags: [TASK_TAGS]
2. Query registry: SELECT agents WHERE capabilities OVERLAP task.tags
3. Filter: health_check == OK AND priority == highest
4. Route task to winning agent
5. Log routing decision to routing_log table
6. On failure: fallback to next priority agent

SACRED RULES:
- Registry is READ by all agents, WRITTEN only by orchestrator
- NEVER hardcode agent URLs in business logic — always resolve via registry
- Health check before every route — no ghost routing

Output: FastAPI /registry/agents GET + /registry/route POST
```

---

## 🔗 Related Skills
- HS-068 — THE CONDUCTOR (Orchestrator Pattern)
- HS-080 — THE TOOL BELT (Universal Agent Tools API)
- HS-079 — THE CREW CHARTER (Agent Role Definitions)

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
