#!/usr/bin/env python3
"""
HYPER-SILLs Skill Vault Linter v2.0
Checks every skill .md file for required structure + Graph-of-Skills (GoS) metadata.

New in v2.0:
  - Validates GoS fields: depends_on, provides, related, graph_notes
  - Detects broken HS-NNN cross-references in depends_on/related
  - Detects circular dependencies across the vault
  - Warns when skill_id in frontmatter doesn’t match filename HS-NNN
  - Warns on skills with no provides (graph dead-ends)

Usage:
  python scripts/skill_linter.py          # scan from repo root
  python scripts/skill_linter.py ./path   # scan from custom root
"""

import os
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── Config ─────────────────────────────────────────────────────────────────
SKILL_DIRS    = ["agents", "content", "dev", "youtube", "broski"]
EXCLUDED_FILES = {"SKILL_TEMPLATE.md", "README.md"}

REQUIRED_FRONTMATTER = [
    "id:", "hero_name:", "category:", "version:", "last_updated:", "best_for:"
]
REQUIRED_HEADINGS = [
    "## \U0001f3af Purpose",
    "## \U0001f4e5 Inputs",
    "## \U0001f4e4 Output Format",
    "## \U0001f52e Prompt Block",
    "## \U0001f4a1 Example Usage",
    "## \U0001f517 Related Skills",
]

VALID_CATEGORIES   = {"coding", "content", "design", "agents", "youtube", "automation", "ND-friendly", "broski"}
VALID_DIFFICULTIES = {"beginner", "intermediate", "advanced"}

SKILL_ID_PATTERN = re.compile(r"^id:\s+SKILL_\d{3,}")
VERSION_PATTERN  = re.compile(r"^version:\s+v\d+\.\d+")
DATE_PATTERN     = re.compile(r"^last_updated:\s+\d{4}-\d{2}-\d{2}")
HS_ID_PATTERN    = re.compile(r"HS-\d{3,}")

# GoS field patterns
GOS_LIST_ITEM    = re.compile(r"^\s+-\s+(HS-\d{3,})")   # - HS-NNN  (with optional comment)
GOS_PROVIDES_STR = re.compile(r"^\s+-\s+([\w\-]+)")      # - some-feature-name

# ── Colours ─────────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ok(msg):   print(f"  {GREEN}\u2705 {msg}{RESET}")
def fail(msg): print(f"  {RED}\u274c {msg}{RESET}")
def warn(msg): print(f"  {YELLOW}\u26a0\ufe0f  {msg}{RESET}")
def info(msg): print(f"  {CYAN}\u2139\ufe0f  {msg}{RESET}")


# ── YAML frontmatter helpers ─────────────────────────────────────────────────
def has_yaml_frontmatter(lines: list[str]) -> bool:
    first = None
    for i, line in enumerate(lines[:30]):
        if line.strip():
            first = i
            break
    if first is None or lines[first].strip() != "---":
        return False
    for j in range(first + 1, min(len(lines), first + 31)):
        if lines[j].strip() == "---":
            return True
    return False


def extract_frontmatter_lines(lines: list[str]) -> list[str]:
    """Return all lines inside the first --- ... --- block."""
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
    return fm_lines


def parse_gos_list(lines: list[str], field: str) -> list[str]:
    """
    Parse a YAML list field like:
      depends_on:
        - HS-098  # comment
        - HS-099
    Returns list of HS-NNN strings (or free-form strings for `provides`).
    """
    collecting = False
    items: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(f"{field}:"):
            collecting = True
            continue
        if collecting:
            if stripped.startswith("-"):
                # grab just the identifier, strip inline comments
                raw = stripped[1:].split("#")[0].strip()
                if raw:
                    items.append(raw)
            elif stripped and not stripped.startswith("#"):
                # new top-level key—stop collecting
                break
    return items


def extract_skill_id_from_header(lines: list[str]) -> str | None:
    """Get HS-NNN from the first non-empty line (legacy header or frontmatter skill_id)."""
    for line in lines:
        if line.strip():
            m = HS_ID_PATTERN.search(line)
            return m.group(0) if m else None
    return None


# ── GoS Validation ───────────────────────────────────────────────────────────
def lint_gos_fields(
    fm_lines: list[str],
    content: str,
    known_ids: set[str],
    skill_id: str | None,
) -> dict:
    """
    Validate Graph-of-Skills fields in frontmatter.
    Returns {errors, warnings, provides, depends_on}.
    """
    errors: list[str]   = []
    warnings: list[str] = []
    fm_text = "\n".join(fm_lines)

    # skill_id field check
    sid_lines = [l for l in fm_lines if l.strip().startswith("skill_id:")]
    if sid_lines:
        declared = sid_lines[0].split(":", 1)[1].strip()
        if skill_id and declared != skill_id:
            warnings.append(
                f"skill_id '{declared}' in frontmatter doesn’t match "
                f"header HS-ID '{skill_id}'"
            )
    else:
        warnings.append("GoS: missing 'skill_id:' in frontmatter")

    # depends_on
    depends_on = parse_gos_list(fm_lines, "depends_on")
    if not depends_on:
        warnings.append("GoS: 'depends_on:' is empty or missing — add at least one dependency (or 'none' if truly standalone)")
    else:
        for dep in depends_on:
            dep_id = HS_ID_PATTERN.search(dep)
            if dep_id and known_ids and dep_id.group(0) not in known_ids:
                errors.append(f"GoS: broken dependency — {dep_id.group(0)} not found in vault")

    # provides
    provides = parse_gos_list(fm_lines, "provides")
    if not provides:
        warnings.append("GoS: 'provides:' is empty or missing — skill is a graph dead-end (nothing consumes it)")

    # related
    related = parse_gos_list(fm_lines, "related")
    for rel in related:
        rel_id = HS_ID_PATTERN.search(rel)
        if rel_id and known_ids and rel_id.group(0) not in known_ids:
            warnings.append(f"GoS: 'related' references unknown skill {rel_id.group(0)}")

    # graph_notes
    if "graph_notes:" not in fm_text:
        warnings.append("GoS: 'graph_notes:' missing — add a one-line description of this skill’s role in the graph")

    return {
        "errors": errors,
        "warnings": warnings,
        "provides": provides,
        "depends_on": [HS_ID_PATTERN.search(d).group(0) for d in depends_on if HS_ID_PATTERN.search(d)],
    }


# ── Circular dependency detection ────────────────────────────────────────────
def detect_cycles(dep_graph: dict[str, list[str]]) -> list[list[str]]:
    """Return list of cycles found in the dependency graph."""
    visited = set()
    in_stack = set()
    cycles: list[list[str]] = []

    def dfs(node: str, path: list[str]):
        visited.add(node)
        in_stack.add(node)
        for neighbour in dep_graph.get(node, []):
            if neighbour not in visited:
                dfs(neighbour, path + [neighbour])
            elif neighbour in in_stack:
                cycle_start = path.index(neighbour) if neighbour in path else 0
                cycles.append(path[cycle_start:] + [neighbour])
        in_stack.discard(node)

    for node in list(dep_graph.keys()):
        if node not in visited:
            dfs(node, [node])

    return cycles


# ── Per-file linters ─────────────────────────────────────────────────────────
def lint_yaml_file(content: str, lines: list[str], known_ids: set[str], skill_id: str | None) -> dict:
    errors: list[str]   = []
    warnings: list[str] = []
    fm_lines = extract_frontmatter_lines(lines)

    if not fm_lines:
        errors.append("No YAML frontmatter block found (expected --- ... ---)")
        return {"errors": errors, "warnings": warnings, "provides": [], "depends_on": []}

    fm_text = "\n".join(fm_lines)

    for field in REQUIRED_FRONTMATTER:
        if field not in fm_text:
            errors.append(f"Missing frontmatter field: {field}")

    id_match = [l for l in fm_lines if l.startswith("id:")]
    if id_match and not SKILL_ID_PATTERN.match(id_match[0]):
        errors.append(f"Bad ID format (expected SKILL_NNN): '{id_match[0].strip()}'")

    ver_match = [l for l in fm_lines if l.startswith("version:")]
    if ver_match and not VERSION_PATTERN.match(ver_match[0]):
        warnings.append(f"Version should be vX.Y format: '{ver_match[0].strip()}'")

    date_match = [l for l in fm_lines if l.startswith("last_updated:")]
    if date_match and not DATE_PATTERN.match(date_match[0]):
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
            warnings.append(f"Unknown difficulty '{diff}'")

    for heading in REQUIRED_HEADINGS:
        if heading not in content:
            errors.append(f"Missing required section: {heading}")

    prompt_idx = content.find("## \U0001f52e Prompt Block")
    if prompt_idx != -1:
        after_prompt = content[prompt_idx + len("## \U0001f52e Prompt Block"):].strip()
        if len(after_prompt) < 30:
            errors.append("Prompt Block section looks empty")

    ex_idx = content.find("## \U0001f4a1 Example Usage")
    if ex_idx != -1:
        after_ex = content[ex_idx + len("## \U0001f4a1 Example Usage"):].strip()
        if len(after_ex) < 20:
            warnings.append("Example Usage section looks very short")

    gos = lint_gos_fields(fm_lines, content, known_ids, skill_id)
    errors   += gos["errors"]
    warnings += gos["warnings"]

    return {
        "errors": errors,
        "warnings": warnings,
        "provides": gos["provides"],
        "depends_on": gos["depends_on"],
    }


def lint_legacy_file(content: str, lines: list[str], known_ids: set[str], skill_id: str | None) -> dict:
    errors: list[str]   = []
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

    prompt_ok = "## \U0001f916 THE PROMPT" in content or "## \U0001f52e Prompt Block" in content
    if not prompt_ok:
        m = re.search(r"(?im)^##\s+.*prompt.*$", content)
        if m and "```" in content[m.end():]:
            prompt_ok = True
    if not prompt_ok and "```" not in content:
        warnings.append("Legacy file has no code block; consider adding a prompt/code example")

    # GoS check — legacy files with GoS block get full validation
    fm_lines = extract_frontmatter_lines(lines)
    gos_present = any(
        l.strip().startswith(k)
        for l in fm_lines
        for k in ("depends_on:", "provides:", "skill_id:")
    )
    if gos_present:
        gos = lint_gos_fields(fm_lines, content, known_ids, skill_id)
        errors   += gos["errors"]
        warnings += gos["warnings"]
        provides   = gos["provides"]
        depends_on = gos["depends_on"]
    else:
        warnings.append(
            "GoS: no graph metadata found — add skill_id, depends_on, provides, related, graph_notes"
        )
        provides   = []
        depends_on = []

    return {
        "errors": errors,
        "warnings": warnings,
        "provides": provides,
        "depends_on": depends_on,
    }


def lint_file(filepath: Path, known_ids: set[str]) -> dict:
    content   = filepath.read_text(encoding="utf-8")
    lines     = content.splitlines()
    skill_id  = extract_skill_id_from_header(lines)

    if has_yaml_frontmatter(lines):
        result = lint_yaml_file(content, lines, known_ids, skill_id)
    else:
        result = lint_legacy_file(content, lines, known_ids, skill_id)

    if not re.match(r"^[A-Z0-9_]+v\d+\.md$", filepath.name):
        result["warnings"].append(
            f"File name '{filepath.name}' doesn’t match pattern NAME_v1.md"
        )

    result["skill_id"] = skill_id
    return result


# ── Vault-wide ID discovery ───────────────────────────────────────────────────
def collect_vault_ids(root: Path) -> set[str]:
    """Walk all skill dirs and collect every HS-NNN found in first non-empty line."""
    ids: set[str] = set()
    for skill_dir in SKILL_DIRS:
        dirpath = root / skill_dir
        if not dirpath.exists():
            continue
        for filepath in dirpath.glob("**/*.md"):
            if filepath.name in EXCLUDED_FILES:
                continue
            try:
                lines = filepath.read_text(encoding="utf-8").splitlines()
                sid = extract_skill_id_from_header(lines)
                if sid:
                    ids.add(sid)
            except Exception:
                pass
    return ids


# ── Main run ─────────────────────────────────────────────────────────────────
def run_linter(root: Path = Path(".")) -> int:
    print(f"\n{BOLD}{CYAN}\U0001f50d HYPER-SILLs Vault Linter v2.0 — scanning skill directories...{RESET}\n")
    print(f"{CYAN}  \U0001f9e0 Graph-of-Skills validation: ON{RESET}\n")

    # Pass 1: collect all known HS-IDs so cross-refs can be validated
    known_ids = collect_vault_ids(root)
    print(f"  {CYAN}\U0001f4cb Found {len(known_ids)} skill IDs in vault{RESET}\n")

    total_files    = 0
    total_errors   = 0
    total_warnings = 0
    failed_files   = []
    dep_graph: dict[str, list[str]] = defaultdict(list)

    for skill_dir in SKILL_DIRS:
        dirpath = root / skill_dir
        if not dirpath.exists():
            warn(f"Directory not found, skipping: {skill_dir}/")
            continue

        md_files = [
            f for f in dirpath.glob("**/*.md")
            if f.name not in EXCLUDED_FILES
        ]
        if not md_files:
            warn(f"No skill files found in {skill_dir}/")
            continue

        print(f"{BOLD}\U0001f4c1 {skill_dir}/{RESET}")
        for filepath in sorted(md_files):
            total_files += 1
            rel    = filepath.relative_to(root)
            result = lint_file(filepath, known_ids)

            e_count = len(result["errors"])
            w_count = len(result["warnings"])
            total_errors   += e_count
            total_warnings += w_count

            # Build dependency graph for cycle detection
            sid = result.get("skill_id")
            if sid:
                for dep in result.get("depends_on", []):
                    dep_graph[sid].append(dep)

            if e_count == 0 and w_count == 0:
                ok(str(rel))
            else:
                status = f"{RED}\u274c" if e_count else f"{YELLOW}\u26a0\ufe0f "
                print(f"  {status} {rel}{RESET}")
                for err_   in result["errors"]:   fail(f"ERROR:   {err_}")
                for warn_  in result["warnings"]: warn(f"WARN:    {warn_}")
                if e_count:
                    failed_files.append(str(rel))
        print()

    # ── Vault-wide cycle detection ────────────────────────────────────────
    cycles = detect_cycles(dep_graph)
    if cycles:
        print(f"{RED}{BOLD}\U0001f504 Circular dependencies detected!{RESET}")
        for cycle in cycles:
            print(f"  {RED}\u274c Cycle: {' \u2192 '.join(cycle)}{RESET}")
            total_errors += 1
            failed_files.append(f"CYCLE: {' -> '.join(cycle)}")
        print()
    else:
        print(f"  {GREEN}\u2705 No circular dependencies found{RESET}\n")

    # ── Summary ──────────────────────────────────────────────────────────
    print(f"{BOLD}{'\u2500'*60}{RESET}")
    print(
        f"{BOLD}\U0001f4ca Results:{RESET}  "
        f"{total_files} files  |  "
        f"{RED}{total_errors} errors{RESET}  |  "
        f"{YELLOW}{total_warnings} warnings{RESET}\n"
    )

    if failed_files:
        print(f"{RED}{BOLD}\U0001f4a5 Failed:{RESET}")
        for f in failed_files:
            print(f"   \u2022 {f}")
        print()
        print(f"{RED}\u274c Linter FAILED — fix errors before committing.{RESET}\n")
        return 1
    elif total_warnings:
        print(f"{YELLOW}\u26a0\ufe0f  Linter passed with warnings — consider fixing them.{RESET}\n")
        return 0
    else:
        print(f"{GREEN}{BOLD}\U0001f3c6 All skills passed! Vault is clean. BROski approved \u221e\ufe0f{RESET}\n")
        return 0


if __name__ == "__main__":
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    sys.exit(run_linter(repo_root))
