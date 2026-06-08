# HS-124 — 🦅 FOCUS HAWK — Focus Tracker Manifest

---
skill_id: HS-124
hero_name: "FOCUS HAWK"
emoji: "🦅"
version: v1.0
category: agents
depends_on:
  - HS-016  # BRAIN PRIMER — brain ecosystem context required
  - HS-011  # MIND BLOCKS — module map needed to call the focus endpoint
provides:
  - focus-session-api
  - adhd-session-tracking
  - streak-scoring
  - focus-start-end-tools
related:
  - HS-017  # MIND CORE — brain core runs the focus tracker
  - HS-013  # DAWN HERALD — morning briefing includes focus stats
  - HS-093  # NIGHT TENDER — nightly loop evaluates focus data
graph_notes: "ADHD focus session tracker manifest — logs sessions, scores streaks; pairs with Brain Level 16 on port 8100."
---
**Category:** Agents / ADHD Tools
**Version:** 1.0.0
**Runtime:** Python
**Entrypoint:** `focus_tracker.py`
**MCP Compatible:** ❌ (direct API call)
**Rescued From:** [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) — `.agents/focus-tracker/manifest.json`

> ADHD focus session tracker — logs, scores, streaks. Pairs with Brain Level 16.

---

## 🛠️ Tools

### `start_session`
Start a new hyperfocus session.
```json
{ "task": "string", "duration_mins": "integer" }
```

### `end_session`
End session and log score.
```json
{ "session_id": "string" }
```

---

## ⚡ Quick Curl Usage

```powershell
# Start
curl -X POST http://localhost:8100/focus/start -H "Content-Type: application/json" -d '{"task": "Build skills", "intensity": "hyper"}'

# End
curl -X POST http://localhost:8100/focus/end -H "Content-Type: application/json" -d '{"notes": "Shipped 5 skills"}'

# Status
curl http://localhost:8100/focus/status
```

---

## 📂 Output
Logs to `05-Focus-Sessions/<date-time>.md` in vault.

## 🔗 Related
- `agents/HYPER_BRAIN_MODULES_v1.md` (HS-011)
- `broski/LEVEL_PROGRESSION_v1.md` (HS-012) — Level 16

*Rescued from BROski-Obsidian-Brain-for-HyperFocus-z0ne — HYPER-SKILLs Vault by WelshDog 🐕⚡*
