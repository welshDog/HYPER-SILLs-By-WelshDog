# 🛠️ HS-114 BRAIN OPS — HYPER BRAIN INFRASTRUCTURE SKILL
**Category:** Dev / Infrastructure
---
skill_id: HS-114
hero_name: "BRAIN OPS"
emoji: "🛠️"
version: v1.1
category: dev
depends_on:
  - HS-016  # BRAIN PRIMER — brain ecosystem orientation required
  - HS-017  # MIND CORE — brain core is the primary target for ops
provides:
  - brain-infrastructure-runbook
  - docker-health-debug-steps
  - github-sync-ops
  - briefing-fix-procedures
related:
  - HS-021  # VAULT SYNC — ops keeps the vault sync healthy
  - DS-028  # PROGRESSIVE_HEALTH_WAIT — health wait used in brain restart
graph_notes: "Living ops runbook for the BROski brain infrastructure — Docker health checks, GitHub sync fixes, and service restart procedures."
---
**Version:** v1.1 (Hardened — Gordon's patches applied)
**Last tested:** 2026-05-31 21:18 BST
**Status:** 🟡 PARTIAL — Health ✅ Briefing ✅ | GitHub Sync ⚠️ | Discord ⚠️

---

## 📍 WHERE WE ARE (Session: 2026-05-31)

### ✅ What's Working
| Step | Result | Notes |
|---|---|---|
| `fix-env` | ✅ ALL GREEN | All 6 checks passed |
| `check-health` | ✅ HEALTHY (10.2s) | Container running, API HTTP 200 |
| `generate-briefing` | ✅ SUCCESS (21.4s) | POST to localhost:8100 worked |

### ⚠️ Known Issues (Fix Before Daily Mode)

#### 1. GitHub Sync — HTTP 401 (all 6 repos)
- **Cause:** `GITHUB_PAT` is set (28 chars) but likely missing `repo` scope, OR is a fine-grained PAT without repo access configured
- **Fix:**
  1. Go to https://github.com/settings/tokens
  2. Verify PAT has `repo` scope (classic) OR all 6 repos listed (fine-grained)
  3. Regenerate → update `.env` → re-run `sync-github`
- **Affected repos:** HyperCode-V2.4, HYPER-SILLs-By-WelshDog, Hyper-Vibe-Coding-Course, WelshDog-Mission-Control, hyper-agents-ide, HyperAgent-SDK

#### 2. Discord Report — HTTP 403
- **Cause:** Webhook URL is invalid or the webhook was deleted in Discord
- **Fix:**
  1. Go to Discord → target channel → Edit → Integrations → Webhooks
  2. Create new webhook or copy existing URL
  3. Update `.env` → `DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...`
  4. Re-run `report`

---

## 🏗️ Architecture

### Directory Structure
```
HYPER-SILLs-By-WelshDog/
└── dev/
    ├── HYPER_BRAIN_OPS_v1.md       ← this file
    └── HYPER_BRAIN_OPS_v2/         ← next version staging
scripts/
└── hyper_brain_ops.py              ← CLI runner (v1.1 hardened)
output/
├── health.json
├── briefing.json
├── sync.json
└── vault_commit.json
```

### Vault Target (Windows)
```
H:\HYPERFOCUSZONE\HperCore\BROski-Obsidian-Brain-for-HyperFocus-z0ne
```
Confirmed exists ✅ | Confirmed Git repo ✅

### Docker Container
- Name: `hyper-brain`
- API: `http://localhost:8100`
- Status: running ✅

---

## 🔧 CLI Reference

```bash
# Environment doctor — run this first every session
uv run scripts\hyper_brain_ops.py fix-env

# Full daily chain
uv run scripts\hyper_brain_ops.py check-health --output output\health.json
uv run scripts\hyper_brain_ops.py generate-briefing --output output\briefing.json
uv run scripts\hyper_brain_ops.py sync-github --output output\sync.json
uv run scripts\hyper_brain_ops.py report

# Repair mode
uv run scripts\hyper_brain_ops.py fix-env
uv run scripts\hyper_brain_ops.py check-health --restart-if-down

# Windows Task Scheduler setup
uv run scripts\hyper_brain_ops.py setup-task
```

---

## 🌍 Required Environment Variables

| Variable | Status | Notes |
|---|---|---|
| `GITHUB_PAT` | ✅ Set (28 chars) | Needs `repo` scope — see fix above |
| `DISCORD_WEBHOOK_URL` | ✅ Set | Needs valid webhook — see fix above |
| `VAULT_PATH` | ✅ Confirmed | H:\HYPERFOCUSZONE\HperCore\BROski-Obsidian-Brain-for-HyperFocus-z0ne |
| `BRIEFING_API_URL` | ✅ | http://localhost:8100 |
| `DOCKER_CONTAINER` | ✅ | hyper-brain |

Set all in `.env` at project root. Never commit `.env`.

---

## 🚀 Next Steps Checklist

- [ ] Fix `GITHUB_PAT` scope → re-run `sync-github` → confirm issues land in `GitHub-Inbox/`
- [ ] Fix Discord webhook → re-run `report` → confirm Discord ping received
- [ ] Verify briefing `.md` file landed in vault `Briefings/` folder
- [ ] Run `setup-task` to register Windows Task Scheduler daily job
- [ ] Set up Obsidian Git auto-commit after each daily run (see `OBSIDIAN_GIT_VAULT_v1.md`)

---

## 🧠 Script Version Notes (v1.1 — Hardened)

Gordon's patches applied to `hyper_brain_ops.py`:
- **Partial-success handling** — every step writes its own status JSON; chain never halts on one failure
- **Rate-limit budget file** — tracks GitHub API usage across runs (1 req/sec, handles 403 with backoff)
- **Vault Git contract** — only commits when there are actual changes (`git diff-index --quiet`)
- **Full report** — reads ALL 4 status files (health, briefing, sync, vault_commit)
- **Windows Task Scheduler wrapper** — emitted via `setup-task` subcommand

---

## 🔗 Related Skills

| Skill | Relevance |
|---|---|
| `OBSIDIAN_GIT_VAULT_v1.md` | Auto-commit vault after daily run |
| `CROSS_REPO_SYNC_v1.md` | Conceptual basis for sync-github logic |
| `PREFLIGHT_CHECKS_SYSTEM_v1.md` | Pattern for fix-env preflight design |
| `PROGRESSIVE_HEALTH_WAIT_v1.md` | Backoff logic for slow container boot |
| `TEST_STATUS_REPORT_v1.md` | Discord report formatting pattern |
| `CORE_AGENT_METRICS_CONTRACT_v1.md` | Metrics for ops observability |

---

*HS-114 BRAIN OPS by welshDog 🐕⚡ — [HYPER-SILLs-By-WelshDog](https://github.com/welshDog/HYPER-SILLs-By-WelshDog)*
