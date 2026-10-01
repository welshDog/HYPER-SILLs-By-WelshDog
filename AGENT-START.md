# 🦸 AGENT-START.md — HYPER-SILLs Skills Vault Boot File
> **For ANY AI, agent, or human working with the HYPER-SILLs skills vault.**
> Read this FIRST. Every session. No exceptions.
> Built by @welshDog — 2026-06-01 · last corrected 2026-10-01

---

## ⚡ WHAT THIS REPO IS

This is the **skills vault** for the entire HyperFocus Z0ne ecosystem.
- **123 hero-named skills, 6 categories** (Marvel naming convention — never rename them)
- Live over MCP at `hyper-sills-by-welshdog-production.up.railway.app/mcp`, and installable
  as a Claude Code plugin (`/plugin install hyper-sills-vault`) — 12 tools either way
- Used by: Claude Code, Cursor, Gemini CLI, custom agents, Perplexity
- Acts as the **6th core infrastructure repo** — treat it like a service, not docs
- Skills are loaded by agents at runtime to gain domain expertise

---

## 📋 STEP 1 — READ THESE FILES FIRST

```
1. WHATS_DONE.md                                     ← single source of truth, always wins
2. docs/handovers/NEXT_SESSION_HANDOVER_[latest].md   ← live state from the last session
3. vault-index.md                                     ← full skills map, every folder
4. SKILL.md                                           ← how to write + load a skill
5. skills-registry.json                               ← machine-readable registry
```

---

## 🗂️ VAULT FOLDER MAP

| Folder | What lives here | Load when... |
|---|---|---|
| `agents/` (51) | AI agent orchestration, swarms, MCP, tool use | Building/debugging agents |
| `dev/` (42) | Docker, FastAPI, React/Vite, Python, infra | Building any dev feature |
| `hypercode/` (12) | HyperCode-V2.4 specific skills — services, runbooks | Working on core platform |
| `broski/` (7) | BROski$ economy, Discord bot, token rewards, ND-first UX | Working on BROski$ or Discord |
| `web3/` (7) | BROskiPets, dNFT, on-chain skills | Working on web3/BROskiPets |
| `youtube/` (4) | YouTube strategy, scripts, thumbnails, shorts | Creating YouTube content |
| `content/` | Placeholder — empty (`.gitkeep` only), not a live category | — |
| `scripts/` | Python automation tools for the vault itself | Vault maintenance |
| `templates/` | Skill templates, YAML frontmatter specs | Creating new skills |
| `packs/` | Curated skill-pack manifests with auto-load triggers | Bundling skills for a goal |
| `.skill-memory/` | Usage logging / learning loop | Vault maintenance |
| `plugins/` | Claude Code plugin bundle (self-contained MCP server copy) | Publishing the plugin |
| `docs/` | Internal vault documentation + session handovers | Understanding vault architecture |
| `output/` | Generated outputs from scripts | Reference only |

> The 6 **live** categories are `agents`, `dev`, `hypercode`, `broski`, `web3`, `youtube` —
> these match `category:` in skill frontmatter and the MCP server's `/health` response exactly.
> `content/` exists on disk but holds no skills; don't file new skills there.

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

### For export to Claude Code / Agent Skills format
```bash
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

## 🔬 SKILL YAML FRONTMATTER (Graph-of-Skills schema — matches `templates/SKILL_TEMPLATE.md`)

Every skill MUST include this at the top (this is the real schema the linter and MCP
server parse — copy `templates/SKILL_TEMPLATE.md`, don't hand-roll it):

```yaml
---
skill_id: HS-NNN
hero_name: "HERO NAME"
emoji: "🦸"
version: v1.0.0  # semver vMAJOR.MINOR.PATCH
status: ACTIVE   # DRAFT | REVIEW | ACTIVE | DEPRECATED | ARCHIVED
category: agents  # agents | dev | hypercode | broski | web3 | youtube
depends_on:
  - HS-XXX  # Skill this one builds on, with a reason comment
provides:
  - feature-slug-one
related:
  - HS-YYY  # Lateral reference — not a hard dependency
graph_notes: "One sentence: where this skill sits in the graph and what it connects."
---
```

> 💡 The `depends_on`, `provides`, `related` fields power the **Skill Graph** (GoS). The
> pre-push linter validates them — see `scripts/skill_linter.py`.

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

> After retrofitting, run: `python scripts/skill_linter.py` to check all frontmatter is valid.

---

## 📈 VAULT HEALTH METRICS (Check Monthly)

- Total skills + dependency graph validity: `python scripts/skill_linter.py` (also runs on
  every pre-push via `scripts/git_pre_push_lint.sh`)
- Server import smoke test: `python scripts/smoke_test.py`
- Registry drift (skill files vs `skills-registry.json`): `python scripts/generate_registry.py`
  regenerates it from disk — diff before committing
- Vault index drift: `python scripts/update_vault_index.py`

---

## 🏁 SESSION END CHECKLIST

- [ ] New skills added to `skills-registry.json` ✔️
- [ ] `vault-index.md` updated ✔️
- [ ] All new skills have `depends_on` / `provides` / `related` frontmatter ✔️
- [ ] If `mcp_server.py` changed: ran `python scripts/build_plugin.py` and committed
      `plugins/hyper-sills-vault/vault/` so the marketplace plugin isn't left stale ✔️
- [ ] `WHATS_DONE.md` updated with what actually shipped ✔️
- [ ] `docs/handovers/NEXT_SESSION_HANDOVER_[DATE].md` created + pushed ✔️
- [ ] All changes committed + pushed, **and the Railway deploy confirmed SUCCESS +
      `/health` checked live** (a merged PR is not a live PR — see DEPLOY.md) ✔️
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
