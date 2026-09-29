#!/usr/bin/env python3
"""Skill execution helpers for HYPER-SILLs.

Turn a passive markdown skill into a runnable prompt template / command pack.
This intentionally keeps the implementation lightweight and dependency-free so it
works in docs-only, CI, and MCP-hosted environments without forcing YAML libs.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any


class ExecutionError(ValueError):
    """Raised when a skill execution block is malformed or variables are invalid."""


def _safe_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.lower() in {"null", "none"}:
        return None
    if re.fullmatch(r"[-+]?\d+", value):
        return int(value)
    if re.fullmatch(r"[-+]?\d+\.\d+", value):
        return float(value)
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except Exception:
            return [part.strip().strip("\"'") for part in value[1:-1].split(",") if part.strip()]
    if value.startswith("{") and value.endswith("}"):
        try:
            return json.loads(value)
        except Exception:
            return value
    if value.startswith("\"") and value.endswith("\""):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def _load_yaml_subset(raw: str) -> dict[str, Any]:
    """Minimal YAML parser for the execution block subset used in skills.

    Supports:
    - top-level dicts
    - nested dicts
    - list items in the form '- key: value'
    - multi-line block scalars using '|' and '>'
    """
    text = raw.strip()
    if not text:
        return {}

    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return data
        if data is None:
            return {}
        return {"value": data}
    except Exception:
        pass

    lines = text.splitlines()
    idx = 0
    root: dict[str, Any] = {}

    def parse_indented_block(start: int, indent: int) -> tuple[Any, int]:
        items: list[Any] = []
        mapping: dict[str, Any] = {}
        while start < len(lines):
            line = lines[start]
            if not line.strip() or line.lstrip().startswith("#"):
                start += 1
                continue
            current_indent = len(line) - len(line.lstrip(" "))
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ExecutionError(f"Unexpected indentation in execution block near: {line!r}")
            stripped = line.strip()
            if stripped.startswith("- "):
                # list item
                item_text = stripped[2:].strip()
                if not item_text:
                    start += 1
                    if start < len(lines):
                        value, start = parse_indented_block(start, indent + 2)
                        items.append(value)
                    continue
                if ":" in item_text and not item_text.startswith("{"):
                    key, remainder = item_text.split(":", 1)
                    key = key.strip()
                    remainder = remainder.strip()
                    item = {key: remainder if remainder else None}
                    start += 1
                    while start < len(lines):
                        next_line = lines[start]
                        if not next_line.strip() or next_line.lstrip().startswith("#"):
                            start += 1
                            continue
                        next_indent = len(next_line) - len(next_line.lstrip(" "))
                        if next_indent <= indent:
                            break
                        if next_indent == indent + 2 and next_line.strip().startswith("-"):
                            break
                        if next_indent > indent + 2:
                            nested_value, start = parse_indented_block(start, indent + 2)
                            item[key] = nested_value
                            continue
                        nested_key, nested_value = next_line.strip().split(":", 1)
                        nested_key = nested_key.strip()
                        nested_value = nested_value.strip()
                        start += 1
                        if nested_value == "|":
                            block_lines: list[str] = []
                            while start < len(lines):
                                candidate = lines[start]
                                cand_indent = len(candidate) - len(candidate.lstrip(" "))
                                if cand_indent <= indent + 2:
                                    break
                                block_lines.append(candidate[indent + 4 :])
                                start += 1
                            item[nested_key] = "\n".join(block_lines)
                        else:
                            item[nested_key] = _safe_scalar(nested_value)
                    items.append(item)
                    continue
                items.append(_safe_scalar(item_text))
                start += 1
                continue
            key, remainder = stripped.split(":", 1)
            key = key.strip()
            remainder = remainder.strip()
            start += 1
            if remainder == "|":
                block_lines: list[str] = []
                while start < len(lines):
                    candidate = lines[start]
                    cand_indent = len(candidate) - len(candidate.lstrip(" "))
                    if cand_indent <= indent:
                        break
                    block_lines.append(candidate[indent + 2 :])
                    start += 1
                mapping[key] = "\n".join(block_lines)
                continue
            if remainder == "":
                if start < len(lines):
                    next_line = lines[start]
                    next_indent = len(next_line) - len(next_line.lstrip(" "))
                    if next_indent > indent:
                        nested_value, start = parse_indented_block(start, next_indent)
                        mapping[key] = nested_value
                        continue
                mapping[key] = None
                continue
            mapping[key] = _safe_scalar(remainder)

        if items:
            return items, start
        return mapping, start

    parsed, _ = parse_indented_block(0, 0)
    if isinstance(parsed, dict):
        return parsed
    return {"value": parsed}


def parse_execution_block(skill_text: str) -> dict[str, Any]:
    """Return the execution block dict from a skill markdown blob."""
    if not skill_text or not isinstance(skill_text, str):
        return {}

    patterns = [
        re.compile(r"```\s*execution\s*\n(.*?)```", re.IGNORECASE | re.DOTALL),
        re.compile(r"```\s*yaml\s*\n(.*?)```", re.IGNORECASE | re.DOTALL),
        re.compile(r"##\s*Execution Block\s*\n```\s*execution\s*\n(.*?)```", re.IGNORECASE | re.DOTALL),
    ]

    for pattern in patterns:
        match = pattern.search(skill_text)
        if match:
            payload = match.group(1).strip()
            if payload:
                parsed = _load_yaml_subset(payload)
                if isinstance(parsed, dict):
                    return parsed
                raise ExecutionError("Execution block must decode to a YAML object.")
            break

    return {}


@dataclass
class SkillExecutor:
    """Parse and render a skill execution block into a runnable prompt template."""

    skill_text: str
    exec_config: dict[str, Any] = field(default_factory=dict)
    variables: list[dict[str, Any]] = field(default_factory=list)
    examples: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.exec_config = parse_execution_block(self.skill_text)
        if self.exec_config:
            self.variables = list(self.exec_config.get("variables", []) or [])
            self.examples = list(self.exec_config.get("examples", []) or [])
        else:
            self.variables = []
            self.examples = []

    @property
    def has_execution_block(self) -> bool:
        return bool(self.exec_config)

    @property
    def category(self) -> str:
        match = re.search(r"^category:\s*[\"']?([^\n\r]+?)[\"']?\s*$", self.skill_text, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return "dev"

    def _coerce_value(self, name: str, value: Any, spec: dict[str, Any]) -> Any:
        expected_type = (spec.get("type") or "string").lower()
        if value is None:
            if "default" in spec:
                value = spec["default"]
            elif expected_type == "bool":
                value = False
            else:
                value = ""

        if expected_type in {"choice", "enum"}:
            choices = spec.get("choices") or []
            if choices and value not in choices:
                raise ExecutionError(f"Variable '{name}' must be one of {choices!r}; got {value!r}")
            return value

        if expected_type in {"int", "integer"}:
            return int(value)
        if expected_type in {"float", "number"}:
            return float(value)
        if expected_type == "bool":
            if isinstance(value, str):
                return value.lower() in {"1", "true", "yes", "y", "on"}
            return bool(value)
        return str(value)

    def render_template(self, values: dict[str, Any] | None = None) -> dict[str, Any]:
        """Render a skill execution block into a runnable payload."""
        if not self.exec_config:
            raise ExecutionError("Skill does not contain an execution block.")

        merged: dict[str, Any] = dict(values or {})
        merged.setdefault("category", self.category)

        for variable in self.variables:
            if not isinstance(variable, dict):
                continue
            name = variable.get("name")
            if not name:
                continue

            if name not in merged:
                if "default" in variable:
                    merged[name] = variable["default"]
                elif variable.get("required"):
                    raise ExecutionError(f"Missing required variable '{name}' for the execution template.")
                else:
                    merged[name] = ""

            merged[name] = self._coerce_value(name, merged[name], variable)

        system_prompt = self.exec_config.get("system_prompt", "")
        user_prompt = self.exec_config.get("user_prompt", "")

        if not isinstance(system_prompt, str):
            system_prompt = str(system_prompt)
        if not isinstance(user_prompt, str):
            user_prompt = str(user_prompt)

        class _SafeDict(dict):
            def __missing__(self, key: str) -> str:
                return "{" + key + "}"

        rendered = {
            "type": self.exec_config.get("type", "prompt-template"),
            "model": self.exec_config.get("model", "generic"),
            "temperature": self.exec_config.get("temperature", 0.0),
            "max_tokens": self.exec_config.get("max_tokens", 2000),
            "system_prompt": system_prompt.format_map(_SafeDict(merged)),
            "user_prompt": user_prompt.format_map(_SafeDict(merged)),
            "variables": self.variables,
            "examples": self.examples,
            "output_format": merged.get("output_format", self.exec_config.get("output_format", "json")),
        }
        rendered.update({k: v for k, v in merged.items() if k not in {"category"}})
        return rendered

    def as_dict(self) -> dict[str, Any]:
        return dict(self.exec_config)


def prepare_skill_template(skill_text: str, values: dict[str, Any] | None = None, model_hint: str | None = None) -> dict[str, Any]:
    """Prepare the runnable payload from a markdown skill.

    Returns:
        {"success": True, "payload": {...}} on success.
        {"success": False, "error": "..."} on failure.
    """
    try:
        executor = SkillExecutor(skill_text)
        if not executor.has_execution_block:
            return {"success": False, "error": "No execution block found in this skill."}
        merged_values = dict(values or {})
        if model_hint:
            merged_values["model_hint"] = model_hint
            executor.exec_config["model"] = model_hint
        payload = executor.render_template(merged_values)
        return {"success": True, "payload": payload}
    except ExecutionError as exc:
        return {"success": False, "error": str(exc)}


__all__ = [
    "ExecutionError",
    "SkillExecutor",
    "parse_execution_block",
    "prepare_skill_template",
]
