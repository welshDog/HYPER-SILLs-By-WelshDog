"""Server-level guards: the checks that would have caught the PR #20 outage.

PR #20 shipped a module-scope NameError and a swallowed ImportError, and the live
MCP was down for two days. Importing the server and asserting its tool surface on
every test run (and in the pre-push hook) makes that impossible to ship quietly.
"""
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

import mcp_server  # noqa: E402  (import failing IS the regression this test exists for)

EXPECTED_TOOLS = {
    "get_model_profile", "get_model_optimized_skill", "search_skills", "semantic_search",
    "load_skill", "get_skill_graph", "recommend_for_task", "list_skills_by_category",
    "broski_agent", "brain_core_agent",
    "get_skill_execution_schema", "execute_skill_template",
}


def _tool_names() -> set[str]:
    return {t.name for t in asyncio.run(mcp_server.mcp.list_tools())}


def test_all_tools_registered():
    missing = EXPECTED_TOOLS - _tool_names()
    assert not missing, f"tools missing from server: {sorted(missing)}"


def test_search_skills_ranks_best_match_first():
    out = json.loads(mcp_server.search_skills(query="circuit breaker healer", limit=3))
    assert out["results"][0]["id"] == "HS-103"


def test_search_skills_is_order_independent_for_filters():
    out = json.loads(mcp_server.search_skills(category="youtube", limit=50))
    assert out["count"] == 4 and all(r["category"] == "youtube" for r in out["results"])


def test_semantic_search_category_filter():
    out = json.loads(mcp_server.semantic_search("how do I recover from errors", limit=5, category="agents"))
    assert out["count"] > 0
    assert all(r["category"] == "agents" for r in out["results"])


def test_gpt_payload_graph_hint_is_interpolated():
    meta = mcp_server.find_by_id("HS-008")
    content, gos = mcp_server._content_and_gos(meta)
    payload = mcp_server._build_model_optimized_payload(meta, gos, content, "gpt", "")
    steps = payload.get("payload", {}).get("next_steps", [])
    assert steps and not any("{skill_meta" in s for s in steps), steps


def test_health_reports_index_state():
    resp = asyncio.run(mcp_server.health(None))
    body = json.loads(resp.body)
    assert body["status"] == "ok"
    assert body["skills"] >= 100
    assert body["index"]["state"] in {"fresh", "stale", "unknown"}
    assert body["index_stale"] is False, body["index"]
