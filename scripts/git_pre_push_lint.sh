#!/bin/sh
# HYPER-SILLs pre-push gate — skill vault linter + MCP server smoke test.
#
# GitHub Actions is billing-locked for this account (hosted runs fail at
# job-startup with zero steps), so this LOCAL hook is the real quality gate —
# same pattern as the evo_harness pre-push gate on HyperCode.
#
#   1. scripts/skill_linter.py   — skill frontmatter / registry integrity
#   2. scripts/smoke_test.py     — py_compile + `import mcp_server` (guards the
#                                  2026-08-19 "unpinned mcp → 2.0.0 → crash on
#                                  import" outage; import check self-skips if the
#                                  runtime deps aren't installed on this machine)
#
# Installed by scripts/install_git_hooks.py into .git/hooks/pre-push.
# Override a single push with:  git push --no-verify

# Resolve repo root from the hook's location (.git/hooks -> repo root).
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$ROOT" ] && cd "$ROOT" || exit 0

# Prefer python, fall back to python3.
if command -v python >/dev/null 2>&1; then PY=python; else PY=python3; fi

echo "[HYPER-SILLs] pre-push (1/2): skill linter…"
PYTHONIOENCODING=utf-8 "$PY" scripts/skill_linter.py
if [ "$?" -ne 0 ]; then
  echo ""
  echo "[HYPER-SILLs] ❌ Lint FAILED — push blocked."
  echo "              Fix the errors above, or override once: git push --no-verify"
  exit 1
fi

echo "[HYPER-SILLs] pre-push (2/2): MCP server smoke test…"
PYTHONIOENCODING=utf-8 PYTHONUTF8=1 "$PY" scripts/smoke_test.py
if [ "$?" -ne 0 ]; then
  echo ""
  echo "[HYPER-SILLs] ❌ Smoke test FAILED — push blocked."
  echo "              mcp_server.py won't compile/import. Fix it, or override"
  echo "              once: git push --no-verify"
  exit 1
fi

echo "[HYPER-SILLs] ✅ Lint clean + smoke test passed — push allowed."
exit 0
