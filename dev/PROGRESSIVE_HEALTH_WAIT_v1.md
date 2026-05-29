# HS-049 — ⏳ PATIENCE ENGINE — Progressive Health Wait Pattern
**Category:** dev
**Version:** 1.0

> *"Wait smart. Not dumb. Exponential backoff with a clear timeout."*

---

## 🎯 What It Does
The progressive health wait pattern used across HyperLaunch. Waits for a service to become healthy using exponential backoff — fast retries first, slower retries later, hard timeout at the end.

## 🌍 Why It Exists
Fixed-interval polling wastes time when services start fast and hammers them when they're slow. Progressive backoff is the Goldilocks solution.

## ⚙️ How To Use
1. Use this pattern anywhere you need to wait for a service to become healthy
2. Replace any `time.sleep(X)` polling loop with this
3. Always set a `max_wait` — never infinite loops

---

## 📋 THE PROMPT

```
Implement progressive health wait for service: [SERVICE_NAME]
Health URL: [HEALTH_URL]
Max wait: [MAX_WAIT_SECONDS] (default: 120)

```python
import time
import requests

def wait_healthy_progressive(
    service: str,
    url: str,
    max_wait: int = 120,
    initial_interval: float = 0.5,
    max_interval: float = 10.0,
    backoff_factor: float = 1.5
) -> bool:
    interval = initial_interval
    elapsed = 0
    attempt = 0

    print(f"⏳ Waiting for {service} at {url}...")

    while elapsed < max_wait:
        attempt += 1
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                print(f"✅ {service} healthy after {elapsed:.1f}s ({attempt} attempts)")
                return True
        except Exception as e:
            pass

        time.sleep(interval)
        elapsed += interval
        interval = min(interval * backoff_factor, max_interval)

    print(f"❌ {service} not healthy after {max_wait}s")
    return False

# Usage
if not wait_healthy_progressive('hypercode-core', 'http://localhost:8000/health'):
    raise SystemExit(1)
```

RULE: Always use localhost NOT 127.0.0.1 (IPv6 fix for Docker healthchecks)
```

---

## 🔗 Related Skills
- HS-046 — LAUNCH SOVEREIGN
- HS-047 — TIER FORGE
- HS-101 — DREAM GUARD (Sleep Cycle Anti-Thrash)

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
