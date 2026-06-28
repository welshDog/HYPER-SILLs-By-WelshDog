#!/bin/sh
# HYPER-SILLs pre-push gate — runs the skill vault linter before every push.
#
# GitHub Actions is billing-locked for this account (hosted runs fail at
# job-startup with zero steps), so this LOCAL hook is the real quality gate —
# same pattern as the evo_harness pre-push gate on HyperCode.
#
# Installed by scripts/install_git_hooks.py into .git/hooks/pre-push.
# Override a single push with:  git push --no-verify

# Resolve repo root from the hook's location (.git/hooks -> repo root).
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$ROOT" ] && cd "$ROOT" || exit 0

echo "[HYPER-SILLs] pre-push: running skill linter..."

# Prefer python, fall back to python3.
if command -v python >/dev/null 2>&1; then PY=python; else PY=python3; fi
PYTHONIOENCODING=utf-8 "$PY" scripts/skill_linter.py
STATUS=$?

if [ "$STATUS" -ne 0 ]; then
  echo ""
  echo "[HYPER-SILLs] ❌ Lint FAILED — push blocked."
  echo "              Fix the errors above, or override once: git push --no-verify"
  exit 1
fi

echo "[HYPER-SILLs] ✅ Lint clean — push allowed."
exit 0
