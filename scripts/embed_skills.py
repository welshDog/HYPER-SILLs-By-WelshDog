#!/usr/bin/env python3
"""
embed_skills.py — Build the HYPER-SILLs vector index for semantic search.

Builds a TF-IDF + cosine index over every (non-archived) skill and caches it to
`vector-store/skill_index.json`. Run once after adding/editing skills; the cache
makes `search_skills.py` and the MCP `semantic_search` tool instant.

    python scripts/embed_skills.py            # build / refresh the cache
    python scripts/embed_skills.py --stats    # build + print index stats

Zero external dependencies (pure stdlib). The backend is pluggable — see
search_skills.build_index() — so a real embedding model (e.g. text-embedding-3
or a local sentence-transformer) can be dropped in without touching callers.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from search_skills import INDEX_PATH, build_index  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the HYPER-SILLs vector index.")
    ap.add_argument("--stats", action="store_true", help="Print index stats after building")
    args = ap.parse_args()

    print("Building skill index (local TF-IDF backend)...")
    idx = build_index()

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")

    n_docs = len(idx["docs"])
    n_terms = len(idx["idf"])
    size_kb = INDEX_PATH.stat().st_size / 1024
    print(f"  indexed {n_docs} skills, {n_terms} terms")
    print(f"  cached -> {INDEX_PATH.relative_to(INDEX_PATH.parent.parent)}  ({size_kb:.0f} KB)")

    if args.stats:
        top = sorted(idx["idf"].items(), key=lambda x: x[1])[:10]
        print(f"  most common terms (low idf): {[t for t, _ in top]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
