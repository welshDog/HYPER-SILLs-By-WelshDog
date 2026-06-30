#!/usr/bin/env python3
"""
build_plugin.py — Assemble the self-contained Claude Code plugin bundle.

A github plugin install caches ONLY the plugin dir, so the MCP server can't
reach the repo-root vault. This bundles everything the server needs into
`plugins/hyper-sills-vault/vault/`:

    vault/
      mcp_server.py          (copy of the repo server)
      skills-registry.json   (copy — used by search)
      skills-bundle.json     (registry + each skill's embedded markdown content)
      scripts/search_skills.py (copy — semantic search)

The server prefers skills-bundle.json (embedded content) so it needs no loose
.md files. Re-run this whenever skills or the server change, then commit
`plugins/hyper-sills-vault/vault/`.

    python scripts/build_plugin.py
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "skills-registry.json"
PLUGIN_DIR = REPO_ROOT / "plugins" / "hyper-sills-vault"
VAULT_OUT = PLUGIN_DIR / "vault"


def main() -> int:
    if not REGISTRY_PATH.exists():
        print("! skills-registry.json missing — run generate_registry.py first")
        return 1
    if not PLUGIN_DIR.exists():
        print(f"! plugin dir missing: {PLUGIN_DIR}")
        return 1

    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    skills = reg.get("skills", [])

    embedded, missing = 0, 0
    for s in skills:
        fp = REPO_ROOT / s.get("file", "")
        if fp.exists():
            s["content"] = fp.read_text(encoding="utf-8", errors="replace")
            embedded += 1
        else:
            missing += 1

    VAULT_OUT.mkdir(parents=True, exist_ok=True)
    (VAULT_OUT / "scripts").mkdir(exist_ok=True)

    # 1. Bundle (registry + embedded content)
    (VAULT_OUT / "skills-bundle.json").write_text(
        json.dumps(reg, ensure_ascii=False), encoding="utf-8")
    # 2. Plain registry (search_skills reads this)
    shutil.copyfile(REGISTRY_PATH, VAULT_OUT / "skills-registry.json")
    # 3. Server + semantic search module
    shutil.copyfile(REPO_ROOT / "mcp_server.py", VAULT_OUT / "mcp_server.py")
    shutil.copyfile(REPO_ROOT / "scripts" / "search_skills.py",
                    VAULT_OUT / "scripts" / "search_skills.py")
    # 4. Prebuilt dense index — so the plugin serves real embeddings immediately
    #    (only the live query is embedded) instead of rebuilding all 120 vectors on
    #    the first search. search_skills resolves it at vault/vector-store/.
    index_src = REPO_ROOT / "vector-store" / "skill_index.json"
    if index_src.exists():
        (VAULT_OUT / "vector-store").mkdir(exist_ok=True)
        shutil.copyfile(index_src, VAULT_OUT / "vector-store" / "skill_index.json")
        print(f"   + prebuilt index ({index_src.stat().st_size // 1024} KB, dense)")
    else:
        print("   ! no vector-store/skill_index.json — run embed_skills.py for dense search")

    bundle_kb = (VAULT_OUT / "skills-bundle.json").stat().st_size / 1024
    print(f"✅ built plugin bundle -> {VAULT_OUT.relative_to(REPO_ROOT)}")
    print(f"   {embedded} skills embedded ({missing} missing files)")
    print(f"   skills-bundle.json {bundle_kb:.0f} KB + mcp_server.py + search_skills.py + registry")
    print("   Remember to commit plugins/hyper-sills-vault/vault/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
