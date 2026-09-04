#!/usr/bin/env python3
"""
smoke_test.py — the cheapest possible "will the MCP server actually start?" check.

Born from the 2026-08-19 incident: `requirements.txt` had `mcp>=1.0.0`, a rebuild
resolved `mcp 2.0.0` (which deleted `mcp.server.fastmcp`), and the server crashed
on import before binding a port — the healthcheck failed 6/6 and the service was
down for 10 days. This would have caught it in under a second.

Two layers:
  1. py_compile mcp_server.py (+ the bundled plugin copy) — always runs, no deps
     needed. Catches syntax / indentation errors.
  2. `import mcp_server` and assert the skill vault loads — runs only if the
     runtime deps are actually installed. On a bare checkout (docs-only machine)
     it prints a skip line and still exits 0, so it never blocks a docs push.

Exit codes: 0 = clean (or skipped import), 1 = a real compile or import failure.

Used by scripts/git_pre_push_lint.sh (local pre-push gate) and
.github/workflows/smoke-test.yml (manual, for when Actions billing returns).
"""

from __future__ import annotations

import importlib.util
import py_compile
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGETS = [
    REPO_ROOT / "mcp_server.py",
    REPO_ROOT / "plugins" / "hyper-sills-vault" / "vault" / "mcp_server.py",
]
MIN_SKILLS = 100


def _compile_all() -> bool:
    ok = True
    for path in TARGETS:
        if not path.exists():
            print(f"  – skip (missing): {path.relative_to(REPO_ROOT)}")
            continue
        try:
            py_compile.compile(str(path), doraise=True)
            print(f"  ✓ compiled: {path.relative_to(REPO_ROOT)}")
        except py_compile.PyCompileError as exc:
            print(f"  ✗ COMPILE FAILED: {path.relative_to(REPO_ROOT)}\n    {exc}")
            ok = False
    return ok


def _import_check() -> bool:
    if importlib.util.find_spec("mcp") is None:
        print("  – runtime deps not installed on this machine — import check skipped.")
        print("    (CI / the Railway build still runs it against requirements.txt.)")
        return True
    sys.path.insert(0, str(REPO_ROOT))
    try:
        import mcp_server  # noqa: PLC0415  (deliberate late import)
    except Exception as exc:  # noqa: BLE001  — any import-time failure is a real fail
        print(f"  ✗ IMPORT FAILED: import mcp_server → {type(exc).__name__}: {exc}")
        return False
    try:
        n = len(mcp_server.skills_list())
    except Exception as exc:  # noqa: BLE001
        print(f"  ✗ skills_list() raised: {type(exc).__name__}: {exc}")
        return False
    if n < MIN_SKILLS:
        print(f"  ✗ only {n} skills loaded (expected ≥ {MIN_SKILLS}) — registry broken?")
        return False
    print(f"  ✓ import mcp_server → {n} skills loaded")
    return True


def main() -> int:
    print("[smoke] compile check…")
    compiled = _compile_all()
    print("[smoke] import check…")
    imported = _import_check()
    if compiled and imported:
        print("[smoke] ✅ clean")
        return 0
    print("[smoke] ❌ failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
