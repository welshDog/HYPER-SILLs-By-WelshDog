# HS-104 — Tier Protection Rules (Hardcoded + Configurable + Self) 🛡️

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

**Rule: tiers 1–3 are NEVER paused. EVER.** This is sacred — no env var, no admin endpoint, no API call can flip it. The list lives in source code.

If you find yourself wanting to pause one of these, the answer is: you shouldn't be. Spawn more capacity instead.

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

For ad-hoc protection of services that aren't infrastructure tier but still mustn't be touched (e.g. a long-running ML training container). Comma-separated, no spaces.

---

## 🏗️ Layer 3 — Self-Protection (Auto-Add)

```python
# At startup
THROTTLE_ACTIVE_CONTAINER = os.getenv("HOSTNAME")  # Docker sets this to container name
if THROTTLE_ACTIVE_CONTAINER:
    PROTECT_CONTAINERS.add(THROTTLE_ACTIVE_CONTAINER)
```

**An agent never pauses itself.** Always self-add. If you forget and the agent pauses its own container mid-action, you lose state + the audit log entry never lands.

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
        logger.warning(
            "pause_blocked_by_protection",
            container=container,
        )
        return  # silent no-op
    await docker.pause(container)
```

---

## 📊 Required Metric

Every agent that can pause/kill must export:

```
protected_pause_attempts_total{container=<name>}
```

If this counter rises sustainedly for a non-tier-1 container, it means another agent (or a bug) is *trying* to touch a protected resource. Investigate. Either:
- The protected list is wrong (remove from list, audit why it was added)
- A bug in the calling agent (file an issue)
- A genuine threat to the system (escalate to Security agent — [[HS-091]])

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

Tiers 4–6 are *pausable* — see [[HS-101]] for which gets paused at which pressure.

---

## 🚨 Anti-patterns

- **Hardcoded tiers in env vars.** Tiers 1–3 must be source-controlled — env-driven invites accident.
- **Forgetting self-protection.** Easy mistake; always self-add at startup.
- **Adding a tier-1 to Layer 2.** Redundant but harmless. Adding a non-tier-1 to Layer 1 = sacred-rule violation, requires code change + review.
- **Empty/whitespace in env list.** `THROTTLE_PROTECT_CONTAINERS=` with no value or trailing comma silently empties the set. Always validate at startup.

---

## 🧩 Related Skills

- [[HS-098]] 6 Laws — Law 2 (PROTECTION) is this skill
- [[HS-099]] Anatomy of an Agent — Shield organ
- [[HS-101]] Sleep Cycle + Anti-Thrash — uses these tiers as the pause cohort source
- [[HS-091]] Top-Tier Identity Cards — Security agent investigates protection-breach signals
- [[HS-097]] Hyper Agent Dependency Graph — protection tiers correlate with dep-graph roots
