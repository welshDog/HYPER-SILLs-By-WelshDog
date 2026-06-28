
# HYPER-SKILLs POWER UPGRADE MASTERPLAN v1.0

> *"A skill unused is a skill wasted. A skill undiscoverable is a skill that doesn't exist."*
>
> **Target**: `welshDog/HYPER-SILLs-By-WelshDog` | **120 rescued skills · 6 categories** *(reconciled 2026-06-28; was 72 rescued · 37 catalogued at research time)*
> **Research Date**: 2026-06-01 | **Sources**: 25+ papers, repos, protocols, frameworks

---

## TL;DR — The 7 Power Moves (Do These First)

| Priority | Power Move | Impact | Effort |
|----------|-----------|--------|--------|
| 1 | **MCP Server Mode** — Expose skills via Model Context Protocol | Any MCP-compatible agent can discover + use skills instantly | Medium |
| 2 | **Skill Graph (GoS)** — Add `depends_on`/`prereq` to YAML frontmatter; build dependency-aware retrieval | +25% reward, -57% tokens (per Graph-of-Skills paper) | Low |
| 3 | **Vector Search Layer** — Embed all skills; semantic retrieval over hero names + descriptions | Find skills by describing the problem, not memorizing IDs | Medium |
| 4 | **Claude Code Format Bridge** — Dual-format output: your format + standard `SKILL.md` | HYPER-SKILLs work in Claude Code, Cursor, Codex CLI automatically | Low |
| 5 | **Auto-Load Skill Packs** — Pack manifest with trigger conditions; auto-inject when relevant | Skills load themselves based on context, not manual copy-paste | Medium |
| 6 | **Session Memory Integration** — Agent remembers which skills you used, learns your patterns | Skills get smarter the more you use them | Medium |
| 7 | **ND-First Skill UI** — Visual skill map, dopamine progress tracker, body-double mode | Lean into what makes HYPER-SKILLs unique for ADHD brains | High |

---

## Table of Contents

1. [Current State Analysis](#1-current-state-analysis)
2. [The Skill Graph Layer (GoS)](#2-the-skill-graph-layer-gos)
3. [MCP Server Integration](#3-mcp-server-integration)
4. [Vector Search & Semantic Retrieval](#4-vector-search--semantic-retrieval)
5. [Claude Code / Agent Skills Format Bridge](#5-claude-code--agent-skills-format-bridge)
6. [Auto-Loading Skill Packs with Triggers](#6-auto-loading-skill-packs-with-triggers)
7. [Agent Memory & Learning Loop](#7-agent-memory--learning-loop)
8. [Obsidian Knowledge Graph Integration](#8-obsidian-knowledge-graph-integration)
9. [ND-First UX Power-Up](#9-nd-first-ux-power-up)
10. [Skill Distribution & Versioning](#10-skill-distribution--versioning)
11. [Implementation Roadmap](#11-implementation-roadmap)
12. [References](#12-references)

---

## 1. Current State Analysis

### What's Already Working (Don't Break These)

Your repo has **exceptional bones**. Here's what's genuinely impressive:

| Feature | Quality | Notes |
|---------|---------|-------|
| **Hero Naming Convention** | Best-in-class | Marvel-style names make skills memorable and discoverable. This is a genuine innovation — don't lose it. |
| **YAML Frontmatter + Legacy Dual Format** | Smart pragmatic | The linter handles both old `# HS-NNN` headers and new YAML frontmatter. Smooth migration path. |
| **Vault Linter (CI/CD)** | Production-grade | Automated quality checks on every push. Required fields, date validation, naming conventions. |
| **Auto-Rescue Pipeline** | Forward-thinking | Nightly extraction from source repos with PR workflow. This is enterprise-grade skill harvesting. |
| **Hyper Brain Ops CLI** | Real infrastructure | Docker health checks, GitHub sync, Discord reporting, vault auto-commit. This is a genuine ops system. |
| **Wikilink Cross-References** | Foundational for graphs | `[[HS-NNN]]` links between skills are natural edges. You've been building a graph without knowing it. |
| **Skill Packs** | Good bundling | Pre-curated combos for common goals. Could be more dynamic. |
| **ND-First Design Ethos** | Unique differentiator | "Stop apologising for your brain" — this positioning is powerful and underserved. |

### What's Holding You Back

| Problem | Impact | Evidence |
|---------|--------|----------|
| **No skill dependencies declared** | Agents miss prerequisite skills | HS-098 (6 Laws) references HS-085 (Guardrails) but this isn't machine-readable. The Graph-of-Skills paper (April 2026) proved this causes a "prerequisite gap" that kills agent performance. |
| **Manual copy-paste usage** | High friction, low adoption | Users must find skill → open file → copy prompt → paste → fill variables. Modern agents (Claude Code, Cursor) auto-load skills contextually. |
| **No semantic search** | Discovery bottleneck | Finding skills requires knowing the hero name or ID. With 72+ skills, this doesn't scale to 200+. |
| **Isolated from MCP ecosystem** | Missing the biggest platform shift | MCP (Model Context Protocol) is becoming the USB-C for AI tools. Anthropic, OpenAI, Google all support it. Your skills aren't accessible via MCP. |
| **No usage analytics** | Flying blind | You don't know which skills are used most, which are never triggered, where users get stuck. |
| **Static skills** | No learning | Skills don't improve from usage. Every session starts from zero. |
| **Category imbalance** | 39 agents vs 1 YouTube | The `youtube/` category is dramatically under-represented given BROski's video-first ecosystem. |

---

## 2. The Skill Graph Layer (GoS)

### The Insight

The [Graph-of-Skills paper](https://arxiv.org/abs/2604.05333) (UPenn/CMU/Brown, April 2026) proved that **structural retrieval beats semantic retrieval** for skill libraries. Your skills already have `[[HS-NNN]]` wikilinks — these are natural graph edges. You just need to make them machine-readable.

### Key Finding from the Paper

> On a 1,000-skill benchmark, GoS achieved **+25.55% reward** while **reducing tokens by 56.72%** vs loading all skills. It consistently outperformed both flat loading and simple vector retrieval across Claude Sonnet 4.5, GPT-5.2 Codex, and MiniMax M2.7.

### What to Add

#### 2.1 Enhanced YAML Frontmatter with Dependencies

```yaml
---
id: HS-100
hero_name: "CRADLE-TO-GRAVE"
category: agents
version: v1.0
last_updated: 2026-05-28
best_for: "Building agent lifecycle containers with proper state management"
difficulty: advanced
estimated_time: "15 min"
tags: [agents, lifecycle, state-machine, docker, fastapi]
# ===== NEW: Skill Graph Metadata =====
depends_on:           # Prerequisites: skills needed to USE this one effectively
  - id: HS-099
    reason: "Must understand agent anatomy before building lifecycle"
  - id: HS-098
    reason: "Law 3 (REPORT) + Law 5 (REST) are enforced per-state"
  - id: HS-105
    reason: "Metrics hooks must be emitted from each state"
prerequisites:        # Domain knowledge prerequisites (free text)
  - "Basic Docker container lifecycle"
  - "FastAPI startup/shutdown events"
provides:             # What capability this skill adds
  - "8-state autopilot loop"
  - "Per-state observability hooks"
  - "Graceful shutdown pattern"
related:              # Cross-references (replaces manual [[HS-NNN]] parsing)
  - HS-087    # Agent Decision Tree (per-task flow)
  - HS-090    # Life Plan (per-conversation flow)
  - HS-093    # Nightly Learning (detects drift)
  - HS-070    # Observable Operations (implements hooks)
packs:
  - Agent Builder Pack
---
```

#### 2.2 GoS Retrieval Pipeline (Add as Script)

```python
# scripts/gos_retrieve.py — Dependency-aware skill retrieval
# Usage: python scripts/gos_retrieve.py --query "how do I add health checks to my agent"
#          --budget 4000  # max tokens for skill bundle

"""
Pipeline:
1. HYBRID SEED: Vector similarity + keyword match on query
2. GRAPH DIFFUSE: Reverse-aware PageRank from seed nodes
3. PREREQ RECOVER: Walk dependency edges upstream
4. RERANK: Combine graph score + field-level relevance
5. HYDRATE: Render bounded skill bundle under token budget
"""
```

### Why This Matters for HYPER-SKILLs

Your `[[HS-NNN]]` wikilinks already form a graph. HS-100 (Lifecycle) links to HS-099 (Anatomy), HS-098 (6 Laws), HS-105 (Metrics). But right now, those links are **visual only** — humans see them, agents don't. By adding structured `depends_on` and `related` fields, you enable:

- **Agent auto-coaching**: When an agent loads HS-100, it automatically gets HS-099 and HS-105 too
- **Learning paths**: "I want to build an agent" → automatic prerequisite chain
- **Bundle completeness**: No more "prerequisite gap" where agents miss needed context

---

## 3. MCP Server Integration

### The Opportunity

MCP (Model Context Protocol) is [now a Linux Foundation project](https://developers.redhat.com/articles/2026/05/25/mcp-servers-vs-skills-choosing-right-context-your-ai). It's becoming the **universal standard** for AI tool integration. Claude Code, Cursor, Gemini CLI, and GitHub Copilot all support MCP.

Your skill vault should be an **MCP server**. Any agent that speaks MCP can then:
- List available skills
- Search skills by description
- Read skill content
- Auto-load relevant skills into context

### Implementation: `mcp/` Directory

```
HYPER-SILLs-By-WelshDog/
├── mcp/
│   ├── server.py           # FastMCP server implementation
│   ├── tools/              # MCP tool definitions
│   │   ├── list_skills.py
│   │   ├── search_skills.py
│   │   ├── get_skill.py
│   │   ├── get_skill_graph.py    # GoS retrieval
│   │   └── get_pack.py
│   └── prompts/            # MCP prompt templates
│       └── skill_system.md
```

### MCP Tools to Expose

| Tool | Input | Output | Use Case |
|------|-------|--------|----------|
| `list_skills` | `category`, `pack`, `difficulty` | Filtered skill list | Browse the vault |
| `search_skills` | Natural language query | Ranked skills with relevance scores | "Find skills about agent health checks" |
| `get_skill` | `id: HS-NNN` | Full skill markdown with prompt block | Load a specific skill |
| `get_skill_bundle` | Query + token budget | GoS-optimized skill set | Auto-load prerequisites |
| `get_pack` | Pack name | All skills in pack | "Give me the Agent Builder Pack" |
| `suggest_skill` | Current task description | Recommended skill + trigger explanation | "What skill should I use for this?" |

### Why This Is Game-Changing

Instead of:
> "Open the repo → find the skill → copy the prompt → paste into Claude → fill variables"

It becomes:
> "Claude, I need to set up health checks for my agent" → MCP auto-finds HS-114 (Brain Ops) + HS-105 (Metrics) + HS-070 (Observable Ops)

---

## 4. Vector Search & Semantic Retrieval

### Current Problem

Your skills are indexed by **ID and hero name only**. To find the right skill, a user must:
1. Know the hero name ("CRADLE-TO-GRAVE")
2. Or know the ID (HS-100)
3. Or browse the vault index manually

This doesn't scale past ~100 skills. At 500+ skills, discovery becomes impossible.

### Solution: Lightweight Vector Layer

```python
# scripts/embed_skills.py — One-time setup + incremental updates
# scripts/search_skills.py — CLI semantic search

"""
Storage options (pick one):
- ChromaDB (local, zero-config, good to ~10K skills)
- PostgreSQL + pgvector (if you already have Postgres)
- SQLite + sqlite-vec (single file, portable)

Embedding: text-embedding-3-small (1536d, cheap, fast)
           or local model (privacy, offline)

Fields embedded:
- hero_name + emoji
- description
- tags
- purpose section
- first 200 chars of prompt block
"""
```

### Search UX

```bash
# CLI semantic search
$ python scripts/search_skills.py "how do I make my agent restart itself when it crashes"

Results:
  1. HS-103 🤝 HEALER'S CHORUS (score: 0.91)
     "Healer Circuit-Breaker Protocol — auto-restart failed services"
     ↳ Prereq: HS-091, HS-070

  2. HS-071 🪂 SOFT LANDING (score: 0.84)
     "Fail Gracefully + Fallback Chain"
     ↳ Prereq: HS-098

  3. HS-114 🛠️ BRAIN OPS (score: 0.79)
     "Hyper Brain Infrastructure — includes health check + restart"
     ↳ Prereq: HS-014
```

### Integration with Brain Ops

Add to `hyper_brain_ops.py`:

```python
# New subcommand: skill-search
uv run scripts/hyper_brain_ops.py skill-search "agent health check"
# → Returns top skills + auto-generates a brief on how to combine them
```

---

## 5. Claude Code / Agent Skills Format Bridge

### The Standard

The [Agent Skills specification](https://www.developersdigest.tech/blog/best-claude-code-skills-2026) is converging across:
- **Claude Code** (`~/.claude/skills/`)
- **OpenAI Codex CLI** (adopted 2026)
- **Cursor** (partial support)
- **GitHub Copilot** (preview)

Format:
```yaml
---
name: cradle-to-grave
description: >
  Use when building agent lifecycle containers with FastAPI.
  Covers BIRTH → WAKE → WATCH → DECIDE → ACT → REPORT → REST → DEATH states.
  Triggers on: docker, container, lifecycle, startup, shutdown, autopilot.
dependencies: []  # Python packages if any
---

# Skill body...
```

### Dual-Format Strategy

**Keep your format** (it's better for the vault) but add an **export bridge**:

```python
# scripts/export_claude_skills.py
# Convert HYPER-SKILLs → Claude Code format

"""
Input: HYPER-SKILLs YAML frontmatter + markdown body
Output: .claude/skills/{hero_name}/SKILL.md

Mapping:
- hero_name → name (kebab-case)
- best_for + category + tags → description
- depends_on → (inline as "Prerequisites:" in body)
- 🔮 Prompt Block → preserved
- Example Usage → preserved
"""
```

### Usage

```bash
# Export all skills to Claude Code
python scripts/export_claude_skills.py --output ~/.claude/skills/hyper-vault/

# Export specific pack only
python scripts/export_claude_skills.py --pack "Agent Builder Pack" --output ./claude-export/

# Auto-install (symlink)
python scripts/export_claude_skills.py --link  # Creates symlinks, live updates
```

### Why Both Formats?

| Format | Best For | Why Keep |
|--------|----------|----------|
| HYPER-SKILLs (yours) | Vault management, cross-references, ops | Rich metadata, graph edges, hero names |
| Agent Skills (standard) | Runtime agent consumption | Auto-loading, tool discovery, ecosystem compatibility |

---

## 6. Auto-Loading Skill Packs with Triggers

### The Problem

Even with MCP and vector search, users still need to **ask** for skills. The best skill system loads skills **before the user asks**.

### Solution: Trigger Conditions in Pack Manifest

```yaml
# packs/agent-builder-pack/manifest.yaml
# NEW FILE

name: "Agent Builder Pack"
description: "Skills for building and orchestrating AI agents"
skills:
  - HS-098  # THE SACRED SIX
  - HS-099  # SIX-ORGAN HEART
  - HS-100  # CRADLE-TO-GRAVE
  - HS-091  # THE FOUNDING SIX
  - ...

triggers:
  # When to auto-suggest this pack
  keywords:
    - "build agent"
    - "agent swarm"
    - "docker container agent"
    - "fastapi agent"
    - "orchestrator"
  file_patterns:
    - "Dockerfile*"
    - "docker-compose*.yml"
    - "main.py"  # if contains FastAPI
    - "agents/**"
  context_signals:
    - "discussing containerization"
    - "mentioning prometheus or grafana"
    - " health check endpoint"
  # Don't trigger if
  exclusions:
    - "web scraping"  # → suggest Web Scraping Pack instead
    - "youtube"       # → suggest YouTube Pack instead

auto_load: false  # If true, load without asking (use sparingly)
suggest: true     # If true, suggest to user when triggers match
```

### Trigger Engine

```python
# scripts/trigger_engine.py — Lightweight trigger matcher
# Runs in Brain Ops daily briefing or as MCP middleware

def match_packs(context: str, file_paths: list[str]) -> list[PackSuggestion]:
    """
    Score each pack against current context.
    Return ranked suggestions with confidence scores.
    """
```

---

## 7. Agent Memory & Learning Loop

### The Vision

Skills should **learn from usage**. Every time a skill is used, the system should:
1. Log what worked
2. Note what didn't
3. Suggest improvements
4. Track which skills are commonly used together

### Implementation: `.skill-memory/` Directory

```
HYPER-SILLs-By-WelshDog/
├── .skill-memory/           # Git-tracked (lightweight)
│   ├── usage-log.yaml       # Aggregated usage (anonymized patterns)
│   ├── co-occurrence.yaml   # "Users who used X also used Y"
│   ├── feedback.yaml        # Structured feedback on skills
│   └── drift-detect.yaml    # Skills that may need updating
```

### Memory Schema

```yaml
# .skill-memory/usage-log.yaml

entries:
  - skill: HS-100
    timestamp: "2026-05-28T14:32:00Z"
    task_type: "building-container-agent"
    success: true
    tokens_used: 4500
    time_saved_estimate: "30 min"
    feedback: "Worked perfectly, but needed HS-070 first"
    # → Auto-adds HS-070 as stronger dependency for HS-100

  - skill: HS-103
    timestamp: "2026-05-28T15:10:00Z"
    task_type: "healer-setup"
    success: false
    error: "Missing Redis connection details"
    # → Flag: skill may need prereq on HS-072 (Redis Context Store)

co_occurrence:
  - skills: [HS-098, HS-085, HS-088]
    count: 47
    note: "Sacred Six + Five Wards + Mirror Oath often used together"
    # → Suggest creating "Agent Governance Super-Pack"
```

### Integration with Night Tender (HS-093)

Your Nightly Learning Loop skill already conceptually does this. Make it **real**:

```python
# In hyper_brain_ops.py, add to the nightly chain:

uv run scripts/hyper_brain_ops.py analyze-skill-usage
# → Reads usage-log.yaml
# → Suggests dependency updates
# → Flags unused skills for review
# → Generates co-occurrence pack recommendations
```

---

## 8. Obsidian Knowledge Graph Integration

### Current State

You already have an Obsidian vault at `H:\HYPERFOCUSZONE\HperCore\BROski-Obsidian-Brain`. Skills are referenced in docs but not **integrated**.

### Upgrade: Bidirectional Vault Sync

```python
# scripts/obsidian_sync.py — NEW

"""
Two-way sync between HYPER-SKILLs repo and Obsidian vault:

REPO → VAULT:
- Write each skill as Obsidian note: Vault/Skills/HS-100-CRADLE-TO-GRAVE.md
- Convert [[HS-NNN]] links to Obsidian [[HS-NNN|HERO NAME]] format
- Embed skill graph as Mermaid diagram
- Create MOC (Map of Content) note per pack

VAULT → REPO:
- Capture backlinks from vault notes to skills
- Detect which skills are referenced in real project notes
- Flag "highly referenced but not recently updated" skills
"""
```

### Visual Skill Map in Obsidian

Use the [obsidian-graph](https://github.com/drewburchfield/obsidian-graph) MCP project as reference:

- **Semantic embeddings** of all skills in pgvector
- **Multi-hop graph traversal**: "Show me all skills related to agent health"
- **Hub detection**: Which skills are most central? (Probably HS-098, HS-091)
- **Orphan detection**: Which skills have few connections? (Needs integration)

### Mermaid Diagram Generation

```python
# scripts/generate_skill_map.py
# Generates Mermaid diagram of skill dependencies

# Output example:
# ```mermaid
# graph TD
#     HS-098["🏛️ THE SACRED SIX"] --> HS-085["🚧 THE FIVE WARDS"]
#     HS-098 --> HS-103["🤝 HEALER'S CHORUS"]
#     HS-099["🧬 SIX-ORGAN HEART"] --> HS-100["🔄 CRADLE-TO-GRAVE"]
#     HS-100 --> HS-105["📊 THE METRICS OATH"]
#     style HS-098 fill:#f9f,stroke:#333,stroke-width:4px
# ```
```

---

## 9. ND-First UX Power-Up

### This Is Your Secret Weapon

Most skill systems are built by neurotypical developers for neurotypical developers. Your **ND-first positioning** is unique and powerful. Lean into it harder.

### 9.1 Visual Skill Map (Dopamine-Friendly)

ADHD brains process visual/spatial information better than text lists. Generate:

- **Interactive skill constellation**: Skills as nodes, dependencies as edges, packs as clusters
- **Color-coded by category**: `agents/` = blue, `dev/` = green, `broski/` = purple, `youtube/` = red
- **Heat map overlay**: Brighter = more used, dimmer = needs love
- **"You Are Here" marker**: Highlight skills relevant to current task

Implementation: Obsidian Graph View + Mermaid + optional web UI

### 9.2 Dopamine Progress Tracker

```yaml
# progress-tracker.yaml — NEW
# Gamified skill usage (opt-in)

user_stats:
  skills_used_total: 47
  packs_completed:
    - "Agent Builder Pack"  # Used all skills at least once
  streak_days: 12
  achievements:
    - name: "First Resurrection"
      desc: "Used auto-rescue to save a lost skill"
      unlocked: "2026-05-20"
    - name: "Sacred Six Scholar"
      desc: "Used all 6 Laws skills in one session"
      unlocked: "2026-05-25"
    - name: "Vault Keeper"
      desc: "Contributed a new skill to the vault"
      unlocked: null  # Not yet...
```

### 9.3 Body Double Mode

Inspired by ADHD body doubling — a low-stakes social accountability practice:

```python
# scripts/body_double.py — NEW

"""
Body Double Mode for HYPER-SKILLs usage.

Usage:
    uv run scripts/body_double.py --task "Build agent health checks" --skills "HS-103,HS-070"

What it does:
    1. Opens a low-friction Discord/terminal status display
    2. Shows: task, skills loaded, time elapsed, next step
    3. Sends gentle nudges every 10 min (configurable)
    4. Celebrates completion with a "BROski-approved" message
    5. Logs the session for future reference

The 'body double' is the script — just enough presence
to reduce ADHD task-initiation friction.
"""
```

### 9.4 Mercy Message Integration

Your HS-069 (MERCY MESSAGE) skill is brilliant. Apply it to the skill system itself:

- **Skill not found**: "No stress — that skill might not exist yet. Here's the closest match..."
- **Dependency missing**: "This skill works better with HS-XXX. Want me to load it too?"
- **Usage confusion**: "Stuck? That's normal. Here's a 30-second explainer..."

---

## 10. Skill Distribution & Versioning

### 10.1 OCI Artifact Distribution

The [skr tool](https://github.com/marketplace/actions/publish-agent-skills) packages skills as OCI artifacts (same format as Docker images). This enables:

- Versioned skill releases
- Pull skills from GitHub Packages / Docker Hub
- Immutable skill bundles with lockfiles

```yaml
# .github/workflows/publish-skills.yaml
# NEW: Publish skills as OCI artifacts on release

- name: Publish Agent Skills
  uses: andrewhowdencom/skr@main
  with:
    skills_dir: ./
    registry: ghcr.io
    repository: welshDog/hyper-skills
```

### 10.2 Semantic Versioning for Skills

Currently all skills are `v1.0`. Add meaningful versioning:

```yaml
---
id: HS-100
version: v1.2.0  # MAJOR.MINOR.PATCH
# MAJOR: Breaking change (prompt behavior changes)
# MINOR: New capability added (new section, new example)
# PATCH: Fix, clarification, typo
version_history:
  - v1.2.0: "Added REST state hook details per HS-101 integration"
  - v1.1.0: "Added anti-patterns section"
  - v1.0.0: "Initial rescue from HyperCode-V2.4"
---
```

### 10.3 Skill Lifecycle States

```
DRAFT → REVIEW → ACTIVE → DEPRECATED → ARCHIVED
  ↑       ↑        ↑          ↑           ↑
  |       |        |          |           |
  |       |        |          |           └── Hidden from search, kept for history
  |       |        |          └── Warn on use, suggest replacement
  |       |        └── Fully supported, appears in all searches
  |       └── Passes linter, has been tested at least once
  └── New skill, not yet validated
```

---

## 11. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2) — Skill Graph
- [ ] Add `depends_on`, `provides`, `related` to skill template
- [ ] Retrofit top 20 most-used skills with dependency metadata
- [ ] Build `scripts/gos_retrieve.py` — graph retrieval engine
- [ ] Update linter to validate dependency fields

### Phase 2: Integration (Weeks 3-4) — MCP + Search
- [ ] Build `mcp/server.py` — FastMCP skill server
- [ ] Implement `search_skills` with vector embeddings
- [ ] Add `scripts/export_claude_skills.py` — format bridge
- [ ] Integrate semantic search into Brain Ops CLI

### Phase 3: Intelligence (Weeks 5-6) — Auto-Load + Memory
- [ ] Build trigger engine for skill packs
- [ ] Implement `.skill-memory/` learning loop
- [ ] Add Obsidian bidirectional sync
- [ ] Generate visual skill map (Mermaid + Obsidian)

### Phase 4: Experience (Weeks 7-8) — ND-First Polish
- [ ] Build progress tracker + dopamine hooks
- [ ] Implement Body Double mode
- [ ] Polish Mercy Message integration
- [ ] Create skill constellation visualization

### Phase 5: Distribution (Week 9+) — Ecosystem
- [ ] OCI artifact publishing
- [ ] Semantic versioning rollout
- [ ] Community contribution workflow
- [ ] Documentation + tutorial videos

---

## 12. References

### Papers
1. [Graph-of-Skills: Dependency-Aware Structural Retrieval for Massive Agent Skills](https://arxiv.org/abs/2604.05333) — Liu et al., UPenn/CMU/Brown, April 2026
2. [Q-VESA: Accelerating Quantization-Aware Vector Search for Fast Retrieval in Prompt Engineering](https://www.computer.org/csdl/journal/tc/2026/03/11303310/2cwBPdFTVUk) — IEEE Trans. Computers, March 2026

### Protocols & Standards
3. [Model Context Protocol (MCP) Registry](https://github.com/modelcontextprotocol/registry) — Anthropic/Linux Foundation
4. [MCP Servers vs. Skills](https://developers.redhat.com/articles/2026/05/25/mcp-servers-vs-skills-choosing-right-context-your-ai) — Red Hat, May 2026
5. [Agent Skills Specification](https://www.developersdigest.tech/blog/best-claude-code-skills-2026) — Developers Digest, April 2026
6. [Claude Code Skills Guide](https://aifordevelopers.substack.com/p/the-complete-guide-to-creating-and) — AI For Developers, April 2026

### Tools & Projects
7. [obsidian-graph](https://github.com/drewburchfield/obsidian-graph) — Semantic knowledge graph for Obsidian with MCP
8. [skr — Skill Registry](https://github.com/marketplace/actions/publish-agent-skills) — OCI artifact skill publishing
9. [Claude Skills Library](https://github.com/alirezarezvani/claude-skills) — 338 skills across 16 domains

### Frameworks & Patterns
10. [LangGraph Agent Memory Patterns](https://callsphere.ai/blog/langgraph-agent-memory-short-long-term-2026) — Short-term + long-term memory, May 2026
11. [How to Coordinate Multiple AI Agents](https://www.developersdigest.tech/blog/how-to-coordinate-multiple-ai-agents) — 6 coordination patterns, April 2026
12. [Agent Orchestration Patterns](https://gurusup.com/blog/agent-orchestration-patterns) — Swarm vs Mesh vs Hierarchical, May 2026
13. [Context Engineering 2026 Guide](https://futureagi.com/blog/context-engineering-genai-2025/) — RAG, Memory & MCP, May 2026

### ND-Focused Resources
14. [Designing Better Coding Tools for ADHD Students](https://www.lancaster.ac.uk/scc/about-us/news/designing-better-coding-tools-for-students-with-adhd) — Lancaster University
15. [Leantime — Work Management for ADHD](https://leantime.io/work-management-for-adhd-and-add/) — Dopamine-driven project management

---

## Appendix A: Quick-Start Dependency Additions

For the top 10 most-referenced skills, here's what to add:

| Skill | Add `depends_on` | Add `provides` |
|-------|------------------|----------------|
| HS-098 (SACRED SIX) | HS-085, HS-088 | 6 philosophical laws for agent behavior |
| HS-099 (SIX-ORGAN HEART) | HS-098 | Anatomy model: Memory, Logic, Voice, Eyes, Hands, Safety |
| HS-100 (CRADLE-TO-GRAVE) | HS-099, HS-105, HS-070 | 8-state lifecycle with per-state hooks |
| HS-091 (FOUNDING SIX) | HS-090, HS-089 | Identity cards for 6 infrastructure agents |
| HS-089 (GRAND ROSTER) | HS-090 | Complete 27-agent role map |
| HS-070 (ALL-SEEING) | HS-105 | Observable ops pattern with Prometheus/Grafana |
| HS-103 (HEALER'S CHORUS) | HS-091, HS-072 | Circuit-breaker + auto-restart protocol |
| HS-104 (THREE WALLS) | HS-098 | Tier protection: hardcoded + config + self |
| HS-105 (METRICS OATH) | — | 5 mandatory metrics contract |
| HS-114 (BRAIN OPS) | HS-014, HS-070, HS-105 | Full daily ops chain: health → briefing → sync → commit |

---

## Appendix B: Directory Structure After Upgrade

```
HYPER-SILLs-By-WelshDog/
|---- README.md
|---- SKILL.md                    # Mega vault (as-is)
|---- skills-registry.json        # Machine-readable registry
|---- vault-index.md              # Human-readable index
|---- templates/
|   |____ SKILL_TEMPLATE.md       # NEW: Enhanced with depends_on
|
|---- scripts/
|   |---- skill_linter.py         # Enhanced: validate dependencies
|   |---- gos_retrieve.py         # NEW: Graph-of-Skills retrieval
|   |---- embed_skills.py         # NEW: Vector embedding
|   |---- search_skills.py        # NEW: Semantic search CLI
|   |---- export_claude_skills.py # NEW: Format bridge
|   |---- trigger_engine.py       # NEW: Auto-load triggers
|   |---- obsidian_sync.py        # NEW: Bidirectional vault sync
|   |---- generate_skill_map.py   # NEW: Mermaid graph generation
|   |---- body_double.py          # NEW: ADHD body-double mode
|   |---- hyper_brain_ops.py      # Enhanced: skill-search subcommand
|   |---- extract_skills.py       # (as-is)
|   |---- generate_registry.py    # (as-is)
|   |____ update_vault_index.py   # (as-is)
|
|---- mcp/                        # NEW: MCP server
|   |---- server.py
|   |____ tools/
|       |---- list_skills.py
|       |---- search_skills.py
|       |---- get_skill.py
|       |---- get_skill_bundle.py
|       |____ get_pack.py
|
|---- packs/                      # NEW: Pack manifests with triggers
|   |____ agent-builder-pack/
|       |____ manifest.yaml
|
|---- .skill-memory/              # NEW: Usage analytics (git-tracked)
|   |---- usage-log.yaml
|   |---- co-occurrence.yaml
|   |____ drift-detect.yaml
|
|---- vector-store/               # NEW: Embeddings (gitignored)
|   |____ ...
|
|---- agents/
|---- broski/
|---- content/
|---- dev/
|---- youtube/
|---- hypercode/                   # NEW: For HS-030→066 when rescued
|---- web3/                        # NEW: For HS-052→058 when rescued
|
|---- .github/
|   |---- workflows/
|   |   |---- skill-lint.yml       # (as-is)
|   |   |---- auto-rescue.yml      # (as-is)
|   |   |____ publish-skills.yaml  # NEW: OCI artifact publishing
|
|____ docs/
    |---- UPGRADE_MASTERPLAN.md    # This document
    |____ superpowers/
        |____ ...
```

---

*Masterplan written for WelshDog HYPER-SKILLs Vault*
*Built with deep research into 25+ sources spanning academic papers, protocol specs, open-source projects, and production frameworks*
*Last updated: 2026-06-01*
