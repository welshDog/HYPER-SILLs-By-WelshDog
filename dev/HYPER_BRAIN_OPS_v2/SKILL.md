# 🛠️ HS-114 — BRAIN OPS
**Skill ID:** `HYPER_BRAIN_OPS_v2`  
**Category:** `dev`  
**Version:** 2.0.0  
**Author:** WelshDog + Gordon Review  
**Last Updated:** 2026-05-31

---

## 🧠 What This Skill Does

Maintains the Hyper Brain infrastructure automatically. Verifies container health, triggers the Morning Briefing API, syncs cross-repo GitHub issues into the Obsidian vault, and delivers a **partial-success status report** via Discord. Includes daily auto-mode and ad-hoc repair mode.

---

## 📦 Directory Structure

```text
dev/HYPER_BRAIN_OPS_v2/
├── SKILL.md                        # This file — agent instructions
└── scripts/
    └── hyper_brain_ops.py          # CLI runner
```

---

## 🔐 Required Environment Variables

```env
VAULT_PATH=H:/HYPERFOCUSZONE/HperCore/BROski-Obsidian-Brain-for-HyperFocus-z0ne
GITHUB_PAT=ghp_xxxxx
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE
BRIEFING_API_URL=http://localhost:8100
DOCKER_CONTAINER=hyper-brain
GITHUB_REPOS=welshDog/HYPER-SILLs-By-WelshDog,welshDog/HyperFocusZone,welshDog/BROski,welshDog/HyperCodeAI
```

Store these in a `.env` file alongside the script and load with `uv run` or `python-dotenv`.

---

## 🔧 Subcommands

| Subcommand | What It Does |
|---|---|
| `fix-env` | Diagnoses vault path, Docker, port, tokens. Run this FIRST. |
| `check-health` | Pings Docker container + API. Use `--restart-if-down` for auto-restart. |
| `generate-briefing` | POSTs to `/briefing/generate`. Writes `.md` to `VAULT_PATH/Briefings/`. |
| `sync-github` | Pulls open issues from all configured repos. Writes to `VAULT_PATH/GitHub-Inbox/`. |
| `report` | Reads all `output/*_status.json` files. Sends ONE emoji table to Discord. |

All subcommands support `--output <file.json>` to dump status for agent reasoning.

---

## 🏃 Usage Modes

### Daily Auto Mode (Windows Task Scheduler)

```cmd
cmd /c "cd /d C:\path\to\HYPER-SILLs-By-WelshDog\dev\HYPER_BRAIN_OPS_v2 && uv run scripts\hyper_brain_ops.py check-health --output output\health_status.json & uv run scripts\hyper_brain_ops.py generate-briefing --output output\briefing_status.json & uv run scripts\hyper_brain_ops.py sync-github --output output\sync_status.json & uv run scripts\hyper_brain_ops.py report"
```

> ⚠️ Use `&` NOT `&&` on Windows — so each step runs regardless of previous step outcome.

### Repair Mode (Ad-hoc)

```bash
uv run scripts/hyper_brain_ops.py fix-env
uv run scripts/hyper_brain_ops.py check-health --restart-if-down
```

---

## 📊 Partial-Success Discord Report Format

The `report` command reads all status JSONs and sends ONE message:

```
🧠 BRAIN OPS — 2026-05-31 08:00
✅ check-health: OK (2.1s)
✅ generate-briefing: OK (7.8s)
⚠️ sync-github: PARTIAL (47/52 issues — timeout on welshDog/HyperCodeAI)
✅ vault-commit: SKIPPED (Obsidian Git owns commits)
❌ discord: FAILED (403 — check DISCORD_WEBHOOK_URL)
```

You get **visibility even if something fails** — no silent mornings. 🔕

---

## 🔐 Rate Limiting

- **GitHub API**: 1 req/sec default. On 403/429: log warning, skip repo, emit ⚠️ in report.
- **Rate budget file** (`output/rate_budget.json`): tracks reads/writes used this hour. Script checks before running sync.
- **Discord Webhook**: 1-second delay before posting to respect 5 req/2s limit.

---

## 📁 Vault-Git Contract

```markdown
## Vault Sync Contract

- HS-114 writes .md files ONLY (Briefings/ and GitHub-Inbox/).
- Obsidian Git plugin owns all git commits when Obsidian is open.
- If running HEADLESS (no Obsidian open / Task Scheduler):
  - Script checks: git diff-index --quiet HEAD
  - Only commits if there ARE changes.
  - Commit message: "ops: sync briefings and github inbox [timestamp]"
- NEVER run git operations from two sources simultaneously.
```

---

## 🧪 Verification Tests

```bash
# 1. Environment doctor
uv run scripts/hyper_brain_ops.py fix-env

# 2. Health check with JSON output
uv run scripts/hyper_brain_ops.py check-health --output output/health_status.json
# → Check output/health_status.json for {"status": "ok"}

# 3. Briefing generation
uv run scripts/hyper_brain_ops.py generate-briefing --output output/briefing_status.json
# → Check VAULT_PATH/Briefings/ for today's .md file

# 4. GitHub sync
uv run scripts/hyper_brain_ops.py sync-github --output output/sync_status.json
# → Check VAULT_PATH/GitHub-Inbox/ for issue files

# 5. Discord report
uv run scripts/hyper_brain_ops.py report
# → Verify Discord channel receives the emoji table
```

---

## 🗺️ Rollout Phases

| Phase | Week | Goal |
|---|---|---|
| 1 | 1-2 | Set .env → run manual loop → briefing lands in H: vault |
| 2 | 3 | Add partial-success handling — status JSONs + resilient chain |
| 3 | 4 | Vault-git contract locked, failure scenario testing |
| 4 | 5 | Windows Task Scheduler deploy — 7-day unattended run |
| 5 | Q3 2026 | Add PREFLIGHT_CHECKS_SYSTEM_v1 + TEST_STATUS_REPORT_v1 |

---

## 🤝 Related Skills

| Skill | Relationship |
|---|---|
| `OBSIDIAN_GIT_VAULT_v1` | Vault versioning — owns git commits when Obsidian is open |
| `CROSS_REPO_SYNC_v1` | Conceptual pattern reference for sync-github logic |
| `PREFLIGHT_CHECKS_SYSTEM_v1` | Future Phase 5 — pre-run system checks |
| `TEST_STATUS_REPORT_v1` | Future Phase 5 — measuring briefing effectiveness |

---

## 💡 Agent Prompt Block

When using this skill, an agent should:

1. Always run `fix-env` first in a new environment.
2. Run subcommands with `--output` flags so results are machine-readable.
3. Always run `report` last — it reads all JSON statuses and sends the Discord summary.
4. Never use `&&` chaining on Windows — use `&` or separate calls.
5. If `check-health` fails and `--restart-if-down` is set, wait 10s before next step.
6. Log all runs to `output/ops.log` with timestamps.
