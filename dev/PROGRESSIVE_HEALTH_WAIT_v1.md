# HS-049 — ⏳ PROGRESSIVE HEALTH WAIT — Progressive Health Wait Pattern

## What it Does
Exponential backoff health check pattern used during service startup. Waits intelligently for services to become healthy without hammering them or timing out too early.

## When To Use
- Any service startup sequence that depends on another service being ready
- Replacing naive `sleep 5` calls in launch scripts
- Health-checking in CI/CD pipelines

## THE PATTERN
```python
import asyncio
import aiohttp
import time
from typing import Optional

async def wait_for_healthy(
    url: str,
    service_name: str,
    timeout: int = 60,
    initial_wait: float = 1.0,
    max_wait: float = 10.0,
    backoff_factor: float = 1.5
) -> bool:
    """
    Progressive health wait with exponential backoff.
    Waits for GET {url} to return 200.
    """
    wait = initial_wait
    deadline = time.time() + timeout
    attempts = 0

    async with aiohttp.ClientSession() as session:
        while time.time() < deadline:
            attempts += 1
            try:
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
                        print(f"✅ {service_name} healthy after {attempts} attempts")
                        return True
            except Exception:
                pass  # Not ready yet

            print(f"⏳ {service_name} not ready, waiting {wait:.1f}s... ({attempts})")
            await asyncio.sleep(wait)
            wait = min(wait * backoff_factor, max_wait)

    print(f"❌ {service_name} failed to become healthy within {timeout}s")
    return False

# Batch health check for a whole tier
async def wait_for_tier(services: list[dict]) -> bool:
    tasks = [wait_for_healthy(**svc) for svc in services if svc.get('health_url')]
    results = await asyncio.gather(*tasks)
    return all(results)

# Usage in launch sequence
await wait_for_healthy(
    url='http://localhost:8000/health',
    service_name='hypercode-core',
    timeout=60
)
```

## Related Skills
- HS-046 HYPERLAUNCH UNIFIED COMMANDER
- HS-047 4-Tier ServiceSpec Launch Pattern
- HS-101 DREAM GUARD Sleep Cycle Anti-Thrash

---
*Source: HyperCode-V2.4 hyperlaunch.py | Category: dev/*
