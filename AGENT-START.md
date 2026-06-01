# 🦸 AGENT-START.md — HYPER-SILLs Skills Vault Boot File
> **For ANY AI, agent, or human working with the HYPER-SILLs skills vault.**
> Read this FIRST. Every session. No exceptions.
> Built by @welshDog — 2026-06-01 · v1.0

---

## ⚡ WHAT THIS REPO IS

This is the **skills vault** for the entire HyperFocus Z0ne ecosystem.
- **72+ hero-named skills** (Marvel naming convention — never rename them)
- Used by: Claude Code, Cursor, Gemini CLI, custom agents, Perplexity
- Acts as the **6th core infrastructure repo** — treat it like a service, not docs
- Skills are loaded by agents at runtime to gain domain expertise

---

## 📋 STEP 1 — READ THESE FILES FIRST

```
1. NEXT_SESSION_HANDOVER_[latest date].md   ← live state, ALWAYS wins
2. vault-index.md                           ← full skills map, every folder
3. SKILL.md                                 ← how to write + load a skill
4. skills-registry.json                     ← machine-readable registry
```

---

## 🗂️ VAULT FOLDER MAP

| Folder | What lives here | Load when... |
|---|---|---|
| `agents/` | AI agent orchestration, swarms, MCP, tool use | Building/debugging agents |
| `broski/` | BROski$ economy, Discord bot, token rewards | Working on BROski$ or Discord |
| `content/` | Course scripts, YouTube, storytelling, ND-first writing | Writing content or course modules |
| `dev/` | Docker, FastAPI, React/Vite, Python, infra | Building any dev feature |
| `hypercode/` | HyperCode-V2.4 specific skills — services, runbooks | Working on core platform |
| `youtube/` | YouTube strategy, scripts, thumbnails, shorts | Creating YouTube content |
| `scripts/` | Python automation tools for the vault itself | Vault maintenance |
| `templates/` | Skill templates, YAML frontmatter specs | Creating new skills |
| `docs/` | Internal vault documentation | Understanding vault architecture |
| `output/` | Generated outputs from scripts | Reference only |

---

## 🚀 STEP 2 — HOW TO LOAD A SKILL

### For AI agents (MCP / Claude Code / Cursor)
```bash
# Skills are auto-discoverable via skills-registry.json
# Point your MCP config at this repo root
# Or load individually by path
```

### For humans / manual load
```
1. Open vault-index.md
2. Find the skill by category or hero name
3. Open the skill file
4. Follow the STOP → WHY → HOW → WIN → NEXT structure
```

### For export to Claude Code
```bash
# Run the export script (when built)
python scripts/export_claude_skills.py --output ./output/claude_skills/
```

---

## 🦸 SKILL NAMING CONVENTION (SACRED — NEVER BREAK)

- All skills use **hero names** (Marvel / DC / anime convention)
- Examples: **THE SACRED SIX**, **IRON DOCKER**, **SPIDER-AGENT**, **CAPTAIN FASTAPI**
- The hero name IS the skill identity — renaming breaks all agent references
- New skills MUST follow the convention — check `SKILL.md` + `templates/`

---

## 📝 STEP 3 — CREATING A NEW SKILL

```
1. Copy template from templates/SKILL_TEMPLATE.md
2. Fill in YAML frontmatter (name, version, description, depends_on, provides, related)
3. Follow the 5-section structure:
   ┃ STOP   — plain English context BEFORE any tech
   ┃ WHY    — real-world use case (Netflix, Stripe, Uber refs)
   ┃ HOW    — step-by-step with ⏱️ time estimates
   ┃ WIN    — clear celebratable moment
   ┃ NEXT   — warm bridge to next skill
4. Place in correct folder (agents/, dev/, broski/, etc.)
5. Add entry to skills-registry.json
6. Update vault-index.md
7. Commit + push
```

---

## 🔬 SKILL YAML FRONTMATTER (v2.0 — Skill Graph Ready)

Every skill MUST include this at the top:

```yaml
---
name: "HERO-NAME-HERE"
version: 2
description: "One sentence. What does this skill teach an agent to do?"
category: "agents | broski | content | dev | hypercode | youtube"
author: "welshDog"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
depends_on:   # Skills that must be loaded BEFORE this one
  - "SKILL-NAME-A"
  - "SKILL-NAME-B"
provides:     # Capabilities this skill unlocks
  - "capability-one"
  - "capability-two"
related:      # Skills that complement this one (no hard dependency)
  - "SKILL-NAME-C"
tags:
  - "docker"
  - "fastapi"
---
```

> 💡 The `depends_on`, `provides`, `related` fields power the **Skill Graph** — the #1 upgrade from MASTERPLAN v1. Add them to ALL new skills and retrofit the top 10 priority skills first.

---

## 🔴 RULES YOU CANNOT BREAK

| Rule | Why |
|---|---|
| Never rename a hero-named skill | Breaks all agent references |
| `depends_on` + `provides` + `related` on ALL new skills | Powers the skill graph |
| Update `skills-registry.json` when adding a skill | Keeps MCP auto-discovery working |
| Update `vault-index.md` when adding a skill | Keeps the map accurate |
| `git fetch` / `git pull --ff-only` BEFORE any push | Auto-commits may be running |
| Nothing is done until committed + pushed | Standard rule, no exceptions |
| Never commit `.env` files | Secrets stay local |

---

## 🎯 PRIORITY SKILLS TO RETROFIT WITH GRAPH METADATA

These 10 are highest-traffic — retrofit `depends_on` / `provides` / `related` first:

| Priority | Skill Hero Name | Folder |
|---|---|---|
| 1 | THE SACRED SIX | `agents/` or `dev/` |
| 2 | Docker Skill | `dev/` |
| 3 | FastAPI Skill | `dev/` |
| 4 | Agent Orchestration | `agents/` |
| 5 | BROski$ Economy | `broski/` |
| 6 | Supabase Skill | `dev/` |
| 7 | Discord Bot Skill | `broski/` |
| 8 | Vite + React Skill | `dev/` |
| 9 | Course Content Skill | `content/` |
| 10 | YouTube Strategy | `youtube/` |

> After retrofitting, run: `python scripts/validate_skills.py` to check all frontmatter is valid.

---

## 📈 VAULT HEALTH METRICS (Check Monthly)

- Total skills: Check `skills-registry.json` entry count
- Skills with graph metadata: Run `python scripts/validate_skills.py --check-graph`
- Broken skill links: Run `python scripts/vault_linter.py`
- Skills missing from registry: Run `python scripts/sync_registry.py --dry-run`

---

## 🏁 SESSION END CHECKLIST

- [ ] New skills added to `skills-registry.json` ✔️
- [ ] `vault-index.md` updated ✔️
- [ ] All new skills have `depends_on` / `provides` / `related` frontmatter ✔️
- [ ] `NEXT_SESSION_HANDOVER_[DATE].md` created + pushed ✔️
- [ ] All changes committed + pushed ✔️
- [ ] Tell Lyndz the ONE next task (one sentence) ✔️
- [ ] 🎉 Celebrate the wins — "Nice one BROski♾️!"

---

## 🔗 LINKED ECOSYSTEM FILES

- Full ecosystem boot: [`github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne/AGENT-START.md`](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne/blob/main/AGENT-START.md)
- Skills masterplan: `HYPER_SKILLs_POWER_UPGRADE_MASTERPLAN_v1.md`
- Skills template: `templates/SKILL_TEMPLATE.md`
- Full vault map: `vault-index.md`

---

> 🐶♾️ Built by @welshDog · Llanelli, Wales
> *"Stop apologising for your brain. Start building."*
