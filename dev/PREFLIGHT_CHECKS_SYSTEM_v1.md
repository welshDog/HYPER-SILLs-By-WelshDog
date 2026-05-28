# HS-048 — ✈️ PREFLIGHT CHECKS — Preflight Checks System

## What it Does
Mandatory pre-launch checks that run BEFORE any `docker compose up`. Validates environment variables, secrets, profiles, and config files are all present and correct.

## When To Use
- ALWAYS before `docker compose up` on a new machine
- After any `.env` changes
- When a service is failing to start and you're not sure why

## THE COMMANDS
```powershell
# Core preflight (always run this minimum)
python scripts/env_check.py --core --secrets --profile discord

# Full preflight with brain + grafana cloud
python scripts/env_check.py --core --secrets --profile discord --brain --grafana-cloud

# Bash wrapper (Linux/WSL)
bash scripts/env-check.sh --core --secrets --profile discord

# Files:
# Engine:      scripts/env_check.py
# Bash wrap:   scripts/env-check.sh
# Tests:       backend/tests/unit/test_env_check_script.py ✅
```

## What It Checks
```
CHECKS PERFORMED:

✅ --core
  Required .env keys for hypercode-core
  Missing = ERROR (blocks launch)

✅ --secrets
  No secrets committed to git
  .env files not in git history

✅ --profile discord
  broski-bot .env keys present
  DISCORD_GUILD_ID (warn if missing, not block)
  DISCORD_BOT_TOKEN present

✅ --brain
  BROski-Obsidian-Brain env vars

✅ --grafana-cloud
  Grafana Cloud credentials present

KNOWN DUPLICATE WARNINGS (expected, not errors):
  BROSKIE_PETS_ENABLED — root .env duplicate
  PETS_WEBHOOK_SECRET  — root .env duplicate

RULE: If preflight fails — fix env BEFORE docker compose up.
Never skip. Never --force.
```

## Related Skills
- HS-046 HYPERLAUNCH UNIFIED COMMANDER
- HS-031 V2.4 Sacred Rules
- HS-064 Dev Commands Cheat Sheet

---
*Source: HyperCode-V2.4 hyperlaunch.py + scripts/env_check.py | Category: dev/*
