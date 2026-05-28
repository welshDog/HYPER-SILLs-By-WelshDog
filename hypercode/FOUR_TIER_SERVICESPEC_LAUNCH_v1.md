# HS-047 — 🏗️ FOUR TIER SERVICESPEC — 4-Tier ServiceSpec Launch Pattern

## What it Does
The 4-tier service launch pattern that controls startup order in HyperCode V2.4. Ensures infrastructure starts before core, core starts before agents, agents start before bots.

## When To Use
- Adding a new service to V2.4 and figuring out its tier
- Debugging "service not ready" startup errors
- Designing launch order for any multi-container system

## THE TIERS
```
4-TIER SERVICESPEC LAUNCH PATTERN:

Tier 1 — INFRASTRUCTURE (start first, no deps)
  Services: postgres, redis, minio, chroma
  Networks: data-net, obs-net
  Rule: NEVER depend on Tier 2+
  Health: TCP port check
  Wait: until port accepts connections

Tier 2 — CORE API (after Tier 1 healthy)
  Services: hypercode-core (port 8000)
  Networks: app-net, data-net
  Depends on: postgres, redis
  Health: GET /health → 200
  Wait: up to 60s with exponential backoff

Tier 3 — AGENTS (after Tier 2 healthy)
  Services: nemoclaw-agent, crew-orchestrator,
            hyperhealth-api, broski-pets-bridge
  Networks: agent-net, app-net
  Depends on: hypercode-core
  Health: GET /health → 200 on each port
  Ports: 8081, 8095, 8098, 8099

Tier 4 — BOTS + UI (after Tier 3 healthy)
  Services: broski-bot (profile:discord),
            hypercode-dashboard
  Networks: agents-net
  Depends on: full stack up
  Health: process check (bots) / port check (UI)
  Profile: discord (bot is profile-gated)

SERVICESPEC DATACLASS:
  name: str
  profile: Optional[str]     # docker compose profile
  depends_on: list[str]      # services that must be healthy first
  health_url: Optional[str]  # URL to hit for health check
  health_timeout: int        # seconds to wait (default 60)
  tier: int                  # 1-4
```

## Related Skills
- HS-046 HYPERLAUNCH UNIFIED COMMANDER
- HS-048 PREFLIGHT CHECKS System
- HS-049 PROGRESSIVE HEALTH WAIT Pattern

---
*Source: HyperCode-V2.4 hyperlaunch.py | Category: hypercode/*
