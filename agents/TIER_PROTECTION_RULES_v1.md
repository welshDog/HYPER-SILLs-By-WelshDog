# HS-104 — 🛡️ THE THREE WALLS — Tier Protection Rules (Hardcoded + Configurable + Self)

---
skill_id: HS-104
hero_name: "THE THREE WALLS"
emoji: "🛡️"
version: v1.0
category: agents
depends_on:
  - HS-098  # SACRED SIX — implements Law 2 (PROTECTION)
  - HS-099  # SIX-ORGAN HEART — Shield organ
  - HS-105  # METRICS OATH — required protected_pause_attempts_total metric
provides:
  - tier-protection-model
  - hardcoded-tier-constants
  - self-protection-pattern
  - is-protected-function
related:
  - HS-101  # Sleep Cycle + Anti-Thrash — uses these tiers as pause cohort source
  - HS-091  # Founding Six — Security agent investigates protection-breach signals
  - HS-097  # Hyper Agent Dependency Graph — protection tiers = dep-graph roots
graph_notes: "Shield organ implementation. Hard dependency on HS-098 (Law 2) and HS-099 (anatomy). Every agent that can pause/kill containers MUST import this skill. Tier constants should be copy-pasted verbatim."
---

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/throttle-agent/HYPER-AGENT-BIBLE.md`
**Version:** v1

---

## 🤔 What It Does

The three-layer protection model that stops any agent from pausing, killing, or evicting critical infrastructure. **Hardcoded tiers** + **configurable list** + **self-protection auto-add**. Implements Law 2 (PROTECTION) from [[HS-098]] and the Shield organ from [[HS-099]].

> If a container is protected and an agent tries to pause it, **the pause silently no-ops + a metric fires**. The protected container never knows it was targeted.

---

## 🏗️ Layer 1 — Hardcoded Tiers (NEVER override)

```python
TIER_1 = {"postgres", "redis", "hypercode-core", "hypercode-ollama"}   # data + cognition
TIER_2 = {"crew-orchestrator", "hypercode-dashboard"}                  # coordination + UI
TIER_3 = {"celery-worker"}                                             # task plumbing

PROTECTED_TIERS = TIER_1 | TIER_2 | TIER_3
```

**Rule: tiers 1–3 are NEVER paused. EVER.** No env var, no admin endpoint, no API call can flip it. The list lives in source code.

---

## 🏗️ Layer 2 — Configurable Protect List

```bash
# .env / docker-compose env
THROTTLE_PROTECT_CONTAINERS=throttle-agent,healer-agent,postgres,redis,my-special-service
```

```python
PROTECT_CONTAINERS = set(
    os.getenv("THROTTLE_PROTECT_CONTAINERS", "").split(",")
)
```

For ad-hoc protection of services that aren’t infrastructure tier but still mustn’t be touched.

---

## 🏗️ Layer 3 — Self-Protection (Auto-Add)

```python
# At startup
THROTTLE_ACTIVE_CONTAINER = os.getenv("HOSTNAME")  # Docker sets this to container name
if THROTTLE_ACTIVE_CONTAINER:
    PROTECT_CONTAINERS.add(THROTTLE_ACTIVE_CONTAINER)
```

**An agent never pauses itself.** Always self-add at startup.

---

## 🔍 The Check (one function, three layers)

```python
def is_protected(container: str) -> bool:
    if container in PROTECTED_TIERS:
        return True                     # Layer 1 — hardcoded
    if container in PROTECT_CONTAINERS:
        return True                     # Layer 2 + 3 — configurable + self
    return False

async def pause(container: str):
    if is_protected(container):
        protected_pause_attempts_total.labels(container=container).inc()
        logger.warning("pause_blocked_by_protection", container=container)
        return  # silent no-op
    await docker.pause(container)
```

---

## 📊 Required Metric

Every agent that can pause/kill must export:

```
protected_pause_attempts_total{container=<name>}
```

If this counter rises sustainedly, another agent (or a bug) is trying to touch a protected resource.

---

## 🎯 Tiering New Containers — Decision Tree

```
Is it data storage (DB, cache, blob)?              → TIER_1 (hardcoded)
Is it the brain or coordinator?                    → TIER_1 (hardcoded)
Is it user-facing UI?                              → TIER_2 (hardcoded)
Is it task queue / scheduler plumbing?             → TIER_3 (hardcoded)
Is it a long-running expensive job?                → Layer 2 (configurable)
Is it the throttler/healer itself?                 → Layer 3 (auto-self)
Otherwise — workload, worker, batch job?           → Pausable (no protection)
```

---

## 🚨 Anti-patterns

- **Hardcoded tiers in env vars.** Tiers 1–3 must be source-controlled.
- **Forgetting self-protection.** Always self-add at startup.
- **Empty/whitespace in env list.** Always validate `THROTTLE_PROTECT_CONTAINERS` at startup.

---

## 🧩 Related Skills

- [[HS-098]] 6 Laws — Law 2 (PROTECTION) is this skill
- [[HS-099]] Anatomy of an Agent — Shield organ
- [[HS-101]] Sleep Cycle + Anti-Thrash — uses these tiers as the pause cohort source
- [[HS-091]] Top-Tier Identity Cards — Security agent investigates protection-breach signals
- [[HS-097]] Hyper Agent Dependency Graph — protection tiers correlate with dep-graph roots
