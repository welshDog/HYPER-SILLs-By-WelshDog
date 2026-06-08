# HS-012 — 🪜 THE ASCENT — Level Progression

---
skill_id: HS-012
hero_name: "THE ASCENT"
emoji: "🪜"
version: v1.0
category: broski
depends_on:
  - HS-002  # SIX_LAWS_OF_AGENTS — Law 5 (REWARD) motivates this system
provides:
  - level-progression-rules
  - xp-calculation
  - tier-unlock-conditions
related:
  - HS-107  # THE RANK & THE NAME — rank titles map to progression tiers
  - HS-034  # BEAT ARCHITECT — module structure produces the XP awarded here
graph_notes: "BROski level/XP progression system — the dopamine engine that converts task completion into tier unlocks."
---
**Category:** Broski / Gamification  
**Version:** 1.0  
**Rescued From:** [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) — `.claude/skills/level-progression/SKILL.md`

> Trigger when: "level X", "level up", "what's next", "level 18", "constellation", Brain progression status.

---

## 🏆 Level Tracker

```
✅ 1–8   Vault scaffold + plugins + PARA structure
✅ 9     GitHub bridge (4hr polling)
✅ 10    Vault Immortal (Obsidian Git auto-commit, 10min)
✅ 11    BROski$ Coin Tracker (Dataview widget)
✅ 12    Hyperfocus CSS Modes (Focus / Calm / Hyper)
✅ 13    Morning Briefing AI                  ✅ May 7
✅ 14    GitHub Webhooks real-time            ✅ May 7
✅ 15    HyperAgent MCP Bridge                ✅ May 7
✅ 16    Focus Tracker + Analytics            ✅ May 7
✅ 17    HyperSplit Task Decomposition        ✅ May 7
⏳ 18    AI Distraction Filter (wired to focus sessions)  ← NEXT
⏳ 19    DifficultyDial + Dynamic XP
⏳ 20    THE HYPER BRAIN Constellation (MCP mesh + RAG)
```

---

## ⏳ Level 18 — What To Build Next

Code DONE: `ai_distraction_filter.py` exists. **Needs wiring into focus sessions.**

1. In `focus_tracker.py` `/focus/start` — register session ID + intensity
2. When `/distraction/report` called during session — increment distraction count
3. When `/focus/end` — include distraction summary in session log
4. Cross-correlate in `/analytics/weekly` (focus quality score)

Estimate: **1–2 hrs**.

---

## ⏳ Level 19 — DifficultyDial + Dynamic XP

XP per task currently flat. Level 19 = task XP scales with HyperSplit depth, time estimate, distractions. DifficultyDial = UI knob in Dashboard.

## ⏳ Level 20 — THE HYPER BRAIN Constellation 🌌

Full MCP mesh (Brain ↔ V2.4 ↔ Course ↔ Pets ↔ SDK) + RAG over the vault. Any agent in the ecosystem can query the vault and get contextual answers.

---

## 🔄 When A Level Ships

1. Update `CLAUDE_CONTEXT.md` — change ⏳ to ✅, add date
2. Update `CLAUDE.md` — same
3. Update this skill's table
4. If new endpoints added → update `HYPER_BRAIN_MODULES_v1.md`
5. Commit + Obsidian Git auto-pushes

---

## ⚠️ Hard Rules

- One level at a time — finish 18 before starting 19
- `CLAUDE_CONTEXT.md` = source of truth for level status
- Code "done but not wired" = ⏳, NOT ✅
- `docker-compose.hyper-brain.yml` at root (not `docker/`)

*Rescued from BROski-Obsidian-Brain-for-HyperFocus-z0ne — HYPER-SKILLs Vault by WelshDog 🐕⚡*
