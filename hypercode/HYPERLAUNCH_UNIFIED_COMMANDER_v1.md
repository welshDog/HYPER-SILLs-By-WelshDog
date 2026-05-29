# HS-046 — 🚀 LAUNCH SOVEREIGN — HyperLaunch Unified Commander
**Category:** hypercode
**Version:** 1.0

> *"One script to launch the entire HyperFocus stack. Preflight to running in one command."*

---

## 🎯 What It Does
The HyperLaunch unified launch pattern — a single commander script that handles preflight checks, service ordering, health validation, and post-launch monitoring for the entire V2.4 stack.

## 🌍 Why It Exists
Launching 30+ containers in the wrong order breaks dependencies. HyperLaunch handles the sequencing, health gates, and fallbacks automatically.

## ⚙️ How To Use
1. Use as the reference pattern when modifying `hyperlaunch.py`
2. Paste when building any multi-service launch orchestration

---

## 📋 THE PROMPT

```
Implement HyperLaunch unified commander pattern for: [STACK or SERVICE_GROUP]

LAUNCH SEQUENCE:
1. PREFLIGHT — env check, secrets validation, port availability
2. FOUNDATION — data-net services first (postgres, redis, minio)
3. CORE — hypercode-core API (depends on foundation)
4. AGENTS — all agents (depend on core)
5. OBSERVABILITY — prometheus, grafana, loki, tempo
6. OPTIONAL PROFILES — discord, nemoclaw, etc.

HEALTH GATE PATTERN (between each stage):
```python
def wait_healthy(service: str, url: str, timeout: int = 60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                print(f"✅ {service} healthy")
                return True
        except:
            pass
        time.sleep(2)
    raise TimeoutError(f"❌ {service} failed health check after {timeout}s")
```

FALLBACK RULE:
- Stage fails health gate → rollback that stage, alert + stop
- NEVER proceed to next stage with unhealthy dependencies
- ALWAYS log launch result to launch_log table

COMMAND:
```powershell
python scripts/hyperlaunch.py --profile discord --verify
```
```

---

## 🔗 Related Skills
- HS-047 — 4-Tier ServiceSpec Launch Pattern
- HS-048 — Preflight Checks System
- HS-049 — Progressive Health Wait Pattern

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
