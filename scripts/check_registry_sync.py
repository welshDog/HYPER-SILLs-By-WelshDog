#!/usr/bin/env python3
"""
check_registry_sync.py - Fail if skill files on disk are missing from skills-registry.json
(or the registry points at files that no longer exist).

The registry is generated from the RESCUED table in vault-index.md. A skill file
that never got a row silently vanishes from the registry, the MCP server and the
search index. generate_registry.py only *warns* about that; this is the hard gate
for the pre-push hook.

    python scripts/check_registry_sync.py        # exit 0 clean, 1 on drift
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from generate_registry import reconcile_disk  # noqa: E402


def check(root: Path = ROOT) -> tuple[list[str], list[str]]:
    reg = json.loads((root / "skills-registry.json").read_text(encoding="utf-8"))
    skills = reg.get("skills", [])
    stranded = reconcile_disk(skills)
    dangling = [s["file"] for s in skills if s.get("file") and not (root / s["file"]).exists()]
    return stranded, dangling


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    stranded, dangling = check()
    if not stranded and not dangling:
        print("registry sync: OK - every skill file is registered, every row has a file")
        return 0
    for f in stranded:
        print(f"  on disk but NOT in registry: {f}")
    for f in dangling:
        print(f"  in registry but file MISSING: {f}")
    print("  fix: add a RESCUED row in vault-index.md, then `python scripts/generate_registry.py`")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
