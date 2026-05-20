# HS-077 — User Agency Approval Gate Pattern 🛑

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §1 Principle 1 + §6 Rule 5
**Version:** v1

---

## 🤔 What It Does

The non-negotiable approval pattern for any agent action that **changes state**. Agent proposes → user approves → agent executes. Never silent autonomous changes. Sits behind every file write, deploy, schema change, and destructive op in the HyperCode crew.

---

## ✅ vs ❌

```
✅ GOOD
Agent: "I recommend adding JWT auth to app/middleware/auth.py. Shall I implement?"
User:  "Yes"
Agent: [implements]

❌ BAD
Agent: [silently adds auth middleware without asking]
```

---

## 🔧 The Pattern

```python
async def implement_feature(feature: str):
    plan = await create_implementation_plan(feature)

    # STOP: get approval
    approval = await request_user_approval(plan)
    if not approval:
        return "Feature not implemented — user declined"

    # Only then execute
    return await execute_plan(plan)
```

---

## 🪜 File-Edit Variant (with diff)

```python
async def update_file(path: str, new_content: str):
    current = await read_file(path)
    diff = create_diff(current, new_content)

    approved = await ask_user(
        f"Update {path}?\n\nDiff:\n{diff}\n\nApprove? (yes/no)"
    )

    if approved.lower() == "yes":
        await write_file(path, new_content)
        return "File updated"
    return "Update cancelled"
```

---

## 🎯 When To Gate (vs proceed silently)

Gate **mandatory** for:
- Deleting files
- Changing API contracts
- Modifying database schemas
- Deployment to production
- Changing authentication logic
- Any breaking change

Proceed **without gate** (but inform) for:
- Formatting code
- Adding comments / logs
- Renaming local-scope variables
- Writing tests

Decision logic = [[HS-075]] Decision Framework Matrix.

---

## 🧩 Related Skills

- [[HS-075]] Agent Decision Framework Matrix — when to ask vs decide
- [[HS-085]] 5 Mandatory Agent Guardrails — full guardrail set
- [[HS-068]] BROski Orchestrator Pattern — orchestrator uses this gate before every plan
