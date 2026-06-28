#!/usr/bin/env python3
"""
embed_skills.py — Build the HYPER-SILLs vector index for semantic search.

Builds a TF-IDF + cosine index over every (non-archived) skill and caches it to
`vector-store/skill_index.json`. Run once after adding/editing skills; the cache
makes `search_skills.py` and the MCP `semantic_search` tool instant.

Embedding backend auto-resolves (best-first): local sentence-transformers
(all-MiniLM-L6-v2, offline, free) → OpenAI (if OPENAI_API_KEY) → TF-IDF fallback.

    python scripts/embed_skills.py                  # auto (prefers local model)
    python scripts/embed_skills.py --backend tfidf   # force stdlib fallback
    python scripts/embed_skills.py --stats           # + print index stats
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
    ap.add_argument("--backend", default="auto", choices=["auto", "local", "openai", "tfidf"])
    ap.add_argument("--stats", action="store_true", help="Print index stats after building")
    args = ap.parse_args()

    print(f"Building skill index (backend: {args.backend})...")
    idx = build_index(args.backend)

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")

    n_docs = len(idx["docs"])
    size_kb = INDEX_PATH.stat().st_size / 1024
    backend = idx.get("backend", "?")
    detail = f"{len(idx['idf'])} terms" if backend == "tfidf" else f"dim {idx.get('dim', '?')}"
    print(f"  backend: {backend}   indexed {n_docs} skills, {detail}")
    print(f"  cached -> {INDEX_PATH.relative_to(INDEX_PATH.parent.parent)}  ({size_kb:.0f} KB)")

    if args.stats and backend == "tfidf":
        top = sorted(idx["idf"].items(), key=lambda x: x[1])[:10]
        print(f"  most common terms (low idf): {[t for t, _ in top]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
