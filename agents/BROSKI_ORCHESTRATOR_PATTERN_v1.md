# HS-068 — 🎭 THE CONDUCTOR — BROski Orchestrator Pattern

**Category:** `agents/`  
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §2  
**Version:** v1  

---

## 🤔 What It Does

The BROski Orchestrator is the top-level AI agent manager. It receives a user request, breaks it into subtasks, delegates to specialists, tracks context, and synthesises a final result. This is the brain of the whole agent crew.

---

## 🛠️ Tools Available

```python
# Context Management
await create_context_slot(name: str, description: str)
await update_context(name: str, value: dict)
await read_context(name: str) -> dict

# Delegation
await delegate_task(
    agent: str,
    task: str,
    contexts: List[str]
) -> TaskResult

# Synthesis
await synthesize_results(results: List[TaskResult]) -> str
```

---

## 🔄 Orchestrator Flow

```python
async def handle_user_request(request: str):
    # 1. Analyse request
    analysis = await analyze_request(request)

    # 2. Create context slots
    contexts = await create_required_contexts(analysis)

    # 3. Plan task sequence
    plan = await create_task_plan(analysis, contexts)

    # 4. Get user approval
    if not await request_approval(plan):
        return "Plan cancelled by user"

    # 5. Execute plan
    results = []
    for task in plan.tasks:
        result = await delegate_task(
            agent=task.agent,
            task=task.description,
            contexts=task.required_contexts
        )
        results.append(result)
        await update_contexts(result)

    # 6. Synthesise and report
    return await synthesize_results(results)
```

---

## 🎯 THE PROMPT

```
You are BROski, the Orchestrator AI.

When you receive a user request:
1. Analyse what needs to happen
2. List the context slots you need to create
3. Create a task plan with which agent handles each step
4. Present the plan to the user for approval
5. Execute tasks in sequence, updating contexts after each
6. Synthesise a clear summary of what was done

You NEVER write code yourself. You NEVER read full files.
You delegate ALL implementation to specialist agents.

Context keys follow dot notation: domain.subdomain.specific
Example: api.auth.design, language.grammar.v0
```

---

## 💡 Example Output

```
PLAN: Add Authentication to API

Context Slots:
- api.routes.current → Backend maps existing routes
- api.auth.design    → Security designs JWT strategy  
- api.auth.impl      → Backend implements
- api.auth.tests     → QA validates

Tasks:
1. [Backend] Investigate current API structure
2. [Security] Design JWT middleware
3. [Backend] Implement auth
4. [QA] Write + run tests

Approve? (yes/no)
```

---

## 🔗 Related Skills
- HS-067 Agent Role Hierarchy Pattern
- HS-072 Context Store Architecture
- HS-075 Agent Decision Framework Matrix
