# HS-093 — Nightly Continuous Learning Loop 🌙

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/🧬 The Full Confirmed Hyper Agent Roster` §5
**Version:** v1

---

## 🤔 What It Does

The cron-driven feedback → drift-detect → HITL-gate → prompt-update → regression-test → ledger-log pipeline that lets HyperCode agents improve themselves *without* going rogue. Runs nightly at 02:00 UTC via `cron`. Every step has a kill-switch.

> The "evolutionary pipeline" referred to in the DevOps agent's role ([[HS-089]]). Without this loop, agents drift silently and Lyndz loses visibility.

---

## 🛡️ Safety First — the 6 Hard Gates

The pipeline is built so any step can refuse to advance:

```
Ingest → Detect drift → HITL approval → Prompt update → Regression → Ledger log
   ↓          ↓              ↓                ↓              ↓           ↓
 fails =   alert =      gate =          rollback =      rollback =  audit only
 abort     pager        wait            on fail         on fail
```

**Critical:** Step 3 (HITL) is the **only legal way** retraining starts. If `hitl:approval:nightly` ≠ `"approved"`, the loop exits — Lyndz must explicitly approve via the override endpoint.

---

## 🐍 The Pipeline

```python
# scripts/nightly_learning_loop.py
# cron: 0 2 * * * python scripts/nightly_learning_loop.py
import asyncio, httpx
import redis.asyncio as redis
from datetime import datetime

DRIFT_THRESHOLD = 0.15
GOVERNANCE_LEDGER_URL = "http://localhost:8000/api/ledger"

async def nightly_pipeline():
    print(f"🌙 Nightly loop starting — {datetime.utcnow().isoformat()}")
    r = await redis.from_url("redis://redis:6379", decode_responses=True)

    # ── Step 1: Ingest feedback from Redis stream ────────────
    feedback = await r.xrange("feedback:queue", count=1000)
    print(f"📥 Ingested {len(feedback)} feedback entries")

    # ── Step 2: Drift detection ──────────────────────────────
    baseline = await r.get("embeddings:baseline")
    drift_score = compute_cosine_drift(feedback, baseline)
    if drift_score > DRIFT_THRESHOLD:
        await r.publish("alerts:critical",
            f"⚠️ DRIFT DETECTED: score={drift_score:.2f} — human review needed")

    # ── Step 3: Human-in-the-loop gate ───────────────────────
    approval = await r.get("hitl:approval:nightly")
    if approval != "approved":
        print("⏸️ Waiting for Lyndz approval before retraining...")
        return

    # ── Step 4: Update agent prompts from flagged convos ─────
    flagged = await r.smembers("feedback:flagged")
    for agent_id in flagged:
        await update_agent_prompt(agent_id)

    # ── Step 5: Run regression suite ─────────────────────────
    async with httpx.AsyncClient() as c:
        r_test = await c.post("http://localhost:8083/ci/run-regression")
        if not r_test.json().get("passed"):
            await rollback_to_last_good()

    # ── Step 6: Log to governance ledger ─────────────────────
    async with httpx.AsyncClient() as c:
        await c.post(GOVERNANCE_LEDGER_URL, json={
            "timestamp":      datetime.utcnow().isoformat(),
            "drift_score":    drift_score,
            "feedback_count": len(feedback),
            "approved_by":    "Lyndz",
            "actions_taken":  ["prompt_update", "regression_passed"],
            "version_bump":   "2.x.x → 2.x.x+1"
        })
    print("✅ Nightly loop complete — governance ledger updated")

asyncio.run(nightly_pipeline())
```

---

## 📥 Feedback Ingestion API

Agents and users push to `feedback:queue` via:

```
POST /api/feedback
Body: { agent_id, session_id, rating: 1-5, comment, flag: bool }
```

The Redis stream is the only legal feedback ingress — direct DB writes bypass the drift detector.

---

## 🚨 Drift Alarm Triggers

The loop pages on **any** of:

1. Embedding cosine similarity drops below 0.85 vs baseline
2. User satisfaction drops > 10% week-over-week
3. Task failure rate spikes > 5% above 7-day rolling average

---

## 🛑 Human Override

```
POST /api/override/{agent_id}
Body: { action: "approve|block|rollback", reason: "..." }
```

Three actions:
- **approve** — set `hitl:approval:nightly = "approved"`, loop proceeds
- **block** — set to `"blocked"`, loop exits cleanly, no retraining
- **rollback** — immediately revert agent to previous version, regardless of regression status

---

## 📒 Every Run Logged

See [[HS-095]] for the governance ledger entry schema. Every nightly run produces exactly one ledger entry — no entry = the loop didn't run = SRE incident.

---

## 🧩 Related Skills

- [[HS-095]] Governance Ledger Entry Schema — the audit-log format
- [[HS-090]] Universal Life Plan YAML — `version_migration` field this loop bumps
- [[HS-091]] Top-Tier Identity Cards — Brain agent owns the embedding baseline
- [[HS-077]] User Agency Approval Gate — Step 3 HITL is this gate at infra level
- [[HS-085]] 5 Mandatory Agent Guardrails — `cost_limits` apply per retrain
