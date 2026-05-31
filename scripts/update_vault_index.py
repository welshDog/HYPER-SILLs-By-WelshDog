#!/usr/bin/env python3
"""
📋 Vault Index Auto-Updater
Scans all skill folders and updates the RESCUED count + folder listings in vault-index.md
"""

import os
import re
from pathlib import Path
from datetime import datetime

DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"

# Vault folder → section header mapping
FOLDER_LABELS = {
    "agents": "Agents",
    "broski": "BROski",
    "content": "Content",
    "dev": "Dev",
    "docs": "Docs",
    "hypercode": "HyperCode",
    "web3": "Web3",
    "youtube": "YouTube",
}


def count_skills_in_folder(folder: Path) -> list[dict]:
    skills = []
    if not folder.exists():
        return skills
    for f in sorted(folder.glob("HS-*.md")):
        m = re.match(r'(HS-\d+)[\-_](.*)\.md', f.name)
        if m:
            skill_id = m.group(1)
            title = m.group(2).replace("-", " ").title()
            skills.append({"id": skill_id, "title": title, "file": f.name})
    return skills


def build_folder_summary(vault_root: Path) -> dict:
    summary = {}
    for folder_name in FOLDER_LABELS:
        folder_path = vault_root / folder_name
        skills = count_skills_in_folder(folder_path)
        summary[folder_name] = skills
    return summary


def update_vault_index(vault_root: Path, summary: dict):
    index_path = vault_root / "vault-index.md"
    if not index_path.exists():
        print("  ⚠️  vault-index.md not found — skipping update")
        return

    content = index_path.read_text()
    total_rescued = sum(len(v) for v in summary.values())
    today = datetime.utcnow().strftime("%Y-%m-%d")

    # Update last-updated timestamp if present
    content = re.sub(
        r'\*\*Last Updated:\*\*.*',
        f'**Last Updated:** {today} (auto-updated by rescue pipeline)',
        content
    )

    # Update RESCUED count
    content = re.sub(
        r'(\*\*)(\d+)(\*\* rescued)',
        lambda m: f"{m.group(1)}{total_rescued}{m.group(3)}",
        content
    )

    # Append auto-rescue summary block if not already there
    rescue_block = f"\n\n---\n\n## 🤖 Auto-Rescue Summary\n\n> Last run: {today}\n\n"
    for folder, skills in summary.items():
        if skills:
            rescue_block += f"### `{folder}/` — {len(skills)} skills\n"
            for s in skills:
                rescue_block += f"- [{s['id']}] {s['title']}\n"
            rescue_block += "\n"

    # Replace existing auto-rescue block or append
    if "## 🤖 Auto-Rescue Summary" in content:
        content = re.sub(
            r'\n\n---\n\n## 🤖 Auto-Rescue Summary.*',
            rescue_block,
            content,
            flags=re.DOTALL
        )
    else:
        content += rescue_block

    if not DRY_RUN:
        index_path.write_text(content)
        print(f"  ✅ vault-index.md updated — {total_rescued} total rescued skills")
    else:
        print(f"  🔍 [DRY RUN] Would update vault-index.md — {total_rescued} total skills")


def main():
    vault_root = Path(".")
    print("\n📋 Updating vault-index.md...")
    summary = build_folder_summary(vault_root)
    for folder, skills in summary.items():
        print(f"   {folder}/: {len(skills)} skills")
    update_vault_index(vault_root, summary)
    print("\n✅ Vault index update complete!")


if __name__ == "__main__":
    main()
