# HS-074 — 🚀 THE API CODEX — API Standards (FastAPI Agent Pattern)

**Category:** `dev/`  
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §3 + §5  
**Version:** v1  

---

## 🤔 What It Does

The canonical FastAPI route pattern used across HyperCode agent services. Every endpoint follows the same structure: auth dependency, trace ID, structlog logging, Pydantic schemas, and consistent error handling.

---

## 🏗️ Route Template

```python
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.execution import ExecuteRequest, ExecutionResult
from app.dependencies.auth import require_api_key
from app.services.execution_service import execution_service
import structlog

router = APIRouter(prefix="/execution", tags=["execution"])
logger = structlog.get_logger()

@router.post("/execute-hc", response_model=ExecutionResult)
async def execute_hypercode(
    request: ExecuteRequest,
    api_key: str = Depends(require_api_key)
):
    trace_id = generate_trace_id()

    logger.info("execution_started",
        trace_id=trace_id,
        source_length=len(request.source)
    )

    try:
        result = await execution_service.execute_hypercode(
            source=request.source,
            timeout=request.timeout or 30
        )
        logger.info("execution_completed",
            trace_id=trace_id,
            success=result.success,
            duration_ms=result.duration_ms
        )
        return result

    except TimeoutError:
        logger.error("execution_timeout", trace_id=trace_id)
        raise HTTPException(status_code=408, detail="Execution timeout.")

    except Exception as e:
        logger.error("execution_failed", trace_id=trace_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")
```

---

## 🔑 Auth Dependency

```python
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def require_api_key(api_key: str = Security(api_key_header)):
    expected_key = os.getenv("API_KEY")
    if not expected_key:
        return "dev_mode"   # Dev: no auth
    if not api_key or api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    return api_key
```

---

## 🌐 Core API Endpoints Reference

```yaml
Base URL: http://localhost:8000

POST /execution/execute-hc      # Run HyperCode source
POST /execution/execute          # Run Python/Shell/HC
GET  /agents/stream              # SSE agent event stream
POST /agents/register            # Register new agent
POST /agents/heartbeat           # Agent heartbeat
POST /memory                     # Create memory
GET  /memory/search?q=           # Search memories
GET  /health                     # Health check
GET  /metrics                    # Prometheus metrics
```

---

## 🛡️ Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/execution/execute-hc")
@limiter.limit("10/minute")
async def execute_hypercode(request: Request):
    pass
```

---

## 🎯 THE PROMPT

```
Create a FastAPI route for this agent service:

Endpoint: [METHOD] /[path]
Input schema: [DESCRIBE INPUT]
Output schema: [DESCRIBE OUTPUT]
Auth required: yes/no
Rate limit: [X]/minute

Follow the HyperCode API standard:
- require_api_key dependency
- trace_id generated at entry
- structlog logging (started / completed / failed)
- HTTPException 408 for timeout, 500 for unexpected
- Pydantic request + response models
```

---

## 🔗 Related Skills
- HS-073 SSE Agent Event Schema
- HS-076 Pre-Commit Testing Checklist
- HS-048 Preflight Checks System
