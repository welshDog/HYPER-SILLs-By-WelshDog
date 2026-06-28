# HS-050 — 🛡️ WATCHDOG PRIME — Guardian Watchdog Post-Launch Monitor
**Category:** agents
**Version:** 1.0


---
skill_id: HS-050
hero_name: "WATCHDOG PRIME"
emoji: "🛡️"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-038  # PHASE WARDEN — watchdog starts after Guardian phases are live
  - HS-041  # METRICS FORGE — metrics must be wired before watchdog can evaluate
provides:
  - watchdog-monitoring-prompt
  - post-launch-monitoring
  - auto-heal-pattern
  - discord-alert-integration
related:
  - HS-122  # GUARDIAN WATCHDOG — Python code companion
  - DS-028  # PROGRESSIVE_HEALTH_WAIT — health wait feeds the watchdog loop
graph_notes: "Prompt block to activate post-launch watchdog monitoring — use with HS-122 for the Python implementation."
---
> *"Launch is just the beginning. Watchdog makes sure it stays up."*

---

## 🎯 What It Does
Post-launch watchdog monitoring pattern. After HyperLaunch completes, Watchdog continuously monitors all services and auto-alerts or auto-heals on failures.

## 🌍 Why It Exists
Services can start healthy and degrade minutes later. Watchdog catches that window before users notice.

## ⚙️ How To Use
1. Start Watchdog immediately after successful HyperLaunch
2. Configure `[ALERT_CHANNEL]` for Discord DM alerts
3. Set `[HEAL_ACTIONS]` for auto-recovery steps

---

## 📋 THE PROMPT

```
Start Guardian Watchdog post-launch for stack: [STACK_NAME]
Alert channel: [DISCORD_CHANNEL or DM]
Check interval: [CHECK_INTERVAL_SECONDS] (default: 30)

MONITOR THESE ENDPOINTS:
  http://localhost:8000/health  → hypercode-core
  http://localhost:8099/health  → nemoclaw-agent
  http://localhost:8098/health  → broski-pets-bridge
  http://localhost:8081/health  → crew-orchestrator
  http://localhost:9090/-/healthy → prometheus

HEAL ACTIONS (in order):
1. SOFT: Send Discord alert to Lyndz
2. MEDIUM: docker compose restart [failed_service]
3. HARD: docker compose up -d [failed_service] (if restart fails)
4. ESCALATE: Page Lyndz — human intervention required

NEVER auto-restart: postgres, redis (data services — human decision only)
ALWAYS log: every failure, every heal action, every alert

WATCHDOG LOOP:
```python
while True:
    for service, url in SERVICES.items():
        status = check_health(url)
        if not status.ok:
            handle_failure(service, status, HEAL_ACTIONS)
    time.sleep(CHECK_INTERVAL_SECONDS)
```
```

---

## 🔗 Related Skills
- HS-046 — LAUNCH SOVEREIGN
- HS-038 — PHASE WARDEN (Guardian Bot Phase Map)
- HS-103 — HEALER'S CHORUS (Circuit-Breaker Protocol)

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
