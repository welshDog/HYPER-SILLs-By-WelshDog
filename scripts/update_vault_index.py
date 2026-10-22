#!/usr/bin/env python3
"""Update the generated rescue summary in vault-index.md."""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"
FOLDER_LABELS = {
    "agents": "Agents", "broski": "BROski", "content": "Content", "dev": "Dev",
    "docs": "Docs", "hypercode": "HyperCode", "web3": "Web3", "youtube": "YouTube",
}


def count_skills_in_folder(folder: Path) -> list[dict]:
    skills = []
    if not folder.exists():
        return skills
    for path in sorted(folder.glob("HS-*.md")):
        match = re.match(r"(HS-\d+)[-_](.*)\.md", path.name)
        if match:
            skills.append({"id": match.group(1), "title": match.group(2).replace("-", " ").title(), "file": path.name})
    return skills


def build_folder_summary(vault_root: Path) -> dict:
    return {name: count_skills_in_folder(vault_root / name) for name in FOLDER_LABELS}


def update_vault_index(vault_root: Path, summary: dict) -> None:
    index_path = vault_root / "vault-index.md"
    if not index_path.exists():
        print("  [WARN] vault-index.md not found - skipping update")
        return
    content = index_path.read_text(encoding="utf-8")
    total = sum(len(items) for items in summary.values())
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(r"\*\*Last Updated:\*\*.*", f"**Last Updated:** {today} (auto-updated by rescue pipeline)", content)
    content = re.sub(r"(\*\*)(\d+)(\*\* rescued)", lambda m: f"{m.group(1)}{total}{m.group(3)}", content)
    block = f"\n\n---\n\n## 🤖 Auto-Rescue Summary\n\n> Last run: {today}\n\n"
    for folder, items in summary.items():
        if items:
            block += f"### `{folder}/` — {len(items)} skills\n"
            block += "".join(f"- [{item['id']}] {item['title']}\n" for item in items) + "\n"
    if "## 🤖 Auto-Rescue Summary" in content:
        content = re.sub(r"\n\n---\n\n## 🤖 Auto-Rescue Summary.*", block, content, flags=re.DOTALL)
    else:
        content += block
    if DRY_RUN:
        print(f"  [DRY RUN] Would update vault-index.md - {total} total skills")
    else:
        index_path.write_text(content, encoding="utf-8")
        print(f"  [OK] vault-index.md updated - {total} total skills")


def main() -> int:
    vault_root = Path(__file__).resolve().parent.parent
    print("\n[INFO] Updating vault-index.md...")
    summary = build_folder_summary(vault_root)
    for folder, items in summary.items():
        print(f"   {folder}/: {len(items)} skills")
    update_vault_index(vault_root, summary)
    print("\n[OK] Vault index update complete!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
