# 🎯 Grafana Setup Guide — HYPER-SILLs Dashboard Configuration

**Time to Complete**: 5-10 minutes  
**Prerequisites**: Grafana and Prometheus deployed to Railway  
**Difficulty**: Easy (point-and-click UI)

---

## Step 1: Access Grafana Dashboard

### Get Your Grafana URL
From Railway dashboard:
```
Service: grafana
Domain: grafana-production-[XXXX].up.railway.app
```

### Login to Grafana
1. Open `https://grafana-production-[XXXX].up.railway.app`
2. Default credentials:
   - Username: `admin`
   - Password: Check Railway service variables (GF_SECURITY_ADMIN_PASSWORD)

---

## Step 2: Add Prometheus Data Source

### In Grafana:
1. Go to **Configuration** → **Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. Enter the following:
   - **Name**: `Prometheus`
   - **URL**: `http://Prometheus:9090`
   - **Access**: Server (default)
5. Click **Save & test**
6. You should see "Data source is working"

---

## Step 3: Create Dashboard 1 — Service Health

### Create Dashboard
1. Click **+** (Create) → **Dashboard**
2. Click **Add panel**

### Panel 1: Request Rate (requests/sec)
- **Title**: Request Rate
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  rate(hyper_sills_http_requests_total[1m])
  ```
- **Visualization**: Graph/Time Series
- **Legend**: Show series

### Panel 2: Error Rate (%)
- **Title**: Error Rate
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  (rate(hyper_sills_errors_total[1m]) / (rate(hyper_sills_http_requests_total[1m]) + 0.001)) * 100
  ```
- **Visualization**: Stat/Gauge
- **Unit**: Percent
- **Thresholds**: Green <1%, Yellow 1-5%, Red >5%

### Panel 3: Health Check Status
- **Title**: Health Check Success Rate
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  (rate(hyper_sills_http_requests_total{path="/health",status_code="200"}[5m]) / rate(hyper_sills_http_requests_total{path="/health"}[5m])) * 100
  ```
- **Visualization**: Gauge
- **Unit**: Percent
- **Thresholds**: Green >99%, Yellow 95-99%, Red <95%

### Panel 4: Uptime Tracker
- **Title**: Service Uptime
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  up{job="hyper-sills"}
  ```
- **Visualization**: Stat
- **Mapping**: 1 = "UP", 0 = "DOWN"

---

## Step 4: Create Dashboard 2 — Performance

### Panel 1: Response Latency (p50, p95, p99)
- **Title**: Response Latency Percentiles
- **Data Source**: Prometheus
- **Metric Queries**:
  ```promql
  histogram_quantile(0.5, rate(hyper_sills_http_request_latency_seconds_bucket[5m])) * 1000  # p50
  histogram_quantile(0.95, rate(hyper_sills_http_request_latency_seconds_bucket[5m])) * 1000  # p95
  histogram_quantile(0.99, rate(hyper_sills_http_request_latency_seconds_bucket[5m])) * 1000  # p99
  ```
- **Visualization**: Graph
- **Unit**: Milliseconds
- **Series**: Show each percentile separately

### Panel 2: CPU Usage
- **Title**: CPU Usage
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  process_resident_memory_bytes / 1024 / 1024
  ```
- **Visualization**: Gauge
- **Unit**: Short
- **Thresholds**: Green <100MB, Yellow 100-500MB, Red >500MB

### Panel 3: Memory Usage
- **Title**: Memory Usage
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  process_resident_memory_bytes / 1024 / 1024
  ```
- **Visualization**: Gauge
- **Unit**: MB
- **Max**: 1000 (1GB limit)
- **Thresholds**: Green <100MB, Yellow 100-500MB, Red >500MB

### Panel 4: Search Latency by Backend
- **Title**: Search Latency (Keyword vs Semantic)
- **Data Source**: Prometheus
- **Metric Queries**:
  ```promql
  histogram_quantile(0.95, rate(hyper_sills_search_latency_seconds_bucket[5m])) * 1000
  histogram_quantile(0.95, rate(hyper_sills_semantic_search_latency_seconds_bucket[5m])) * 1000
  ```
- **Visualization**: Graph
- **Unit**: Milliseconds
- **Series**: "keyword" and "semantic"

---

## Step 5: Create Dashboard 3 — Multi-Region

### Panel 1: Traffic Distribution
- **Title**: Traffic by Region
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  sum(rate(hyper_sills_http_requests_total[5m])) by (region)
  ```
- **Visualization**: Pie Chart
- **Legend**: Show percentages

### Panel 2: Regional Latency Comparison
- **Title**: Latency by Region (p95)
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  histogram_quantile(0.95, rate(hyper_sills_http_request_latency_seconds_bucket[5m])) by (region) * 1000
  ```
- **Visualization**: Bar Chart
- **Unit**: Milliseconds

### Panel 3: Regional Error Rates
- **Title**: Error Rate by Region
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  (rate(hyper_sills_errors_total[5m]) / (rate(hyper_sills_http_requests_total[5m]) + 0.001)) * 100 by (region)
  ```
- **Visualization**: Graph
- **Unit**: Percent

### Panel 4: Failover Events
- **Title**: Failover/Recovery Events
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  changes(up[1h])
  ```
- **Visualization**: Stat
- **Description**: "0 = no failovers, >0 = failovers detected"

---

## Step 6: Create Dashboard 4 — Skill Registry

### Panel 1: Total Skills Loaded
- **Title**: Skills Loaded
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  hyper_sills_skills_loaded_total
  ```
- **Visualization**: Stat/Big Number
- **Font Size**: Large
- **Color**: Green

### Panel 2: Skills by Category
- **Title**: Skills per Category
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  hyper_sills_skills_by_category
  ```
- **Visualization**: Pie Chart / Bar Chart
- **Legend**: Show labels and percentages

### Panel 3: Search Performance by Tool
- **Title**: Tool Execution Latency
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  histogram_quantile(0.95, rate(hyper_sills_tool_execution_latency_seconds_bucket[5m])) * 1000 by (tool_name)
  ```
- **Visualization**: Table
- **Unit**: Milliseconds
- **Columns**: Tool Name, Latency (p95)

### Panel 4: Search Backend Health
- **Title**: Dense Embeddings Backend
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  hyper_sills_dense_embeddings_active
  ```
- **Visualization**: Stat
- **Mapping**: 1 = "ACTIVE", 0 = "INACTIVE"
- **Color Mapping**: Green = ACTIVE, Red = INACTIVE

### Panel 5: Registry Load Time
- **Title**: Last Registry Load Duration
- **Data Source**: Prometheus
- **Metric Query**:
  ```promql
  rate(hyper_sills_registry_load_time_seconds_sum[1h]) / rate(hyper_sills_registry_load_time_seconds_count[1h]) * 1000
  ```
- **Visualization**: Stat
- **Unit**: Milliseconds
- **Threshold**: Green <2000ms, Yellow 2-5s, Red >5s

---

## Step 7: Set Up Alerts (Optional but Recommended)

### Alert 1: High Error Rate
1. Go to **Alerting** → **Alert rules**
2. Create new rule:
   - **Name**: High Error Rate
   - **Condition**: `error_rate > 0.05` (5%)
   - **Duration**: 5 minutes
   - **Notification Channel**: Email (configure separately)

### Alert 2: High Latency
1. Create new rule:
   - **Name**: High Latency
   - **Condition**: `latency_p95 > 0.5` (500ms)
   - **Duration**: 10 minutes

### Alert 3: Service Down
1. Create new rule:
   - **Name**: Service Down
   - **Condition**: `up == 0`
   - **Duration**: 2 minutes

---

## Troubleshooting

### "No Data" in Panels
**Problem**: Prometheus data source not connected  
**Solution**: 
1. Check data source: Configuration → Data Sources
2. Verify Prometheus URL: `http://Prometheus:9090`
3. Test connection
4. Check that metrics are being scraped (Prometheus UI at port 9090)

### Metrics Not Showing
**Problem**: Instrumentation not enabled in mcp_server.py  
**Solution**:
1. Import prometheus_metrics in mcp_server.py
2. Add `/metrics` endpoint
3. Redeploy service
4. Wait 30 seconds for Prometheus to scrape

### Grafana Won't Load
**Problem**: Service offline or crashed  
**Solution**:
1. Check Railway dashboard for service status
2. Check logs for errors
3. Restart service if needed

---

## Next Steps

After Grafana is configured:
1. **Monitor dashboards** for 24 hours to ensure stability
2. **Add alerts** for critical metrics
3. **Customize colors** and thresholds based on your goals
4. **Share dashboards** with team members
5. **Proceed to Level 2**: Add code instrumentation

---

## Dashboard Export/Backup

To save your dashboards:
1. Dashboard menu (top right) → **Dashboard settings**
2. Click **Save dashboard**
3. Export via **Share** → **Export** (JSON)
4. Store JSON in your repo for version control

---

**Questions?** Check the [Grafana Documentation](https://grafana.com/docs/) or Railway docs.

**Ready for Level 2?** Start adding Prometheus instrumentation to your code!

