# HS-085 — 🚧 THE FIVE WARDS — 5 Mandatory Agent Guardrails

---
skill_id: HS-085
hero_name: "THE FIVE WARDS"
emoji: "🚧"
version: v1.0
category: agents
depends_on: []
provides:
  - agent-guardrails
  - input-validation-pattern
  - cost-limit-pattern
  - timeout-pattern
  - approval-gate-pattern
related:
  - HS-077  # User Agency Approval Gate — Rule 5 mechanism
  - HS-071  # Fail Gracefully + Fallback Chain — when Rule 3 fires
  - HS-076  # Pre-Commit Testing Checklist
  - HS-088  # Agent Final Self-Audit
graph_notes: "Foundation skill — no dependencies. Provides the 5 core safety constraints consumed by most agent skills."
---

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §6
**Version:** v1

---

## 🤔 What It Does

The five hard rules every BROski-crew agent must enforce in code, not vibes. Each one has a `✅ GOOD` and `❌ BAD` pattern. Skip any of these and the agent will either hallucinate APIs, leak budget, hang forever, or silently destroy a user's file.

---

## 1️⃣ Never Hallucinate APIs

Verify the API exists before calling it.

```python
# ✅ GOOD
apis = await search_code("def ", file_types=["*.py"])
if "execute_hypercode" in apis:
    await call_api("execute_hypercode", source=code)
else:
    return f"API not found. Available: {list(apis.keys())}"

# ❌ BAD
await call_api("execute_hypercode", source=code)  # assumes it exists
```

---

## 2️⃣ Always Validate Input

Reject bad input early with a friendly message.

```python
# ✅ GOOD
async def execute_code(source: str, timeout: int = 30):
    if not source or not source.strip():
        raise ValueError("Source code cannot be empty")
    if timeout < 1 or timeout > 300:
        raise ValueError("Timeout must be between 1 and 300 seconds")

# ❌ BAD
async def execute_code(source: str, timeout: int = 30):
    return await run(source, timeout)  # hope for the best
```

---

## 3️⃣ Timeout Everything

Every external call wrapped in `asyncio.wait_for`.

```python
# ✅ GOOD
async def risky_operation():
    try:
        return await asyncio.wait_for(long_running_task(), timeout=30)
    except asyncio.TimeoutError:
        return "Operation timed out after 30 seconds"

# ❌ BAD
async def risky_operation():
    return await long_running_task()  # could hang forever
```

---

## 4️⃣ Cost Limits

Track LLM/API spend per agent; refuse before exceeding budget.

```python
# ✅ GOOD
class Agent:
    def __init__(self, max_cost_usd: float = 1.0):
        self.max_cost_usd = max_cost_usd
        self.cost_spent = 0.0

    async def call_llm(self, prompt: str):
        estimated = estimate_cost(prompt)
        if self.cost_spent + estimated > self.max_cost_usd:
            raise BudgetExceededError(f"Would exceed ${self.max_cost_usd}")
        result = await llm.generate(prompt)
        self.cost_spent += result.cost
        return result

# ❌ BAD
async def call_llm(prompt: str):
    return await llm.generate(prompt)  # no tracking
```

---

## 5️⃣ Never Modify Files Without Approval

State-changing writes always go through [[HS-077]].

```python
# ✅ GOOD
async def update_file(path: str, content: str):
    diff = create_diff(await read_file(path), content)
    approved = await ask_user(f"Update {path}?\n\nDiff:\n{diff}\n\nApprove? (yes/no)")
    if approved.lower() == "yes":
        await write_file(path, content)
        return "File updated"
    return "Update cancelled"

# ❌ BAD
async def update_file(path: str, content: str):
    await write_file(path, content)  # silent change
```

---

## 🧪 Quick Self-Audit

Before shipping a new agent, grep its source for:
- [ ] Every `await call_*` has a prior existence check OR is a known stable API
- [ ] Every public function has input validation at the top
- [ ] Every external `await` is wrapped in `wait_for` with a numeric timeout
- [ ] LLM-calling code tracks `cost_spent` against a budget
- [ ] No `write_file` outside an approval-gated function

5/5 = ship. < 5/5 = fix.

---

## 🧩 Related Skills

- [[HS-077]] User Agency Approval Gate — Rule 5's mechanism
- [[HS-071]] Fail Gracefully + Fallback Chain — what to do when Rule 3 fires
- [[HS-076]] Pre-Commit Testing Checklist — automation that catches some of these
- [[HS-090]] Agent Final Self-Audit
