# 🎯 Agent Manifest: FOCUS_TRACKER
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
