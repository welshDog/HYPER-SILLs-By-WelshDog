# 🧠⚡ HYPER-SILLs Vault — Claude Code Plugin

> The neurodivergent-first AI skill vault, installable in one command.

This plugin bundles the **HYPER-SILLs** skill vault — 89 hero-named skills across
`agents`, `dev`, `broski`, and `youtube` — with **Graph-of-Skills** dependency retrieval
(arXiv:2604.05333: +25.55% reward, -56.72% tokens vs flat loading).

## Install

```bash
/plugin marketplace add welshDog/HYPER-SILLs-By-WelshDog
/plugin install hyper-sills-vault
```

## What you get

**MCP server** (`hyper-sills`) with 5 tools:

| Tool | What it does |
|---|---|
| `search_skills` | Keyword / category / tag search |
| `load_skill` | Load a skill's full content + GoS metadata by ID |
| `get_skill_graph` | `depends_on` / `provides` / `related` for load-order |
| `recommend_for_task` | Best skills for a natural-language task |
| `list_skills_by_category` | Browse `agents` / `dev` / `broski` / `youtube` |

**Slash commands:**

| Command | What it does |
|---|---|
| `/skill-find <keywords>` | Find skills by keyword |
| `/skill-load <HS-NNN>` | Load + apply a skill (prereqs first) |
| `/skill-recommend <task>` | Recommend skills for what you're doing |

## Requirements

- Python 3.11+ with the `mcp` package (`pip install "mcp>=1.0.0"`), or run via `uv`.

---

*Part of the [HyperFocus Zone](https://github.com/welshDog) ecosystem — built by welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
*Stop apologising for your brain. Start building.*
