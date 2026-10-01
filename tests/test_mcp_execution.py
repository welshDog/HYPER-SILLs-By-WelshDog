"""Tests for MCP execution-tool registration."""

import json

from mcp_execution import register_execution_tools


class FakeMCP:
    def __init__(self):
        self.tools = {}

    def tool(self):
        def decorator(func):
            self.tools[func.__name__] = func
            return func
        return decorator


SKILL = '''---
skill_id: HS-042
hero_name: TEST EXECUTOR
category: dev
---

```execution
type: prompt-template
model: generic
system_prompt: |
  You are a {category} assistant.
user_prompt: |
  Process: {input_var}
variables:
  - name: input_var
    type: string
    required: true
  - name: mode
    type: choice
    choices: [fast, deep]
    default: fast
```
'''


def _fixtures():
    meta = {"id": "HS-042", "hero_name": "TEST EXECUTOR", "file": "test.md"}
    return meta, SKILL


def test_registers_schema_and_execution_tools():
    server = FakeMCP()
    meta, content = _fixtures()
    register_execution_tools(server, lambda _id: meta, lambda _meta: (content, {}), lambda _id: '{"ok": false}')
    assert set(server.tools) == {"get_skill_execution_schema", "execute_skill_template"}


def test_schema_tool_returns_variables():
    server = FakeMCP()
    meta, content = _fixtures()
    register_execution_tools(server, lambda _id: meta, lambda _meta: (content, {}), lambda _id: '{"ok": false}')
    result = json.loads(server.tools["get_skill_execution_schema"]("HS-042"))
    assert result["ok"] is True
    assert result["variables"][0]["name"] == "input_var"


def test_execute_tool_renders_payload_and_defaults():
    server = FakeMCP()
    meta, content = _fixtures()
    register_execution_tools(server, lambda _id: meta, lambda _meta: (content, {}), lambda _id: '{"ok": false}')
    result = json.loads(server.tools["execute_skill_template"]("HS-042", '{"input_var":"hello"}', "gpt"))
    assert result["ok"] is True
    assert result["payload"]["model"] == "gpt"
    assert "hello" in result["payload"]["user_prompt"]


def test_execute_tool_reports_invalid_json():
    server = FakeMCP()
    meta, content = _fixtures()
    register_execution_tools(server, lambda _id: meta, lambda _meta: (content, {}), lambda _id: '{"ok": false}')
    result = json.loads(server.tools["execute_skill_template"]("HS-042", "not-json"))
    assert result["ok"] is False
    assert "valid JSON" in result["error"]


def test_execute_tool_reports_missing_required_variable():
    server = FakeMCP()
    meta, content = _fixtures()
    register_execution_tools(server, lambda _id: meta, lambda _meta: (content, {}), lambda _id: '{"ok": false}')
    result = json.loads(server.tools["execute_skill_template"]("HS-042", "{}"))
    assert result["ok"] is False
    assert "input_var" in result["error"]
