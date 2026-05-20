# HS-072 — Context Store Architecture (Redis) 🗃️

**Category:** `agents/`  
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §7  
**Version:** v1  

---

## 🤔 What It Does

The Context Store is the shared memory of your agent crew. Agents create, read, and update context slots so they can hand off work without losing information. Built on Redis. Uses dot-notation keys for structure.

---

## 🏗️ Architecture

```
Context Store (Redis)
    ├─ api.routes.current_structure
    ├─ api.auth.design
    ├─ api.auth.implementation
    ├─ language.grammar.v0
    ├─ language.examples.basic
    ├─ frontend.editor.config
    └─ observability.dashboards.execution
```

---

## 🔑 Key Naming Convention

```
{domain}.{subdomain}.{specific}

✅ GOOD:
"api.routes.current_structure"
"auth.design.jwt_strategy"
"language.grammar.version_0"

❌ BAD:
"stuff"
"the_api_routes_we_found"
"data"
```

---

## 📦 Context Value Structure

```python
{
    "created_at": "2026-02-03T16:00:00Z",
    "created_by": "Backend Specialist",
    "version": 1,
    "data": {
        # Your actual context data
    },
    "metadata": {
        "source_files": ["app/routers/execution.py"],
        "confidence": "high",   # high | medium | low
        "expires_at": None       # Optional TTL
    }
}
```

---

## 🔄 Context Lifecycle

```python
# 1. Create (Orchestrator)
await create_context(
    name="api.auth.design",
    value={
        "created_by": "BROski Orchestrator",
        "data": { "strategy": "JWT", "token_expiry": 3600 },
        "metadata": { "confidence": "high" }
    }
)

# 2. Read (Worker agent)
auth_design = await read_context("api.auth.design")

# 3. Update (Worker reports back)
await update_context(
    name="api.auth.implementation",
    value={
        "created_by": "Backend Specialist",
        "data": {
            "files_created": ["app/middleware/jwt.py"],
            "endpoints_protected": 12
        },
        "metadata": { "status": "complete" }
    }
)

# 4. Future agent reads previous work
prev = await read_context("api.auth.implementation")
```

---

## ✅ DO / ❌ DON'T

**DO:**
- Use structured dot-notation keys
- Include metadata (source, confidence, timestamp)
- Keep contexts focused + single-purpose
- Expire stale contexts

**DON'T:**
- Store full file contents (use summaries)
- Create vague keys
- Let contexts grow unbounded
- Store secrets without encryption
- Create circular dependencies

---

## 🎯 THE PROMPT

```
Design a Context Store layout for this agent workflow:

[DESCRIBE YOUR AGENT WORKFLOW]

Output:
1. List of context slot keys (dot notation)
2. What agent creates each slot
3. What agent reads each slot
4. Data shape for each slot
5. Confidence level + expiry for each
```

---

## 🔗 Related Skills
- HS-068 BROski Orchestrator Pattern
- HS-073 SSE Agent Event Schema
- HS-067 Agent Role Hierarchy Pattern
