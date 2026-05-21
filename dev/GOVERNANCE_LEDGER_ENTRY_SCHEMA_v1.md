# HS-095 — 📒 THE LEDGER LAW — Governance Ledger Entry Schema

**Category:** `dev/`
**Source:** HyperCode-V2.4 — `agents/🧬 The Full Confirmed Hyper Agent Roster` §6
**Version:** v1

---

## 🤔 What It Does

The append-only audit format every agent retrain, prompt update, version bump, or HITL override writes to. This is the SOC 2 paper trail — if it's not in the ledger, it didn't happen.

> Consumed by the doc portal (`docs/portal/governance/audit_ledger.json`) and the nightly learning loop ([[HS-093]]).

---

## 🧱 The Schema

```json
{
  "timestamp": "2026-03-23T02:00:00Z",
  "agent": "brain-agent",
  "action": "prompt_update",
  "version_from": "2.1.0",
  "version_to": "2.1.1",
  "approved_by": "Lyndz",
  "drift_score": 0.12,
  "regression_passed": true,
  "data_sources": ["feedback:queue", "interaction-logs"]
}
```

---

## 🔑 Field Rules

| Field | Required | Type | Notes |
|---|---|---|---|
| `timestamp` | ✅ | ISO 8601 UTC | Append-only — never edit |
| `agent` | ✅ | string | Agent name from [[HS-089]] roster |
| `action` | ✅ | enum | `prompt_update` · `version_bump` · `rollback` · `override` · `retrain_blocked` |
| `version_from` | ✅ | semver | Pre-change version |
| `version_to` | ✅ | semver | Post-change version (same as `from` if action blocked/rolled back) |
| `approved_by` | ✅ | string | Human identifier — `"Lyndz"` or `"automated:nightly"` for self-approving safe ops |
| `drift_score` | conditional | float 0–1 | Required if `action ∈ {prompt_update, retrain_blocked}` |
| `regression_passed` | conditional | bool | Required if `action = prompt_update` |
| `data_sources` | ✅ | string[] | Redis streams / DB tables that fed the change |
| `reason` | conditional | string | Required for `rollback` and `override` |

---

## 📂 Storage

- **Live append:** PostgreSQL `audit_log` table (SOC 2 immutable)
- **Portal mirror:** `docs/portal/governance/audit_ledger.json` (auto-generated nightly, read-only)
- **Retention:** Indefinite. Never delete. Archive to S3 after 1 year.

---

## 🔍 Query Patterns

```sql
-- Every retrain Lyndz approved this month
SELECT * FROM audit_log
WHERE action = 'prompt_update'
  AND approved_by = 'Lyndz'
  AND timestamp >= date_trunc('month', now());

-- Agents with most drift in 7d
SELECT agent, AVG(drift_score) AS avg_drift
FROM audit_log
WHERE timestamp >= now() - interval '7 days'
  AND drift_score IS NOT NULL
GROUP BY agent
ORDER BY avg_drift DESC;

-- Rollbacks (incident signal)
SELECT * FROM audit_log
WHERE action = 'rollback'
ORDER BY timestamp DESC;
```

---

## 🚨 Invariants

- **One entry per nightly run.** Missing entry = pipeline didn't execute → SRE incident.
- **Never UPDATE, only INSERT.** Append-only is the whole point.
- **`approved_by = "Lyndz"`** is the only legal source for `action = override` — automated approvers cannot self-override.

---

## 🧩 Related Skills

- [[HS-093]] Nightly Continuous Learning Loop — writes the entries
- [[HS-090]] Universal Life Plan YAML — `security_compliance.soc2.audit_logging` references this table
- [[HS-091]] Top-Tier Identity Cards — Security agent reads this passively
- [[HS-076]] Pre-Commit Testing Checklist — `bandit` / `pip-audit` failures also append here
