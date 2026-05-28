# HS-048 — ✈️ PREFLIGHT ACE — Preflight Checks System

> *"Never launch without running preflight. It's the difference between a clean start and a 2am debug session."*

---

## 🎯 What It Does
The complete preflight check system for HyperCode V2.4. Validates environment, secrets, port availability, and dependencies BEFORE docker compose up.

## 🌍 Why It Exists
Launching with missing env vars, wrong secrets, or occupied ports wastes hours. Preflight catches everything in 10 seconds.

## ⚙️ How To Use
1. ALWAYS run before `docker compose up` on a new machine or after .env changes
2. Fix every RED item before proceeding
3. YELLOW items = warnings, can proceed with caution

---

## 📋 THE PROMPT

```
Run HyperFocus preflight checks for: [PROFILE — core|discord|full]

COMMAND:
```powershell
# Core + secrets check
python scripts/env_check.py --core --secrets

# Full stack with discord profile
python scripts/env_check.py --core --secrets --profile discord

# Full including grafana cloud + brain
python scripts/env_check.py --core --secrets --profile discord --brain --grafana-cloud

# Bash wrapper
bash scripts/env-check.sh --core --secrets --profile discord
```

CHECK CATEGORIES:
✔ ENV VARS — all required vars present in .env
✔ SECRETS — no secrets accidentally in git history
✔ PORTS — 8000, 8081, 8088, 8095, 8098, 8099, 9090, 3001 all free
✔ DOCKER — docker-ce-cli available, socket accessible
✔ PROFILES — requested profile vars all present

WARNINGS (YELLOW — proceed with caution):
- DISCORD_GUILD_ID missing (warn, not fail)
- Root .env duplicate keys (BROSKIE_PETS_ENABLED, PETS_WEBHOOK_SECRET)

FAILS (RED — fix before proceeding):
- Any CRITICAL env var missing
- Port conflict on core services
- .env file committed to git

Files: scripts/env_check.py (engine) · scripts/env-check.sh (bash)
Tests: backend/tests/unit/test_env_check_script.py ✅
```

---

## 🔗 Related Skills
- HS-046 — LAUNCH SOVEREIGN
- HS-031 — V2.4 Sacred Rules
- HS-039 — CLOSE PROTOCOL (Session End Checklist)

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*