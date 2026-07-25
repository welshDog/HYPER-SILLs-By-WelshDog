# 🚀 LEVEL 1 Implementation Guide — Enterprise Observability Setup

**Status**: Ready to implement  
**Total Time**: ~50 minutes  
**Risk Level**: Low (no breaking changes)  
**Impact**: 10x visibility + safer deployments + code insights

---

## Overview

Level 1 consists of 3 quick wins that will transform your observability:

1. **Wire Prometheus → Grafana** (5 min) ⚡ **HIGHEST IMPACT**
2. **Instrument Your Code** (30 min) 📊 **UNDERSTAND YOUR USERS**
3. **Create Staging Environment** (15 min) 🔄 **CATCH ISSUES EARLY**

---

## Part 1: Wire Prometheus to Grafana (5 min) ⚡

### What This Does
Connects Prometheus metrics to Grafana dashboards for real-time visualization.

### Current State
```
Prometheus: ✅ Running (collecting metrics)
Grafana: ✅ Running (empty, no dashboards)
Connection: ❌ Not wired (Grafana doesn't know about Prometheus)
```

### Steps

1. **Access Grafana**
   - URL: Check Railway dashboard for `grafana` service
   - Default: `https://grafana-production-[XXXX].up.railway.app`
   - Login: admin / (check GF_SECURITY_ADMIN_PASSWORD in variables)

2. **Add Prometheus Data Source**
   - Go to Configuration → Data Sources
   - Click "Add data source"
   - Select "Prometheus"
   - URL: `http://Prometheus:9090`
   - Save & Test

3. **Create First Dashboard**
   - Click "+" → "Dashboard"
   - Add panel
   - Query: `up` (should return 1 if service is healthy)
   - Save dashboard as "Service Health"

### Verify It Works
- Grafana shows Prometheus metrics
- "Service Health" panel displays service status
- You can create custom queries

### Success Indicators
✅ Prometheus data source shows "Data source is working"  
✅ First panel displays live metrics  
✅ You can query Prometheus from Grafana

---

## Part 2: Instrument Your Code (30 min) 📊

### What This Does
Adds Prometheus metrics to your MCP tools so you can track:
- Search latency by backend (keyword vs semantic)
- Error rates
- Tool execution times
- Registry health

### Files to Create/Modify

**NEW**: `prometheus_metrics.py` ✅ (Already created)
- Defines all Prometheus metrics
- Provides decorators for automatic tracking
- Ready to import

**MODIFY**: `mcp_server.py`
- Import prometheus_metrics
- Add `/metrics` endpoint
- Decorate tool functions
- Update health check with metrics

### Step-by-Step

#### Step 1: Add Imports
```python
# At the top of mcp_server.py
from prometheus_metrics import (
    skill_searches_total,
    search_latency_seconds,
    skills_loaded_total,
    skills_by_category,
    dense_embeddings_active,
    tool_executions_total,
    tool_execution_latency_seconds,
    get_metrics,
    track_metric,
)
```

#### Step 2: Add `/metrics` Endpoint
```python
# Add this route
@mcp.custom_route("/metrics", methods=["GET"])
async def metrics(request: Request) -> Response:
    """Prometheus metrics endpoint."""
    return Response(get_metrics(), media_type="text/plain; version=0.0.4")
```

#### Step 3: Update Health Check
```python
# In your health() endpoint
async def health(request: Request) -> JSONResponse:
    try:
        skills = len(skills_list())
        meta = get_registry().get("_meta", {})
        
        # Update gauges
        skills_loaded_total.set(skills)
        dense_embeddings_active.set(1 if _search_backend_report()['dense_active'] else 0)
        
        # Update category gauges
        for category, count in meta.get('categories', {}).items():
            skills_by_category.labels(category=category).set(count)
        
        return JSONResponse({
            "status": "ok",
            "service": "hyper-sills-mcp",
            "version": SERVER_VERSION,
            "skills": skills,
            "categories": meta.get("categories", {}),
            "search_backend": _search_backend_report(),
        })
    except Exception as exc:
        return JSONResponse({"status": "degraded", "error": str(exc)}, status_code=503)
```

#### Step 4: Instrument Tool Functions
```python
# For search_skills
@mcp.tool()
def search_skills(query: str = "", category: str = "", tag: str = "", limit: int = 10) -> str:
    """Search the HYPER-SILLs vault by keyword, category, or tag."""
    import time
    start = time.time()
    
    try:
        # ... existing search logic ...
        results = [...]  # Your search code
        
        # Track metrics
        skill_searches_total.labels(
            category=category or "all",
            backend_type="keyword",
            status="success"
        ).inc()
        
        search_latency_seconds.labels(
            backend_type="keyword",
            category=category or "all"
        ).observe(time.time() - start)
        
        tool_executions_total.labels(
            tool_name="search_skills",
            status="success"
        ).inc()
        
        return json.dumps({"count": len(results), "results": results})
    
    except Exception as e:
        search_latency_seconds.labels(
            backend_type="keyword",
            category=category or "all"
        ).observe(time.time() - start)
        
        tool_executions_total.labels(
            tool_name="search_skills",
            status="error"
        ).inc()
        
        raise
```

#### Step 5: Similar for semantic_search
```python
@mcp.tool()
def semantic_search(query: str, limit: int = 5) -> str:
    """Find skills by semantic similarity."""
    import time
    start = time.time()
    
    try:
        # ... existing semantic search code ...
        hits = _ss(query, limit=limit)
        
        semantic_search_total.labels(status="success").inc()
        search_latency_seconds.labels(
            backend_type="semantic",
            category="all"
        ).observe(time.time() - start)
        
        return json.dumps({...})
    
    except Exception:
        semantic_search_total.labels(status="fallback").inc()
        search_latency_seconds.labels(
            backend_type="semantic",
            category="all"
        ).observe(time.time() - start)
        
        # Fallback to keyword search
        return search_skills(query=query, limit=limit)
```

### Verify It Works

After deploying:
1. Test the `/metrics` endpoint
   ```bash
   curl https://hyper-sills-by-welshdog-production.up.railway.app/metrics
   ```
   Should return Prometheus text format metrics

2. In Grafana, query: `hyper_sills_searches_total`
   Should show your search metrics

3. Perform some searches, then check metrics again
   Values should increase

### Success Indicators
✅ `/metrics` endpoint returns Prometheus format data  
✅ Grafana can query custom metrics  
✅ Metrics update after tool usage  

---

## Part 3: Create Staging Environment (15 min) 🔄

### What This Does
Creates a separate staging environment for safe testing of:
- New skill registry updates
- Code changes before production
- Deployment automation

### Current Setup
```
Environment: sincere-strength
  └─ production (main branch)
      └─ HYPER-SILLs-By-WelshDog (live service)

Desired Setup
Environment: sincere-strength
  ├─ production (main branch)
  │   └─ HYPER-SILLs-By-WelshDog (live service)
  └─ staging (develop branch)
      └─ HYPER-SILLs-By-WelshDog-staging (test service)
```

### Steps

#### Option A: Using Railway UI (Easiest)
1. Go to Railway dashboard
2. Go to your project (sincere-strength)
3. Click "Environments"
4. Create new environment: "staging"
5. Clone services to staging environment
6. In staging HYPER-SILLs service:
   - Change branch from "main" to "develop"
   - Deploy
7. Now you have:
   - production: tracks main branch
   - staging: tracks develop branch

#### Option B: Using CLI Commands
```bash
# List environments
railway env list

# Create staging environment
railway env create staging

# Switch to staging
railway switch

# Deploy to staging
railway deploy
```

### Git Workflow Setup
In your repository, set up branches:

```bash
# Create develop branch (if not exists)
git checkout main
git pull
git checkout -b develop
git push -u origin develop

# Now your branches are:
# main    → production (stable, release-ready)
# develop → staging (testing, integration)
```

### Testing Workflow
```
Feature Development
  ↓
Create feature branch (feature/xyz)
  ↓
Push to develop
  ↓
Auto-deploy to staging
  ↓
Test & validate
  ↓
Create PR to main
  ↓
Code review
  ↓
Merge to main
  ↓
Auto-deploy to production
```

### Verify It Works
1. In Railway: See both environments (production + staging)
2. Production service: Running on main branch
3. Staging service: Running on develop branch
4. Both services healthy and accessible

### Success Indicators
✅ Two separate environments visible  
✅ Staging deploys from develop branch  
✅ Production deploys from main branch  
✅ Services are independent (different URLs)

---

## Summary Checklist

### Part 1: Prometheus → Grafana
- [ ] Access Grafana at `https://grafana-production-[XXXX].up.railway.app`
- [ ] Add Prometheus data source at `http://Prometheus:9090`
- [ ] Create "Service Health" dashboard
- [ ] Verify Grafana shows metrics

### Part 2: Code Instrumentation
- [ ] Import prometheus_metrics in mcp_server.py
- [ ] Add `/metrics` endpoint
- [ ] Update health check with gauges
- [ ] Instrument search_skills function
- [ ] Instrument semantic_search function
- [ ] Instrument other tools (load_skill, recommend_for_task, etc.)
- [ ] Deploy changes
- [ ] Verify `/metrics` endpoint works
- [ ] Test queries in Grafana

### Part 3: Staging Environment
- [ ] Create staging environment in Railway
- [ ] Create develop branch in Git
- [ ] Configure staging to track develop
- [ ] Configure production to track main
- [ ] Test auto-deploy on both branches

---

## Expected Results After Level 1

### Visibility ✅
- Real-time dashboard of service health
- Request rates, error rates, latency percentiles
- Resource usage (CPU, memory)
- Multi-region traffic distribution

### Safety ✅
- Staging environment for testing
- Separate branch workflows
- Can test changes before production
- Easy rollback if needed

### Understanding ✅
- Know what tools are being used most
- See which searches are slowest
- Identify performance bottlenecks
- Understand search patterns

---

## Time Breakdown

| Task | Time | Status |
|------|------|--------|
| Wire Prometheus to Grafana | 5 min | ⏳ Start here |
| Create first 4 dashboards | 15 min | Then this |
| Instrument code (import + endpoints) | 15 min | Then this |
| Test metrics in Grafana | 10 min | Then verify |
| Create staging environment | 15 min | Final step |
| **TOTAL** | **50 min** | **Ready now!** |

---

## What Comes Next (Level 2)

After Level 1, you'll be ready for:
1. **Add rate limiting** (20 min) — Protect from abuse
2. **Deploy caching** (30 min) — 10x faster repeated searches
3. **Setup CI/CD testing** (45 min) — Automated quality gates

But first, **let's get Level 1 done!** 🚀

---

## Need Help?

1. **Grafana questions**: Check [Grafana docs](https://grafana.com/docs/)
2. **Prometheus metrics**: See [prometheus_metrics.py](prometheus_metrics.py)
3. **Code instrumentation**: See [mcp_server.py modifications](#part-2-instrument-your-code-30-min)
4. **Staging setup**: See [Railway documentation](https://docs.railway.app)

---

**Ready? Let's start with Part 1!** 🎯

