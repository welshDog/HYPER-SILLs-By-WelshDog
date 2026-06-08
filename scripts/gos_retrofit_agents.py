#!/usr/bin/env python3
"""
GoS Retrofit — agents/ folder (36 files)
Inserts skill_id / depends_on / provides / related / graph_notes frontmatter
into every agents/ skill that is missing it.

Run from repo root:
    python scripts/gos_retrofit_agents.py [--dry-run]
"""

import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DRY_RUN = "--dry-run" in sys.argv

# ── GoS metadata for all 36 files ─────────────────────────────────────────────
# Format per entry:
#   new_id      : ID to use in the inserted GoS block (and update H1 if different)
#   hero_name   : canonical hero name (matches registry)
#   emoji       : skill emoji
#   depends_on  : list of (HS-NNN, comment) tuples
#   provides    : list of capability slugs
#   related     : list of (HS-NNN, comment) tuples
#   graph_notes : one-sentence graph position description

METADATA = {
    "AB_TESTING_FRAMEWORK_AGENTS_v1.md": {
        "new_id": "HS-120",
        "hero_name": "AB FORGE",
        "emoji": "🧪",
        "depends_on": [
            ("HS-002", "SIX_LAWS_OF_AGENTS — governs test behaviour boundaries"),
            ("HS-043", "LOOP MASTER — A/B test plugs into the 5-loop"),
        ],
        "provides": [
            "ab-test-code",
            "traffic-splitting-implementation",
            "variant-management",
        ],
        "related": [
            ("HS-044", "AB SPLITTER — prompt-block companion to this code pattern"),
            ("HS-093", "NIGHT TENDER — nightly loop runs the A/B evaluation"),
        ],
        "graph_notes": "Python A/B testing code for agent behaviour comparison — code companion to HS-044 AB SPLITTER.",
    },
    "AB_TESTING_FRAMEWORK_v1.md": {
        "new_id": "HS-044",
        "hero_name": "AB SPLITTER",
        "emoji": "🧪",
        "depends_on": [
            ("HS-002", "SIX_LAWS_OF_AGENTS — tests must respect agent laws"),
            ("HS-043", "LOOP MASTER — A/B test is a sub-loop of the 5-loop"),
        ],
        "provides": [
            "ab-test-prompt",
            "behaviour-comparison-workflow",
            "winner-promotion-pattern",
        ],
        "related": [
            ("HS-120", "AB FORGE — Python code companion"),
            ("HS-093", "NIGHT TENDER — nightly evaluation loop"),
        ],
        "graph_notes": "Prompt-block A/B testing pattern for comparing agent behaviours — use with HS-120 for implementation.",
    },
    "AGENT_COMMUNICATION_PATTERNS_v1.md": {
        "new_id": "HS-083",
        "hero_name": "THE THREE VOICES",
        "emoji": "🗣️",
        "depends_on": [
            ("HS-067", "THE THRONE LADDER — roles determine who talks to whom"),
            ("HS-008", "BROSKI ORCHESTRATOR PATTERN — orchestrator drives comms"),
        ],
        "provides": [
            "request-response-pattern",
            "streaming-pattern",
            "error-signalling-pattern",
            "inter-agent-comms",
        ],
        "related": [
            ("HS-073", "PULSE STREAM — SSE schema for streaming events"),
            ("HS-080", "THE TOOL BELT — tools use these patterns"),
        ],
        "graph_notes": "Three canonical inter-agent comms patterns (req-res, streaming, errors) — every agent-to-agent call uses one of these three.",
    },
    "AGENT_DECISION_FRAMEWORK_MATRIX_v1.md": {
        "new_id": "HS-075",
        "hero_name": "THE CHOICE MATRIX",
        "emoji": "🎯",
        "depends_on": [
            ("HS-002", "SIX_LAWS_OF_AGENTS — laws constrain the decision space"),
            ("HS-077", "CONSENT GUARDIAN — ask-vs-decide maps to the approval gate"),
        ],
        "provides": [
            "ask-vs-decide-matrix",
            "delegate-vs-execute-model",
            "speed-cost-quality-triad",
        ],
        "related": [
            ("HS-087", "THE BRANCHING PATH — decision tree uses this matrix"),
            ("HS-078", "FLOW KEEPER — flow-state preservation shapes small decisions"),
        ],
        "graph_notes": "Three decision matrices (ask/decide, delegate/execute, speed/cost/quality) resolving the recurring dilemmas every agent faces.",
    },
    "AGENT_DECISION_TREE_FLOWCHART_v1.md": {
        "new_id": "HS-087",
        "hero_name": "THE BRANCHING PATH",
        "emoji": "🌳",
        "depends_on": [
            ("HS-075", "THE CHOICE MATRIX — matrix feeds the tree nodes"),
            ("HS-067", "THE THRONE LADDER — role check is first tree node"),
            ("HS-077", "CONSENT GUARDIAN — approval gate is second tree node"),
        ],
        "provides": [
            "task-routing-tree",
            "agent-entry-point-flow",
            "decision-flowchart",
        ],
        "related": [
            ("HS-088", "THE MIRROR OATH — tree terminates at the 8-point audit"),
            ("HS-079", "THE CREW CHARTER — delegation node uses role definitions"),
        ],
        "graph_notes": "Single-page decision flowchart every agent runs on every task — from receipt to HS-088 completion audit.",
    },
    "AGENT_FINAL_SELF_AUDIT_v1.md": {
        "new_id": "HS-088",
        "hero_name": "THE MIRROR OATH",
        "emoji": "🪞",
        "depends_on": [
            ("HS-087", "THE BRANCHING PATH — tree leads here as terminal gate"),
            ("HS-004", "FIVE MANDATORY GUARDRAILS — audit checks all 5 guardrails"),
        ],
        "provides": [
            "completion-audit",
            "8-point-checklist",
            "task-sign-off-gate",
        ],
        "related": [
            ("HS-077", "CONSENT GUARDIAN — check 1 in the audit"),
            ("HS-078", "FLOW KEEPER — check 2 in the audit"),
            ("HS-019", "OBSERVABLE AGENT OPERATIONS — checks 4+5 in the audit"),
        ],
        "graph_notes": "Terminal gate before task_completed — 8 binary checks; any failure requires a fix before the completion event is emitted.",
    },
    "AGENT_MANIFEST_FOCUS_TRACKER_v1.md": {
        "new_id": "HS-124",
        "hero_name": "FOCUS HAWK",
        "emoji": "🦅",
        "depends_on": [
            ("HS-016", "BRAIN PRIMER — brain ecosystem context required"),
            ("HS-011", "MIND BLOCKS — module map needed to call the focus endpoint"),
        ],
        "provides": [
            "focus-session-api",
            "adhd-session-tracking",
            "streak-scoring",
            "focus-start-end-tools",
        ],
        "related": [
            ("HS-017", "MIND CORE — brain core runs the focus tracker"),
            ("HS-013", "DAWN HERALD — morning briefing includes focus stats"),
            ("HS-093", "NIGHT TENDER — nightly loop evaluates focus data"),
        ],
        "graph_notes": "ADHD focus session tracker manifest — logs sessions, scores streaks; pairs with Brain Level 16 on port 8100.",
    },
    "AGENT_MANIFEST_HYPER_BRAIN_CORE_v1.md": {
        "new_id": "HS-017",
        "hero_name": "MIND CORE",
        "emoji": "🧠",
        "depends_on": [
            ("HS-016", "BRAIN PRIMER — orientation required before calling the core"),
        ],
        "provides": [
            "brain-query-api",
            "brain-state-update",
            "mcp-compatible-brain-interface",
        ],
        "related": [
            ("HS-018", "BRIDGE KEEPER — MCP bridge routes calls to this core"),
            ("HS-011", "MIND BLOCKS — module map for this core's endpoints"),
            ("HS-009", "THE GRAND CODEX — master context loads before the core"),
        ],
        "graph_notes": "Core brain agent manifest — MCP-compatible; Claude/Cursor can call it directly for knowledge queries and state updates.",
    },
    "AGENT_MANIFEST_MCP_BRIDGE_v1.md": {
        "new_id": "HS-018",
        "hero_name": "BRIDGE KEEPER",
        "emoji": "🌉",
        "depends_on": [
            ("HS-017", "MIND CORE — bridge routes to the brain core"),
            ("HS-016", "BRAIN PRIMER — ecosystem orientation required"),
        ],
        "provides": [
            "mcp-bridge-api",
            "tool-call-routing",
            "brain-cluster-access",
        ],
        "related": [
            ("DS-020", "MCP_SERVER_AGENT_REGISTRATION — registration pattern for this bridge"),
        ],
        "graph_notes": "MCP protocol bridge manifest — entry point for any AI IDE (Claude Code, Cursor) to reach the BROski brain cluster.",
    },
    "AGENT_MANIFEST_MORNING_BRIEFING_v1.md": {
        "new_id": "HS-020",
        "hero_name": "HERALD'S SCROLL",
        "emoji": "🌄",
        "depends_on": [
            ("HS-013", "DAWN HERALD — trigger reference for the briefing AI"),
            ("HS-016", "BRAIN PRIMER — brain ecosystem context required"),
        ],
        "provides": [
            "morning-briefing-api",
            "daily-task-summary",
            "briefing-manifest",
        ],
        "related": [
            ("HS-124", "FOCUS HAWK — focus stats feed into the briefing"),
            ("HS-021", "VAULT SYNC — brain sync often follows the morning briefing"),
        ],
        "graph_notes": "Daily AI briefing manifest — delivers tasks, energy, BROski$ summary each morning via the brain cluster.",
    },
    "AGENT_ROLE_HIERARCHY_PATTERN_v1.md": {
        "new_id": "HS-067",
        "hero_name": "THE THRONE LADDER",
        "emoji": "👑",
        "depends_on": [
            ("HS-001", "ANATOMY_OF_AN_AGENT — anatomy defines role components"),
            ("HS-002", "SIX_LAWS_OF_AGENTS — laws set role boundaries"),
        ],
        "provides": [
            "role-hierarchy",
            "orchestrator-worker-validator-model",
            "delegation-boundaries",
        ],
        "related": [
            ("HS-008", "BROSKI ORCHESTRATOR PATTERN — the Orchestrator role defined here"),
            ("HS-079", "THE CREW CHARTER — per-specialist role definitions"),
        ],
        "graph_notes": "Canonical Orchestrator→Worker→Validator role structure — the skeleton all multi-agent systems build on.",
    },
    "AGENTS_BRAIN_README_v1.md": {
        "new_id": "HS-016",
        "hero_name": "BRAIN PRIMER",
        "emoji": "📖",
        "depends_on": [
            ("HS-009", "THE GRAND CODEX — master context is the root; brain sits inside it"),
        ],
        "provides": [
            "brain-ecosystem-map",
            "agent-boot-sequence",
            "obsidian-architecture-overview",
        ],
        "related": [
            ("HS-017", "MIND CORE — the core agent described in this README"),
            ("HS-018", "BRIDGE KEEPER — the MCP bridge described in this README"),
            ("HS-028", "SDK PRIMER — SDK sits at same layer as the brain"),
        ],
        "graph_notes": "Master orientation for the BROski brain ecosystem — read this before any brain or agent work.",
    },
    "CONTEXT_RETENTION_ANTI_INTERRUPT_v1.md": {
        "new_id": "HS-078",
        "hero_name": "FLOW KEEPER",
        "emoji": "🌊",
        "depends_on": [
            ("HS-002", "SIX_LAWS_OF_AGENTS — Law 2 (MINIMISE INTERRUPTIONS) is this skill"),
        ],
        "provides": [
            "flow-state-preservation",
            "anti-interrupt-defaults",
            "silent-decision-pattern",
        ],
        "related": [
            ("HS-077", "CONSENT GUARDIAN — sits in tension; gate state-changes, default small ones"),
            ("HS-075", "THE CHOICE MATRIX — matrix formalises when to interrupt vs default"),
        ],
        "graph_notes": "Critical ND-first principle — agents preserve hyperfocus by defaulting small decisions rather than interrupting the user.",
    },
    "CONTEXT_STORE_ARCHITECTURE_v1.md": {
        "new_id": "HS-072",
        "hero_name": "THE MEMORY VAULT",
        "emoji": "🗃️",
        "depends_on": [
            ("HS-001", "ANATOMY_OF_AN_AGENT — memory is one of the 6 organs"),
            ("HS-003", "AGENT_LIFECYCLE_STATE_MACHINE — context store feeds every state"),
        ],
        "provides": [
            "redis-context-store",
            "context-slot-pattern",
            "agent-shared-memory",
            "dot-notation-key-schema",
        ],
        "related": [
            ("HS-078", "FLOW KEEPER — context store enables seamless handoffs"),
            ("HS-008", "BROSKI ORCHESTRATOR PATTERN — orchestrator writes shared context"),
        ],
        "graph_notes": "Shared Redis memory for the agent crew — dot-notation keys let agents hand off state without losing context mid-task.",
    },
    "COST_OPTIMISATION_AUTO_PATTERN_v1.md": {
        "new_id": "HS-045",
        "hero_name": "FRUGAL ENGINE",
        "emoji": "💰",
        "depends_on": [
            ("HS-041", "METRICS FORGE — cost monitoring requires metrics to be wired"),
            ("HS-008", "BROSKI ORCHESTRATOR PATTERN — throttle signals route through orchestrator"),
        ],
        "provides": [
            "cost-monitoring",
            "auto-throttle",
            "budget-enforcement",
            "llm-spend-control",
        ],
        "related": [
            ("HS-093", "NIGHT TENDER — nightly loop evaluates cost trends"),
            ("HS-019", "OBSERVABLE AGENT OPERATIONS — cost metrics feed observability"),
        ],
        "graph_notes": "Self-tuning cost optimizer — monitors LLM token spend and container resources, throttles before the budget cap.",
    },
    "GOALKEEPER_SELF_IMPROVING_AGENT_v1.md": {
        "new_id": "HS-040",
        "hero_name": "GOALKEEPER",
        "emoji": "🥅",
        "depends_on": [
            ("HS-043", "LOOP MASTER — goalkeeper runs the 5-loop autonomously"),
            ("HS-003", "AGENT_LIFECYCLE_STATE_MACHINE — lifecycle governs when improvement fires"),
        ],
        "provides": [
            "goal-tracking",
            "kpi-measurement",
            "autonomous-improvement-trigger",
            "proactive-agent-pattern",
        ],
        "related": [
            ("HS-093", "NIGHT TENDER — nightly loop is the scheduled executor"),
            ("HS-045", "FRUGAL ENGINE — cost KPIs feed into goalkeeper metrics"),
        ],
        "graph_notes": "Proactive goal-tracking agent — knows what done looks like and pushes toward it without being asked.",
    },
    "GOD_MODE_HYPERFLOW_v1.md": {
        "new_id": "HS-006",
        "hero_name": "GODFLOW",
        "emoji": "⚡",
        "depends_on": [
            ("HS-002", "SIX_LAWS_OF_AGENTS — God Mode respects the 6 laws"),
            ("HS-001", "ANATOMY_OF_AN_AGENT — anatomy is the foundation"),
        ],
        "provides": [
            "god-mode-protocol",
            "nd-first-flow",
            "momentum-chunking",
            "agent-handoff-rules",
            "dopamine-loop-structure",
        ],
        "related": [
            ("HS-008", "BROSKI ORCHESTRATOR PATTERN — orchestrator runs the flow"),
            ("HS-007", "NODE SMITH — node-graph design complements the flow"),
            ("HS-009", "THE GRAND CODEX — master context loads first"),
        ],
        "graph_notes": "Root workflow skill — activates ND-first hyperfocus mode, chunks any project into momentum-building wins.",
    },
    "GUARDIAN_BOT_PHASE_MAP_v1.md": {
        "new_id": "HS-038",
        "hero_name": "PHASE WARDEN",
        "emoji": "🛡️",
        "depends_on": [
            ("HS-002", "SIX_LAWS_OF_AGENTS — moderation must respect agent laws"),
            ("HS-004", "FIVE MANDATORY GUARDRAILS — ban actions require hard-stop guardrails"),
            ("HS-077", "CONSENT GUARDIAN — P3c ban requires explicit human approval"),
        ],
        "provides": [
            "guardian-phase-map",
            "discord-mod-phases",
            "one-door-architecture",
            "p1-to-p3c-reference",
        ],
        "related": [
            ("HS-050", "WATCHDOG PRIME — watchdog monitors after Guardian acts"),
            ("HS-122", "GUARDIAN WATCHDOG — Python monitoring code companion"),
        ],
        "graph_notes": "Complete Server Guardian phase map (P1 reactive → P3c veto-gated ban) — must-read before any Discord moderation work.",
    },
    "GUARDIAN_WATCHDOG_MONITOR_v1.md": {
        "new_id": "HS-122",
        "hero_name": "GUARDIAN WATCHDOG",
        "emoji": "🔭",
        "depends_on": [
            ("HS-038", "PHASE WARDEN — watchdog operates within Guardian phases"),
            ("HS-041", "METRICS FORGE — metrics must be wired before watchdog can evaluate"),
        ],
        "provides": [
            "watchdog-code-pattern",
            "service-health-loop",
            "failure-restart-logic",
            "consecutive-failure-counter",
        ],
        "related": [
            ("HS-050", "WATCHDOG PRIME — prompt-block companion to this code pattern"),
            ("DS-028", "PROGRESSIVE_HEALTH_WAIT — health wait pattern used in restart logic"),
        ],
        "graph_notes": "Python implementation of the post-launch watchdog — code companion to HS-050 WATCHDOG PRIME.",
    },
    "GUARDIAN_WATCHDOG_POST_LAUNCH_v1.md": {
        "new_id": "HS-050",
        "hero_name": "WATCHDOG PRIME",
        "emoji": "🛡️",
        "depends_on": [
            ("HS-038", "PHASE WARDEN — watchdog starts after Guardian phases are live"),
            ("HS-041", "METRICS FORGE — metrics must be wired before watchdog can evaluate"),
        ],
        "provides": [
            "watchdog-monitoring-prompt",
            "post-launch-monitoring",
            "auto-heal-pattern",
            "discord-alert-integration",
        ],
        "related": [
            ("HS-122", "GUARDIAN WATCHDOG — Python code companion"),
            ("DS-028", "PROGRESSIVE_HEALTH_WAIT — health wait feeds the watchdog loop"),
        ],
        "graph_notes": "Prompt block to activate post-launch watchdog monitoring — use with HS-122 for the Python implementation.",
    },
    "HYPER_BRAIN_MODULES_v1.md": {
        "new_id": "HS-011",
        "hero_name": "MIND BLOCKS",
        "emoji": "🧩",
        "depends_on": [
            ("HS-016", "BRAIN PRIMER — orientation required before reading the module map"),
            ("HS-017", "MIND CORE — core agent hosts these modules"),
        ],
        "provides": [
            "brain-module-map",
            "port-8100-reference",
            "brain-api-endpoints",
            "8-module-overview",
        ],
        "related": [
            ("HS-013", "DAWN HERALD — morning_briefing_ai module lives here"),
            ("HS-124", "FOCUS HAWK — focus_tracker module lives here"),
            ("HS-018", "BRIDGE KEEPER — mcp_bridge module lives here"),
        ],
        "graph_notes": "API reference for all 8 HyperBrain modules on port 8100 — the map agents load before calling any brain endpoint.",
    },
    "HYPERAGENT_SDK_AGENTS_README_v1.md": {
        "new_id": "HS-028",
        "hero_name": "SDK PRIMER",
        "emoji": "📖",
        "depends_on": [
            ("HS-009", "THE GRAND CODEX — master context gives the 5-repo map SDK sits in"),
        ],
        "provides": [
            "sdk-ecosystem-map",
            "agent-interface-standard",
            "write-once-deploy-anywhere",
        ],
        "related": [
            ("HS-016", "BRAIN PRIMER — brain sits at same ecosystem layer"),
            ("DS-016", "SDK_PUBLISH_WORKFLOW — publish workflow for SDK changes"),
            ("DS-017", "HYPERAGENT_SDK_PUBLISH_SKILL — SDK publish skill details"),
        ],
        "graph_notes": "Orientation for HyperAgent-SDK — the shared agent interface standard that connects all 5 ecosystem repos.",
    },
    "HYPERFOCUS_ZONE_MASTER_CONTEXT_v1.md": {
        "new_id": "HS-009",
        "hero_name": "THE GRAND CODEX",
        "emoji": "🏆",
        "depends_on": [],
        "provides": [
            "ecosystem-context",
            "sacred-rules-reference",
            "system-architecture-snapshot",
            "5-repo-map",
        ],
        "related": [
            ("HS-016", "BRAIN PRIMER — brain readme sits inside this ecosystem"),
            ("HS-028", "SDK PRIMER — SDK readme sits inside this ecosystem"),
            ("DS-012", "TRUTH VS CLAIM AUDIT — contradictions in the codex must be surfaced"),
        ],
        "graph_notes": "Root context skill for the entire ecosystem — load in any AI session before any HyperFocus z0ne work.",
    },
    "HYPERGRAPH_NODE_SKILL_v1.md": {
        "new_id": "HS-007",
        "hero_name": "NODE SMITH",
        "emoji": "🔗",
        "depends_on": [
            ("HS-001", "ANATOMY_OF_AN_AGENT — agents are nodes; anatomy defines their shape"),
        ],
        "provides": [
            "hypergraph-pattern",
            "node-based-design",
            "visual-architecture-spec",
            "typed-port-model",
        ],
        "related": [
            ("HS-008", "BROSKI ORCHESTRATOR PATTERN — orchestrator is a hub node"),
            ("HS-006", "GODFLOW — god mode workflow maps to a hypergraph"),
        ],
        "graph_notes": "Visual node-graph architecture pattern — design any agent system as a circuit-board of typed input/brain/output nodes.",
    },
    "METRICS_ENGINE_INTEGRATION_v1.md": {
        "new_id": "HS-041",
        "hero_name": "METRICS FORGE",
        "emoji": "⚡",
        "depends_on": [
            ("HS-001", "ANATOMY_OF_AN_AGENT — metrics are the Eyes organ"),
            ("HS-019", "OBSERVABLE AGENT OPERATIONS — observability schema defines what to emit"),
        ],
        "provides": [
            "prometheus-wiring-pattern",
            "agent-metrics-template",
            "grafana-auto-scrape",
            "python-and-node-support",
        ],
        "related": [
            ("HS-050", "WATCHDOG PRIME — watchdog consumes these metrics"),
            ("HS-073", "PULSE STREAM — SSE events complement Prometheus metrics"),
        ],
        "graph_notes": "Standard pattern for wiring any agent into Prometheus/Grafana — apply at agent creation, never retroactively.",
    },
    "MORNING_BRIEFING_AI_v1.md": {
        "new_id": "HS-013",
        "hero_name": "DAWN HERALD",
        "emoji": "🌅",
        "depends_on": [
            ("HS-011", "MIND BLOCKS — module map needed to call the briefing endpoint"),
            ("HS-016", "BRAIN PRIMER — brain ecosystem context required"),
        ],
        "provides": [
            "briefing-generation",
            "daily-ai-summary",
            "vault-briefing-note",
            "port-8100-briefing-trigger",
        ],
        "related": [
            ("HS-020", "HERALD'S SCROLL — morning briefing manifest"),
            ("HS-124", "FOCUS HAWK — focus stats included in briefing"),
            ("HS-021", "VAULT SYNC — brain sync often follows the briefing"),
        ],
        "graph_notes": "Trigger reference for the morning briefing AI — curl endpoint, sections, output path on port 8100.",
    },
    "NIGHTLY_LEARNING_LOOP_v1.md": {
        "new_id": "HS-093",
        "hero_name": "NIGHT TENDER",
        "emoji": "🌙",
        "depends_on": [
            ("HS-003", "AGENT_LIFECYCLE_STATE_MACHINE — loop is a recurring lifecycle phase"),
            ("HS-043", "LOOP MASTER — nightly loop executes the 5-loop pattern"),
            ("HS-004", "FIVE MANDATORY GUARDRAILS — 6 hard gates mirror the guardrails"),
        ],
        "provides": [
            "nightly-improvement-loop",
            "drift-detection",
            "hitl-gate-pattern",
            "rollback-on-fail",
            "prompt-update-pipeline",
        ],
        "related": [
            ("HS-040", "GOALKEEPER — goalkeeper triggers the loop when KPIs slip"),
            ("HS-044", "AB SPLITTER — A/B tests feed the prompt-update step"),
            ("HS-088", "THE MIRROR OATH — regression check mirrors the audit"),
        ],
        "graph_notes": "Safe overnight self-improvement pipeline — 6 hard gates prevent agents going rogue while still allowing them to evolve.",
    },
    "OBSIDIAN_BRAIN_SYNC_SKILL_v1.md": {
        "new_id": "HS-021",
        "hero_name": "VAULT SYNC",
        "emoji": "🔄",
        "depends_on": [
            ("DS-018", "OBSIDIAN_GIT_VAULT — git workflow for the vault is a prerequisite"),
            ("HS-016", "BRAIN PRIMER — brain ecosystem context required"),
        ],
        "provides": [
            "brain-sync-workflow",
            "sprint-knowledge-update",
            "vault-maintenance-checklist",
            "commit-push-pattern",
        ],
        "related": [
            ("HS-009", "THE GRAND CODEX — codex is the primary sync target"),
            ("DS-015", "PARALLEL_GIT_WORKFLOW_SURVIVAL — parallel workflow awareness needed"),
        ],
        "graph_notes": "Post-sprint knowledge sync — WHATS_DONE → CLAUDE_CONTEXT → architecture → commit → push.",
    },
    "SELF_IMPROVEMENT_5_LOOP_LOGIC_v1.md": {
        "new_id": "HS-043",
        "hero_name": "LOOP MASTER",
        "emoji": "🔄",
        "depends_on": [
            ("HS-003", "AGENT_LIFECYCLE_STATE_MACHINE — improvement loops within the lifecycle"),
            ("HS-002", "SIX_LAWS_OF_AGENTS — Law 4 (IMPROVE) mandates this loop"),
        ],
        "provides": [
            "5-loop-pattern",
            "observe-analyse-update-deploy-review",
            "self-improvement-reference",
        ],
        "related": [
            ("HS-093", "NIGHT TENDER — nightly loop is the scheduled executor"),
            ("HS-040", "GOALKEEPER — goalkeeper measures KPIs between loops"),
            ("HS-044", "AB SPLITTER — A/B tests feed the UPDATE step"),
        ],
        "graph_notes": "Canonical 5-loop self-improvement pattern — the difference between a static tool and an autonomous, compounding system.",
    },
    "SELF_IMPROVEMENT_5_LOOP_v1.md": {
        "new_id": "HS-121",
        "hero_name": "LOOP FORGE",
        "emoji": "🔄",
        "depends_on": [
            ("HS-043", "LOOP MASTER — this code implements the 5-loop reference"),
            ("HS-003", "AGENT_LIFECYCLE_STATE_MACHINE — loop fires within the lifecycle"),
        ],
        "provides": [
            "self-improvement-code",
            "loop-implementation",
            "autonomous-metric-check",
            "observation-store-pattern",
        ],
        "related": [
            ("HS-040", "GOALKEEPER — goalkeeper uses this loop implementation"),
            ("HS-093", "NIGHT TENDER — nightly scheduler runs this loop"),
        ],
        "graph_notes": "Python code companion to HS-043 LOOP MASTER — implement all 5 loops in any agent background task runner.",
    },
    "SKILL_REGISTRY_AGENT_PATTERN_v1.md": {
        "new_id": "HS-042",
        "hero_name": "REGISTRY LORD",
        "emoji": "📋",
        "depends_on": [
            ("HS-008", "BROSKI ORCHESTRATOR PATTERN — orchestrator uses the registry for routing"),
            ("HS-067", "THE THRONE LADDER — hierarchy determines registry authority"),
        ],
        "provides": [
            "skill-registry-pattern",
            "task-routing",
            "agent-capability-index",
            "yellow-pages-pattern",
        ],
        "related": [
            ("HS-079", "THE CREW CHARTER — role definitions feed the registry"),
            ("HS-009", "THE GRAND CODEX — codex is the source of truth for capabilities"),
        ],
        "graph_notes": "Central registry pattern for a 30+ agent swarm — the Yellow Pages that routes tasks to the best-matched agent.",
    },
    "SPECIALIST_AGENT_ROLES_v1.md": {
        "new_id": "HS-079",
        "hero_name": "THE CREW CHARTER",
        "emoji": "👥",
        "depends_on": [
            ("HS-067", "THE THRONE LADDER — hierarchy defines the 6 slots"),
            ("HS-008", "BROSKI ORCHESTRATOR PATTERN — orchestrator manages all 6"),
        ],
        "provides": [
            "specialist-role-definitions",
            "can-cannot-tools-envelope",
            "6-specialist-roster",
        ],
        "related": [
            ("HS-080", "THE TOOL BELT — minimum tools every specialist must expose"),
            ("HS-075", "THE CHOICE MATRIX — delegate decision uses role definitions"),
        ],
        "graph_notes": "Defines the CAN/CANNOT/Tools envelope for each of the 6 BROski specialist agents — load before spawning or auditing a role.",
    },
    "SSE_AGENT_EVENT_SCHEMA_v1.md": {
        "new_id": "HS-073",
        "hero_name": "PULSE STREAM",
        "emoji": "📡",
        "depends_on": [
            ("HS-001", "ANATOMY_OF_AN_AGENT — Voice organ defines what agents emit"),
            ("HS-083", "THE THREE VOICES — streaming is one of the three comms patterns"),
        ],
        "provides": [
            "sse-event-schema",
            "real-time-agent-events",
            "frontend-streaming-contract",
            "typescript-event-interface",
        ],
        "related": [
            ("HS-019", "OBSERVABLE AGENT OPERATIONS — logs + metrics complement SSE events"),
            ("HS-041", "METRICS FORGE — Prometheus and SSE are parallel observability streams"),
        ],
        "graph_notes": "Canonical SSE schema for streaming real-time agent activity to the frontend — every agent emits structured events so the timeline UI stays live.",
    },
    "SURFACE_CONTRADICTIONS_DONT_PICK_SIDES_v1.md": {
        "new_id": "HS-111",
        "hero_name": "TRUTH FLAGGER",
        "emoji": "🚩",
        "depends_on": [
            ("HS-002", "SIX_LAWS_OF_AGENTS — Law 6 (SURFACE) is this skill"),
        ],
        "provides": [
            "contradiction-surfacing",
            "silent-pick-prevention",
            "doc-correction-pattern",
        ],
        "related": [
            ("DS-012", "TRUTH VS CLAIM AUDIT — audit tool that detects contradictions"),
            ("DS-011", "CROSS_REFERENCE_BEFORE_WRITING — cross-ref prevents contradictions"),
        ],
        "graph_notes": "Single most important AI-collaboration discipline — surface contradictions visibly instead of silently picking a side.",
    },
    "UNIVERSAL_AGENT_TOOLS_API_v1.md": {
        "new_id": "HS-080",
        "hero_name": "THE TOOL BELT",
        "emoji": "🧰",
        "depends_on": [
            ("HS-001", "ANATOMY_OF_AN_AGENT — tools are the Hands organ"),
            ("HS-067", "THE THRONE LADDER — role determines which tools are in the belt"),
        ],
        "provides": [
            "minimum-tool-surface",
            "file-ops-api",
            "code-ops-api",
            "agent-tools-checklist",
        ],
        "related": [
            ("HS-079", "THE CREW CHARTER — role-specific tools extend this minimum"),
            ("HS-077", "CONSENT GUARDIAN — write_file uses require_approval=True by default"),
        ],
        "graph_notes": "Minimum tool surface every BROski crew agent must expose — use as a checklist when stubbing or auditing any agent.",
    },
    "USER_AGENCY_APPROVAL_GATE_v1.md": {
        "new_id": "HS-077",
        "hero_name": "CONSENT GUARDIAN",
        "emoji": "🛑",
        "depends_on": [
            ("HS-002", "SIX_LAWS_OF_AGENTS — Law 1 (RESPECT USER AGENCY) is this skill"),
        ],
        "provides": [
            "approval-gate-pattern",
            "propose-approve-execute-flow",
            "state-change-guard",
        ],
        "related": [
            ("HS-078", "FLOW KEEPER — sits in tension; gate state-changes, default small ones"),
            ("HS-088", "THE MIRROR OATH — check 1 in the completion audit"),
            ("HS-004", "FIVE MANDATORY GUARDRAILS — approval gate is guardrail 1"),
        ],
        "graph_notes": "Non-negotiable approval pattern for any state-changing agent action — propose → approve → execute, never silent.",
    },
}


def build_gos_block(meta: dict) -> str:
    """Render the --- ... --- GoS frontmatter block."""
    lines = ["---"]
    lines.append(f'skill_id: {meta["new_id"]}')
    lines.append(f'hero_name: "{meta["hero_name"]}"')
    lines.append(f'emoji: "{meta["emoji"]}"')
    lines.append("version: v1.0")
    lines.append("category: agents")

    deps = meta.get("depends_on", [])
    if deps:
        lines.append("depends_on:")
        for ref, comment in deps:
            lines.append(f"  - {ref}  # {comment}")
    else:
        lines.append("depends_on: []  # root skill — no prerequisites")

    lines.append("provides:")
    for p in meta["provides"]:
        lines.append(f"  - {p}")

    rels = meta.get("related", [])
    if rels:
        lines.append("related:")
        for ref, comment in rels:
            lines.append(f"  - {ref}  # {comment}")
    else:
        lines.append("related: []")

    lines.append(f'graph_notes: "{meta["graph_notes"]}"')
    lines.append("---")
    return "\n".join(lines)


def retrofit_file(filepath: Path, meta: dict, dry_run: bool = False) -> str:
    """
    Insert GoS block after the H1 header line.
    Also updates the H1 if the file's ID differs from meta['new_id'].
    Returns a status string.
    """
    content = filepath.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines(keepends=True)

    # Already has GoS — skip
    if "depends_on:" in content or "provides:" in content:
        return "SKIP (already has GoS)"

    # Find H1 line index
    h1_idx = None
    for i, line in enumerate(lines):
        if line.startswith("#"):
            h1_idx = i
            break
    if h1_idx is None:
        return "SKIP (no H1 found)"

    # Optionally fix the HS-NNN in the H1 header
    new_id = meta["new_id"]
    h1 = lines[h1_idx]
    id_in_h1 = re.search(r"(HS|DS)-\d+", h1)
    if id_in_h1 and id_in_h1.group(0) != new_id:
        old_id = id_in_h1.group(0)
        lines[h1_idx] = h1.replace(old_id, new_id, 1)

    # Build insertion: blank line + GoS block + blank line
    gos_block = "\n" + build_gos_block(meta) + "\n"

    # Find first blank line after H1 to use as insertion point
    insert_after = h1_idx  # default: right after H1
    for j in range(h1_idx + 1, min(h1_idx + 4, len(lines))):
        if lines[j].strip() == "":
            insert_after = j
            break

    new_lines = lines[: insert_after + 1] + [gos_block] + lines[insert_after + 1 :]
    new_content = "".join(new_lines)

    if not dry_run:
        filepath.write_text(new_content, encoding="utf-8")

    return f"{'DRY-RUN ' if dry_run else ''}RETROFITTED ({new_id})"


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    repo_root = Path(__file__).parent.parent
    agents_dir = repo_root / "agents"

    print(f"\n{'[DRY-RUN] ' if DRY_RUN else ''}GoS Retrofit — agents/ ({len(METADATA)} files)\n")
    print(f"{'─' * 60}")

    ok = skipped = updated = 0
    for filename, meta in sorted(METADATA.items()):
        fp = agents_dir / filename
        if not fp.exists():
            print(f"  ❌ NOT FOUND: {filename}")
            continue
        status = retrofit_file(fp, meta, dry_run=DRY_RUN)
        icon = "✅" if "RETROFITTED" in status else ("⏭️ " if "SKIP" in status else "❌")
        print(f"  {icon} {filename:<55} {status}")
        if "RETROFITTED" in status:
            updated += 1
        elif "SKIP" in status:
            skipped += 1
        ok += 1

    print(f"\n{'─' * 60}")
    print(f"  Total: {ok} | Updated: {updated} | Skipped: {skipped}\n")
    if DRY_RUN:
        print("  Run without --dry-run to apply changes.\n")


if __name__ == "__main__":
    main()
