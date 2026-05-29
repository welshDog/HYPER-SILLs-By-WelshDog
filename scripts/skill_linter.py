#!/usr/bin/env python3
"""
HYPER-SILLs Skill Vault Linter
Checks every skill .md file for required structure.
Usage: python scripts/skill_linter.py
"""

import os
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── Config ─────────────────────────────────────────────────────────────────
SKILL_DIRS = ["agents", "content", "dev", "youtube", "broski"]
EXCLUDED_FILES = {"SKILL_TEMPLATE.md", "README.md"}

REQUIRED_FRONTMATTER = ["id:", "hero_name:", "category:", "version:", "last_updated:", "best_for:"]
REQUIRED_HEADINGS    = ["## 🎯 Purpose", "## 📥 Inputs", "## 📤 Output Format", "## 🔮 Prompt Block", "## 💡 Example Usage", "## 🔗 Related Skills"]

VALID_CATEGORIES = {"coding", "content", "design", "agents", "youtube", "automation", "ND-friendly", "broski"}
VALID_DIFFICULTIES = {"beginner", "intermediate", "advanced"}

SKILL_ID_PATTERN = re.compile(r"^id:\s+SKILL_\d{3,}")
VERSION_PATTERN  = re.compile(r"^version:\s+v\d+\.\d+")
DATE_PATTERN     = re.compile(r"^last_updated:\s+\d{4}-\d{2}-\d{2}")

# ── Colours ─────────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ok(msg):   print(f"  {GREEN}✅ {msg}{RESET}")
def fail(msg): print(f"  {RED}❌ {msg}{RESET}")
def warn(msg): print(f"  {YELLOW}⚠️  {msg}{RESET}")

def has_yaml_frontmatter(lines: list[str]) -> bool:
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

def lint_yaml_file(content: str, lines: list[str]) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    in_fm = False
    fm_lines: list[str] = []
    for line in lines:
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                break
        if in_fm:
            fm_lines.append(line)

    if not fm_lines:
        errors.append("No YAML frontmatter block found (expected --- ... ---)")
    else:
        fm_text = "\n".join(fm_lines)

        for field in REQUIRED_FRONTMATTER:
            if field not in fm_text:
                errors.append(f"Missing frontmatter field: {field}")

        id_match = [l for l in fm_lines if l.startswith("id:")]
        if id_match:
            if not SKILL_ID_PATTERN.match(id_match[0]):
                errors.append(f"Bad ID format (expected SKILL_NNN): '{id_match[0].strip()}'")

        ver_match = [l for l in fm_lines if l.startswith("version:")]
        if ver_match:
            if not VERSION_PATTERN.match(ver_match[0]):
                warnings.append(f"Version should be vX.Y format: '{ver_match[0].strip()}'")

        date_match = [l for l in fm_lines if l.startswith("last_updated:")]
        if date_match:
            if not DATE_PATTERN.match(date_match[0]):
                errors.append(f"last_updated should be YYYY-MM-DD: '{date_match[0].strip()}'")

        cat_match = [l for l in fm_lines if l.startswith("category:")]
        if cat_match:
            cats = [c.strip() for c in cat_match[0].split(":", 1)[1].split("|")]
            for c in cats:
                if c and c not in VALID_CATEGORIES:
                    warnings.append(f"Unknown category '{c}' (valid: {', '.join(sorted(VALID_CATEGORIES))})")

        diff_match = [l for l in fm_lines if l.startswith("difficulty:")]
        if diff_match:
            diff = diff_match[0].split(":", 1)[1].strip()
            if diff not in VALID_DIFFICULTIES:
                warnings.append(f"Unknown difficulty '{diff}' (valid: beginner, intermediate, advanced)")

    for heading in REQUIRED_HEADINGS:
        if heading not in content:
            errors.append(f"Missing required section: {heading}")

    prompt_idx = content.find("## 🔮 Prompt Block")
    if prompt_idx != -1:
        after_prompt = content[prompt_idx + len("## 🔮 Prompt Block"):].strip()
        if len(after_prompt) < 30:
            errors.append("Prompt Block section looks empty (less than 30 chars after heading)")

    ex_idx = content.find("## 💡 Example Usage")
    if ex_idx != -1:
        after_ex = content[ex_idx + len("## 💡 Example Usage"):].strip()
        if len(after_ex) < 20:
            warnings.append("Example Usage section looks very short — add a real example")

    return {"errors": errors, "warnings": warnings}

def lint_legacy_file(content: str, lines: list[str]) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    first_non_empty = None
    for line in lines:
        if line.strip():
            first_non_empty = line.strip()
            break

    if not first_non_empty or not re.match(r"^#\s+HS-\d{3,}\b", first_non_empty):
        errors.append("Missing legacy header (expected '# HS-NNN — ...')")

    if "**Category:**" not in content:
        warnings.append("Missing legacy field: **Category:**")

    if "**Version:**" not in content:
        warnings.append("Missing legacy field: **Version:**")

    prompt_ok = ("## 🤖 THE PROMPT" in content) or ("## 🔮 Prompt Block" in content)
    if not prompt_ok:
        m = re.search(r"(?im)^##\s+.*prompt.*$", content)
        if m and "```" in content[m.end():]:
            prompt_ok = True

    if not prompt_ok:
        if "```" not in content:
            warnings.append("Legacy file has no code block; consider adding a prompt/code example")

    return {"errors": errors, "warnings": warnings}

def lint_file(filepath: Path) -> dict:
    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()

    if has_yaml_frontmatter(lines):
        result = lint_yaml_file(content, lines)
    else:
        result = lint_legacy_file(content, lines)

    # ── File naming convention ────────────────────────────────────────────
    if not re.match(r"^[A-Z0-9_]+v\d+\.md$", filepath.name):
        result["warnings"].append(f"File name '{filepath.name}' doesn't match pattern NAME_v1.md")

    return result


# ── Main run ─────────────────────────────────────────────────────────────────
def run_linter(root: Path = Path(".")) -> int:
    print(f"\n{BOLD}{CYAN}🔍 HYPER-SILLs Vault Linter — scanning skill directories...{RESET}\n")

    total_files    = 0
    total_errors   = 0
    total_warnings = 0
    failed_files   = []

    for skill_dir in SKILL_DIRS:
        dirpath = root / skill_dir
        if not dirpath.exists():
            warn(f"Directory not found, skipping: {skill_dir}/")
            continue

        md_files = [f for f in dirpath.glob("**/*.md") if f.name not in EXCLUDED_FILES]
        if not md_files:
            warn(f"No skill files found in {skill_dir}/")
            continue

        print(f"{BOLD}📁 {skill_dir}/{RESET}")
        for filepath in sorted(md_files):
            total_files += 1
            rel = filepath.relative_to(root)
            result = lint_file(filepath)

            e_count = len(result["errors"])
            w_count = len(result["warnings"])
            total_errors   += e_count
            total_warnings += w_count

            if e_count == 0 and w_count == 0:
                ok(str(rel))
            else:
                status = f"{RED}❌" if e_count else f"{YELLOW}⚠️ "
                print(f"  {status} {rel}{RESET}")
                for err   in result["errors"]:   fail(f"ERROR:   {err}")
                for warn_ in result["warnings"]: warn(f"WARN:    {warn_}")
                if e_count:
                    failed_files.append(str(rel))
        print()

    # ── Summary ──────────────────────────────────────────────────────────
    print(f"{BOLD}{'─'*55}{RESET}")
    print(f"{BOLD}📊 Results:{RESET}  {total_files} files scanned  |  {RED}{total_errors} errors{RESET}  |  {YELLOW}{total_warnings} warnings{RESET}\n")

    if failed_files:
        print(f"{RED}{BOLD}💥 Failed files:{RESET}")
        for f in failed_files:
            print(f"   • {f}")
        print()
        print(f"{RED}❌ Linter FAILED — fix errors above before committing.{RESET}\n")
        return 1
    elif total_warnings:
        print(f"{YELLOW}⚠️  Linter passed with warnings — consider fixing them.{RESET}\n")
        return 0
    else:
        print(f"{GREEN}{BOLD}🏆 All skills passed! Vault is clean. BROski approved ♾️{RESET}\n")
        return 0


if __name__ == "__main__":
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    sys.exit(run_linter(repo_root))
