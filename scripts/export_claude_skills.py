#!/usr/bin/env python3
"""
export_claude_skills.py — HYPER-SILLs format bridge.

Converts HYPER-SILLs skill files into the portable Agent Skills format
(agentskills.io / Claude Code `SKILL.md`), so every HYPER-SILL runs in
Claude Code, Cursor, Codex CLI, Gemini CLI, Copilot, and 30+ other agents.

The HYPER-SILLs format stays the source of truth (rich GoS metadata, hero
names, graph edges). This emits a derived, runtime-friendly copy.

Usage:
    python scripts/export_claude_skills.py                       # all skills -> dist/agent-skills/
    python scripts/export_claude_skills.py --pack "Agent Builder Pack"
    python scripts/export_claude_skills.py --category agents
    python scripts/export_claude_skills.py --format claude       # claude | agentskills (default)
    python scripts/export_claude_skills.py --out ~/.claude/skills/hyper-vault
    python scripts/export_claude_skills.py --check               # dry-run, just report

Stdlib only — no dependency on the `mcp` package.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = VAULT_ROOT / "skills-registry.json"
DEFAULT_OUT = VAULT_ROOT / "dist" / "agent-skills"

# Statuses we never export (DEPRECATED still exports with a warning banner).
SKIP_STATUSES = {"archived"}


def kebab(text: str) -> str:
    """HERO NAME -> hero-name (safe for directory + skill `name`)."""
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return text or "skill"


def split_frontmatter(content: str) -> tuple[dict, str]:
    """Return (gos_fields, body_without_frontmatter).

    HYPER-SILLs files are: `# H1 title` line, then a `--- ... ---` GoS block,
    then the body. We pull a few scalar fields and strip the block so the
    exported body is clean markdown.
    """
    lines = content.splitlines()
    start = next((i for i, l in enumerate(lines) if l.strip() == "---"), None)
    if start is None:
        return {}, content
    end = next((i for i in range(start + 1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, content

    block = "\n".join(lines[start + 1 : end])

    def scalar(key: str) -> str:
        m = re.search(rf'^{key}:\s*["\']?(.+?)["\']?\s*$', block, re.MULTILINE)
        return m.group(1).strip() if m else ""

    fields = {
        "skill_id": scalar("skill_id"),
        "hero_name": scalar("hero_name"),
        "version": scalar("version"),
        "category": scalar("category"),
        "status": scalar("status"),
        "graph_notes": scalar("graph_notes"),
    }
    # Body = title line(s) before the block + everything after the block.
    head = "\n".join(lines[:start]).rstrip()
    tail = "\n".join(lines[end + 1 :]).lstrip()
    body = (head + "\n\n" + tail).strip() if head else tail
    return fields, body


def build_description(skill: dict, gos: dict) -> str:
    """Trigger-aware description in the Agent Skills convention.

    Pattern: "Use when <purpose>. Triggers on: <tags>." — this is what host
    apps match against to auto-load the skill.
    """
    desc = (skill.get("description") or gos.get("graph_notes") or "").strip().rstrip(".")
    tags = [t for t in skill.get("tags", []) if t]
    hero = skill.get("hero_name", "")
    base = f"Use when you need {desc}" if desc else f"The {hero} skill"
    if tags:
        base += f". Triggers on: {', '.join(tags)}"
    return base.strip() + "."


def render_skill_md(skill: dict, gos: dict, body: str, fmt: str) -> str:
    name = kebab(skill.get("hero_name") or skill.get("id", "skill"))
    description = build_description(skill, gos)

    fm = ["---", f"name: {name}", f"description: >-", f"  {description}"]
    if fmt == "claude":
        # Claude Code reads `name` + `description`; extra metadata is ignored but
        # harmless and useful for provenance.
        fm += [
            "metadata:",
            f"  hyper_sill_id: {skill.get('id', '')}",
            f"  hero_name: \"{skill.get('hero_name', '')}\"",
            f"  category: {skill.get('category', '')}",
            f"  version: {skill.get('version', gos.get('version', ''))}",
            f"  source: HYPER-SILLs-By-WelshDog",
        ]
    fm.append("---")

    banner = ""
    if (gos.get("status") or skill.get("status", "")).lower() == "deprecated":
        banner = "> ⚠️ **Deprecated skill** — kept for reference; check the vault for a replacement.\n\n"

    return "\n".join(fm) + "\n\n" + banner + body + "\n"


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Export HYPER-SILLs to Agent Skills format.")
    ap.add_argument("--pack", default="", help="Only skills in this pack")
    ap.add_argument("--category", default="", help="Only this category (agents/dev/broski/youtube)")
    ap.add_argument("--format", choices=["agentskills", "claude"], default="agentskills")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="Output directory")
    ap.add_argument("--check", action="store_true", help="Dry run — report only, write nothing")
    args = ap.parse_args()

    reg = load_registry()
    skills = reg.get("skills", [])
    out_root = Path(args.out).expanduser()

    written, skipped, missing = 0, 0, 0
    for s in skills:
        if args.pack and s.get("pack", "") != args.pack:
            continue
        if args.category and s.get("category", "").lower().rstrip("/") != args.category.lower():
            continue
        if s.get("status", "").lower() in SKIP_STATUSES:
            skipped += 1
            continue

        fp = VAULT_ROOT / s["file"]
        if not fp.exists():
            print(f"  ! missing file: {s['file']}", file=sys.stderr)
            missing += 1
            continue

        content = fp.read_text(encoding="utf-8", errors="replace")
        gos, body = split_frontmatter(content)
        rendered = render_skill_md(s, gos, body, args.format)

        name = kebab(s.get("hero_name") or s.get("id", "skill"))
        dest = out_root / name / "SKILL.md"
        if args.check:
            print(f"  would write {dest.relative_to(out_root.parent) if out_root.parent in dest.parents else dest}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(rendered, encoding="utf-8")
        written += 1

    verb = "would export" if args.check else "exported"
    print(f"\n{verb} {written} skills -> {out_root}  (skipped {skipped} archived, {missing} missing)")
    if not args.check and written:
        print(f"format: {args.format}.  Point your agent at: {out_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
