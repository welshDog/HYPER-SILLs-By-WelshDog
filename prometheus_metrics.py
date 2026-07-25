"""
Prometheus metrics for HYPER-SILLs MCP Server.
Tracks skill searches, latency, errors, and backend health.
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import REGISTRY
import time
from typing import Callable, Any
import functools

# ─── Skill Search Metrics ───────────────────────────────────────────────────

skill_searches_total = Counter(
    'hyper_sills_searches_total',
    'Total skill searches',
    ['category', 'backend_type', 'status'],
    help='Count of skill searches by category and backend'
)

search_latency_seconds = Histogram(
    'hyper_sills_search_latency_seconds',
    'Skill search latency in seconds',
    ['backend_type', 'category'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0],
    help='Search operation latency distribution'
)

# ─── Semantic Search Metrics ───────────────────────────────────────────────

semantic_search_total = Counter(
    'hyper_sills_semantic_searches_total',
    'Total semantic searches',
    ['status'],
    help='Semantic search requests (success/fallback/error)'
)

semantic_search_latency_seconds = Histogram(
    'hyper_sills_semantic_search_latency_seconds',
    'Semantic search latency in seconds',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
    help='Semantic search operation latency'
)

# ─── Skill Load Metrics ──────────────────────────────────────────────────

skills_loaded_total = Gauge(
    'hyper_sills_skills_loaded_total',
    'Total skills in registry',
    help='Current count of loaded skills'
)

skills_by_category = Gauge(
    'hyper_sills_skills_by_category',
    'Skills per category',
    ['category'],
    help='Skill count breakdown by category'
)

registry_load_time_seconds = Histogram(
    'hyper_sills_registry_load_time_seconds',
    'Time to load skill registry',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
    help='Registry initialization latency'
)

# ─── Backend Health Metrics ──────────────────────────────────────────────

dense_embeddings_active = Gauge(
    'hyper_sills_dense_embeddings_active',
    'Whether dense embeddings backend is active (1=yes, 0=no)',
    help='Status of MiniLM-L6-v2 dense embeddings'
)

search_backend_latency_seconds = Histogram(
    'hyper_sills_search_backend_latency_seconds',
    'Latency of underlying search backend',
    ['backend'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0],
    help='Time to execute search on backend'
)

# ─── Tool Execution Metrics ──────────────────────────────────────────────

tool_executions_total = Counter(
    'hyper_sills_tool_executions_total',
    'Total tool executions',
    ['tool_name', 'status'],
    help='Count of tool calls by tool and result'
)

tool_execution_latency_seconds = Histogram(
    'hyper_sills_tool_execution_latency_seconds',
    'Tool execution latency',
    ['tool_name'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0],
    help='Time to execute tool'
)

# ─── Error Metrics ──────────────────────────────────────────────────────

errors_total = Counter(
    'hyper_sills_errors_total',
    'Total errors',
    ['error_type', 'tool_name'],
    help='Error count by type and tool'
)

# ─── Request Metrics (from health check) ────────────────────────────────

http_requests_total = Counter(
    'hyper_sills_http_requests_total',
    'Total HTTP requests',
    ['method', 'path', 'status_code'],
    help='HTTP request count'
)

http_request_latency_seconds = Histogram(
    'hyper_sills_http_request_latency_seconds',
    'HTTP request latency',
    ['method', 'path'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0],
    help='HTTP request latency'
)

# ─── Cache Metrics (when implemented) ──────────────────────────────────

cache_hits_total = Counter(
    'hyper_sills_cache_hits_total',
    'Total cache hits',
    ['cache_type'],
    help='Number of cache hits'
)

cache_misses_total = Counter(
    'hyper_sills_cache_misses_total',
    'Total cache misses',
    ['cache_type'],
    help='Number of cache misses'
)

cache_hit_rate = Gauge(
    'hyper_sills_cache_hit_rate',
    'Cache hit rate (0-1)',
    ['cache_type'],
    help='Ratio of cache hits to total requests'
)


# ─── Decorator for easy metric collection ──────────────────────────────

def track_metric(tool_name: str):
    """Decorator to automatically track tool execution metrics."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start
                tool_execution_latency_seconds.labels(tool_name=tool_name).observe(duration)
                tool_executions_total.labels(tool_name=tool_name, status='success').inc()
                return result
            except Exception as e:
                duration = time.time() - start
                tool_execution_latency_seconds.labels(tool_name=tool_name).observe(duration)
                tool_executions_total.labels(tool_name=tool_name, status='error').inc()
                error_type = type(e).__name__
                errors_total.labels(error_type=error_type, tool_name=tool_name).inc()
                raise

        def sync_wrapper(*args, **kwargs) -> Any:
            start = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start
                tool_execution_latency_seconds.labels(tool_name=tool_name).observe(duration)
                tool_executions_total.labels(tool_name=tool_name, status='success').inc()
                return result
            except Exception as e:
                duration = time.time() - start
                tool_execution_latency_seconds.labels(tool_name=tool_name).observe(duration)
                tool_executions_total.labels(tool_name=tool_name, status='error').inc()
                error_type = type(e).__name__
                errors_total.labels(error_type=error_type, tool_name=tool_name).inc()
                raise

        # Return async or sync wrapper based on function
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator


def get_metrics():
    """Get all metrics in Prometheus text format."""
    return generate_latest(REGISTRY)


import asyncio

