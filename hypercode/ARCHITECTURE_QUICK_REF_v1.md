# HS-037 — ⚡ GRID MASTER — Architecture Quick Ref (Ports + Networks)
**Category:** hypercode
**Version:** 1.0

> *"The full V2.4 network map in one paste. Never guess a port again."*

---

## 🎯 What It Does
The complete HyperCode V2.4 network topology — all ports, all Docker networks, all key services. Paste into any session to give AI instant spatial awareness of the system.

## 🌍 Why It Exists
With ~30 containers and 4 networks, AI without this context will suggest wrong ports, wrong networks, or create conflicts.

## ⚙️ How To Use
1. Paste when working on Docker, networking, or service-to-service communication
2. AI uses exact ports and networks — no guessing

---

## 📋 THE PROMPT

```
You are working on HyperCode V2.4. Use this architecture reference:

DOCKER NETWORKS:
  app-net    → core services (internal)
  data-net   → redis, postgres, chroma, minio (internal)
  obs-net    → prometheus, grafana, loki, tempo (internal)
  agent-net  → all agents
  agents-net → broski-bot + hyper-agents

  NOTE: minio is on BOTH data-net AND obs-net — correct, intentional

KEY PORTS:
  8000  hypercode-core API         8081  crew-orchestrator
  8088  hypercode-dashboard         8095  hyperhealth-api
  8098  broski-pets-bridge          8099  nemoclaw-agent
  9090  prometheus                  3001  grafana
  3100  loki                        3200  tempo
  6379  redis                       5432  postgres

REDIS DB SPLIT (NEVER mix these):
  DB 1 = cache
  DB 2 = rate limits

HEALTHCHECK RULE:
  Always use `localhost` NOT `127.0.0.1` (IPv6 fix)

PROMETHEUS:
  ACTIVE config: monitoring/prometheus/prometheus.yml
  Root prometheus.yml = STALE — ignore it

ALEMBIC MIGRATIONS:
  Current: up to 015
  If missing migration: alembic stamp <prev> → upgrade head

[INPUT: describe the networking/Docker task]
```

---

## 🔗 Related Skills
- HS-031 — V2.4 Sacred Rules
- HS-060 — 50 Container Stack Reference
- HS-061 — 42-Port Network Map

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
