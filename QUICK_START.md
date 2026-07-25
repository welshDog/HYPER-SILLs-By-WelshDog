# ⚡ LEVEL 1 Quick Start — 5-Minute Setup

**Goal**: Get real-time dashboards working  
**Time**: 5 minutes  
**Difficulty**: Easy (UI only, no code changes needed for this step)

---

## Step 1: Get Grafana URL

Go to Railway dashboard → sincere-strength project → grafana service

**Your Grafana URL**:
```
https://grafana-production-[XXXX].up.railway.app
```

---

## Step 2: Login to Grafana

1. Open your Grafana URL
2. Login with default credentials:
   - Username: `admin`
   - Password: Get from service variables (GF_SECURITY_ADMIN_PASSWORD)

---

## Step 3: Add Prometheus Data Source

1. Click **Configuration** (gear icon) → **Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. Fill in:
   - **Name**: Prometheus
   - **URL**: http://Prometheus:9090
   - Leave other settings default
5. Click **Save & test**
6. You should see: "Data source is working"

---

## Step 4: Create Service Health Dashboard

1. Click **+** (Create) → **Dashboard**
2. Click **Add panel**
3. In the query box, enter: `up`
4. You should see a line graph
5. Click **Save dashboard**
6. Name it: "Service Health"

---

## Done! ✅

Your dashboards are now live!

**Next**: Go to [GRAFANA_SETUP.md](GRAFANA_SETUP.md) to create the 4 main dashboards.

---

## Full Dashboard Setup (15 min)

After the quick start, open [GRAFANA_SETUP.md](GRAFANA_SETUP.md) for:

- Dashboard 1: Service Health (requests, errors, uptime)
- Dashboard 2: Performance (latency p50/p95/p99, CPU, memory)
- Dashboard 3: Multi-Region (traffic split, regional latency)
- Dashboard 4: Skill Registry (skills loaded, search backend health)

Each takes 2-3 minutes to create.

---

## Then: Instrument Your Code (30 min)

See [LEVEL_1_IMPLEMENTATION.md](LEVEL_1_IMPLEMENTATION.md) Part 2 for:
- Adding Prometheus metrics to your code
- Tracking search latency by backend
- Monitoring error rates
- Measuring tool performance

---

## Finally: Create Staging (15 min)

See [LEVEL_1_IMPLEMENTATION.md](LEVEL_1_IMPLEMENTATION.md) Part 3 for:
- Setting up staging environment
- Git workflow (develop → staging, main → production)
- Safe testing before production

---

**Questions?** Check the full guides or ask! 🚀

