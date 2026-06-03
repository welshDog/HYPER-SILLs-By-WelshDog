#!/usr/bin/env python3
"""
skills_query.py
BROski HYPER-SILLs Skills Registry Query Tool
Agent-callable: search, filter, recommend skills from skills-registry.json
Usage: python skills_query.py --query "docker" --level beginner
"""

import json
import argparse
import sys
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent / "skills-registry.json"


def load_registry():
    if not REGISTRY_PATH.exists():
        print(json.dumps({"error": f"Registry not found at {REGISTRY_PATH}"}))
        sys.exit(1)
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def search_skills(registry, query: str = "", level: str = "", category: str = "", tag: str = "", limit: int = 10):
    """Search skills registry with optional filters."""
    # Handle both list and dict registry formats
    if isinstance(registry, dict):
        skills = []
        for key, val in registry.items():
            if isinstance(val, list):
                skills.extend(val)
            elif isinstance(val, dict):
                val["_category"] = key
                skills.append(val)
    else:
        skills = registry

    results = []
    query_lower = query.lower()

    for skill in skills:
        if not isinstance(skill, dict):
            continue

        skill_str = json.dumps(skill).lower()

        # Apply filters
        if query_lower and query_lower not in skill_str:
            continue
        if level and level.lower() not in skill_str:
            continue
        if category and category.lower() not in skill_str:
            continue
        if tag and tag.lower() not in skill_str:
            continue

        results.append(skill)

        if len(results) >= limit:
            break

    return results


def recommend_for_task(registry, task: str, limit: int = 5):
    """Recommend skills relevant to a given task description."""
    keywords = task.lower().split()
    if isinstance(registry, dict):
        skills = []
        for key, val in registry.items():
            if isinstance(val, list):
                skills.extend(val)
    else:
        skills = registry

    scored = []
    for skill in skills:
        if not isinstance(skill, dict):
            continue
        skill_str = json.dumps(skill).lower()
        score = sum(1 for kw in keywords if kw in skill_str)
        if score > 0:
            scored.append((score, skill))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [s for _, s in scored[:limit]]


def list_categories(registry):
    """List all top-level categories in the registry."""
    if isinstance(registry, dict):
        return list(registry.keys())
    return ["(flat list — no categories)"]


def get_stats(registry):
    """Return registry stats."""
    if isinstance(registry, dict):
        categories = list(registry.keys())
        total = sum(
            len(v) if isinstance(v, list) else 1
            for v in registry.values()
        )
    else:
        categories = []
        total = len(registry)

    return {
        "total_skills": total,
        "categories": len(categories),
        "category_list": categories,
        "registry_file": str(REGISTRY_PATH),
        "file_size_kb": round(REGISTRY_PATH.stat().st_size / 1024, 1)
    }


def main():
    parser = argparse.ArgumentParser(description="BROski HYPER-SILLs Skills Query Tool")
    parser.add_argument("--query",    "-q", default="",  help="Search query")
    parser.add_argument("--level",    "-l", default="",  help="Filter by level (beginner/intermediate/advanced)")
    parser.add_argument("--category", "-c", default="",  help="Filter by category")
    parser.add_argument("--tag",      "-t", default="",  help="Filter by tag")
    parser.add_argument("--task",           default="",  help="Recommend skills for a task description")
    parser.add_argument("--categories",     action="store_true", help="List all categories")
    parser.add_argument("--stats",          action="store_true", help="Show registry stats")
    parser.add_argument("--limit",    "-n", default=10,  type=int, help="Max results (default 10)")
    parser.add_argument("--pretty",         action="store_true", help="Pretty print output")

    args = parser.parse_args()
    registry = load_registry()
    indent = 2 if args.pretty else None

    if args.stats:
        print(json.dumps(get_stats(registry), indent=indent))
    elif args.categories:
        print(json.dumps(list_categories(registry), indent=indent))
    elif args.task:
        results = recommend_for_task(registry, args.task, args.limit)
        print(json.dumps({"recommended": results, "count": len(results)}, indent=indent))
    else:
        results = search_skills(
            registry,
            query=args.query,
            level=args.level,
            category=args.category,
            tag=args.tag,
            limit=args.limit
        )
        print(json.dumps({"results": results, "count": len(results)}, indent=indent))


if __name__ == "__main__":
    main()
