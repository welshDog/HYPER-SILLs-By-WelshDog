# HS-071 — Fail Gracefully + Fallback Chain 🔄

**Category:** `agents/`  
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §1 Principle 5 + §6  
**Version:** v1  

---

## 🤔 What It Does

Agents can fail. This skill gives you the patterns to handle every failure type gracefully — with fallback chains, timeouts, cost limits, and ND-friendly error messages — so your agent never crashes the user's workflow.

---

## 🔄 Fallback Chain Pattern

```python
async def get_code_suggestion(code: str) -> str:
    try:
        # Primary: Advanced agent
        return await advanced_agent.suggest(code)
    except AgentTimeout:
        # Fallback 1: Simple heuristic
        return await simple_heuristic(code)
    except Exception:
        # Fallback 2: Cached suggestion
        return await get_cached_suggestion(code)
    finally:
        # Never return nothing
        return "Agent temporarily unavailable. Try again or ask BROski."
```

---

## ⏱️ Timeout Everything

```python
async def risky_operation():
    try:
        result = await asyncio.wait_for(
            long_running_task(),
            timeout=30
        )
        return result
    except asyncio.TimeoutError:
        return "Operation timed out after 30 seconds"
```

---

## 💰 Cost Limits

```python
class Agent:
    def __init__(self, max_cost_usd: float = 1.0):
        self.max_cost_usd = max_cost_usd
        self.cost_spent = 0.0

    async def call_llm(self, prompt: str):
        estimated_cost = estimate_cost(prompt)
        if self.cost_spent + estimated_cost > self.max_cost_usd:
            raise BudgetExceededError(
                f"Would exceed budget: ${self.max_cost_usd}"
            )
        result = await llm.generate(prompt)
        self.cost_spent += result.cost
        return result
```

---

## 🚨 Error Propagation Pattern

```python
try:
    result = await risky_operation()
except Exception as e:
    await log_error("Operation failed", error=str(e), agent="Backend Specialist")
    await emit_event({
        "event": "task_failed",
        "agent": "Backend Specialist",
        "data": {
            "error": str(e),
            "recovery_suggestion": "Check API connectivity"
        }
    })
    return TaskResult(
        success=False,
        error=str(e),
        recovery_suggestion="Check API connectivity"
    )
```

---

## 5 Mandatory Guardrails

1. **Never hallucinate APIs** — search first, call only if exists
2. **Always validate input** — empty source, bad timeout → raise early
3. **Timeout everything** — `asyncio.wait_for()` on all async ops
4. **Cost limits** — track spend, raise before exceeding budget
5. **Never modify files without approval** — show diff, ask first

---

## 🎯 THE PROMPT

```
Add fail-gracefully patterns to this agent code:

[PASTE CODE HERE]

Add:
1. 3-level fallback chain (primary → heuristic → cache → default message)
2. asyncio.wait_for() timeout of 30s on all async operations
3. Cost tracking with max_cost_usd = 1.0 guard
4. Input validation before execution
5. Error event emission on failure with recovery_suggestion
```

---

## 🔗 Related Skills
- HS-069 ND-First Error Messages Template
- HS-070 Observable Agent Operations Pattern
- HS-075 Agent Decision Framework Matrix
