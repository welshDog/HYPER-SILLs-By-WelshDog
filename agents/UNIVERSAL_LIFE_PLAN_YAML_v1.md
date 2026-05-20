# HS-090 — 📜 SOUL SCROLL — Universal Life Plan YAML v2.0 Template

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/🧬 The Full Confirmed Hyper Agent Roster` §1
**Version:** v1 (wraps Life Plan schema v2.0.0)

---

## 🤔 What It Does

The standardised YAML spec **every HyperCode agent inherits from**. Drop at `agents/{agent_name}/life_plan.yaml`, customise the identity + a few collaboration fields, and the agent gets a versioned identity, ethics charter, dialogue state machine, swarm rules, autoscale config, security posture, and deprecation schedule — for free.

> This is the canonical schema. New agents that *don't* ship a `life_plan.yaml` won't be picked up by Crew Orchestrator's dependency graph or the nightly learning loop ([[HS-093]]).

---

## 🧬 The Template

```yaml
# ════════════════════════════════════════════════
# HYPER AGENT LIFE PLAN — v2.0.0
# Universal Template | HyperCode V2.0 Ecosystem
# git: agents/{agent_name}/life_plan.yaml
# ════════════════════════════════════════════════

identity_manifest:
  name: "AGENT_NAME"
  codename: "AGENT_CODENAME"
  version: "2.0.0"
  created: "YYYY-MM-DD"
  port: 0000
  container: "hypercode-AGENT_NAME"
  core_purpose: >
    One sentence. What this agent DOES and WHY it exists.
  ethical_charter:
    - "Never harm users, data, or system stability"
    - "Respect GDPR — no PII storage without TTL + consent"
    - "Escalate ALL irreversible actions to human-in-the-loop"
    - "Log every decision to governance ledger"
    - "Never block another agent's async work"
  evolution_path:
    v2_current: "describe current capability"
    v3_next:    "describe 2027 upgrade target"
    v4_future:  "quantum/DNA compute integration"

communication_stack:
  input_modes:  ["text", "JSON-RPC", "WebSocket", "REST", "Redis-Pub/Sub"]
  output_modes: ["text", "JSON", "SSE-stream", "voice_TTS"]
  dialogue_state_machine:
    states:
      - idle         # waiting for trigger
      - listening    # receiving input
      - planning     # decomposing goal
      - executing    # running tasks
      - reporting    # broadcasting results
      - conflict     # escalating exception
      - resting      # scheduled downtime / low-load
    transitions:
      idle         → listening:    "on_trigger"
      listening    → planning:     "intent_parsed"
      planning     → executing:    "plan_approved OR auto"
      executing    → reporting:    "task_complete"
      any          → conflict:     "exception_detected"
      conflict     → human_review: "uncertainty > 0.8 OR destructive_op"
  empathy_model:
    engine:              "sentiment_aware_response_shaping"
    adhd_friendly_mode:  true   # short bursts, no walls of text
    dyslexia_mode:       true   # chunked, visual anchor language
    fatigue_detection:   true   # reduces verbosity on repeated requests
    adaptation_strategy: "reduce_verbosity + offer_quick_wins"
  conflict_resolution:
    protocol: "RAFT_consensus via Crew Orchestrator"
    fallback:  "graceful_degrade → log → human_override"
    timeout_ms: 5000

collaboration_matrix:
  role:  "ARCHITECT | EXECUTOR | OBSERVER | COMMUNICATOR | VALIDATOR"
  dependency_graph:
    depends_on: []
    depended_by: []
  consensus_algorithm: "weighted_voting"   # weight = agent confidence score
  leader_election:     "highest_uptime_agent_wins"
  swarm_rules:
    min_quorum:              3
    max_swarm_size:          8
    formation_trigger:       "task_complexity_score > 0.7"
    dissolve_trigger:        "task_complete OR timeout_60s"
    split_brain_resolution:  "Brain agent casts tiebreak vote"

work_pipeline:
  goal_decomposition:
    engine:   "recursive_task_tree"   # LangGraph / CrewAI planner
    method:   "SMART + OKR hybrid"
    max_depth: 5
    leaf_node_max_duration_ms: 10000
  task_prioritization:
    heuristic: "urgency × impact / effort"
    queue:     "Redis priority queue"
    tiebreak:  "FIFO"
  resource_allocation:
    cpu_limit:    "500m"
    memory_limit: "512Mi"
    autoscale:    true
    burst_allowed: true
  checkpoint_strategy:
    frequency:        "every_5_steps OR every_30s"
    storage:          "Redis pub/sub + PostgreSQL snapshots"
    rollback_policy:  "last_known_good"
    rollback_trigger: "error_rate > 5%"

play_framework:
  creativity_generators:
    - "random_seed_ideation"
    - "cross_domain_metaphor_injection"
    - "esoteric_language_code_golf"   # Brainfuck, Befunge, Malbolge
  game_theory_minigames:
    - name: "SwarmOptimise"
      type: "cooperative_iterated_game"
      reward: "BROski$ coins"
    - name: "ChaosDefend"
      type: "adversarial_red_vs_blue"
      reward: "XP + uptime_badges"
    - name: "PrisonersDilemma"
      type: "multi_agent_trust_builder"
      reward: "+50 BROski$ for cooperative outcome"
  stress_test_sims:
    - "chaos_monkey: random_service_kill"
    - "flood_test: 10x_normal_load_60s"
    - "latency_injection: +500ms_all_calls"
  reward_functions:
    prosocial_multiplier: 1.5    # bonus for helping another agent recover
    latency_bonus:    "p95 < 150ms → +10 BROski$"
    uptime_streak:    "99.9% for 7 days → Level Up 🏆"
    creativity_bonus: "novel_solution_path → +100 BROski$"

future_proofing:
  auto_update_contract:
    check_interval:     "nightly 02:00 UTC"
    channel:            "GitHub Actions → Docker Hub → ghcr.io"
    approval_required:  "breaking_changes_only"
    rollback_window:    "24h"
  version_migration:
    strategy:          "blue_green_deployment"
    schema_migrations: "Alembic auto-generated"
    config_versioning: "semver on all YAML"
    zero_downtime:     true
  deprecation_schedule:
    notice_period: "90 days"
    v2_to_v3: "2027-Q1"
    v3_to_v4: "2028-Q2"
    sunset_endpoint: "/_deprecated/{feature}"
  extensibility_hooks:
    plugin_interface:      "POST /api/plugins/register"
    microservice_contract: "OpenAPI 3.1 JSON schema"
    llm_swap_interface:    "LiteLLM-compatible /v1/chat adapter"
    event_bus:             "Redis Streams + SSE WebSocket broadcast"

security_compliance:
  owasp:
    input_validation: "Pydantic v2 on ALL endpoints"
    secret_scanning:  ".secrets.baseline + detect-secrets pre-commit"
    rate_limiting:    "nginx: 100 req/min per IP"
    sql_injection:    "SQLAlchemy parameterised queries only"
  gdpr:
    data_minimisation: "No PII stored beyond session TTL"
    session_ttl:       "24h Redis expiry"
    right_to_erasure:  "DELETE /api/user/{id}/data"
    data_residency:    "EU regions only in production"
  soc2:
    audit_logging:     "All agent actions → PostgreSQL audit_log table"
    access_control:    "JWT + RBAC on all admin endpoints"
    backup_policy:     "Daily PostgreSQL dump + S3 30-day retention"
    incident_response: "MedBot auto-alerts + webhook notification"
```

---

## 🎯 Minimum-Customise Fields (per new agent)

Just override these — leave the rest as inherited defaults:

```yaml
identity_manifest:
  name: "..."
  codename: "..."
  port: 0000
  container: "hypercode-..."
  core_purpose: >
    One sentence.

collaboration_matrix:
  role: "EXECUTOR"   # pick one
  dependency_graph:
    depends_on: ["brain", "crew-orchestrator"]
    depended_by: []
```

Everything else inherits from this template's defaults.

---

## 🚀 Drop-In Workflow

```bash
mkdir -p agents/life-plans
cp agents/life-plans/TEMPLATE.yaml agents/{your_agent}/life_plan.yaml
# customise identity_manifest + collaboration_matrix.dependency_graph
git add agents/{your_agent}/life_plan.yaml
git commit -m "feat: 🦅 add life_plan for {your_agent}"
```

---

## 🧩 Related Skills

- [[HS-089]] Hyper Agent Roster — the 22 + 5 agents this template serves
- [[HS-091]] Top-Tier Agent Identity Cards — concrete examples for the 5 special agents
- [[HS-085]] 5 Mandatory Agent Guardrails — `security_compliance` enforcement
- [[HS-092]] Agent Contract Test Suite — verifies a life-plan is wired correctly
- [[HS-093]] Continuous Learning Loop — reads `version_migration` + governance fields
- [[HS-095]] Governance Ledger Entry Schema — sibling spec
