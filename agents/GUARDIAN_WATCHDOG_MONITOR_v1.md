# HS-122 — 🛡️ GUARDIAN WATCHDOG — Guardian Watchdog Post-Launch Monitor
**Category:** agents
**Version:** 1.0


---
skill_id: HS-122
hero_name: "GUARDIAN WATCHDOG"
emoji: "🔭"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-038  # PHASE WARDEN — watchdog operates within Guardian phases
  - HS-041  # METRICS FORGE — metrics must be wired before watchdog can evaluate
provides:
  - watchdog-code-pattern
  - service-health-loop
  - failure-restart-logic
  - consecutive-failure-counter
related:
  - HS-050  # WATCHDOG PRIME — prompt-block companion to this code pattern
  - DS-028  # PROGRESSIVE_HEALTH_WAIT — health wait pattern used in restart logic
graph_notes: "Python implementation of the post-launch watchdog — code companion to HS-050 WATCHDOG PRIME."
problem_keywords:
  - crash
  - crashed
  - restart crashed service
  - watchdog
  - monitor and restart
  - keeps dying
  - auto restart
  - won't stay up
  - service health loop

---
## What it Does
Post-launch watchdog monitor that continuously verifies all services remain healthy after startup. Triggers alerts and optionally restarts failing services.

## When To Use
- Setting up continuous health monitoring after launch
- Building self-healing restart logic for any service
- Wiring up Prometheus alerts for service health

## THE PATTERN
```python
import asyncio
import aiohttp
from datetime import datetime

class GuardianWatchdog:
    def __init__(self, services: list[dict], interval: int = 30):
        self.services = services
        self.interval = interval  # seconds between checks
        self.failures: dict[str, int] = {}  # service → consecutive failures
        self.MAX_FAILURES = 3  # failures before restart attempt

    async def watch(self):
        """Continuous watchdog loop."""
        print(f"🛡️ Guardian Watchdog started — monitoring {len(self.services)} services")
        while True:
            await self._check_all()
            await asyncio.sleep(self.interval)

    async def _check_all(self):
        for svc in self.services:
            healthy = await self._ping(svc['health_url'])
            name = svc['name']

            if healthy:
                if name in self.failures:
                    print(f"✅ {name} recovered")
                    del self.failures[name]
            else:
                self.failures[name] = self.failures.get(name, 0) + 1
                count = self.failures[name]
                print(f"⚠️ {name} unhealthy ({count}/{self.MAX_FAILURES})")

                if count >= self.MAX_FAILURES:
                    await self._handle_failure(name, svc)

    async def _handle_failure(self, name: str, svc: dict):
        # Log to Prometheus / emit to MetricsEngine (HS-041)
        # Attempt restart if restart_cmd provided
        if restart_cmd := svc.get('restart_cmd'):
            print(f"🔄 Attempting restart: {name}")
            # Note: restart is logged, human notified
            # Sacred Rule: autonomous restarts OK for stateless services
            # Data services (postgres, redis) = human approval required
        else:
            print(f"🚨 ALERT: {name} needs manual intervention")
            await self._notify(name)  # Discord alert via broski-bot

    async def _ping(self, url: str) -> bool:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url, timeout=5) as r:
                    return r.status == 200
        except:
            return False
```

## Related Skills
- HS-046 HYPERLAUNCH UNIFIED COMMANDER
- HS-038 GUARDIAN BOT PHASE MAP
- HS-103 HEALER’S CHORUS Circuit-Breaker

---
*Source: HyperCode-V2.4 hyperlaunch.py | Category: agents/*
