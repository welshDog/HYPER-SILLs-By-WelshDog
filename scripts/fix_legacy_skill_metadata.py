import re
from pathlib import Path

SKILL_DIRS = ["agents", "content", "dev", "youtube", "broski", "hypercode"]
EXCLUDED_FILES = {"SKILL_TEMPLATE.md", "README.md"}

HEADER_RE = re.compile(r"^#\s+HS-\d{3,}\b")
VERSION_RE = re.compile(r"_v(\d+)\.md$", re.IGNORECASE)


def derive_version(filename: str) -> str:
    m = VERSION_RE.search(filename)
    if not m:
        return "1.0"
    return f"{int(m.group(1))}.0"


def has_frontmatter(lines: list[str]) -> bool:
    first = None
    for i, line in enumerate(lines[:30]):
        if line.strip():
            first = i
            break
    if first is None:
        return False
    if lines[first].strip() != "---":
        return False
    for j in range(first + 1, min(len(lines), first + 31)):
        if lines[j].strip() == "---":
            return True
    return False


def inject_blocks(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    if has_frontmatter(lines):
        return False

    header_idx = None
    for i, line in enumerate(lines):
        if line.strip() and HEADER_RE.match(line.strip()):
            header_idx = i
            break

    if header_idx is None:
        return False

    category = path.parent.name
    version = derive_version(path.name)

    need_category = "**Category:**" not in content
    need_version = "**Version:**" not in content

    needs_code_block = "```" not in content
    prompt_heading_present = re.search(r"(?im)^##\s+.*prompt.*$", content) is not None

    insert_lines: list[str] = []
    if need_category:
        insert_lines.append(f"**Category:** {category}")
    if need_version:
        insert_lines.append(f"**Version:** {version}")

    if insert_lines:
        if header_idx + 1 < len(lines) and lines[header_idx + 1].strip() == "":
            pass
        else:
            insert_lines.append("")
        lines[header_idx + 1:header_idx + 1] = insert_lines

    if needs_code_block:
        if not prompt_heading_present:
            lines.append("")
            lines.append("## 📋 THE PROMPT")
        lines.append("")
        lines.append("```text")
        lines.append("Use this skill by copying the relevant sections and adapting placeholders to your context.")
        lines.append("```")

    new_content = "\n".join(lines).rstrip() + "\n"
    original = content if content.endswith("\n") else content + "\n"
    if new_content == original:
        return False

    path.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    root = Path(".")
    changed = 0
    for d in SKILL_DIRS:
        dirpath = root / d
        if not dirpath.exists():
            continue
        for f in dirpath.glob("**/*.md"):
            if f.name in EXCLUDED_FILES:
                continue
            if inject_blocks(f):
                changed += 1
    print(f"Updated {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
