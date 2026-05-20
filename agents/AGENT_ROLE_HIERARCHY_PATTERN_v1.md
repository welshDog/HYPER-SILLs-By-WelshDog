# HS-067 — Agent Role Hierarchy Pattern 🏛️

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
