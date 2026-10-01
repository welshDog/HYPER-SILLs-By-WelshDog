"""MCP registration helpers for runnable HYPER-SILL execution templates."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from skill_execution import ExecutionError, SkillExecutor


def register_execution_tools(
    mcp: Any,
    find_by_id: Callable[[str], dict | None],
    content_and_gos: Callable[[dict], tuple[str | None, dict]],
    mercy_not_found: Callable[[str], str],
) -> None:
    """Register execution tools on an existing FastMCP server.

    Kept separate from the server so the bundled plugin and root server can share
    the exact same execution behavior without duplicating the renderer.
    """

    @mcp.tool()
    def get_skill_execution_schema(skill_id: str) -> str:
        """Return the runnable variables and examples declared by a skill."""
        meta = find_by_id(skill_id)
        if not meta:
            return mercy_not_found(skill_id)
        content, _gos = content_and_gos(meta)
        if content is None:
            return json.dumps({"ok": False, "error": f"Content unavailable for {meta.get('file')}"})
        executor = SkillExecutor(content)
        if not executor.has_execution_block:
            return json.dumps({
                "ok": False,
                "skill_id": meta.get("id"),
                "message": "No execution block found in this skill yet.",
                "next_step": "Add a fenced ```execution YAML block to the skill.",
            }, ensure_ascii=False, indent=2)
        return json.dumps({
            "ok": True,
            "skill_id": meta.get("id"),
            "hero_name": meta.get("hero_name"),
            "execution": executor.as_dict(),
            "variables": executor.variables,
            "examples": executor.examples,
        }, ensure_ascii=False, indent=2)

    @mcp.tool()
    def execute_skill_template(
        skill_id: str,
        variables: str = "{}",
        model_hint: str = "",
    ) -> str:
        """Render a skill execution block into a runnable model prompt payload.

        Args:
            skill_id: Skill ID such as HS-042.
            variables: JSON object containing template values.
            model_hint: Optional model/persona hint such as claude, gpt, gemini, or local.
        """
        meta = find_by_id(skill_id)
        if not meta:
            return mercy_not_found(skill_id)
        content, _gos = content_and_gos(meta)
        if content is None:
            return json.dumps({"ok": False, "error": f"Content unavailable for {meta.get('file')}"})

        try:
            values = json.loads(variables or "{}")
        except json.JSONDecodeError as exc:
            return json.dumps({"ok": False, "error": f"variables must be valid JSON: {exc}"}, indent=2)
        if not isinstance(values, dict):
            return json.dumps({"ok": False, "error": "variables must be a JSON object."}, indent=2)

        executor = SkillExecutor(content)
        if not executor.has_execution_block:
            return json.dumps({
                "ok": False,
                "skill_id": meta.get("id"),
                "message": "No execution block found in this skill yet.",
                "next_step": "Add a fenced ```execution YAML block to the skill.",
            }, ensure_ascii=False, indent=2)

        if model_hint:
            executor.exec_config["model"] = model_hint
        try:
            payload = executor.render_template(values)
        except (ExecutionError, TypeError, ValueError) as exc:
            return json.dumps({
                "ok": False,
                "skill_id": meta.get("id"),
                "error": str(exc),
                "schema_tool": f'get_skill_execution_schema("{meta.get("id")}")',
            }, ensure_ascii=False, indent=2)

        return json.dumps({
            "ok": True,
            "skill_id": meta.get("id"),
            "hero_name": meta.get("hero_name"),
            "model_hint": model_hint,
            "payload": payload,
        }, ensure_ascii=False, indent=2)


__all__ = ["register_execution_tools"]
