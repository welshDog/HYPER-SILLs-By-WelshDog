#!/usr/bin/env python3
"""
🤖 HYPER Auto-Rescue Skill Extractor
Scans source repos and extracts skills into the vault.
"""

import os
import re
import json
import requests
from pathlib import Path
from datetime import datetime

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
TARGET_REPOS = os.environ.get(
    "TARGET_REPOS",
    "welshDog/HyperCode-V2.4,welshDog/HyperAgent-SDK,welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne"
).split(",")
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Files to scan in each source repo
SOURCE_FILES = [
    "CLAUDE.md",
    "README.md",
    "WHATS_DONE.md",
    "AGENT-START.md",
    "docs/SKILLS.md",
    "docs/skills.md",
]

# Folder routing rules — keyword → vault folder
FOLDER_ROUTING = [
    (["agent", "swarm", "roster", "orchestrat"], "agents"),
    (["web3", "nft", "wallet", "pets", "wagmi", "rainbow"], "web3"),
    (["youtube", "content", "video", "script", "thumbnail"], "youtube"),
    (["docker", "deploy", "infra", "k8s", "kubernetes", "devops", "ci", "pipeline"], "dev"),
    (["broski", "adhd", "hyperfocus", "nd", "neurodivergent"], "broski"),
    (["hypercode", "fastapi", "container", "prometheus", "grafana", "redis"], "hypercode"),
]
DEFAULT_FOLDER = "dev"

# Skill block pattern — looks for ## HS-NNN or ## 🔥 sections
SKILL_PATTERN = re.compile(
    r'(#{1,3}\s+(?:HS-\d+[:\s]|🔥|⚡|🧠|🐕|🚀)[^\n]+\n(?:(?!#{1,3}\s).+\n?)*)',
    re.MULTILINE
)

# Next skill ID tracker
def get_next_skill_id(vault_root: Path) -> int:
    existing = []
    for f in vault_root.rglob("HS-*.md"):
        m = re.search(r'HS-(\d+)', f.stem)
        if m:
            existing.append(int(m.group(1)))
    # Also check skills-registry.json
    registry_path = vault_root / "skills-registry.json"
    if registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text())
            for skill in registry.get("skills", []):
                m = re.search(r'HS-(\d+)', skill.get("id", ""))
                if m:
                    existing.append(int(m.group(1)))
        except Exception:
            pass
    return max(existing, default=113) + 1


def route_to_folder(title: str, content: str) -> str:
    text = (title + " " + content).lower()
    for keywords, folder in FOLDER_ROUTING:
        if any(kw in text for kw in keywords):
            return folder
    return DEFAULT_FOLDER


def fetch_file(repo: str, filepath: str) -> str | None:
    url = f"https://api.github.com/repos/{repo}/contents/{filepath}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        import base64
        content = r.json().get("content", "")
        return base64.b64decode(content).decode("utf-8", errors="ignore")
    return None


def extract_skill_blocks(content: str, repo: str) -> list[dict]:
    blocks = []
    matches = SKILL_PATTERN.findall(content)
    for match in matches:
        title_line = match.split("\n")[0].strip("# ").strip()
        # Skip if it's already an HS-NNN skill
        if re.match(r'HS-\d+', title_line):
            continue
        # Only extract if block has meaningful content (>100 chars)
        if len(match) > 100:
            blocks.append({
                "title": title_line,
                "content": match.strip(),
                "source_repo": repo,
                "extracted_at": datetime.utcnow().strftime("%Y-%m-%d")
            })
    return blocks


def skill_file_exists(vault_root: Path, title: str) -> bool:
    """Check if a skill with similar title already exists."""
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    for f in vault_root.rglob("*.md"):
        if slug[:20] in f.stem.lower():
            return True
    return False


def write_skill_file(vault_root: Path, skill_id: int, skill: dict, folder: str) -> Path:
    slug = re.sub(r'[^a-z0-9]+', '-', skill['title'].lower()).strip('-')[:40]
    filename = f"HS-{skill_id:03d}-{slug}.md"
    folder_path = vault_root / folder
    folder_path.mkdir(parents=True, exist_ok=True)
    filepath = folder_path / filename

    skill_content = f"""# HS-{skill_id:03d}: {skill['title']}

> 🤖 Auto-rescued from `{skill['source_repo']}` on {skill['extracted_at']}
> ⚠️ Review and refine before use — auto-extracted, not manually curated.

---

## 📋 Skill Block

{skill['content']}

---

## 🏷️ Metadata

- **ID:** HS-{skill_id:03d}
- **Source:** [{skill['source_repo']}](https://github.com/{skill['source_repo']})
- **Folder:** `{folder}/`
- **Status:** 🟡 AUTO-RESCUED — needs review
- **Extracted:** {skill['extracted_at']}
"""
    if not DRY_RUN:
        filepath.write_text(skill_content)
        print(f"  ✅ Wrote: {folder}/{filename}")
    else:
        print(f"  🔍 [DRY RUN] Would write: {folder}/{filename}")
    return filepath


def main():
    vault_root = Path(".")
    print(f"\n🤖 Auto-Rescue Pipeline starting...")
    print(f"   Repos: {TARGET_REPOS}")
    print(f"   Dry run: {DRY_RUN}\n")

    next_id = get_next_skill_id(vault_root)
    total_extracted = 0

    for repo in TARGET_REPOS:
        repo = repo.strip()
        print(f"\n🔍 Scanning: {repo}")
        for source_file in SOURCE_FILES:
            content = fetch_file(repo, source_file)
            if not content:
                continue
            print(f"   📄 Found: {source_file}")
            blocks = extract_skill_blocks(content, repo)
            for block in blocks:
                if skill_file_exists(vault_root, block["title"]):
                    print(f"   ⏭️  Already exists: {block['title'][:50]}")
                    continue
                folder = route_to_folder(block["title"], block["content"])
                write_skill_file(vault_root, next_id, block, folder)
                next_id += 1
                total_extracted += 1

    print(f"\n✅ Auto-Rescue complete! {total_extracted} new skills extracted.")
    if DRY_RUN:
        print("   (DRY RUN — no files written)")


if __name__ == "__main__":
    main()
