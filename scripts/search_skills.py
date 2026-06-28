#!/usr/bin/env python3
"""
search_skills.py — Semantic-ish skill search over the HYPER-SILLs vault.

Find skills by *describing the problem*, not memorising hero names or IDs.
Ships a zero-dependency local TF-IDF + cosine backend (works offline, no API
key), architected so a real embedding backend can be swapped in later.

    python scripts/search_skills.py "make my agent restart when it crashes"
    python scripts/search_skills.py "publish my skills to everyone" --limit 3

The vector index is built by `embed_skills.py` and cached in
`vector-store/skill_index.json`. If it's missing, this script builds it on the
fly (and warns), so search always works.

Importable: `from search_skills import semantic_search` for the MCP server.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = VAULT_ROOT / "skills-registry.json"
INDEX_PATH = VAULT_ROOT / "vector-store" / "skill_index.json"

_STOP = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with", "is",
    "are", "be", "this", "that", "it", "as", "at", "by", "an", "my", "your",
    "how", "do", "i", "you", "when", "what", "which", "use", "using", "via",
}


def tokenize(text: str) -> list[str]:
    words = re.split(r"[^a-z0-9]+", text.lower())
    return [w for w in words if len(w) > 2 and w not in _STOP]


# ── Document text per skill (what we embed) ────────────────────────────────────

def skill_document(skill: dict) -> str:
    """The searchable text for a skill: hero + description + tags + body excerpt."""
    parts = [
        skill.get("hero_name", ""),
        skill.get("hero_name", ""),  # weight hero name x2
        skill.get("description", ""),
        skill.get("category", ""),
        " ".join(skill.get("tags", [])),
    ]
    fp = VAULT_ROOT / skill.get("file", "")
    if fp.exists():
        body = fp.read_text(encoding="utf-8", errors="replace")
        # Pull the "What It Does" / first prose paragraph + graph_notes.
        gn = re.search(r'graph_notes:\s*["\'](.+?)["\']', body)
        if gn:
            parts.append(gn.group(1))
        parts.append(body[:1200])
    return " ".join(parts)


# ── TF-IDF index ───────────────────────────────────────────────────────────────

def build_index() -> dict:
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    skills = [s for s in reg.get("skills", []) if s.get("status", "").lower() != "archived"]

    tokenized = []
    df: dict[str, int] = {}
    for s in skills:
        toks = tokenize(skill_document(s))
        tf: dict[str, int] = {}
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        tokenized.append(tf)
        for t in tf:
            df[t] = df.get(t, 0) + 1

    n = len(skills)
    idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}

    docs = []
    for s, tf in zip(skills, tokenized):
        vec = {t: (1 + math.log(c)) * idf[t] for t, c in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        docs.append({
            "id": s["id"],
            "hero_name": s.get("hero_name", ""),
            "description": s.get("description", ""),
            "category": s.get("category", ""),
            "vec": vec,
            "norm": norm,
        })

    return {"backend": "local-tfidf", "idf": idf, "docs": docs}


def load_index(rebuild: bool = False) -> dict:
    if not rebuild and INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    idx = build_index()
    return idx


def _query_vec(query: str, idf: dict) -> tuple[dict, float]:
    tf: dict[str, int] = {}
    for t in tokenize(query):
        tf[t] = tf.get(t, 0) + 1
    vec = {t: (1 + math.log(c)) * idf.get(t, 1.0) for t, c in tf.items()}
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
    return vec, norm


def semantic_search(query: str, limit: int = 5, index: dict | None = None) -> list[dict]:
    """Rank skills by cosine similarity to the query. Returns list of dicts."""
    idx = index or load_index()
    qvec, qnorm = _query_vec(query, idx["idf"])
    if not qvec:
        return []
    results = []
    for d in idx["docs"]:
        dot = sum(qvec.get(t, 0.0) * v for t, v in d["vec"].items())
        score = dot / (qnorm * d["norm"]) if dot else 0.0
        if score > 0:
            results.append((score, d))
    results.sort(key=lambda x: x[0], reverse=True)
    return [
        {
            "id": d["id"],
            "hero_name": d["hero_name"],
            "description": d["description"],
            "category": d["category"],
            "score": round(score, 4),
        }
        for score, d in results[:limit]
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description="Semantic search over HYPER-SILLs.")
    ap.add_argument("query", nargs="*", help="What you're trying to do")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--rebuild", action="store_true", help="Rebuild the index first")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    query = " ".join(args.query).strip()
    if not query:
        print('Describe what you need, e.g.: search_skills.py "auto-restart a crashed agent"')
        return 1

    if not INDEX_PATH.exists() and not args.rebuild:
        print("(no cached index — building in memory; run embed_skills.py to cache)\n", file=sys.stderr)

    idx = load_index(rebuild=args.rebuild)
    hits = semantic_search(query, limit=args.limit, index=idx)

    if args.json:
        print(json.dumps({"query": query, "results": hits}, ensure_ascii=False, indent=2))
        return 0

    if not hits:
        print(f"No stress — nothing matched '{query}'. Try fewer / different words.")
        return 0
    print(f"\nTop {len(hits)} for: {query}\n")
    for h in hits:
        print(f"  {h['id']}  {h['hero_name']}  (score {h['score']}, {h['category']})")
        print(f"      {h['description']}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
