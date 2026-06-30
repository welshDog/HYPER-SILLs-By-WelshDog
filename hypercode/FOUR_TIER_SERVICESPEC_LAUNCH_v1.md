# HS-047 — 🏗️ TIER FORGE — 4-Tier ServiceSpec Launch Pattern
**Category:** hypercode
**Version:** 1.0

> *"Every service has a tier. Tiers have order. Order prevents chaos."*

---

## 🎯 What It Does
The 4-tier service specification and launch ordering pattern for HyperCode V2.4. Ensures services always start in the right order with the right dependencies.

## 🌍 Why It Exists
Docker compose doesn't guarantee startup order by health. This pattern adds intelligent tier-based sequencing on top.

## ⚙️ How To Use
1. Classify any new service into one of the 4 tiers
2. Launch tiers in order — never skip or parallel across tiers
3. Each tier must be fully healthy before the next starts
problem_keywords:
  - service tiers
  - launch pattern
  - servicespec
  - tiered launch

---

## 📋 THE PROMPT

```
Classify and launch services using the 4-Tier ServiceSpec pattern:

TIER 1 — FOUNDATION (start first, everything depends on these)
  - postgres (port 5432, data-net)
  - redis (port 6379, data-net)
  - minio (port 9000, data-net + obs-net)
  Health gate: all 3 healthy before proceeding

TIER 2 — CORE (depends on Tier 1)
  - hypercode-core (port 8000, app-net)
  Health gate: /health returns 200 before proceeding

TIER 3 — AGENTS (depends on Tier 2)
  - All agents in agent-net
  - nemoclaw-agent (port 8099)
  - broski-pets-bridge (port 8098)
  - crew-orchestrator (port 8081)
  Health gate: all registered agents healthy

TIER 4 — OBSERVABILITY + OPTIONAL (depends on Tier 2, parallel with Tier 3)
  - prometheus (port 9090)
  - grafana (port 3001)
  - loki (port 3100)
  - tempo (port 3200)
  - discord profile: broski-bot

ServiceSpec schema for new services:
```yaml
name: [SERVICE_NAME]
tier: [1|2|3|4]
networks: [app-net|data-net|obs-net|agent-net]
health_url: http://[SERVICE_NAME]:[PORT]/health
depends_on_healthy: [[DEPENDENCY_1], [DEPENDENCY_2]]
```
```

---

## 🔗 Related Skills
- HS-046 — LAUNCH SOVEREIGN (HyperLaunch Commander)
- HS-048 — Preflight Checks System
- HS-037 — GRID MASTER (Architecture Quick Ref)

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
