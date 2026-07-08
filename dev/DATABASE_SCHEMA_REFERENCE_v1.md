# HS-062 — 🗄️ THE SCHEMA SCRIBE — Database Schema Reference

---
skill_id: HS-062
hero_name: "THE SCHEMA SCRIBE"
emoji: "🗄️"
version: v1.0.0
status: ACTIVE
category: dev
depends_on:
  - none  # foundational reference map — no upstream skill required
provides:
  - postgres-table-inventory
  - alembic-migration-discipline
  - shared-version-table-safety
related:
  - HS-060  # FLEET ADMIRAL — Container Stack Reference (sibling reference map)
  - HS-061  # PORT WARDEN — Port + Network Map (sibling reference map)
  - HS-063  # THE QUARTERMASTER — Backend Deps Stack (sibling reference map)
graph_notes: "Core hypercode Postgres table inventory + Alembic discipline. Foundational reference so migrations don't collide or re-stamp the shared version table."
---

**Category:** dev
**Version:** 1.0

> *"Every core table + the migration that made it. Verify head before you add one."*

---

## 🎯 What It Does

The core `hypercode` Postgres table inventory + Alembic discipline, so an AI
designs migrations that don't collide or re-stamp the shared version table.

## 🌍 Why It Exists

Migration numbering goes stale fast (a brief assumed head 015 when it was 017).
Shared `alembic_version` re-stamps crash-loop core. One reference prevents both.

## ⚙️ How To Use

Paste before any schema/migration work. **Always `alembic current` first.**
problem_keywords:
  - database schema
  - db tables
  - schema reference

---

## 📋 THE PROMPT

```
HyperCode core DB (`hypercode`), Alembic head 018 (verify with `alembic current`):

Core: users, projects, tasks, dashboard_tasks
Economy: broski_wallets, broski_transactions, broski_achievements,
         broski_user_achievements, focus_sessions, daily_mission_claims
Agents/auth: agent_api_keys, mod_actions
Course bridge: course_sync_events, access_provisions, graduation_events, code_health_scans
Pets: pet_provision_events
Control plane: hyperflow_runs (016), broski_identity_agents (017), governance_ledger (018)

Rules:
  - alembic tables live in the `hypercode` DB (not `postgres` → false "no relation").
  - Each service gets its OWN version_table — NEVER re-stamp the shared one.
  - New migration: revision=<head+1>, down_revision=<head>; upgrade + downgrade.
  - gen_random_uuid() available (pgcrypto, mig 009). JSONB doesn't work on SQLite tests.
  - Supabase is a SEPARATE schema — never merge with V2.4.
```

## ✅ Example

> "Add a table" → `alembic current` shows 018 → new file `019_*`, down_revision
> "018", register model in `app/db/base.py`, apply via `alembic upgrade head`.

## 🔗 Related Skills

[[BACKEND_DEPS_STACK_v1]] · [[GOVERNANCE_LEDGER_ENTRY_SCHEMA_v1]]
