#!/usr/bin/env python3
"""
HYPER-SILLs Agent Loadout Validator

Validates agent-loadouts.json against skills-registry.json so per-agent skill
loadouts can never drift from the vault. Runs standalone OR as part of the
pre-push lint gate (skill_linter.py imports validate_loadouts()).

Invariants enforced:
  1. agent-loadouts.json is valid JSON with the expected shape.
  2. Every referenced skill id exists in skills-registry.json.
  3. No referenced id is deprecated/archived in the registry.
  4. Per agent: effective_required (_defaults + own) does NOT intersect
     effective_forbidden. A skill can't be both mandatory and banned.
  5. (warn) No duplicate ids inside a single list.

Graceful: if agent-loadouts.json is absent, this is a no-op (exit 0) so the
gate keeps working before the file exists.

Usage:
  python scripts/validate_loadouts.py          # from repo root
  python scripts/validate_loadouts.py ./path   # custom root
"""

import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

GREEN, RED, YELLOW, CYAN, BOLD, RESET = (
    "\033[92m", "\033[91m", "\033[93m", "\033[96m", "\033[1m", "\033[0m"
)

REGISTRY_FILE = "skills-registry.json"
LOADOUTS_FILE = "agent-loadouts.json"
LIST_KEYS = ("required", "optional", "forbidden")
# Statuses a loadout must never reference (a live agent shouldn't depend on a
# retired skill). Matches skill_linter.py's VALID_STATUSES lifecycle tail.
DEAD_STATUSES = {"deprecated", "archived"}


def _effective(defaults: dict, entry: dict, key: str) -> set[str]:
    """Union of _defaults[key] and the agent entry[key]."""
    return set(defaults.get(key, [])) | set(entry.get(key, []))


def validate_loadouts(root: Path = Path(".")) -> int:
    """Return 0 if loadouts are valid (or absent), 1 on any error."""
    loadouts_path = root / LOADOUTS_FILE
    registry_path = root / REGISTRY_FILE

    print(f"\n{BOLD}{CYAN}🎒 Agent Loadout Validator — checking {LOADOUTS_FILE}...{RESET}")

    if not loadouts_path.exists():
        print(f"  {CYAN}ℹ️  {LOADOUTS_FILE} not present — skipping (no-op).{RESET}\n")
        return 0

    # ── Load registry (source of truth for valid ids + statuses) ──────────
    if not registry_path.exists():
        print(f"  {YELLOW}⚠️  {REGISTRY_FILE} not found — cannot validate ids, skipping.{RESET}\n")
        return 0
    reg = {s["id"]: s for s in json.loads(registry_path.read_text(encoding="utf-8"))["skills"]}

    # ── Load loadouts (malformed JSON is a hard fail) ─────────────────────
    try:
        lo = json.loads(loadouts_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  {RED}❌ {LOADOUTS_FILE} is not valid JSON: {e}{RESET}\n")
        return 1

    defaults = lo.get("_defaults", {})
    agents = lo.get("agents", {})
    if not isinstance(agents, dict):
        print(f"  {RED}❌ 'agents' must be an object.{RESET}\n")
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    def check_scope(name: str, entry: dict) -> None:
        for key in LIST_KEYS:
            ids = entry.get(key, [])
            if not isinstance(ids, list):
                errors.append(f"{name}.{key} must be a list")
                continue
            if len(ids) != len(set(ids)):
                dupes = sorted({i for i in ids if ids.count(i) > 1})
                warnings.append(f"{name}.{key} has duplicate ids: {dupes}")
            for sid in ids:
                if sid not in reg:
                    errors.append(f"{name}.{key}: '{sid}' not found in {REGISTRY_FILE}")
                elif reg[sid].get("status", "").lower() in DEAD_STATUSES:
                    errors.append(
                        f"{name}.{key}: '{sid}' is "
                        f"{reg[sid]['status']} — cannot be in a loadout"
                    )

    # _defaults scope
    check_scope("_defaults", defaults)

    # each agent
    for agent, entry in agents.items():
        if not isinstance(entry, dict):
            errors.append(f"agents.{agent} must be an object")
            continue
        check_scope(f"agents.{agent}", entry)
        req = _effective(defaults, entry, "required")
        forb = _effective(defaults, entry, "forbidden")
        clash = req & forb
        if clash:
            errors.append(
                f"agents.{agent}: {sorted(clash)} is both required and forbidden"
            )

    # ── Report ────────────────────────────────────────────────────────────
    n_skills = len({
        sid
        for scope in [defaults, *agents.values()] if isinstance(scope, dict)
        for key in LIST_KEYS
        for sid in scope.get(key, [])
    })
    print(f"  {CYAN}📋 {len(agents)} agents · {n_skills} distinct skills referenced{RESET}")

    for w in warnings:
        print(f"  {YELLOW}⚠️  {w}{RESET}")
    for e in errors:
        print(f"  {RED}❌ {e}{RESET}")

    if errors:
        print(f"\n{RED}❌ Loadout validation FAILED ({len(errors)} error(s)).{RESET}\n")
        return 1
    print(f"\n{GREEN}{BOLD}🏆 Loadouts valid — every id exists, no required/forbidden clashes.{RESET}\n")
    return 0


if __name__ == "__main__":
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    sys.exit(validate_loadouts(repo_root))
