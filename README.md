# 🧠 HYPER-SILLs By WelshDog
### *The Neurodivergent-First AI Skills Vault*

> **96 battle-tested skills. One MCP server. Zero friction.**
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
python skills_query.py --category broski
```

---

## 📦 The Vault — 96 Skills Across 10 Domains

| Domain | Skills | Highlights |
|---|---|---|
| 🤖 Agents | HS-001 → HS-030 | Swarm orchestration, nested agents, observable ops |
| 🐳 HyperCode | HS-031 → HS-060 | Docker, Kubernetes, 48-container deployments |
| 🧠 BROski | HS-061 → HS-080 | ADHD tools, body-double mode, focus systems |
| 🌐 Web3 | HS-081 → HS-100 | dNFTs, Solidity, on-chain agent triggers |
| 🎬 YouTube | HS-128 → HS-134 | Thumbnail duels, Shorts alchemy, signal-to-script |
| 🔌 Plugins | HS-128 PLUGIN FORGE | Claude Code plugin authoring |
| 🚢 OCI | HS-130 OCI SKILL SHIP | Ship skills as container artifacts |
| 🕸️ MCP | HS-129 SKILLS-OVER-MCP | Skills-over-MCP / SEP-2640 standard |
| 🐝 Swarm | HS-131 NESTED SWARM | Multi-agent nested orchestration |
| 📊 Dev | HS-113 → HS-127 | Metrics contracts, linting, semantic versioning |

---

## 🔍 Find Skills Fast

```bash
# Semantic search (zero dependencies — local TF-IDF)
python scripts/search_skills.py "redis rate limiting"

# Via MCP tool
semantic_search(query="discord bot cog")

# Trigger engine — auto-suggests packs from your current context
python scripts/trigger_engine.py
```

---

## 🏗️ Architecture

```
HYPER-SILLs-By-WelshDog/
├── agents/          ← Agent skill packs
├── broski/          ← ND-first focus tools
├── content/         ← Content creation skills
├── dev/             ← Dev + DevOps skills
├── hypercode/       ← Docker/K8s infrastructure
├── packs/           ← Curated skill bundles (manifest.yaml)
├── plugins/         ← Claude Code plugin definitions
├── scripts/         ← Linter, embed, memory, export tools
├── templates/       ← Skill authoring templates
├── web3/            ← Blockchain + dNFT skills
├── youtube/         ← YouTube creator skills
├── mcp_server.py    ← MCP server (tools + resources)
├── skills_query.py  ← CLI skill finder
└── skills-registry.json  ← Full vault index (45KB)
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
# Target: 0 errors ✅ (currently clean — v2.2)
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
| **v3.0** | 2026-06-28 | Claude Code plugin, semantic search, ND-UX tools, OCI publish, 7 new skills |
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
