# HS-013 — 🌅 DAWN HERALD — Morning Briefing AI

---
skill_id: HS-013
hero_name: "DAWN HERALD"
emoji: "🌅"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-011  # MIND BLOCKS — module map needed to call the briefing endpoint
  - HS-016  # BRAIN PRIMER — brain ecosystem context required
provides:
  - briefing-generation
  - daily-ai-summary
  - vault-briefing-note
  - port-8100-briefing-trigger
related:
  - HS-020  # HERALD'S SCROLL — morning briefing manifest
  - HS-124  # FOCUS HAWK — focus stats included in briefing
  - HS-021  # VAULT SYNC — brain sync often follows the briefing
graph_notes: "Trigger reference for the morning briefing AI — curl endpoint, sections, output path on port 8100."
---
**Category:** Agents / Brain Modules  
**Version:** 1.0  
**Rescued From:** [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) — `.claude/skills/morning-briefing-ai/SKILL.md`

> Trigger when: "briefing", "morning briefing", "generate briefing", "daily summary", "/briefing", "auto-fire briefing", or extending the briefing AI.

---

## ⚡ Trigger A Briefing

```powershell
curl -X POST http://localhost:8100/briefing/generate
# → drops markdown note into HYPERFOCUS_ZONE/00-Inbox/Briefings/<YYYY-MM-DD>.md
# → returns: { "status": "ok", "path": "<vault path>", "summary": "<first 200 chars>" }
```

Same day = overwrites (regenerate is expected default).

---

## 📋 Briefing Sections

```markdown
## Overnight GitHub
- Repo: N issues opened, N PRs merged

## Today's Focus
- Top 3 tasks from 01-Projects/* with status: active + priority: high
- Estimated focus blocks needed

## Yesterday's Wins
- Focus hours + quality

## Blockers / Watch
- Key pending items

## Energy Mode Suggested
hyper-mode / focus-mode / calm-mode
```

---

## 🌅 Daily Cron — 3 Options

**Option A: Windows Task Scheduler (recommended)**
```powershell
$action = New-ScheduledTaskAction -Execute 'curl.exe' -Argument '-X POST http://localhost:8100/briefing/generate'
$trigger = New-ScheduledTaskTrigger -Daily -At 7am
Register-ScheduledTask -TaskName "HyperBrain-MorningBriefing" -Action $action -Trigger $trigger
```

**Option B: Cron in container** — add `briefing-cron` service to `docker-compose.hyper-brain.yml`

**Option C: Manual** — phone alarm + run curl. ADHD-friendly, low ceremony.

---

## 🔧 Required Env

```env
OBSIDIAN_VAULT_PATH=H:/BROski-Obsidian-Brain-for-HyperFocus-z0ne/HYPERFOCUS_ZONE
GITHUB_PAT=github_pat_xxx
LLM_ENDPOINT=<URL of LLM>
LLM_MODEL=<model name>
```

---

## 🚑 Common Failures

| Symptom | Fix |
|---|---|
| 500 on `/briefing/generate` | Check `LLM_ENDPOINT` connectivity |
| File written but empty | LLM returned empty — check container logs |
| GitHub section missing | Check `GITHUB_PAT` scope (`repo` required) |
| Briefing fires twice | Check Task Scheduler / cron config |

---

## ⚠️ Hard Rules

- Edit `morning_briefing_ai.py` at **repo root** — NOT `scripts/`
- Briefing path is `00-Inbox/Briefings/` — sacred
- Date format `YYYY-MM-DD` for filename — sortable
- LLM must be configured — without `LLM_ENDPOINT` briefings fail

*Rescued from BROski-Obsidian-Brain-for-HyperFocus-z0ne — HYPER-SKILLs Vault by WelshDog 🐕⚡*
