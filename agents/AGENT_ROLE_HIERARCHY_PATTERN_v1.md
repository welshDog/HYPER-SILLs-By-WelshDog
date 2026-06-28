# HS-067 — 👑 THE THRONE LADDER — Agent Role Hierarchy Pattern


---
skill_id: HS-067
hero_name: "THE THRONE LADDER"
emoji: "👑"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-001  # ANATOMY_OF_AN_AGENT — anatomy defines role components
  - HS-002  # SIX_LAWS_OF_AGENTS — laws set role boundaries
provides:
  - role-hierarchy
  - orchestrator-worker-validator-model
  - delegation-boundaries
related:
  - HS-008  # BROSKI ORCHESTRATOR PATTERN — the Orchestrator role defined here
  - HS-079  # THE CREW CHARTER — per-specialist role definitions
graph_notes: "Canonical Orchestrator→Worker→Validator role structure — the skeleton all multi-agent systems build on."
---
**Category:** `agents/`  
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §2  
**Version:** v1  

---

## 🤔 What It Does

Defines the canonical role structure for a multi-agent AI system. One Orchestrator manages multiple specialist Workers and Validators. Each role has strict boundaries — they can only do certain things and must delegate the rest.

---

## 🏛️ The Role Hierarchy

```
User
  ↓
BROski Orchestrator (Manager)
  ├─→ Language Engine Specialist (Worker)
  ├─→ Frontend Specialist (Worker)
  ├─→ Backend Specialist (Worker)
  ├─→ Observability Specialist (Validator)
  ├─→ Security Specialist (Validator)
  └─→ QA Specialist (Validator)
```

---

## 🔑 Core Rules Per Role Type

### Orchestrator
- ✅ Break down requests, delegate, synthesise results
- ❌ CANNOT write code, read full files, or deploy

### Workers (Language / Frontend / Backend)
- ✅ Execute their specialist domain
- ❌ CANNOT touch other domains — must delegate

### Validators (Observability / Security / QA)
- ✅ Review, test, audit, alert
- ❌ CANNOT modify application logic

---

## 🎯 THE PROMPT

```
You are an AI agent in a multi-agent system.
Your role is: [ROLE_NAME]

You CAN:
[LIST_OF_CAPABILITIES]

You CANNOT (delegate these):
[LIST_OF_RESTRICTIONS]

When you receive a task outside your role, respond:
"This task is outside my role. Delegating to [CORRECT_AGENT]."

When you complete a task, emit:
{ "event": "task_completed", "agent": "[ROLE_NAME]", "result": "[SUMMARY]" }
```

---

## 💡 Example

```
User: "Add authentication to the API"

BROski Orchestrator:
1. Creates context slots: [api_routes, auth_design, auth_implementation]
2. Delegates to Backend Specialist → investigate current API
3. Delegates to Security Specialist → design JWT middleware
4. Delegates to Backend Specialist → implement
5. Delegates to QA Specialist → test
6. Synthesises: "Added JWT auth to 12 endpoints, 100% test coverage"
```

---

## 🔗 Related Skills
- HS-068 BROski Orchestrator Pattern
- HS-073 SSE Agent Event Schema
- HS-075 Agent Decision Framework Matrix
