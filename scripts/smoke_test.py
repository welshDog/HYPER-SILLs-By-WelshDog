#!/usr/bin/env python3
"""Compile and import smoke test for the MCP server and plugin bundle."""
from __future__ import annotations

import importlib.util
import py_compile
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGETS = [REPO_ROOT / "mcp_server.py", REPO_ROOT / "plugins" / "hyper-sills-vault" / "vault" / "mcp_server.py"]
MIN_SKILLS = 100


def _compile_all() -> bool:
    ok = True
    for path in TARGETS:
        if not path.exists():
            print(f"  [SKIP] missing: {path.relative_to(REPO_ROOT)}")
            continue
        try:
            py_compile.compile(str(path), doraise=True)
            print(f"  [OK] compiled: {path.relative_to(REPO_ROOT)}")
        except py_compile.PyCompileError as exc:
            print(f"  [FAIL] compile: {path.relative_to(REPO_ROOT)}\n    {exc}")
            ok = False
    return ok


def _import_check() -> bool:
    if importlib.util.find_spec("mcp") is None:
        print("  [SKIP] runtime dependencies are not installed; import check skipped.")
        return True
    sys.path.insert(0, str(REPO_ROOT))
    try:
        import mcp_server
        count = len(mcp_server.skills_list())
    except Exception as exc:
        print(f"  [FAIL] import mcp_server: {type(exc).__name__}: {exc}")
        return False
    if count < MIN_SKILLS:
        print(f"  [FAIL] loaded {count} skills; expected at least {MIN_SKILLS}")
        return False
    print(f"  [OK] import mcp_server: {count} skills loaded")
    return True


def main() -> int:
    print("[smoke] compile check...")
    compiled = _compile_all()
    print("[smoke] import check...")
    imported = _import_check()
    print("[smoke] CLEAN" if compiled and imported else "[smoke] FAILED")
    return 0 if compiled and imported else 1


if __name__ == "__main__":
    raise SystemExit(main())
