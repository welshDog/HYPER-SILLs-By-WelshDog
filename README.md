# 🧠 HYPER-SILLs By WelshDog
### *The Neurodivergent-First AI Skills Vault*

> **120 battle-tested skills. One MCP server. Zero friction.**
> Built for ADHD brains, hyperfocus zones, and autonomous AI agents.

---

## ⚡ What Is This?

HYPER-SILLs is a living vault of **AI agent skills** — structured knowledge packs that any Claude, MCP-compatible agent, or AI IDE can load and execute instantly.

Think of it as a **skill OS** for your AI stack:
- 🔌 Drop into Claude Code via the plugin marketplace
- 🌐 Serve over MCP — agents discover, query, and load skills on demand
- 📦 Ship as OCI artifacts — pin exact skill versions in production
- 🧠 Learns from your usage — `.skill-memory/` tracks what you reach for

---

## 🚀 Quick Start

### Claude Code (Recommended)
```bash
/plugin marketplace add welshDog/HYPER-SILLs-By-WelshDog
/plugin install hyper-sills-vault
```
Then just use `/skill-find`, `/skill-load`, or `/skill-recommend` in any Claude session.

### MCP Server
```bash
git clone https://github.com/welshDog/HYPER-SILLs-By-WelshDog
cd HYPER-SILLs-By-WelshDog
pip install -e .
python mcp_server.py
```

### Skills Query (CLI)
```bash
python skills_query.py "docker agent"
python skills_query.py --category agents
python skills_query.py --category dev
```

---

## 📦 The Vault — 120 Skills, 6 Categories

> Categories match the live MCP server exactly — use these names with `semantic_search(query="...", category="agents")`.

| Category | Count | Example Skills | Key IDs |
|---|---|---|---|
| 🤖 `agents` | **51** | Swarm orchestration, nested agents, decision trees, guardrails, lifecycle state machines | HS-007, HS-075, HS-085, HS-099, HS-131 |
| 🛠️ `dev` | **39** | FastAPI standards, pre-commit checks, OCI skill ship, plugin forge, MCP resources, infra references | HS-074, HS-076, HS-128, HS-129, HS-130 |
| 🐳 `hypercode` | **12** | Sacred rules, master constitution, ecosystem inventory, launch commander, integrations map | HS-030, HS-031, HS-046, HS-059, HS-065 |
| 🧠 `broski` | **7** | ND-first error messages, body-double mode, PARA vault structure, analogy arsenal, level progression | HS-034, HS-036, HS-069, HS-107 |
| 🌐 `web3` | **7** | BROskiPets integration, dNFT on-chain portfolio, pet rarity rolls, species power mapping, XP triggers | HS-052, HS-053, HS-055, HS-056, HS-058 |
| 🎬 `youtube` | **4** | Analytics debugger, A/B thumbnail duels, Shorts repurposing, data-driven script loop | HS-127, HS-132, HS-133, HS-134 |

> **Note:** Skill IDs are non-contiguous by design — assigned at creation time, not by category block. Use `skills_query.py` or `semantic_search` to find skills rather than guessing ID ranges.

---

## 📦 Curated Packs

| Pack | Skills | Best For |
|---|---|---|
| 🐝 Agent Builder Pack | 51 skills | Building + deploying autonomous agents |
| 💻 ND-Friendly Coding Pack | 41 skills | Dev workflows built for neurodivergent flow |
| 🎬 YouTube Growth Pack | 4 skills | Data-driven content creation |

---

## 🔍 Find Skills Fast

```bash
# Semantic search (zero dependencies — local TF-IDF)
python scripts/search_skills.py "redis rate limiting"

# Via MCP tool (category names: agents, dev, broski, youtube)
semantic_search(query="discord bot cog")
semantic_search(query="ND error messages", category="broski")

# Trigger engine — auto-suggests packs from your current context
python scripts/trigger_engine.py
```

---

## 🏗️ Architecture

```
HYPER-SILLs-By-WelshDog/
├── agents/          ← 51 agent skill packs
├── dev/             ← 39 dev + DevOps skills
├── hypercode/       ← 12 ecosystem/infra constitution skills
├── broski/          ← 7 ND-first focus tools
├── web3/            ← 7 dNFT / BROskiPets / on-chain skills
├── youtube/         ← 4 YouTube creator skills
├── packs/           ← Curated skill bundles (manifest.yaml)
├── plugins/         ← Claude Code plugin definitions
├── scripts/         ← Linter, embed, memory, export tools
├── templates/       ← Skill authoring templates
├── .skill-memory/   ← Usage learning loop
├── .claude-plugin/  ← Claude Code marketplace integration
├── mcp_server.py    ← MCP server (tools + resources)
├── skills_query.py  ← CLI skill finder
└── skills-registry.json  ← Full vault index (~60KB, 120 skills)
```

---

## 🧠 ND-First Features

Built for ADHD, Dyslexia, and Autistic builders:

- **Body-double mode** — `python scripts/body_double.py` — presence, nudges, session logging
- **Mercy messages** — no-blame "skill not found" responses, always a fallback path
- **Progress tracker** — `progress-tracker.yaml` tracks your skill journey
- **Skill constellation** — visual Mermaid map of your skill graph (`docs/skill-map.md`)
- **Learning loop** — `.skill-memory/` remembers what you use, surfaces it next time

---

## 📡 MCP Resources

Skills are available as MCP Resources following the SEP-2640 standard:

```
skills://index          ← Full vault index
skill://HS-128          ← Individual skill by ID
```

---

## 🛠️ Skill Lifecycle

Every skill has a status: `DRAFT → REVIEW → ACTIVE → DEPRECATED → ARCHIVED`

Run the linter before committing:
```bash
python scripts/skill_linter.py
# Target: 0 errors ✅ (currently clean — v3.0)
```

---

## 📤 Export & Distribute

```bash
# Export to agentskills.io / Claude SKILL.md format
python scripts/export_claude_skills.py --format skill-md --category broski

# Export a full pack
python scripts/export_claude_skills.py --pack focus-toolkit

# OCI artifacts published automatically on GitHub release
# See: .github/workflows/publish-skills.yml
```

---

## 📋 Changelog Highlights

| Version | Date | What Dropped |
|---|---|---|
| **v3.1** | 2026-06-28 | Registry reconciliation — promoted 24 stranded `hypercode/` + `web3/` + `dev/` skills into the registry, +2 categories → **120 skills, 6 categories** |
| v3.0 | 2026-06-28 | Claude Code plugin, semantic search, ND-UX tools, OCI publish, 7 new skills (96 total) |
| v2.2 | 2026-06-01 | Linter clean — 0 errors |
| v2.1 | 2026-05-26 | GoS cross-reference validation |
| v2.0 | 2026-05-20 | Graph-of-Skills (GoS) layer |
| v1.0 | 2026-05-01 | Initial vault + linter |

---

## 🤝 Built By

**Lyndz Williams ([@welshDog](https://github.com/welshDog))** — Llanelli, South Wales 🏴󠁧󠁢󠁷󠁬󠁳󠁥

Part of the **Hyperfocus Zone** ecosystem — the world's first neurodivergent-first autonomous AI infrastructure platform.

🔗 [HyperCode-V2.4](https://github.com/welshDog/HyperCode-V2.4) · [HyperAgent-SDK](https://github.com/welshDog/HyperAgent-SDK) · [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) · [BROskiPets-LLM-dNFT](https://github.com/welshDog/BROskiPets-LLM-dNFT) · [Hyper-Vibe-Course](https://github.com/welshDog/Hyper-Vibe-Coding-Course)

---

*Built with hyperfocus ⚡ — ADHD + Dyslexia + Autistic. The neurodivergent brain is the superpower.*
