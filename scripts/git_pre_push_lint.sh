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

echo "[HYPER-SILLs] pre-push (1/5): skill linter…"
PYTHONIOENCODING=utf-8 "$PY" scripts/skill_linter.py
if [ "$?" -ne 0 ]; then
  echo ""
  echo "[HYPER-SILLs] ❌ Lint FAILED — push blocked."
  echo "              Fix the errors above, or override once: git push --no-verify"
  exit 1
fi

echo "[HYPER-SILLs] pre-push (2/5): MCP server smoke test…"
PYTHONIOENCODING=utf-8 PYTHONUTF8=1 "$PY" scripts/smoke_test.py
if [ "$?" -ne 0 ]; then
  echo ""
  echo "[HYPER-SILLs] ❌ Smoke test FAILED — push blocked."
  echo "              mcp_server.py won't compile/import. Fix it, or override"
  echo "              once: git push --no-verify"
  exit 1
fi

echo "[HYPER-SILLs] pre-push (3/5): registry <-> disk sync…"
PYTHONIOENCODING=utf-8 PYTHONUTF8=1 "$PY" scripts/check_registry_sync.py
if [ "$?" -ne 0 ]; then
  echo ""
  echo "[HYPER-SILLs] ❌ Registry drift — push blocked (a skill file would be invisible to the MCP)."
  exit 1
fi

echo "[HYPER-SILLs] pre-push (4/5): search index freshness…"
PYTHONIOENCODING=utf-8 PYTHONUTF8=1 "$PY" scripts/embed_skills.py --check
if [ "$?" -ne 0 ]; then
  echo ""
  echo "[HYPER-SILLs] ❌ Search index is stale — rebuild it and commit vector-store/skill_index.json."
  exit 1
fi

echo "[HYPER-SILLs] pre-push (5/5): pytest (server surface + search quality, ~1 min)…"
if "$PY" -c "import pytest" >/dev/null 2>&1; then
  PYTHONIOENCODING=utf-8 PYTHONUTF8=1 "$PY" -m pytest -q -x
  if [ "$?" -ne 0 ]; then
    echo ""
    echo "[HYPER-SILLs] ❌ Tests FAILED — push blocked."
    exit 1
  fi
else
  echo "              (pytest not installed here — skipped)"
fi

echo "[HYPER-SILLs] ✅ Lint clean + smoke test + sync + index + tests passed — push allowed."
exit 0
