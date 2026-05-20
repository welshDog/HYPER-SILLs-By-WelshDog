# HS-087 — Agent Decision Tree (Quick Ref Flowchart) 🌳

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` (Quick Reference)
**Version:** v1

---

## 🤔 What It Does

The single-page decision flow every BROski-crew agent runs on every incoming task. Pin this on the agent's system prompt. If an agent ever loops, hangs, or guesses — it's because it skipped a node on this tree.

---

## 🌳 The Tree

```
Task received
    ↓
Am I the right agent?
    ├─ No  → Delegate to correct agent     (see HS-079)
    └─ Yes ↓
Do I need user approval?
    ├─ Yes → Request approval              (see HS-077)
    └─ No  ↓
Do I have required context?
    ├─ No  → Request from orchestrator     (see HS-068)
    └─ Yes ↓
Execute task                               (with guardrails — HS-085)
    ↓
Did it succeed?
    ├─ No  → Report error + fallback       (see HS-071, HS-083 §3)
    └─ Yes ↓
Update contexts                            (see HS-082)
    ↓
Emit completion event                      (see HS-073)
    ↓
Report results
```

---

## 🚨 Emergency Branches

**When uncertain:**
1. Cite the relevant Bible section / HS-### skill
2. Ask BROski Orchestrator for clarification
3. Request user input (via [[HS-077]] gate)

**When blocked:**
1. Report blocker with details
2. Suggest alternatives
3. Wait for resolution — **don't guess**

**When error occurs:**
1. Log error with `trace_id`
2. Emit error event ([[HS-073]])
3. Return graceful failure ([[HS-071]])
4. Suggest recovery steps

---

## 🪞 Mirror To Final Checklist

Every "Yes" node on the tree has a matching `[ ]` line in [[HS-088]] Agent Final Self-Audit. Run the audit before reporting `task_completed`.

---

## 🧩 Related Skills

- [[HS-079]] Specialist Agent Role Definitions — for the "am I the right agent" node
- [[HS-077]] User Agency Approval Gate — for the approval node
- [[HS-068]] BROski Orchestrator Pattern — context broker
- [[HS-085]] 5 Mandatory Agent Guardrails — wraps "execute task"
- [[HS-071]] Fail Gracefully + Fallback Chain
- [[HS-088]] Agent Final Self-Audit
