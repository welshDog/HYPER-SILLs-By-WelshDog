# HS-088 — Agent Final Self-Audit (8-Point Checklist) ✅

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` (Final Checklist)
**Version:** v1

---

## 🤔 What It Does

The last gate before any agent reports `task_completed`. Eight binary checks. If any fails, the agent fixes it before emitting the completion event — never after. Pair with [[HS-087]] (Decision Tree) which gets you to this audit in the first place.

---

## ✅ The 8 Checks

```
[ ] 1. User Agency
       Did I get approval for state-changing actions?               → HS-077

[ ] 2. Context Retention
       Did I minimise user interruptions?                           → HS-078

[ ] 3. ND-Friendly Output
       Are my outputs clear, structured, plain-language?            → HS-069

[ ] 4. Observable
       Did I emit task_started / task_completed events + logs?      → HS-070, HS-073

[ ] 5. Fail Gracefully
       Do I have fallbacks for the realistic failure modes?         → HS-071

[ ] 6. Validated
       Did I run / write the tests for my change?                   → HS-076, HS-086

[ ] 7. Documented
       Did I update the relevant docs / CLAUDE.md?                  → HS-084

[ ] 8. Cited Sources
       Did I reference the Bible / HS-### skill when uncertain?     → (golden rule)
```

---

## 🧪 How To Run It

Drop the checklist into the agent's "before completion" hook:

```python
async def complete_task(task_id: str, result: TaskResult):
    audit = await self_audit({
        "user_agency": result.required_approval is False or result.approval_granted,
        "context_retention": result.user_interruption_count <= 1,
        "nd_friendly": result.output_has_what_why_how or result.is_machine_only,
        "observable": result.events_emitted >= 2,  # started + completed
        "fail_gracefully": result.has_fallback_path,
        "validated": result.tests_passed,
        "documented": result.docs_updated or not result.changes_docs_worthy,
        "cited_sources": result.citations or result.was_routine,
    })

    if not all(audit.values()):
        failed = [k for k, v in audit.items() if not v]
        await log_warning("Self-audit failed", failures=failed)
        return await fix_audit_failures(failed, task_id, result)

    await emit_event({
        "event": "task_completed",
        "agent": self.name,
        "task_id": task_id,
        "audit": audit,
    })
```

---

## 🚨 Hard Stops

These checks **must** pass — no judgment call:
- **#1 User Agency** — if a state-changing action ran without approval, that's a Sacred Rule violation. Roll back, file an incident.
- **#5 Fail Gracefully** — no fallback = no completion. The whole crew assumes graceful failure.

The other six can be downgraded to warnings with a justification logged.

---

## 🧩 Related Skills

- [[HS-087]] Agent Decision Tree — the flow that leads here
- [[HS-077]] User Agency Approval Gate
- [[HS-069]] ND-First Error Messages Template
- [[HS-070]] Observable Agent Operations Pattern
- [[HS-071]] Fail Gracefully + Fallback Chain
- [[HS-076]] Pre-Commit Testing Checklist
- [[HS-085]] 5 Mandatory Agent Guardrails
