# 📜 CHANGELOG — HYPER-SKILLs Vault

> *"Every version is a raid log. Every release is a victory."*

All notable changes to the HYPER-SKILLs vault are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows `vMAJOR.MINOR.PATCH` — major = vault milestone, minor = new skills batch, patch = fixes.

---

## [v1.0.0] — 2026-05-22 🏆 THE GREAT RESCUE

> *"72 heroes pulled from 86 repos, catalogued, named, and ready to deploy."*

This is the **founding release** of the HYPER-SKILLs Vault — the moment a scattered collection
of prompt patterns across Lyndz's entire GitHub constellation got rescued, hero-branded, and
shipped as a single deployable vault.

### 🦸 72 Skills Rescued

All 72 skills now live on disk as structured `.md` files, ready to copy and use:

| Category | Count | Highlights |
|---|---|---|
| `agents/` | 39 | THE SACRED SIX, SWARM CROWN, THE GRAND ROSTER, CRADLE-TO-GRAVE, HEALER'S CHORUS |
| `dev/` | 27 | SDK SOVEREIGN, REALITY ANCHOR, DREAM GUARD, SLOPE ORACLE, FETCH FORGE |
| `broski/` | 5 | THE AESTHETE, MERCY MESSAGE, THE RANK & THE NAME, THE FOUR DRAWERS, THE ASCENT |
| `youtube/` | 1 | SIGNAL HUNTER |

### 🏛️ Vault Infrastructure (NEW)

- **`README.md`** — Full upgrade: badges, 🚀 Start Here table, Skill Pack Bundles, Vault Quality section, contributing guide
- **`vault-index.md`** — Master tracking index: 72 rescued + 37 catalogued + 4 in progress, full raid log of 86 repos scanned
- **`templates/SKILL_TEMPLATE.md`** — Universal skill template with YAML frontmatter: `id`, `hero_name`, `category`, `version`, `last_updated`, `best_for`, `difficulty`, `estimated_time`, `tags`
- **`skills-registry.json`** — Machine-readable registry of all 72 rescued skills, auto-queryable by category, tag, and pack
- **`scripts/generate_registry.py`** — Registry generator: parses `vault-index.md` → outputs `skills-registry.json` automatically
- **`scripts/skill_linter.py`** — Vault quality linter: checks every skill `.md` for required frontmatter, sections, ID format, version format, date format, and file naming convention
- **`.github/workflows/skill-lint.yml`** — GitHub Action: auto-runs linter on every push/PR touching skill folders

### 📦 Skill Pack Bundles (NEW)

Four curated skill bundles introduced:
- 🎬 **YouTube Growth Pack** — Content creators scaling their channel
- 🤖 **Agent Builder Pack** — Devs building AI agent systems
- 🧠 **ND-Friendly Coding Pack** — ADHD/Dyslexia-first coders
- 🎨 **Design Audit Pack** — UI/UX designers

### 🦸 Hero Rebrand Complete

- All 72 rescued skills now carry **Marvel-style hero names** — power baked into every title
- Header convention standardised: `# HS-### — 🎯 HERO NAME — Descriptive Title`
- 25 legacy `Hyper Skill:` headers migrated to the new convention

### 🔍 Vault Raid Log (v1.0 era)

| Date | Event | Skills Added |
|---|---|---|
| Pre-May 2026 | Initial vault creation, HS-001 + HS-006→009 | 5 |
| May 2026 | BROski-Obsidian-Brain raid | HS-010→021 (+12) |
| May 2026 | HyperAgent-SDK raid | HS-022→029 (+8) |
| 20 May 2026 | 86-repo galaxy scan + HyperCode-V2.4 Bible deep-raid | HS-067→088 (+22) |
| 21 May 2026 | Roster + Life Plans Master raid | HS-089→097 (+9) |
| 21 May 2026 | Throttle-Agent Bible raid | HS-098→107 (+10) |
| 21 May 2026 | Claude's Favourites — session synthesis | HS-108→113 (+6) |
| 21 May 2026 | Full Hero Rebrand 🦸✨ | All 72 renamed |
| 22 May 2026 | v1.0 infrastructure push (linter, registry, README, template, CHANGELOG) | — |

### 📊 Stats at v1.0

| Metric | Count |
|---|---|
| Repos scanned | 86 |
| Skills rescued (file on disk) | **72** |
| Skills catalogued (pattern found, no file yet) | 37 |
| Skills in progress | 4 |
| Skill packs | 4 |
| GitHub Actions | 1 (Vault Linter) |
| Registry entries | 72 |

---

## 🗺️ What's Coming in v1.1

- [ ] Rescue catalogued skills HS-030→066 (37 patterns, no `.md` file yet)
- [ ] Apply universal template to all 72 existing skill files (frontmatter upgrade)
- [ ] Create `hypercode/` and `web3/` folders for pending skill categories
- [ ] Skill quality scores (clarity, reusability, ND-friendliness, output strictness)
- [ ] CHANGELOG auto-update step in GitHub Action

## 🗺️ What's Coming in v2.0

- [ ] Skill Runner CLI — list, filter, copy-to-clipboard
- [ ] Skill Cards static site (Astro or 11ty)
- [ ] Community submission flow — issue form + PR template for new skills
- [ ] Use-case Playbooks — "I want to build a YouTube channel", "I want to orchestrate agents"
- [ ] Prompt Linter — detects vague language, missing inputs, broken structure

---

*HYPER-SKILLs Vault — Built with Hyperfocus. Powered by BROski energy. 🧠🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
*Maintained by [@welshDog](https://github.com/welshDog) — Llanelli, Wales 🏴󠁧󠁢󠁷󠁬󠁳󠁧*
