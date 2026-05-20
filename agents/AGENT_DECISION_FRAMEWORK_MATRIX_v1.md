# HS-075 — Agent Decision Framework Matrix 🎯

**Category:** `agents/`  
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §10  
**Version:** v1  

---

## 🤔 What It Does

Gives every agent a clear decision matrix for three recurring dilemmas:
1. **Ask user vs decide autonomously**
2. **Delegate vs execute**
3. **Speed vs cost vs quality**

No more guessing. Check the matrix, take the right action.

---

## 🤔 Matrix 1 — Ask vs Decide

```python
if impact == "high" or uncertainty == "high":
    await request_approval(plan)       # ASK USER
elif impact == "low" and uncertainty == "low":
    await execute(plan)                # PROCEED
else:
    await inform_user(f"Proceeding with: {plan}")
    await execute(plan)                # INFORM + PROCEED
```

| Situation | Action |
|---|---|
| Deleting files | ✋ ASK |
| Changing API contracts | ✋ ASK |
| Modifying DB schema | ✋ ASK |
| Deploy to production | ✋ ASK |
| Breaking changes | ✋ ASK |
| Ambiguous requirements | ✋ ASK |
| Formatting code | ✅ PROCEED |
| Adding comments | ✅ PROCEED |
| Adding logs | ✅ PROCEED |
| Writing tests | ✅ PROCEED |

---

## 🤝 Matrix 2 — Delegate vs Execute

```python
if task_requires_specialization:
    await delegate_task(agent="Specialist", task=task)
elif task_is_strategic:
    await broski.handle(task)   # Orchestrator only
elif task_is_routine and agent_has_capability:
    await execute(task)
```

| Task | Who |
|---|---|
| Code implementation | Delegate → Language/Frontend/Backend |
| Security review | Delegate → Security Specialist |
| Test writing | Delegate → QA Specialist |
| Dashboard creation | Delegate → Observability |
| Breaking down requests | Orchestrator ONLY |
| Creating context slots | Orchestrator ONLY |
| Synthesising results | Orchestrator ONLY |

---

## ⚡ Matrix 3 — Speed vs Quality vs Cost

```python
if user_is_waiting:
    strategy = "fast_simple_agent"         # SPEED
elif task_is_critical:
    strategy = "multiple_agents_compete"   # QUALITY
elif budget_is_limited:
    strategy = "cached_responses_first"    # COST
```

---

## 🌳 Agent Decision Tree

```
Task received
    ↓
Am I the right agent?
    → No  → Delegate to correct agent
    ↓ Yes
Do I need user approval?
    → Yes → Request approval
    ↓ No
Do I have required context?
    → No  → Request from orchestrator
    ↓ Yes
Execute task
    ↓
Did it succeed?
    → No  → Report error + fallback
    ↓ Yes
Update contexts → Emit completion event → Report results
```

---

## 🎯 THE PROMPT

```
I need to decide how to handle this agent task:

[DESCRIBE THE TASK]

Evaluate:
1. Impact level: high / medium / low
2. Uncertainty level: high / medium / low
3. Which agent role should handle it?
4. Does it need user approval? Why?
5. What's the priority: speed / quality / cost?

Output the recommended action and why.
```

---

## 🔗 Related Skills
- HS-067 Agent Role Hierarchy Pattern
- HS-068 BROski Orchestrator Pattern
- HS-071 Fail Gracefully + Fallback Chain
