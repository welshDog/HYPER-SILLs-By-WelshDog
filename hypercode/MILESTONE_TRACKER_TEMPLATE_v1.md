# HS-066 — 🏆 THE MILESTONE KEEPER — Milestone Tracker Template

**Category:** hypercode
**Version:** 1.0

> *"A phase plan that stays honest — verified-against-reality, not vibes."*

---

## 🎯 What It Does

A reusable template for tracking phased delivery (P0 → P1 → P2) where every item
carries a *verified* status, not an assumed one.

## 🌍 Why It Exists

Roadmaps rot. Snapshots lag the parallel git workflow. This template forces a
disk/origin check so the tracker never lies (the exact trap that made a "37
catalogued" list 22 stale).

## ⚙️ How To Use

Drop into `docs/NEXT_TASKS.md`. Update status only after verifying against
`origin/main` + the live system — never from memory.

---

## 📋 THE PROMPT

```
Milestone tracker (verify before you tick):

| # | Task | Status | Evidence |
|---|---|---|---|
| P0-1 | <task> | ✅ Done / ⬜ Next / 🔨 WIP | commit sha + live proof |

Rules:
  - ✅ requires: committed + pushed (post-push 0/0) AND a live/E2E check.
  - Before marking the "next" task, git fetch + diff origin/main (3 tasks were
    already done in one session — see HS-113 Parallel Git Workflow).
  - Surface contradictions: if a brief assumes state X but reality is Y, say so
    (HS-111). e.g. "brief said migration 016, alembic current shows head 017 → use 018".
  - One task at a time. Quick wins first. No overwhelm.
```

## ✅ Example

> Brief: "create migration 016". Tracker forces `alembic current` → head is 017 →
> tracker records "018 (corrected; 016/017 taken)" with the commit as evidence.

## 🔗 Related Skills

[[ECOSYSTEM_INVENTORY_v1]] · [[SESSION_END_CHECKLIST_v1]]
