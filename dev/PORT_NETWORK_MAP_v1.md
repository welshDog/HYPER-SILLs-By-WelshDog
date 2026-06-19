# HS-061 — 🔌 THE PORT WARDEN — Port + Network Map

**Category:** dev
**Version:** 1.0

> *"Every published port + every Docker network. Never guess or collide again."*

---

## 🎯 What It Does

The canonical host-port and network map for HyperCode V2.4 — all bound to
`127.0.0.1` (never public) — so an AI wires service-to-service calls correctly.

## 🌍 Why It Exists

60+ published ports and 5 networks. Wrong port/network = a call that silently
can't connect (e.g. prometheus can't scrape an agent not on a shared net).

## ⚙️ How To Use

Paste for Docker/networking/scrape work.

---

## 📋 THE PROMPT

```
HyperCode V2.4 — key host ports (all 127.0.0.1, internal only):
  8000 core API        8081 crew-orchestrator   8088 dashboard
  8095 hyperhealth     8096 safety-shepherd      8098 broski-pets-bridge
  8099 nemoclaw        8077 agent-registry        8100 brain engine
  3301/3302/3303 brain agents
  9090 prometheus  3001 grafana  3100 loki  3200 tempo  4040 pyroscope
  4317/4318 OTLP   9100 node-exporter  9808 celery-exporter
  6379 redis  5432 postgres  9000/9001 minio  2375 docker-socket-proxy

Networks (compose):
  app-net / backend-net → core services
  data-net   → redis, postgres, chroma, minio        (internal: true)
  obs-net    → prometheus, grafana, loki, tempo        (internal: true)
  agents-net → all agents (+ prometheus, for scraping)
  frontend-net → dashboard / IDE

Rule: a scraper/caller must SHARE a network with its target. prometheus is on
obs-net + agents-net; grafana needed data-net added to read postgres (P1-2).
```

## ✅ Example

> "Why is the safety panel empty?" → grafana wasn't on data-net → couldn't reach
> postgres:5432. Add data-net. (Real P1-2 fix.)

## 🔗 Related Skills

[[CONTAINER_STACK_REFERENCE_v1]] · [[ARCHITECTURE_QUICK_REF_v1]]
