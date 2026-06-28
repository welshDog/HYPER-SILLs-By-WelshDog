# HS-078 — 🌊 FLOW KEEPER — Context Retention / Anti-Interrupt Pattern


---
skill_id: HS-078
hero_name: "FLOW KEEPER"
emoji: "🌊"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-002  # SIX_LAWS_OF_AGENTS — Law 2 (MINIMISE INTERRUPTIONS) is this skill
provides:
  - flow-state-preservation
  - anti-interrupt-defaults
  - silent-decision-pattern
related:
  - HS-077  # CONSENT GUARDIAN — sits in tension; gate state-changes, default small ones
  - HS-075  # THE CHOICE MATRIX — matrix formalises when to interrupt vs default
graph_notes: "Critical ND-first principle — agents preserve hyperfocus by defaulting small decisions rather than interrupting the user."
---
**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §1 Principle 2
**Version:** v1

---

## 🤔 What It Does

Preserves the user's flow state. Agents handle small decisions themselves with sensible defaults instead of context-switching the user every time. Critical for ADHD/autistic builders — every interruption shatters hyperfocus.

> Sits in tension with [[HS-077]] (Approval Gate). Rule of thumb: **gate state-changing actions, default small ones.**

---

## ✅ vs ❌

```
✅ GOOD
User coding → agent detects missing dep → silently checks package.json,
adds latest stable version, notifies low-priority. User stays in flow.

❌ BAD
User coding → agent stops → "What version of React do you want?"
User context-switches, flow broken.
```

---

## 🔧 The Pattern

```python
async def add_dependency(package: str):
    # Don't ask for version if latest stable is safe
    version = await get_latest_stable_version(package)
    await install_dependency(package, version)

    # Inform, don't interrupt
    await notify_user(f"Added {package}@{version}", priority="low")
```

---

## 🎚️ Notification Priority Ladder

| Priority | Use For | UX Surface |
|---|---|---|
| `low` | "I did a small thing" | Toast / log line, no sound |
| `normal` | Status updates | Visible notification, no modal |
| `high` | Needs eventual attention | Persistent badge |
| `block` | Cannot proceed without input | Modal — escalate to [[HS-077]] |

---

## 🚦 Decision Heuristic

```
Will the default work for 90%+ of users?
  ├─ Yes → take the default, notify low-priority
  └─ No  → escalate to [[HS-077]] approval gate
```

---

## 🧩 Related Skills

- [[HS-077]] User Agency Approval Gate — for state-changing ops
- [[HS-075]] Agent Decision Framework Matrix
- [[HS-069]] ND-First Error Messages — same ND-first philosophy applied to errors
