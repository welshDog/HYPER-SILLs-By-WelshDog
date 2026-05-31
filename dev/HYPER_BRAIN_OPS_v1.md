---
name: "hyper-brain-ops"
hero: "🛠️ BRAIN OPS"
id: "HS-114"
category: "dev"
pack: "ND-Friendly Coding Pack"
version: "v1.0"
author: "welshDog"
last_updated: "2026-05-31"
trigger_modes:
  - "daily" # Auto-run: check-health → generate-briefing → sync-github → report
  - "repair" # Ad-hoc fix: fix-env → check-health --restart-if-down
env_vars_required:
  - GITHUB_PAT
  - DISCORD_WEBHOOK_URL
  - VAULT_PATH
---

# 🛠️ BRAIN OPS — HS-114

> *"Your Second Brain should maintain itself. This skill is the engineer who never sleeps."*
> Built by welshDog 🐕 Llanelli, Wales 🏴󠁧󠁢󠁷󠁬󠁳󠁧

---

## 🎯 What This Skill Does

Automatically maintains your Hyper Brain infrastructure. It verifies the `hyper-brain` Docker container is healthy, triggers the Morning Briefing API, syncs cross-repo GitHub issues into your Obsidian vault, handles common errors (missing deps, crashed containers, broken volume mounts), and delivers a status report to Discord.

**Two modes:**
- 🌅 **Daily Mode** — runs the full pipeline every morning
- 🔧 **Repair Mode** — diagnoses and fixes the environment on demand

---

## 📥 Inputs

| Variable | Source | Example |
|---|---|---|
| `GITHUB_PAT` | env var | `ghp_xxxxxxxxxxxx` |
| `DISCORD_WEBHOOK_URL` | env var | `https://discord.com/api/webhooks/...` |
| `VAULT_PATH` | env var | `C:/Users/Lyndon/HyperBrain` |
| `BRIEFING_API_URL` | env var (default: `http://localhost:8100`) | `http://localhost:8100` |
| `DOCKER_CONTAINER` | env var (default: `hyper-brain`) | `hyper-brain` |
| `GITHUB_REPOS` | env var, comma-separated | `welshDog/HYPER-SILLs-By-WelshDog,welshDog/HyperFocusZone` |

---

## 📤 Outputs

| Output | Location | Description |
|---|---|---|
| Morning briefing `.md` | `$VAULT_PATH/Briefings/` | Today's briefing from the AI engine |
| GitHub issues `.md` files | `$VAULT_PATH/GitHub-Inbox/` | One file per open issue, per repo |
| `health.json` | `./output/` | Container + API health status |
| `briefing.json` | `./output/` | Briefing generation result |
| `sync.json` | `./output/` | GitHub sync result (issues written) |
| Discord message | Your server | BROski-style status report 🔔 |

---

## 🚀 Usage

### 🌅 Daily Mode (full pipeline)
```bash
uv run scripts/hyper_brain_ops.py check-health --output output/health.json && \
uv run scripts/hyper_brain_ops.py generate-briefing --output output/briefing.json && \
uv run scripts/hyper_brain_ops.py sync-github --output output/sync.json && \
uv run scripts/hyper_brain_ops.py report
```

### 🔧 Repair Mode (when things break)
```bash
uv run scripts/hyper_brain_ops.py fix-env && \
uv run scripts/hyper_brain_ops.py check-health --restart-if-down
```

### 🩺 Individual Subcommands
```bash
# Ping Docker + API health endpoint
uv run scripts/hyper_brain_ops.py check-health

# Trigger morning briefing generation
uv run scripts/hyper_brain_ops.py generate-briefing

# Pull GitHub issues into vault
uv run scripts/hyper_brain_ops.py sync-github

# Diagnose env: volume mounts, GITHUB_PAT, port bindings
uv run scripts/hyper_brain_ops.py fix-env

# Send summary to Discord webhook
uv run scripts/hyper_brain_ops.py report
```

---

## 🧠 Agent Prompt Block

Copy this into your AI agent (Perplexity, Claude, HyperCode):

```
[HYPER BRAIN OPS — HS-114]

You are running the Hyper Brain Ops maintenance skill.

Your job:
1. Run check-health. If container is down and --restart-if-down is set, restart it.
2. Run generate-briefing. If it returns a 500 error, extract the error message and log it — do NOT crash.
3. Run sync-github. Pull open issues from all repos in GITHUB_REPOS. Write one .md file per issue to $VAULT_PATH/GitHub-Inbox/. Respect rate limits (1 req/sec).
4. Run report. Send a clean BROski-style Discord message with: ✅ successes, ⚠️ warnings, ❌ failures.

Input variables:
- VAULT_PATH: [YOUR VAULT PATH]
- GITHUB_REPOS: [COMMA-SEPARATED REPOS]
- BRIEFING_API_URL: http://localhost:8100
- DOCKER_CONTAINER: hyper-brain

Always write --output JSON files so the agent can read results.
Never crash the whole pipeline because one step failed — catch errors, log them, continue.
```

---

## ⚡ Rate Limiting

| API | Limit | Strategy |
|---|---|---|
| GitHub REST | 5000 req/hr (authenticated) | 1 req/sec default, backoff on 403 |
| Discord Webhook | 5 req / 2 sec | 1-second delay before final push |
| Briefing API (local) | Unlimited | No throttle needed |

---

## 🛡️ Error Handling

| Error | Behaviour |
|---|---|
| Container down | Log error. If `--restart-if-down` passed → `docker restart $CONTAINER` |
| Briefing 500 KeyError | Catch exception, extract response body, log to JSON — pipeline continues |
| GitHub 403 Rate Limit | Log warning, skip remaining requests for that repo, continue to next |
| Missing `GITHUB_PAT` | `fix-env` detects and prints a clear ND-friendly fix message |
| Bad volume mount path | `fix-env` checks if `$VAULT_PATH` exists on disk and warns if not |
| Discord webhook fail | Log warning — never crash on a notification failure |

---

## ✅ Verification Plan

```bash
# Step 1 — Health check
uv run scripts/hyper_brain_ops.py check-health --output output/health.json
cat output/health.json
# Expected: {"status": "healthy", "container": "running", "api": "200"}

# Step 2 — Briefing generation
uv run scripts/hyper_brain_ops.py generate-briefing --output output/briefing.json
# Expected: briefing .md file appears in $VAULT_PATH/Briefings/

# Step 3 — Discord test (use a test webhook URL)
uv run scripts/hyper_brain_ops.py report
# Expected: Discord message received

# Step 4 — Manual review
# Open SKILL.md in Obsidian and verify it matches HYPER-SILLs format
```

---

## 🔗 Related Skills

- `HS-021` 🔄 **VAULT SYNC** — Obsidian Brain Sync
- `HS-013` 🌅 **DAWN HERALD** — Morning Briefing AI
- `HS-023` 🔗 **REPO BRIDGE** — Cross-Repo Sync
- `HS-071` 🪂 **SOFT LANDING** — Fail Gracefully + Fallback Chain

---

*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡ — HS-114 added: 2026-05-31*
