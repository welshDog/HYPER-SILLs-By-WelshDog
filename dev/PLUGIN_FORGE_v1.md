# HS-128 — 🏗️ PLUGIN FORGE — Build & Publish a Claude Code Plugin Marketplace

---
skill_id: HS-128
hero_name: "PLUGIN FORGE"
emoji: "🏗️"
version: v1.0.0
status: ACTIVE
category: dev
depends_on:
  - DS-020  # PORTAL FORGE — MCP server + agent registration (a plugin bundles one)
provides:
  - claude-code-plugin-marketplace
  - one-command-skill-distribution
  - plugin-manifest-pattern
related:
  - HS-129  # SKILLS-OVER-MCP — expose skills as MCP Resources inside the plugin
  - HS-130  # OCI SKILL SHIP — versioned OCI distribution alongside the marketplace
graph_notes: "Packages a vault of skills + an MCP server + hooks + commands into one installable Claude Code plugin, distributed via a marketplace.json users add in one command."
problem_keywords:
  - claude plugin
  - plugin marketplace
  - distribute skills
  - publish plugin

---
**Category:** `dev/`
**Source:** Born-here — code.claude.com/docs/en/plugin-marketplaces (2026-06)
**Version:** v1

---

## 🤔 What It Does

Turns a pile of skills, an MCP server, hooks, and slash commands into a single
**Claude Code plugin** that anyone installs with two commands. The marketplace is
just a git repo with a `.claude-plugin/marketplace.json` at its root. This is the
biggest reach unlock of 2026 — the marketplace ecosystem already hosts 21,600+
skills and 12,500+ MCP servers.

---

## 🎯 Purpose

- **Who uses it:** Anyone with a skill vault, an MCP server, or a useful hook set.
- **When to use it:** When "copy-paste this prompt" friction is killing adoption.
- **What it unlocks:** `/plugin marketplace add <repo>` → `/plugin install <name>` → done.

---

## 📥 Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `marketplace_name` | `string` | ✅ | NOT a reserved Anthropic name (e.g. not `claude-plugins-official`) |
| `plugin_source` | `path` | ✅ | Folder holding the plugin package (`./plugins/<name>`) |
| `mcp_server` | `path` | ❌ | An existing MCP server to bundle |

---

## 📤 Output Format

```
<repo>/
├── .claude-plugin/marketplace.json     # marketplace manifest (lists plugins)
└── plugins/<name>/
    ├── .claude-plugin/plugin.json       # plugin manifest (name, version, mcpServers)
    ├── commands/*.md                    # slash commands (auto-discovered)
    ├── agents/*.md                      # subagents (optional)
    └── hooks/hooks.json                 # hooks (optional)
```

---

## 🔮 Prompt Block

```
You are PLUGIN FORGE. Package the given skill vault as a Claude Code plugin marketplace.

Steps:
1. Write .claude-plugin/marketplace.json at repo root: name (NOT reserved), owner,
   version, description, and a `plugins` array with one entry per plugin
   (name, source: "./plugins/<name>", version, keywords).
2. Write plugins/<name>/.claude-plugin/plugin.json: name, version, description, author,
   and `mcpServers` referencing the bundled server via ${CLAUDE_PLUGIN_ROOT}.
3. Add commands/*.md slash commands as thin wrappers over the MCP tools.
4. Validate both JSON files parse. Document install as:
   /plugin marketplace add <repo>  then  /plugin install <name>

Rules:
- Never use a reserved marketplace name.
- Reference bundled files with ${CLAUDE_PLUGIN_ROOT}, never absolute paths.
- Keep the plugin a thin wrapper — reuse existing server/hooks, don't rewrite them.
```

---

## 💡 Example Usage

```bash
# After forging the manifests:
/plugin marketplace add welshDog/HYPER-SILLs-By-WelshDog
/plugin install hyper-sills-vault
# → MCP tools + /skill-find, /skill-load, /skill-recommend now live
```

---

## 🚨 Anti-patterns

- **Don't hardcode absolute paths** — use `${CLAUDE_PLUGIN_ROOT}`; the repo clones to a random dir on install.
- **Don't claim a reserved name** — `claude-code-plugins`, `claude-plugins-official`, etc. are blocked.
- **Don't fork the source server into the plugin** — reference it; one source of truth.

---

## 🔗 Related Skills

- [[HS-081]] PORTAL FORGE — the MCP server your plugin bundles
- [[HS-129]] SKILLS-OVER-MCP — expose the vault's skills as MCP Resources
- [[HS-130]] OCI SKILL SHIP — versioned OCI artifact distribution

---

## 📋 THE PROMPT

> Copy this block into any AI session to activate the skill:

```text
Use skill HS-128 [PLUGIN FORGE]. Package my skills + MCP server into a Claude Code plugin marketplace (marketplace.json + plugin.json + command wrappers), validate the JSON, and give me the two install commands.
```
