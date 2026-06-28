# HS-015 — 🗂️ THE FOUR DRAWERS — Vault PARA Structure

---
skill_id: HS-015
hero_name: "THE FOUR DRAWERS"
emoji: "🗂️"
version: v1.0.0
category: broski
depends_on:
  - none  # root vault structure — no prerequisites
provides:
  - para-vault-structure
  - projects-areas-resources-archive
  - knowledge-filing-system
related:
  - HS-021  # VAULT SYNC — sync workflow targets the PARA structure
  - HS-010  # THE AESTHETE — vault structure follows design principles
graph_notes: "PARA knowledge organisation for the BROski vault — the filing system that keeps 1000+ notes findable without a search."
---
**Category:** Broski / Knowledge Management  
**Version:** 1.0  
**Rescued From:** [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) — `.claude/skills/vault-para-structure/SKILL.md`

> Trigger when: "where does this go", "file this note", "organize", "PARA", "vault structure", "create a note", vault hygiene.

---

## 🗂️ The Vault Tree (PARA + extensions)

```
HYPERFOCUS_ZONE/               ← OPEN THIS in Obsidian (NOT repo root)
├── 00-Inbox/                  # New stuff, captures, AI drops
│   ├── GitHub/                # Auto-synced GitHub issues + PRs
│   ├── Briefings/             # morning_briefing_ai.py output
│   └── AI-Capture/            # Voice → Whisper → notes (future)
├── 01-Projects/               # Active builds
│   ├── HyperCode-V2.4/
│   ├── HyperAgent-SDK/
│   ├── Hyper-Vibe-Coding-Course/
│   └── BROskiPets-LLM-dNFT/
├── 02-Areas/                  # Ongoing responsibilities
│   ├── Health/
│   ├── Admin/
│   ├── DevOps/
│   └── Focus-Analytics/       # analytics_engine.py output
├── 03-Resources/              # Reference material
│   ├── Economy/               # BROski$ ledger snapshots
│   ├── Snippets/              # Reusable code blocks
│   ├── Agent-YAMLs/           # HyperAgent manifests
│   └── MCP/                   # MCP config templates
├── 04-Archive/                # Done + retired
├── 05-Focus-Sessions/         # focus_tracker.py output
├── 06-AI-Context/             # RAG chunks, prompt library
├── 07-Streaks-Achievements/   # XP, streak recovery, badges
├── 99-Templates/              # Daily, Project, Task, Briefing, Session
└── Hub/                       # Dashboard + Focus Command Center
```

---

## 📌 Sacred Placement Rule

**Notes NEVER go in repo root or vault root. Every note has exactly one correct folder.**

| Note type | Lives in |
|---|---|
| New idea / capture | `00-Inbox/` |
| GitHub issue/PR | `00-Inbox/GitHub/<repo>/` |
| Daily briefing | `00-Inbox/Briefings/<date>.md` |
| Active project doc | `01-Projects/<project-name>/` |
| Health log, admin | `02-Areas/<area>/` |
| Code snippet, reference | `03-Resources/<topic>/` |
| Completed project | `04-Archive/<project>/` |
| Focus session log | `05-Focus-Sessions/<date-time>.md` |
| LLM context chunk | `06-AI-Context/<topic>/` |
| XP / achievement | `07-Streaks-Achievements/` |
| Reusable template | `99-Templates/` |
| Dashboard widget | `Hub/Dashboard.md` |

---

## 📝 Frontmatter Standard

```yaml
---
created: 2026-05-08
tags: [project, hypercode, sprint-10n]
status: active        # active | parked | done | archived
project: HyperCode-V2.4
priority: high        # low | medium | high
---
```

---

## 🚨 Common Mistakes

| Wrong | Right |
|---|---|
| Note in vault root | Move to `00-Inbox/` first |
| Project doc in `02-Areas/` | Active = `01-Projects/`. Areas = no end date |
| Completed project in `01-Projects/` | Move to `04-Archive/` |
| Notes in repo root | Move inside `HYPERFOCUS_ZONE/` |

---

## ⚠️ Hard Rules

- NEVER place notes in repo root — always inside `HYPERFOCUS_ZONE/`
- NEVER place notes in vault root — always in a numbered folder
- Active projects = `01-`. Ongoing areas = `02-`. Don't confuse them
- `HYPERFOCUS_ZONE/` is the Obsidian vault path — open THIS in Obsidian

*Rescued from BROski-Obsidian-Brain-for-HyperFocus-z0ne — HYPER-SKILLs Vault by WelshDog 🐕⚡*
