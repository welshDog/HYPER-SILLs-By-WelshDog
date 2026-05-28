# HS-046 — 🚀 HYPERLAUNCH UNIFIED COMMANDER — HyperLaunch Unified Commander

## What it Does
The master launch orchestrator for HyperCode V2.4. Manages ordered service startup, dependency resolution, and health verification across all 30+ containers.

## When To Use
- Starting the full V2.4 stack from scratch
- Debugging startup order issues between services
- Building new launch scripts for V2.4

## THE PATTERN
```python
# hyperlaunch.py — unified launch commander pattern
import subprocess
import time
import sys
from dataclasses import dataclass
from typing import Optional

@dataclass
class ServiceSpec:
    name: str
    profile: Optional[str] = None
    depends_on: list[str] = None
    health_url: Optional[str] = None
    health_timeout: int = 60
    tier: int = 1  # Launch tier (1=first, 4=last)

# 4-TIER LAUNCH ORDER:
# Tier 1: Infrastructure (postgres, redis, minio)
# Tier 2: Core API (hypercode-core)
# Tier 3: Agents (nemoclaw, crew-orchestrator, etc.)
# Tier 4: Bots + UI (broski-bot, dashboard)

LAUNCH_SEQUENCE = [
    ServiceSpec('postgres', tier=1),
    ServiceSpec('redis', tier=1),
    ServiceSpec('minio', tier=1),
    ServiceSpec('hypercode-core', tier=2,
                depends_on=['postgres','redis'],
                health_url='http://localhost:8000/health'),
    ServiceSpec('nemoclaw-agent', tier=3,
                health_url='http://localhost:8099/health'),
    ServiceSpec('crew-orchestrator', tier=3,
                health_url='http://localhost:8081/health'),
    ServiceSpec('broski-bot', profile='discord', tier=4),
    ServiceSpec('hypercode-dashboard', tier=4,
                health_url='http://localhost:8088/health'),
]

def launch(profile: str = None, tier_max: int = 4):
    """Launch services in tier order with health verification."""
    for tier in range(1, tier_max + 1):
        services = [s for s in LAUNCH_SEQUENCE if s.tier == tier]
        for svc in services:
            _start_service(svc)
        _verify_tier_health(services)

# Run preflight BEFORE launch (see HS-048)
# python scripts/env_check.py --core --secrets --profile discord
```

## Related Skills
- HS-047 4-Tier ServiceSpec Launch Pattern
- HS-048 PREFLIGHT CHECKS System
- HS-037 ARCHITECTURE QUICK REF

---
*Source: HyperCode-V2.4 hyperlaunch.py | Category: hypercode/*
