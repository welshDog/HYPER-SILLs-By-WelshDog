# 🔄 Hyper Skill: OBSIDIAN_BRAIN_SYNC_v1
**Category:** Agents / Brain Maintenance
**Version:** 1.0
**Rescued From:** [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) — `.agents/skills/obsidian-brain-sync/SKILL.md`

> Trigger when: updating brain docs, syncing sprint plans, adding new knowledge nodes, keeping the meta-layer up to date after a sprint.

---

## ⚡ After Every Sprint — Update Flow

1. Open `WHATS_DONE.md` → add new wins at the top
2. Open `CLAUDE_CONTEXT.md` → update current sprint focus
3. If architecture changed → update `CLAUDE.md` architecture section
4. Commit with clear message:
```powershell
git commit -m "🧠 Brain sync: [what changed] — [date]"
```
5. Push to main

---

## 📋 Brain File Hierarchy

| File | Purpose |
|---|---|
| `CLAUDE.md` | Master brain — architecture, rules, container status |
| `CLAUDE_CONTEXT.md` | Current context snapshot for agents |
| `WHATS_DONE.md` | Milestone tracker — update after every win |
| `HYPER_ECOSYSTEM_PLAN_*.md` | Sprint + roadmap plans |

---

## 🆕 Adding A New Knowledge Node

1. Create `.md` file in relevant vault folder
2. Add frontmatter:
```yaml
---
tags: [ecosystem, sprint, pets, sdk, course]
created: YYYY-MM-DD
status: active
---
```
3. Link from `CLAUDE_CONTEXT.md` or relevant plan file

---

## ✅ Success Criteria

- All brain files reflect current system state
- No stale sprint goals in `CLAUDE_CONTEXT.md`
- `WHATS_DONE.md` shows latest milestone at top
- Vault is clean, linked, and agent-readable

---

## 📜 Sacred Rules

- Short sentences — no walls of text
- **Bold key info**
- PowerShell first for commands
- Bullet points over paragraphs

*Rescued from BROski-Obsidian-Brain-for-HyperFocus-z0ne — HYPER-SKILLs Vault by WelshDog 🐕⚡*
