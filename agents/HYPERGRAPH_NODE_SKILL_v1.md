# HS-126 — 🔗 NODE SMITH — HyperGraph Node Skill

---
skill_id: HS-126
hero_name: "NODE SMITH"
emoji: "🔗"
version: v1.0
category: agents
depends_on:
  - HS-001  # ANATOMY_OF_AN_AGENT — agents are nodes; anatomy defines their shape
provides:
  - hypergraph-pattern
  - node-based-design
  - visual-architecture-spec
  - typed-port-model
related:
  - HS-008  # BROSKI ORCHESTRATOR PATTERN — orchestrator is a hub node
  - HS-123  # GODFLOW — god mode workflow maps to a hypergraph
graph_notes: "Visual node-graph architecture pattern — design any agent system as a circuit-board of typed input/brain/output nodes."
---
**Category:** Agents / Dev Architecture  
**Version:** 1.0  
**Author:** WelshDog  
**Rescued From:** [GOD-Agent-Mode](https://github.com/welshDog/GOD-Agent-Mode) (archived)  
**Optimised For:** Visual programming, graph-based system design, ND-friendly architecture

---

## 📋 What This Skill Does

Designs systems using the **HyperGraph** pattern — a visual, node-based architecture that replaces overwhelming text-heavy code design with spatial, circuit-board-style thinking.

Use this skill to:
- Design any agent system as a visual node graph
- Break logic into HyperNodes (input → brain → output)
- Map data flow left-to-right with typed ports
- Spec a new feature or system visually before writing code

---

## 📥 Input Format

```
[SYSTEM_NAME] = Name of the system you're designing
[GOAL] = What this system needs to do (1-2 sentences)
[INPUTS] = What data goes in (e.g. user text, API response, file)
[OUTPUTS] = What comes out (e.g. processed result, action, UI update)
[COMPLEXITY] = simple / medium / complex
```

---

## 🤖 THE PROMPT (Copy + Paste This)

```
You are a HyperGraph System Architect for the Hyperfocus Zone.

Design [SYSTEM_NAME] as a visual HyperGraph using the HyperNode pattern.

HyperNode Rules:
- Every node has: Inputs on the LEFT, Logic/Brain in the CENTER, Outputs on the RIGHT
- Data flows LEFT to RIGHT only (unidirectional)
- All ports are typed: String / Number / Boolean / Flow / Array / Object
- Nodes are reactive: when input changes, node re-evaluates
- Keep each node focused on ONE transformation

HyperGraph Rules:
- Start with an INPUT node (raw data entry point)
- End with an OUTPUT node (result / action / display)
- Max 7 nodes for a simple system, 15 for complex
- Name every node clearly (e.g. "Parse User Input", "Call API", "Format Result")

Delivery format:
1. ASCII or text-based node map showing the full graph
2. For each node: Name | Inputs | Logic | Outputs
3. Data flow description (how data travels through the system)
4. Tech stack suggestion (Zod for schema, Zustand for state, React Flow for viz if applicable)
5. First prototype node to build (the simplest possible proof of concept)

System to design:
- Name: [SYSTEM_NAME]
- Goal: [GOAL]
- Inputs: [INPUTS]
- Outputs: [OUTPUTS]
- Complexity: [COMPLEXITY]
```

---

## 💡 Example Usage

```
System Name: YT Analytics Debugger Pipeline
Goal: Take YouTube video stats and output a debug report + fix plan
Inputs: CTR, impressions, AVD, retention dips (text)
Outputs: Diagnosis summary, bug report, refactor plan (markdown)
Complexity: simple
```

**Expected Output:**
```
[Raw Stats Input] → [Parse Metrics] → [Diagnose Issues] → [Generate Fix Plan] → [Format Report Output]
```

---

## 🌊 HyperNode Quick Template

```
Node Name: _______________
Inputs:  [left ports]  ← typed
Logic:   [what it does to the data]
Outputs: [right ports] → typed
Reactive: yes / no
```

---

## 🔗 Related Skills
- `agents/GOD_MODE_HYPERFLOW_v1.md` (HS-006)
- `dev/SYSTEM_ARCHITECT_v1.md` *(coming soon)*
- `agents/AGENT_INTERFACE_v1.md` *(coming soon)*

---

*Rescued from GOD-Agent-Mode — HYPER-SKILLs Vault by WelshDog 🐕⚡*
