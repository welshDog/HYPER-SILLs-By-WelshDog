# 🛡️ HS-104 — THE THREE WALLS — Tier Protection Rules (Hardcoded + Configurable + Self)

---
skill_id: HS-104
hero_name: "THE THREE WALLS"
emoji: "🛡️"
version: v1.0
category: agents
depends_on:
  - HS-002  # SIX_LAWS_OF_AGENTS — implements Law 2 (PROTECTION)
  - HS-001  # ANATOMY_OF_AN_AGENT — Shield organ lives in anatomy
provides:
  - tier-protection-model
  - hardcoded-tier-constants
  - self-protection-pattern
  - is-protected-function
related:
  - HS-003  # AGENT_LIFECYCLE_STATE_MACHINE
  - HS-009  # HYPER_AGENT_ROSTER — protection tiers = dep-graph roots
graph_notes: "Shield organ implementation. Every agent that can pause/kill containers MUST import this skill. Tier constants should be copy-pasted verbatim."
---

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/throttle-agent/HYPER-AGENT-BIBLE.md`
**Version:** v1

---

## 🤔 What It Does

The three-layer protection model that stops any agent from pausing, killing, or evicting critical infrastructure. **Hardcoded tiers** + **configurable list** + **self-protection auto-add**.

> If a container is protected and an agent tries to pause it, **the pause silently no-ops + a metric fires**.

---

## 🏗️ Layer 1 — Hardcoded Tiers (NEVER override)

```python
TIER_1 = {"postgres", "redis", "hypercode-core", "hypercode-ollama"}   # data + cognition
TIER_2 = {"crew-orchestrator", "hypercode-dashboard"}                  # coordination + UI
TIER_3 = {"celery-worker"}                                             # task plumbing

PROTECTED_TIERS = TIER_1 | TIER_2 | TIER_3
```

---

## 🏗️ Layer 2 — Configurable Protect List

```bash
THROTTLE_PROTECT_CONTAINERS=throttle-agent,healer-agent,postgres,redis
```

```python
PROTECT_CONTAINERS = set(
    os.getenv("THROTTLE_PROTECT_CONTAINERS", "").split(",")
)
```

---

## 🏗️ Layer 3 — Self-Protection (Auto-Add)

```python
THROTTLE_ACTIVE_CONTAINER = os.getenv("HOSTNAME")
if THROTTLE_ACTIVE_CONTAINER:
    PROTECT_CONTAINERS.add(THROTTLE_ACTIVE_CONTAINER)
```

---

## 🔍 The Check

```python
def is_protected(container: str) -> bool:
    if container in PROTECTED_TIERS:
        return True
    if container in PROTECT_CONTAINERS:
        return True
    return False

async def pause(container: str):
    if is_protected(container):
        protected_pause_attempts_total.labels(container=container).inc()
        logger.warning("pause_blocked_by_protection", container=container)
        return
    await docker.pause(container)
```

---

## 🔗 Related Skills

- [[HS-002]] SIX_LAWS_OF_AGENTS — Law 2 (PROTECTION)
- [[HS-003]] AGENT_LIFECYCLE_STATE_MACHINE
- [[HS-009]] HYPER_AGENT_ROSTER

## 📋 THE PROMPT
```text
Use skill HS-104 THE THREE WALLS. Apply tier protection to agent [AGENT_NAME] — implement all 3 layers.
```
