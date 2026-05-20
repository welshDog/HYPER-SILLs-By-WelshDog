# ⚙️ Hyper Skill: HYPERCODE_SDK_MASTER_v1
**Category:** Dev / SDK Operations
**Version:** 0.3.0
**npm package:** `@w3lshdog/hyper-agent`
**Rescued From:** [HyperAgent-SDK](https://github.com/welshDog/HyperAgent-SDK) — `.Claude/skills/hypercode-sdk/SKILL.md`

> The HUB skill for the entire SDK. Route to companion skills for specific workflows.

---

## 📦 Current State (v0.3.0 — April 30, 2026)

- **Tests:** 57/57 passing
- **Subpath exports:** `.`, `./registry`, `./client`
- **Runtime deps:** `ajv`, `ajv-formats` only

---

## 🗺️ Phase Status

| Phase | Status |
|---|---|
| Phase 2 — Starter pack (init + 4 templates + validator UX) | ✅ 0.2.0 shipped |
| Phase 3 — Token sync client (`awardFromCourse`) | ✅ 0.3.0 shipped |
| Phase 4 — Graduation flagship | ⏳ NEXT |
| Phase 5 — Public registry surface | 🔜 |
| Phase 6 — Ops commands (`status`, `logs`, `tokens`, `agents`) | ✅ live |

---

## 🛠️ CLI Commands

| Command | What it does |
|---|---|
| `init <dir> --template <name>` | Scaffold from python/node/typescript/mcp templates |
| `validate <dir> [--strict]` | Validates agent manifest with human-readable hints |
| `registry build/search/show` | Agent registry with auto-computed badges |
| `studio` | Launches GUI at localhost:4040 |
| `status` | Shows all 29 V2.4 container statuses |
| `agents list` | Lists agent heartbeats |
| `tokens award <discord_id> <amount>` | Awards BROski$ tokens |
| `graduate <discord_id>` | Triggers student graduation (Phase 4) |
| `logs --tail N` | Streams recent logs |

---

## 📚 Library API

```javascript
// Manifest validation
const { validateAgent } = require('@w3lshdog/hyper-agent');

// Registry + badges
const { computeBadges, BADGE_RULES } = require('@w3lshdog/hyper-agent/registry');

// Phase 3 — Course → V2.4 token sync (SERVER-ONLY)
const { awardFromCourse, AwardFromCourseError } = require('@w3lshdog/hyper-agent/client');
```

---

## 🏅 Badge Rules (auto-computed)

```
✅ Verified       → manifest.verified: true
⚡ MCP Ready      → mcp_compatible: true
🧠 Memory Enabled → memory !== 'none'
🔧 Multi-Tool     → tools.length >= 3
🔐 Env Declared   → env_vars.length > 0
🚀 HyperCoder     → course_level >= 4
👑 Elite          → course_level >= 5
💚 Health Checked → health_check defined
```

---

## 🔌 MCP Port Convention

```
3100-3199 → Writing agents
3200-3299 → Code agents (mcp-starter default: 3200)
3300-3399 → Data agents
3400-3499 → Discord agents
3500-3599 → Automation agents
```

---

## ⚠️ Common Gotchas

- **AJV strict** — never put `errorMessage` in `then` blocks
- **`awardFromCourse` is server-only** — never import from `'use client'`
- **Scoped publish** needs `--access public` always
- **MCP port collisions** — validator catches duplicates
- **Spec changes are cross-repo events** — use `cross-repo-sync` skill

*Rescued from HyperAgent-SDK — HYPER-SKILLs Vault by WelshDog 🐕⚡*
