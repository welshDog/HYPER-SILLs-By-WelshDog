# HS-097 — 🕸️ THE WEB OF NEEDS — Hyper Agent Dependency Graph (Worked Example, 8 Codenames)

---
skill_id: HS-097
hero_name: "THE WEB OF NEEDS"
emoji: "🕸️"
version: v1.0
category: agents
depends_on:
  - HS-090  # SOUL SCROLL — dependency graph is a worked example of the life_plan schema
  - HS-009  # HYPER_AGENT_ROSTER — roster gives the 22 agents; this graph maps the founding 8
provides:
  - dependency-graph-example
  - agent-codename-reference
  - collaboration-matrix-template
  - founding-8-wiring
related:
  - HS-008  # BROSKI ORCHESTRATOR PATTERN — orchestrator uses the dependency graph for routing
  - HS-042  # REGISTRY LORD — registry pattern builds on the dependency map
graph_notes: "Worked example of the collaboration_matrix.dependency_graph field — copy as starting point when wiring depends_on/depended_by for new agents."
---

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/🦅 HYPER AGENT LIFE PLANS — MASTER ARCHITECTURE` §1 (collaboration_matrix)
**Version:** v1

---

## 🤔 What It Does

A **concrete worked example** of the abstract `collaboration_matrix.dependency_graph` field from [[HS-090]]. Maps the 8 original Hyper Agent codenames to their declared dependencies. Copy this as a starting point when wiring `depends_on` / `depended_by` for new agents.

> The Roster ([[HS-089]]) gives you 22 agents; this graph captures the **founding 8** with their classical codenames (MetaArchitect, BROski Brain, AutoEvo, MedBot, SwarmMaster, TerminalGod, DashBoss, QuantumX) and the wiring between them. Newer agents bolt onto this skeleton.

---

## 🧬 The 8 Codenames + Ports

| Codename | Display name | Port | Role taxonomy |
|---|---|---|---|
| `MetaArchitect` | 🦅 Agent X | 8080 | Orchestrator |
| `SwarmMaster` | 🤖 Crew Orchestrator | 8081 | Orchestrator |
| `BROski Brain` | 🧠 The Brain | 8082 | Specialist |
| `AutoEvo` | 🛠️ DevOps Engineer | 8083 | Executor |
| `MedBot` | 🩺 Healer Agent | 8008 | Executor |
| `TerminalGod` | 💬 BROski Terminal | 3000 | Interface |
| `DashBoss` | 📊 Mission Control | 8088 | Interface |
| `QuantumX` | 🔮 Quantum Compiler | 8090 | Specialist |

> Role taxonomy values: `Orchestrator | Executor | Interface | Specialist`. New agents must declare exactly one.

---

## 🕸️ The Graph (YAML — drop into `life_plan.yaml`)

```yaml
collaboration_matrix:
  dependency_graph:
    MetaArchitect: []                                  # root — depends on nothing
    SwarmMaster:   ["MetaArchitect"]
    BROski Brain:  ["SwarmMaster"]
    AutoEvo:       ["SwarmMaster", "MetaArchitect"]
    MedBot:        ["AutoEvo"]
    TerminalGod:   ["BROski Brain", "SwarmMaster"]
    DashBoss:      ["SwarmMaster", "MedBot"]
    QuantumX:      ["MetaArchitect", "BROski Brain"]
```

---

## 🌳 Visual

```
                    MetaArchitect (root)
                    /              \
              SwarmMaster          AutoEvo ──┐
              /    |    \             │      │
      BROski    DashBoss MedBot ◄─────┘      │
       Brain    /                            │
         │    /                              │
    TerminalGod                              │
         │                                   │
    QuantumX ◄────────────────────────────── (depends on MetaArchitect + BROski Brain)
```

---

## 📜 The Three Wiring Rules

1. **Roots have empty `depends_on`** — only `MetaArchitect` qualifies. Anything else with `[]` is misconfigured.
2. **No cycles.** Validated by the Crew Orchestrator on agent registration — a cycle = registration refused.
3. **`depended_by` is auto-derived** — never write it by hand. The Crew Orchestrator computes it from everyone else's `depends_on`.

---

## 🔌 How To Add A New Agent

```yaml
# agents/your_agent/life_plan.yaml
identity_manifest:
  name: "YourAgent"
  codename: "YourCodename"
  port: 8XXX
  # ...

collaboration_matrix:
  role: "Specialist"   # pick from Orchestrator/Executor/Interface/Specialist
  dependency_graph:
    depends_on: ["SwarmMaster", "BROski Brain"]   # what YOU need to function
    depended_by: []                                # leave empty — auto-derived
```

Push, register with Crew Orchestrator, and the rest of the graph re-derives.

---

## 🚨 Invariants

- **`MetaArchitect` must stay rootless.** If it ever gets a `depends_on` entry, the spawn-lock breaks ([[HS-091]] Agent X invariant).
- **`MedBot` must depend on `AutoEvo`.** The deploy pipeline writes the healer's manifest — break this dep and the healer can't be redeployed.
- **`SwarmMaster` is the "second root" practically** — most agents transitively depend on it. If `SwarmMaster` goes down, the swarm degrades to direct point-to-point calls (allowed for queries, not for task delegation — see [[HS-091]] Crew Orchestrator invariant).

---

## 🧩 Related Skills

- [[HS-090]] Universal Life Plan YAML — schema this populates
- [[HS-089]] Hyper Agent Roster — the 22-agent superset (this is the founding 8)
- [[HS-091]] Top-Tier Agent Identity Cards — invariants referenced above
- [[HS-092]] Agent Contract Test Suite — verifies the live graph matches the YAML
