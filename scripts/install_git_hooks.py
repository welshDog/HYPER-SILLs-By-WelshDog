#!/usr/bin/env python3
"""
install_git_hooks.py — Install the HYPER-SILLs local pre-push lint gate.

GitHub Actions is billing-locked for this account, so the skill linter runs as a
LOCAL pre-push hook instead (mirrors the evo_harness gate on HyperCode). This
installs scripts/git_pre_push_lint.sh into .git/hooks/pre-push WITHOUT clobbering
the existing XP post-commit hook.

    python scripts/install_git_hooks.py          # install / refresh
    python scripts/install_git_hooks.py --check   # report only, write nothing

Re-run after a fresh clone (git hooks are not cloned).
"""

from __future__ import annotations

import argparse
import shutil
import stat
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOK_SRC = REPO_ROOT / "scripts" / "git_pre_push_lint.sh"
HOOKS_DIR = REPO_ROOT / ".git" / "hooks"
MARKER = "HYPER-SILLs pre-push gate"


def main() -> int:
    ap = argparse.ArgumentParser(description="Install the pre-push lint hook.")
    ap.add_argument("--check", action="store_true", help="Report only, don't write")
    args = ap.parse_args()

    if not HOOK_SRC.exists():
        print(f"! hook source missing: {HOOK_SRC}")
        return 1
    if not HOOKS_DIR.exists():
        print(f"! not a git repo (no {HOOKS_DIR}) — run from a clone")
        return 1

    dest = HOOKS_DIR / "pre-push"
    if dest.exists():
        existing = dest.read_text(encoding="utf-8", errors="replace")
        if MARKER in existing:
            print(f"pre-push hook already installed ({dest}) — refreshing.")
        else:
            print(f"! a different pre-push hook exists at {dest} — not overwriting.")
            print("  Inspect it; merge manually or remove it, then re-run.")
            return 1

    if args.check:
        print(f"would install {HOOK_SRC.name} -> {dest}")
        return 0

    shutil.copyfile(HOOK_SRC, dest)
    dest.chmod(dest.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f"✅ installed pre-push lint gate -> {dest}")
    print("   Every push now runs scripts/skill_linter.py first.")
    print("   Override a single push with: git push --no-verify")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
