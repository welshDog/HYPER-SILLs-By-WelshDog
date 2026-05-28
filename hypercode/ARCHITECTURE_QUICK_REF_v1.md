# HS-037 — ⚡ ARCHITECTURE QUICK REF — Architecture Quick Ref (Ports + Networks)

## What it Does
Instant reference for HyperCode V2.4 network topology and port map. Use this before touching docker-compose files, nginx config, or any service-to-service communication.

## When To Use
- Configuring a new service in V2.4
- Debugging network connectivity between containers
- Checking which port a service runs on
- Onboarding a new agent to the stack

## THE REFERENCE
```
V2.4 NETWORK TOPOLOGY:

Networks:
  app-net     → core services (internal)
  data-net    → redis, postgres, chroma, minio (internal)
  obs-net     → prometheus, grafana, loki, tempo (internal)
  agent-net   → all agents
  agents-net  → broski-bot + hyper-agents

⚠️ minio is on BOTH data-net AND obs-net — correct, intentional
⚠️ data-net + obs-net = internal: true — NEVER expose externally

KEY PORTS:
  8000  hypercode-core API
  8081  crew-orchestrator
  8088  hypercode-dashboard
  8095  hyperhealth-api
  8098  broski-pets-bridge
  8099  nemoclaw-agent (code health "Alive")
  9090  prometheus
  3001  grafana
  3100  loki
  3200  tempo
  6379  redis
  5432  postgres

HEALTH CHECK URLS:
  curl http://localhost:8000/health   # core
  curl http://localhost:8098/health   # broski-pets-bridge
  curl http://localhost:8099/health   # nemoclaw-agent

⚠️ hypercore healthcheck → use localhost NOT 127.0.0.1 (IPv6 fix)

DOCKER COMPOSE FILES (20 total, profile-dependent):
  docker-compose.yml              — main stack
  docker-compose.secrets.yml      — secrets injection (always alongside main)
  docker-compose.core.yml         — core + broski-bot (profile:discord)
  docker-compose.brain.yml        — brain agent cluster
  docker-compose.agents.yml       — full agent swarm (42KB)
```

## Related Skills
- HS-031 V2.4 Sacred Rules
- HS-060 50 Container Stack Reference
- HS-061 42-Port Network Map

---
*Source: HyperCode-V2.4 CLAUDE.md §4 | Category: hypercode/*
