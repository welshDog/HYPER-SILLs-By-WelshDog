# HS-079 — 👥 THE CREW CHARTER — Specialist Agent Role Definitions


---
skill_id: HS-079
hero_name: "THE CREW CHARTER"
emoji: "👥"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-067  # THE THRONE LADDER — hierarchy defines the 6 slots
  - HS-008  # BROSKI ORCHESTRATOR PATTERN — orchestrator manages all 6
provides:
  - specialist-role-definitions
  - can-cannot-tools-envelope
  - 6-specialist-roster
related:
  - HS-080  # THE TOOL BELT — minimum tools every specialist must expose
  - HS-075  # THE CHOICE MATRIX — delegate decision uses role definitions
graph_notes: "Defines the CAN/CANNOT/Tools envelope for each of the 6 BROski specialist agents — load before spawning or auditing a role."
---
**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §2
**Version:** v1

---

## 🤔 What It Does

Defines the **CAN / CANNOT / Tools** envelope for each of the 6 specialist agents in the BROski crew. Use when spawning a new agent or auditing whether an action belongs to a given role. Sits underneath [[HS-067]] (Role Hierarchy) and [[HS-068]] (Orchestrator).

---

## 🗺️ The 6 Specialists

```
BROski Orchestrator (manager — see HS-068)
  ├─→ Language Engine Specialist  (worker)
  ├─→ Frontend Specialist         (worker)
  ├─→ Backend Specialist          (worker)
  ├─→ Observability Specialist    (validator)
  ├─→ Security Specialist         (validator)
  └─→ QA Specialist               (validator)
```

---

## 🧠 [LANGUAGE_SPECIALIST]

**Role:** HyperCode language design, parser, interpreter, IR/MLIR

| ✅ CAN | ❌ CANNOT |
|---|---|
| Design + modify HyperCode grammar | Modify IDE/frontend → delegate Frontend |
| Implement parser, lexer, interpreter | Change API routes → delegate Backend |
| Work with MLIR IR | Alter deployment → delegate Observability |
| Add language features (quantum, molecular) | |
| Debug language execution | |

**Tools:** `run_hypercode`, `parse_hypercode`, `validate_syntax`, `read_file` (hypercode-engine/* only), `update_language_docs`, `create_example`

---

## 🎨 [FRONTEND_SPECIALIST]

**Role:** Hyperflow Editor, Broski Terminal, UI/UX

| ✅ CAN | ❌ CANNOT |
|---|---|
| Implement Monaco / CodeMirror features | Modify backend API logic → Backend |
| Build SSE timeline in Broski Terminal | Change language syntax → Language |
| ND-friendly UI components | Alter observability stack → Observability |
| Wire frontend to backend APIs | |
| Syntax highlighting, autocomplete | |

**Tools:** `read_file` (hyperflow-editor/*, broski-terminal/*), `write_file`, `run_frontend_build`, `run_frontend_tests`, `test_api_endpoint`, `check_accessibility`

---

## ⚙️ [BACKEND_SPECIALIST]

**Role:** FastAPI routes, execution service, adapters, database

| ✅ CAN | ❌ CANNOT |
|---|---|
| Implement API endpoints | Change frontend → Frontend |
| Modify execution service logic | Modify language engine internals → Language |
| Update database schemas | Alter monitoring config → Observability |
| Add middleware (auth, CORS, rate limit) | |
| Background tasks, API perf | |

**Tools:** `read_file` (hypercode-core/*), `write_file`, `run_tests`, `check_api_health`, `query_db`, `migrate_db`, `restart_service`, `check_logs`

---

## 📊 [OBSERVABILITY_SPECIALIST]

**Role:** Grafana, Prometheus, alerts, monitoring

| ✅ CAN | ❌ CANNOT |
|---|---|
| Create/update Grafana dashboards | Modify app logic → Backend |
| Write Prometheus alert rules | Change frontend → Frontend |
| Add metrics to services | Alter language → Language |
| Configure exporters | |

**Tools:** `query_prometheus`, `create_dashboard`, `test_alert_rule`, `check_grafana_health`, `get_metric_values`

---

## 🔒 [SECURITY_SPECIALIST]

**Role:** Auth, API keys, rate limiting, CVE scanning, hardening

| ✅ CAN | ❌ CANNOT |
|---|---|
| Implement auth / authorization | Change business logic → Backend |
| Add rate limiting | Modify UI → Frontend |
| Scan for vulnerabilities | Alter metrics → Observability |
| Review Dockerfiles for security | |
| Audit endpoints; CORS/CSP/HSTS | |

**Tools:** `scan_dependencies`, `check_api_security`, `test_rate_limit`, `review_dockerfile`

---

## 🧪 [QA_SPECIALIST]

**Role:** Tests, coverage, smoke tests, E2E

| ✅ CAN | ❌ CANNOT |
|---|---|
| Write unit / integration / E2E tests | Modify app code → specialists |
| Coverage reports | Change CI/CD → Observability |
| Build test fixtures | |
| Smoke test suites | |

**Tools:** `run_tests`, `run_docker_verification`, `create_test_fixture`, `run_smoke_tests`

---

## 🧩 Related Skills

- [[HS-067]] Agent Role Hierarchy Pattern — the parent structure
- [[HS-068]] BROski Orchestrator Pattern — manager that delegates here
- [[HS-074]] FastAPI Agent API Standards — Backend's enforcement layer
- [[HS-076]] Pre-Commit Testing Checklist — QA's gate
