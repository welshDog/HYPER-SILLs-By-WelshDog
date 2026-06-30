#!/usr/bin/env python3
"""
seed_problem_keywords.py — Inject curated `problem_keywords` into skill frontmatter.

The registry `keywords` field is auto-extracted body word-frequency (noisy:
stopwords + field names leak in). `problem_keywords` is the *curated* layer:
the natural language a user actually types when they have the problem a skill
solves. It lives in each skill's YAML frontmatter (the source of truth) so
`generate_registry.py` carries it through, and `search_skills.skill_document`
weights it x3 — directly closing the "wellness drift" (e.g. a query for
"crashing agents" should surface the watchdog/circuit-breaker skills, not the
poetically-named sleep/recovery ones).

Curated by hand for the highest-traffic technical skills + every hypercode/web3
skill (those carry NO `provides` slugs, so they had almost no clean signal).
Skills not listed here already get strong signal from their description +
`provides`, so they're intentionally left alone.

Keyed by REGISTRY id (HS-xxx / DS-xxx). NOTE the dual-namespace gotcha: a file's
frontmatter `skill_id` differs from its registry `id` (e.g. registry HS-103 ==
file skill_id HS-005). We resolve registry id -> file via the registry, then
write into that file. Idempotent: re-running replaces the block.

    python scripts/seed_problem_keywords.py            # apply
    python scripts/seed_problem_keywords.py --dry-run  # preview only
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = VAULT_ROOT / "skills-registry.json"

# Registry-id -> curated problem language (what a user TYPES, not formal slugs).
CURATED: dict[str, list[str]] = {
    # ── Agents: failure / recovery / lifecycle ──────────────────────────────
    "HS-103": ["crash", "crashed", "keeps crashing", "agent down", "service unhealthy",
               "auto recover", "self heal", "restart on failure", "circuit breaker", "keeps dying"],
    "HS-122": ["crash", "crashed", "restart crashed service", "watchdog", "monitor and restart",
               "keeps dying", "auto restart", "won't stay up", "service health loop"],
    "HS-050": ["crash", "monitor after launch", "auto heal", "watchdog", "alert on down",
               "keeps failing", "post launch monitoring"],
    "HS-071": ["crash", "fail gracefully", "fallback", "error recovery", "graceful degradation",
               "what to do when it breaks", "fallback chain"],
    "HS-100": ["agent stuck", "restart agent", "agent states", "boot sequence", "retire agent",
               "lifecycle", "state machine"],
    "HS-131": ["agents spawning forever", "infinite spawn", "runaway subagents", "recursion limit",
               "depth limit", "too many agents", "stop spawning", "bounded delegation"],
    "HS-045": ["spending too much", "llm cost", "throttle", "budget", "expensive", "token spend",
               "cap cost", "cost optimisation"],
    # ── Agents: orchestration / structure ───────────────────────────────────
    "HS-007": ["multiple agents", "agent swarm", "coordinate agents", "swarm core"],
    "HS-008": ["route tasks", "dispatch", "orchestrate", "delegate to agents", "orchestrator"],
    "HS-019": ["logs", "metrics", "tracing", "prometheus", "debug agent", "observability",
               "structured logging"],
    "HS-040": ["track goals", "kpi", "self improving", "autonomous improvement"],
    "HS-041": ["prometheus", "grafana", "metrics wiring", "scrape metrics"],
    "HS-072": ["shared memory", "redis", "context store", "agents share state", "memory between agents"],
    "HS-073": ["streaming", "server sent events", "sse", "realtime updates", "live agent events"],
    "HS-077": ["approval", "confirm before", "human in the loop", "ask before acting", "consent gate"],
    "HS-085": ["guardrails", "safety", "hard stops", "prevent dangerous actions", "agent guardrails"],
    "HS-098": ["agent rules", "laws of agents", "compliance", "agent policy"],
    "HS-089": ["agent roster", "list of agents", "which agents exist", "agent inventory"],
    "HS-042": ["skill registry", "route to capability", "yellow pages", "find the right agent"],
    # ── Dev: workflow / tooling ─────────────────────────────────────────────
    "HS-076": ["pre commit", "before commit", "ci checks", "block bad commit", "commit gate"],
    "HS-113": ["merge conflict", "git workflow", "branches", "parallel work", "rebase", "git survival"],
    "HS-081": ["mcp server", "register tools", "expose to claude", "tool discovery", "agent registration"],
    "HS-128": ["claude plugin", "plugin marketplace", "distribute skills", "publish plugin"],
    "HS-129": ["mcp resources", "expose skills as mcp", "sep-2640", "skills over mcp"],
    "HS-130": ["oci artifact", "distribute skills", "signed skills", "registry publish"],
    "DS-009": ["boot checks", "validate env", "dependency check", "startup validation", "preflight"],
    "DS-028": ["wait for healthy", "backoff", "retry", "health check wait", "smart retry"],
    "DS-002": ["cli args", "argparse", "command line entrypoint", "launch script"],
    "HS-025": ["token sync", "auth broken", "env token", "fix auth", "token debug"],
    "HS-105": ["agent metrics", "required metrics", "prometheus contract", "mandatory metrics"],
    "HS-114": ["brain runbook", "docker debug", "github sync broken", "brain infrastructure"],
    "HS-074": ["fastapi route", "api standards", "router registration", "endpoint pattern"],
    "HS-108": ["verify claims", "truth audit", "did it actually work", "validate ai output"],
    "HS-109": ["check before building", "duplication", "grep before write", "already exists"],
    # ── Hypercode (no provides slugs — full curation) ───────────────────────
    "HS-030": ["ecosystem rules", "master constitution", "top level rules", "hyperfocus rules"],
    "HS-031": ["v2.4 rules", "sacred rules", "hypercode rules", "20 rules"],
    "HS-032": ["course rules", "course sacred rules"],
    "HS-033": ["shop rules", "broski shop rules", "shop sacred rules"],
    "HS-035": ["ai behaviour", "tool matrix", "which tool to use", "protocol prime"],
    "HS-037": ["ports", "networks", "architecture quick ref", "docker networks", "grid"],
    "HS-039": ["session end", "handover", "wrap up", "end of session", "handoff", "close protocol"],
    "HS-046": ["hyperlaunch", "launch stack", "start services", "unified launcher"],
    "HS-047": ["service tiers", "launch pattern", "servicespec", "tiered launch"],
    "HS-059": ["ecosystem inventory", "what services exist", "full map", "cartographer"],
    "HS-065": ["external integrations", "third party services", "integrations map", "connectors"],
    "HS-066": ["milestone tracker", "track progress", "milestones"],
    # ── Web3 (no provides slugs — full curation) ────────────────────────────
    "HS-052": ["broskipets", "pet integration", "nft pets", "pet master plan"],
    "HS-053": ["pet rarity", "roll formula", "rarity odds", "fate roll"],
    "HS-054": ["dev xp", "xp trigger", "reward dev actions", "xp spark"],
    "HS-055": ["on chain portfolio", "dnft", "wallet", "chain ledger"],
    "HS-056": ["pet species", "power mapping", "beast codex"],
    "HS-057": ["broskipets phase 0", "genesis build prompt", "pet phase zero"],
    "HS-058": ["broskipets phase 1", "hatch prompt", "pet hatch"],
    # ── Dev reference cards ─────────────────────────────────────────────────
    "HS-060": ["containers", "docker stack", "container reference", "fleet"],
    "HS-061": ["ports", "network map", "port warden", "which port"],
    "HS-062": ["database schema", "db tables", "schema reference"],
    "HS-063": ["backend deps", "dependencies", "stack", "quartermaster"],
    "HS-064": ["dev commands", "cheat sheet", "commands", "quick reference"],
}


def inject(fm_text: str, keywords: list[str]) -> str:
    """Return the frontmatter block with a fresh `problem_keywords:` list."""
    block = "problem_keywords:\n" + "\n".join(f"  - {k}" for k in keywords)
    # Replace an existing block (idempotent), else append before the closing ---.
    existing = re.search(r"^problem_keywords:\n(?:  - .*\n?)*", fm_text, flags=re.M)
    if existing:
        return fm_text[:existing.start()] + block + "\n" + fm_text[existing.end():]
    return fm_text.rstrip("\n") + "\n" + block + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    id_to_file = {s["id"]: s.get("file", "") for s in reg["skills"]}

    done, missing = 0, []
    for reg_id, kws in CURATED.items():
        rel = id_to_file.get(reg_id)
        if not rel:
            missing.append(reg_id)
            continue
        fp = VAULT_ROOT / rel
        if not fp.exists():
            missing.append(f"{reg_id} ({rel})")
            continue
        text = fp.read_text(encoding="utf-8")
        m = re.search(r"(\n---\n)(.*?)(\n---\n)", text, flags=re.S)
        if m:
            new_fm = inject(m.group(2), kws)
            new_text = text[:m.start(2)] + new_fm + text[m.end(2):]
        else:
            # Legacy RESCUED skills (web3/) carry no YAML frontmatter. Insert a
            # minimal block right after the H1 title so generate_registry can read
            # problem_keywords. skill_id is recovered from the H1 (e.g. "# HS-052 —").
            h1 = re.match(r"(# (HS-\d+|DS-\d+).*?\n)", text)
            sid = h1.group(2) if h1 else reg_id
            block = ("---\nskill_id: " + sid + "\nproblem_keywords:\n"
                     + "\n".join(f"  - {k}" for k in kws) + "\n---\n")
            insert_at = h1.end() if h1 else 0
            sep = "\n" if not text[insert_at:insert_at + 1] == "\n" else ""
            new_text = text[:insert_at] + sep + block + text[insert_at:]
        if not args.dry_run and new_text != text:
            fp.write_text(new_text, encoding="utf-8")
        done += 1
        print(f"  {reg_id:7} -> {rel}  ({len(kws)} kw)")

    print(f"\n{'[dry-run] would update' if args.dry_run else 'updated'} {done} skills.")
    if missing:
        print(f"!! could not resolve: {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
