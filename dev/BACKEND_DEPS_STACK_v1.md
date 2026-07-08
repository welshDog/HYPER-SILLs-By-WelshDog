# HS-063 — 📦 THE QUARTERMASTER — Backend Deps Stack

---
skill_id: HS-063
hero_name: "THE QUARTERMASTER"
emoji: "📦"
version: v1.0.0
status: ACTIVE
category: dev
depends_on:
  - none  # foundational reference map — no upstream skill required
provides:
  - backend-dependency-map
  - reuse-before-adding-discipline
  - requirements-inventory
related:
  - HS-062  # SCHEMA SCRIBE — Database Schema Reference (sibling reference map)
  - HS-064  # THE QUICK HAND — Dev Commands Cheat Sheet (sibling reference map)
  - HS-060  # FLEET ADMIRAL — Container Stack Reference (sibling reference map)
graph_notes: "Map of the core backend's ~316-pin dependency stack grouped by purpose. Foundational reference so an AI reuses what's installed instead of bloating requirements.txt."
---

**Category:** dev
**Version:** 1.0

> *"What's already installed — reuse it before adding a dependency."*

---

## 🎯 What It Does

A map of the core backend's dependency stack (`backend/requirements.txt`, ~316
pins) grouped by purpose, so an AI reuses what's there instead of bloating it.

## 🌍 Why It Exists

The stack is large and already covers most needs. Adding a redundant dep =
slower builds + CVE surface. Vendoring deps into git has burned this repo before.

## ⚙️ How To Use

Paste before adding any backend dependency — check the group first.
problem_keywords:
  - backend deps
  - dependencies
  - stack
  - quartermaster

---

## 📋 THE PROMPT

```
HyperCode backend stack (backend/requirements.txt, ~316 pinned):

Web/API:     fastapi, uvicorn, starlette, pydantic v2, python-multipart
DB:          sqlalchemy 2.0, asyncpg, psycopg, alembic
Cache/queue: redis, celery
Auth/crypto: passlib, python-jose, cryptography
LLM/agents:  anthropic, openai, langgraph, crewai (+ ollama fallback)
Observability: prometheus-client, prometheus-fastapi-instrumentator,
               opentelemetry-* (FastAPI/SQLAlchemy/Redis/httpx/OTLP), structlog
Payments:    stripe
HTTP:        httpx, requests, aiohttp
Test:        pytest, pytest-asyncio

Rules:
  - REUSE before adding. Pin versions. NEVER `pip install --target` + git add
    (it once committed a Windows temp-path tree). Use requirements.txt + rebuild.
  - Trivy target: 0 CRITICAL per image. agent-base already ships fastapi/redis/httpx.
```

## ✅ Example

> "Need an HTTP client" → `httpx` is already in. Don't add `urllib3`/`aiohttp` for
> a new path; reuse the AsyncClient pattern (see orchestrator dispatch).

## 🔗 Related Skills

[[DATABASE_SCHEMA_REFERENCE_v1]] · [[CONTAINER_STACK_REFERENCE_v1]]
