#!/usr/bin/env python3
"""HyperFocus Z0ne - HYPER-SILLs Config Validator.

Enforces Sacred Rules on skills-registry.json and .mcp.json:
  - NEVER docker.io image references
  - NEVER 'from backend.app.' in inline commands
  - WARN if MCP server command uses an absolute Windows path (portability)

Usage:
    python scripts/sills_config_validator.py skills-registry.json
    python scripts/sills_config_validator.py .mcp.json
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_BANNED_IMAGE_PREFIXES = ("docker.io/", "index.docker.io/")
_BANNED_IMPORT_RE = re.compile(r"from\s+backend\.app\.")
_WIN_ABS_PATH_RE = re.compile(r"[A-Za-z]:\\\\")


def _resolve_config(arg):
    p = Path(arg)
    if p.is_absolute():
        return p
    for base in (Path.cwd(), ROOT):
        candidate = base / p
        if candidate.exists():
            return candidate
    return Path.cwd() / p


def validate(config_path):
    errors = []
    warnings = []

    if not config_path.exists():
        errors.append("file not found: " + str(config_path))
        return errors, warnings

    for i, raw in enumerate(config_path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.strip()
        if not stripped:
            continue

        for prefix in _BANNED_IMAGE_PREFIXES:
            if prefix in stripped:
                errors.append("line " + str(i) + ": docker.io reference -- " + repr(stripped))

        if _BANNED_IMPORT_RE.search(stripped):
            errors.append("line " + str(i) + ": forbidden 'from backend.app.*' -- " + repr(stripped))

        if _WIN_ABS_PATH_RE.search(stripped):
            warnings.append("line " + str(i) + ": hardcoded Windows path -- prefer relative or env var")

    return errors, warnings


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/sills_config_validator.py <config-file>")
        return 2

    config_path = _resolve_config(sys.argv[1])

    print("\n[CONFIG VALIDATOR] HyperFocus Z0ne SILLs -- " + sys.argv[1])
    print("-" * 40)
    print("   Path: " + str(config_path))
    print()

    errors, warnings = validate(config_path)

    for w in warnings:
        print("   WARN  " + w)
    if warnings:
        print()

    if errors:
        for e in errors:
            print("   FAIL  " + e)
        print()
        print("FAIL  Validation FAILED -- " + str(len(errors)) + " error(s).\n")
        return 1

    print("PASS  " + config_path.name + " passed all Sacred Rules checks!")
    if warnings:
        print("      (" + str(len(warnings)) + " warning(s) -- non-blocking)")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
