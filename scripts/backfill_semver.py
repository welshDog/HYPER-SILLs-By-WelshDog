#!/usr/bin/env python3
"""
backfill_semver.py — One-time migration: semver + lifecycle status for legacy skills.

Legacy rescued skills carry `version: v1.0` and no `status:` line. This normalises
every skill's FRONTMATTER `version:` to 3-part semver (v1.0 -> v1.0.0) and adds
`status: ACTIVE` where missing — so the registry and linter see a real lifecycle.

Touches ONLY the frontmatter `version:`/`status:` lines (raw-text edit preserves
each file's existing line endings, so no CRLF churn). Idempotent — safe to re-run.

    python scripts/backfill_semver.py --check    # dry run, report only
    python scripts/backfill_semver.py            # apply
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "skills-registry.json"

VERSION_RE = re.compile(r"(?m)^(version:[ \t]*)(v\S+?)([ \t]*\r?\n)")
STATUS_RE = re.compile(r"(?m)^status:[ \t]*\S")
SEMVER_RE = re.compile(r"^v(\d+)(?:\.(\d+))?(?:\.(\d+))?$")
DEFAULT_STATUS = "ACTIVE"


def to_semver(v: str) -> str:
    m = SEMVER_RE.match(v.strip())
    if not m:
        return v  # leave anything non-numeric untouched
    major, minor, patch = m.group(1), m.group(2) or "0", m.group(3) or "0"
    return f"v{major}.{minor}.{patch}"


def migrate_text(text: str) -> tuple[str, bool]:
    m = VERSION_RE.search(text)
    if not m:
        return text, False
    old_v = m.group(2)
    new_v = to_semver(old_v)
    has_status = STATUS_RE.search(text) is not None

    line_end = "\r\n" if m.group(3).endswith("\r\n") else "\n"
    repl = f"{m.group(1)}{new_v}{m.group(3)}"
    if not has_status:
        repl += f"status: {DEFAULT_STATUS}{line_end}"

    if repl == m.group(0):
        return text, False
    return text[: m.start()] + repl + text[m.end():], True


def skill_files() -> list[Path]:
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    seen, out = set(), []
    for s in reg.get("skills", []):
        fp = REPO_ROOT / s.get("file", "")
        key = str(fp)
        if fp.exists() and key not in seen:
            seen.add(key)
            out.append(fp)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Backfill semver + status into skill frontmatter.")
    ap.add_argument("--check", action="store_true", help="Dry run — report only")
    args = ap.parse_args()

    changed, skipped = [], 0
    for fp in skill_files():
        raw = fp.read_text(encoding="utf-8", newline="")  # keep original line endings
        new, did = migrate_text(raw)
        if did:
            changed.append(fp)
            if not args.check:
                fp.write_text(new, encoding="utf-8", newline="")  # write bytes as-is
        else:
            skipped += 1

    verb = "would update" if args.check else "updated"
    print(f"{verb} {len(changed)} files  (skipped {skipped} already-compliant)")
    for fp in changed[:8]:
        print(f"  {verb}: {fp.relative_to(REPO_ROOT)}")
    if len(changed) > 8:
        print(f"  ... +{len(changed) - 8} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
