# HS-076 — Pre-Commit Testing Checklist ✅

**Category:** `dev/`  
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §9  
**Version:** v1  

---

## 🤔 What It Does

The mandatory checklist every agent (and developer) runs before committing code to the HyperCode repo. Covers tests, coverage, type checking, linting, security, and dependencies.

---

## ✅ The 6-Step Pre-Commit Checklist

```bash
# 1. Run tests with coverage
pytest tests/ --cov=app --cov-report=term-missing

# 2. Enforce 80%+ coverage
coverage report --fail-under=80

# 3. Type checking
mypy app/

# 4. Linting
flake8 app/
black --check app/

# 5. Security scan
bandit -r app/

# 6. Dependency audit
pip-audit
```

---

## 🧪 Test Levels Reference

| Level | Scope | Speed | Location |
|---|---|---|---|
| Unit | Individual functions | < 100ms | `tests/test_*.py` |
| Integration | Service interactions | < 1s | `tests/integration/*` |
| E2E | Full Docker workflows | < 30s | `tests/docker_verification.py` |
| Smoke | Critical paths post-deploy | < 5s total | `tests/smoke_tests.py` |

---

## 🧪 Unit Test Template

```python
import pytest
from app.services.execution_service import execution_service

@pytest.mark.asyncio
async def test_execute_success():
    source = 'print("Hello")'
    result = await execution_service.execute_hypercode(source)
    assert result.success is True
    assert "Hello" in result.stdout
    assert result.exit_code == 0

@pytest.mark.asyncio
async def test_execute_timeout():
    source = 'while True: pass'
    result = await execution_service.execute_hypercode(source, timeout=1)
    assert result.success is False
    assert "timeout" in result.stderr.lower()
    assert result.exit_code == 124
```

---

## 🚀 Smoke Test Template

```python
import httpx, asyncio

async def smoke_test_health():
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

async def smoke_test_execution():
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "http://localhost:8000/execution/execute-hc",
            json={"source": 'print("test")'},
            headers={"X-API-Key": "dev"}
        )
        assert r.status_code == 200
        assert r.json()["success"] is True

if __name__ == "__main__":
    asyncio.run(smoke_test_health())
    asyncio.run(smoke_test_execution())
    print("✅ All smoke tests passed")
```

---

## ✅ Final Agent Checklist (Before ANY Task Completion)

- [ ] User Agency: Got approval for changes?
- [ ] Context Retention: Minimised user interruptions?
- [ ] ND-Friendly: Outputs are clear and structured?
- [ ] Observable: Emitted events and logged actions?
- [ ] Fail Gracefully: Fallbacks in place?
- [ ] Validated: Changes tested?
- [ ] Documented: Relevant docs updated?
- [ ] Cited Sources: Referenced the Bible when uncertain?

---

## 🎯 THE PROMPT

```
Run the HyperCode pre-commit checklist on this code:

[PASTE CODE OR DESCRIBE CHANGES]

Check:
1. Are there tests? If not, write them.
2. Is coverage > 80%? If not, add tests.
3. Do type hints pass mypy? Fix if not.
4. Is code black + flake8 compliant?
5. Any security issues (bandit)?
6. Any vulnerable dependencies?

Report: PASS / FAIL per step with fixes needed.
```

---

## 🔗 Related Skills
- HS-074 API Standards FastAPI Pattern
- HS-048 Preflight Checks System
- HS-070 Observable Agent Operations Pattern
