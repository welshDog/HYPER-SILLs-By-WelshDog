# HS-106 — New Agent Build Checklist (10-Point) 🌱

**Category:** `dev/`
**Source:** HyperCode-V2.4 — `agents/throttle-agent/HYPER-AGENT-BIBLE.md`
**Version:** v1

---

## 🤔 What It Does

The pre-deploy checklist for any new HyperCode agent. Different from [[HS-088]] (Final Self-Audit, runs *per task at completion*) and [[HS-076]] (Pre-Commit Checklist, runs *per commit*). This one runs **once per new agent** — the day you first ship it.

> Every point is non-negotiable. Skipping any of them = you don't have a HyperCode agent, you have a script.

---

## ✅ The 10 Checks

```
[ ]  1. SINGLE RESPONSIBILITY
       One purpose. One name. If you can't summarise the agent in one
       sentence, split it.

[ ]  2. FASTAPI WITH /health + /metrics
       Plus your core endpoint. /health returns 200 + JSON, /metrics
       returns Prometheus format. See HS-105.

[ ]  3. JSON LOGGING
       structlog or equivalent. Fields: component, action, timestamp.
       No plain print() in prod paths.

[ ]  4. ≥ 5 PROMETHEUS METRICS
       The mandatory 5 from HS-105. More if specialty (throttle-agent
       has 15+).

[ ]  5. HEALER INTEGRATION
       Check circuit breaker before any state-mutating action.
       See HS-103.

[ ]  6. GRACEFUL FAILURE
       Docker down? Healer unreachable? DB out? Return safe defaults
       and log — never crash. Implements Law 4 (HS-098) + HS-071.

[ ]  7. ENVIRONMENT CONFIG
       No hardcoded URLs, ports, credentials, or feature flags.
       Everything goes through env vars. Validated at startup.

[ ]  8. SELF-PROTECTION
       Auto-add self to PROTECT_CONTAINERS at startup.
       See HS-104 Layer 3.

[ ]  9. CHOOSE YOUR NAME
       Set AGENT_NAME env var. Single strong noun ("The Sentinel",
       "The Archivist"). See HS-107.

[ ] 10. FILL YOUR BIBLE
       Document your purpose in agents/<your-agent>/HYPER-AGENT-BIBLE.md
       (don't leave it as a 0-byte stub — irony intended).
```

---

## 🧪 The 5-Minute Verification

After deploy, run all of these against the agent's host:port. All must pass:

```bash
AGENT_URL=http://localhost:<port>

# 1. Health
curl -fs $AGENT_URL/health | jq -e '.status == "healthy"'

# 2. Identity contract (HS-092)
curl -fs $AGENT_URL/identity | jq -e '.name and .version and .core_purpose'

# 3. Mandatory metrics
curl -fs $AGENT_URL/metrics | \
  grep -E '^agent_(up|uptime_seconds|last_action_ts|error_total|decision_reasons)' | \
  awk 'END { exit (NR >= 5 ? 0 : 1) }'

# 4. p95 latency < 200ms
for i in {1..50}; do
  curl -fs -w "%{time_total}\n" -o /dev/null $AGENT_URL/health
done | sort -n | awk 'NR==48 { exit ($1 < 0.2 ? 0 : 1) }'

# 5. Healer circuit-breaker check works
curl -fs http://healer-agent:8008/circuit-breaker/$AGENT_NAME
```

Any failure → fix before declaring shipped.

---

## 📅 Promotion Path

After the 10 checks pass + the agent has run for 7 days clean:
- **Rank up via [[HS-107]] Agent Ranks ladder** (Recruit → Operative → Guardian → Legend)
- Add agent's name + path to the roster ([[HS-089]])
- Wire it into the dependency graph ([[HS-097]])
- Run the full contract suite ([[HS-092]])

---

## 🚨 Anti-patterns

- **Skipping #10.** Empty Bible files are useless to future readers — and lying to the index (e.g. claiming a Bible exists when it's 0 bytes) is the bug we discovered when raiding the specialist Bibles.
- **Skipping #5 "because it's read-only".** Healer needs to know about every agent's existence regardless. Register at startup.
- **Treating #7 as optional in dev.** Hardcoded values *will* leak to prod. Use env vars from day 1.
- **Choosing a verb as the name (#9).** Names are nouns. "The Throttler" not "Throttling". Identity is what you ARE, not what you DO.

---

## 🧩 Related Skills

- [[HS-099]] Anatomy of an Agent — 6 organs that must all exist
- [[HS-105]] Core Agent Metrics Contract — Check #4
- [[HS-103]] Healer Circuit-Breaker Protocol — Check #5
- [[HS-104]] Tier Protection Rules — Check #8
- [[HS-107]] Agent Ranks + Naming + Creed — Check #9
- [[HS-092]] Agent Contract Test Suite — automated 5-Min Verification harness
- [[HS-088]] Agent Final Self-Audit — per-task sibling to this per-agent checklist
- [[HS-076]] Pre-Commit Testing Checklist — per-commit sibling
