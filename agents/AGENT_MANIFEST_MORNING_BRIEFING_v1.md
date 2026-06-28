# HS-020 — 🌄 HERALD'S SCROLL — Morning Briefing Manifest

---
skill_id: HS-020
hero_name: "HERALD'S SCROLL"
emoji: "🌄"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-013  # DAWN HERALD — trigger reference for the briefing AI
  - HS-016  # BRAIN PRIMER — brain ecosystem context required
provides:
  - morning-briefing-api
  - daily-task-summary
  - briefing-manifest
related:
  - HS-124  # FOCUS HAWK — focus stats feed into the briefing
  - HS-021  # VAULT SYNC — brain sync often follows the morning briefing
graph_notes: "Daily AI briefing manifest — delivers tasks, energy, BROski$ summary each morning via the brain cluster."
---
**Category:** Agents / Daily Automation
**Version:** 1.0.0
**Runtime:** Python
**Entrypoint:** `morning_briefing_ai.py`
**MCP Compatible:** ❌ (direct API call)
**Rescued From:** [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) — `.agents/morning-briefing/manifest.json`

> Daily AI morning briefing — tasks, energy, BROski$ summary.

---

## 🛠️ Tools

### `get_briefing`
Generate today's morning briefing.
```json
{ "discord_id": "string" }
```

---

## ⚡ Quick Curl Usage

```powershell
curl -X POST http://localhost:8100/briefing/generate
# → drops to HYPERFOCUS_ZONE/00-Inbox/Briefings/<YYYY-MM-DD>.md
```

---

## 📂 Output
Drops markdown note in `00-Inbox/Briefings/<date>.md` with sections:
- Overnight GitHub activity
- Today's top 3 tasks
- Yesterday's wins
- Blockers / Watch
- Energy mode suggestion

## 🔗 Related
- `agents/MORNING_BRIEFING_AI_v1.md` (HS-013) — full deep dive
- `broski/LEVEL_PROGRESSION_v1.md` (HS-012) — Level 13

*Rescued from BROski-Obsidian-Brain-for-HyperFocus-z0ne — HYPER-SKILLs Vault by WelshDog 🐕⚡*
