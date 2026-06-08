# HS-077 — 🛑 CONSENT GUARDIAN — User Agency Approval Gate Pattern


---
skill_id: HS-077
hero_name: "CONSENT GUARDIAN"
emoji: "🛑"
version: v1.0
category: agents
depends_on:
  - HS-002  # SIX_LAWS_OF_AGENTS — Law 1 (RESPECT USER AGENCY) is this skill
provides:
  - approval-gate-pattern
  - propose-approve-execute-flow
  - state-change-guard
related:
  - HS-078  # FLOW KEEPER — sits in tension; gate state-changes, default small ones
  - HS-088  # THE MIRROR OATH — check 1 in the completion audit
  - HS-004  # FIVE MANDATORY GUARDRAILS — approval gate is guardrail 1
graph_notes: "Non-negotiable approval pattern for any state-changing agent action — propose → approve → execute, never silent."
---
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
