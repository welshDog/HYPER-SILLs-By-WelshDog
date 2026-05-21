# HS-086 — 🔺 THE FOUR TIERS — Test Pyramid (4 Levels)

**Category:** `dev/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §9
**Version:** v1

---

## 🤔 What It Does

The four-tier test taxonomy used across the HyperCode crew. Defines what each level covers, how fast it should run, and when to write which. Use this when deciding "is this a unit test or an E2E?".

---

## 🏗️ The Pyramid

```
            /\
           /  \   Smoke         < 5s total       — critical paths only
          /----\
         /      \  E2E           < 30s/test       — full workflows (Docker)
        /--------\
       /          \ Integration  < 1s/test        — service interactions
      /------------\
     /              \ Unit       < 100ms/test    — functions/classes (mocked)
    /________________\
```

More tests at the bottom, fewer at the top.

---

## 1️⃣ Unit Tests

**What:** individual functions or classes, all deps mocked.
**Speed:** < 100ms per test.
**Where:** `tests/test_*.py`.
**Example:**

```python
@pytest.mark.asyncio
async def test_execute_hypercode_syntax_error():
    source = 'print("missing closing quote'
    result = await execution_service.execute_hypercode(source)
    assert result.success is False
    assert "SyntaxError" in result.stderr
    assert result.exit_code != 0
```

---

## 2️⃣ Integration Tests

**What:** real service-to-service interactions (DB, Redis, internal API).
**Speed:** < 1s per test.
**Where:** `tests/integration/*`.
**Uses:** a real test database / test Redis — **not** mocks.

---

## 3️⃣ E2E Tests

**What:** full workflow through the running Docker stack.
**Speed:** < 30s per test.
**Where:** `tests/docker_verification.py`.
**Triggers:** Stripe checkout, full crew orchestration, browser flows (Playwright).

---

## 4️⃣ Smoke Tests

**What:** quick liveness checks of critical paths post-deploy.
**Speed:** < 5s **total** for the whole suite.
**Where:** `tests/smoke_tests.py`.
**Pattern:**

```python
import httpx, asyncio

async def smoke_test_health_endpoints():
    services = [
        "http://localhost:8000/health",
        "http://localhost:3000/api/health",
        "http://localhost:5173/health",
    ]
    async with httpx.AsyncClient() as client:
        for url in services:
            r = await client.get(url, timeout=5)
            assert r.status_code == 200
            assert r.json()["status"] == "healthy"
```

---

## 🎯 When To Write Which

| You're adding... | Write this test |
|---|---|
| A new pure function | Unit |
| A new DB query / Redis call | Integration |
| A new API endpoint | Unit (handler logic) + Integration (DB/external) + E2E (Docker) |
| A new deploy / infra change | Smoke (health endpoints) |
| Bug fix | Unit reproducing the bug **first**, then fix |

---

## 📈 Coverage Target

≥ 80% line coverage across `app/`. Enforced by the pre-commit gate ([[HS-076]]).

```bash
pytest tests/ --cov=app --cov-report=term-missing
coverage report --fail-under=80
```

---

## 🧩 Related Skills

- [[HS-076]] Pre-Commit Testing Checklist — the gate that runs these
- [[HS-079]] Specialist Agent Roles — QA owns this pyramid
- [[HS-070]] Observable Agent Operations Pattern — what the tests assert on
