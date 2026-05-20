# 🧠 Hyper Skill: HYPER_BRAIN_MODULES_v1
**Category:** Agents / Brain API  
**Version:** 1.0  
**Rescued From:** [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) — `.claude/skills/hyper-brain-modules/SKILL.md`

> Trigger when: "brain module", "endpoint X not responding", "8100", "/focus", "/hypersplit", "/briefing", "module reference", or extending the Brain API.

---

## 🗺️ Module Map (all green May 7, 2026)

THE HYPER BRAIN v3.0 — 8 modules behind one FastAPI on `http://localhost:8100`. Container #30. Memory cap: 256MB.

| Module | File | Endpoints | Purpose |
|---|---|---|---|
| `focus_tracker` | `focus_tracker.py` | `/focus/start` `/focus/end` `/focus/status` `/focus/snapshot` | Track focus sessions → `05-Focus-Sessions/` |
| `ai_distraction_filter` | `ai_distraction_filter.py` | `/distraction/report` `/distraction/patterns` | Detect + log distractions |
| `hyper_split` | `hyper_split.py` | `/hypersplit` | Recursive task decomposition |
| `mcp_bridge` | `mcp_bridge.py` | `/mcp/status` `/mcp/query` | Bridge to HyperAgent MCP gateway (port 8820) |
| `analytics_engine` | `analytics_engine.py` | `/analytics/weekly` `/analytics/heatmap` | Focus analytics + reports |
| `github_webhook_server` | `github_webhook_server.py` | `/webhook/github` | GitHub issue/PR → vault notes real-time |
| `morning_briefing_ai` | `morning_briefing_ai.py` | `/briefing/generate` | AI daily briefing → `00-Inbox/Briefings/` |
| `session_snapshot` | (in `focus_tracker.py`) | `/focus/snapshot` | Snapshot active session |

---

## ⚡ Quick Reference Commands

```powershell
# Health check
curl http://localhost:8100/health
# → {"status":"hyper","level":20,"containers":30}

# Start focus session
curl -X POST http://localhost:8100/focus/start -H "Content-Type: application/json" -d '{"task": "Build skill", "intensity": "hyper"}'

# End session
curl -X POST http://localhost:8100/focus/end -H "Content-Type: application/json" -d '{"notes": "Shipped 5 skills"}'

# Generate briefing
curl -X POST http://localhost:8100/briefing/generate

# HyperSplit a task
curl -X POST http://localhost:8100/hypersplit -H "Content-Type: application/json" -d '{"task": "Build payment system", "depth": 3}'

# Weekly analytics
curl http://localhost:8100/analytics/weekly

# Focus heatmap
curl http://localhost:8100/analytics/heatmap
```

---

## 🚨 IRON RULE — Canonical Files

| Location | Status | Action |
|---|---|---|
| Root `*.py` (e.g. `focus_tracker.py`) | ✅ CANONICAL v3.0 | Edit these |
| `scripts/*.py` (9 stub files) | ❌ OLD STUBS | NEVER edit |
| `scripts/github_to_obsidian.py` | ✅ Real script | OK to edit |

**NEVER edit `scripts/*.py` stubs. Dockerfile copies root `.py` files.**

---

## 🐳 Bring The Brain Up

```powershell
cd H:\BROski-Obsidian-Brain-for-HyperFocus-z0ne
$env:OBSIDIAN_VAULT_PATH   = "H:/BROski-Obsidian-Brain-for-HyperFocus-z0ne/HYPERFOCUS_ZONE"
$env:GITHUB_WEBHOOK_SECRET = "<your secret>"
$env:GITHUB_PAT            = "github_pat_xxx"
docker network create app-net 2>$null
docker network create agents-net 2>$null
docker compose -f docker-compose.hyper-brain.yml up -d --build
curl http://localhost:8100/health
```

---

## 🔗 Related Skills
- `broski/LEVEL_PROGRESSION_v1.md` (HS-012)
- `agents/MORNING_BRIEFING_AI_v1.md` (HS-013)
- `broski/VAULT_PARA_STRUCTURE_v1.md` (HS-015)

*Rescued from BROski-Obsidian-Brain-for-HyperFocus-z0ne — HYPER-SKILLs Vault by WelshDog 🐕⚡*
