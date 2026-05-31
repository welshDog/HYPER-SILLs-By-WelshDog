---
id: SKILL_XXX
hero_name: "Your Skill Hero Name"
category: coding | content | design | agents | youtube | automation | ND-friendly
version: v1.0.0
last_updated: YYYY-MM-DD
best_for: "One sentence on when to use this skill"
difficulty: beginner | intermediate | advanced
estimated_time: "~5 min"
tags: [tag1, tag2, tag3]

# ===== 🧠 SKILL GRAPH METADATA (GoS) — Added v2.0 =====
# These fields power dependency-aware retrieval (+25% reward, -57% tokens)
# All fields are OPTIONAL but strongly recommended for new skills

depends_on:           # Skills needed BEFORE using this one effectively
  - id: SKILL_XXX
    reason: "Why this skill is a prerequisite"
  # - id: SKILL_YYY
  #   reason: "Another prereq if needed"

provides:             # What capabilities/outputs this skill adds
  - "Capability 1 — what the agent can do after loading this skill"
  - "Capability 2"

related:              # Cross-references (replaces manual [[HS-NNN]] wikilinks)
  - SKILL_XXX         # Related Skill Name — why it connects
  # - SKILL_YYY

packs:                # Which skill packs this belongs to
  - "Pack Name Here"  # e.g. "Agent Builder Pack"

trigger_keywords:     # Words/phrases that should auto-suggest this skill
  - "keyword one"
  - "keyword two"

# ===== 📦 VERSIONING =====
semantic_version: v1.0.0   # MAJOR.MINOR.PATCH
# MAJOR = breaking change (prompt behaviour changes)
# MINOR = new capability added
# PATCH = fix, clarification, typo
version_history:
  - v1.0.0: "Initial skill added to vault"

# ===== 🔄 LIFECYCLE =====
# DRAFT → REVIEW → ACTIVE → DEPRECATED → ARCHIVED
skill_lifecycle: DRAFT
# DRAFT      = new, not yet validated
# REVIEW     = passes linter, tested at least once
# ACTIVE     = fully supported, appears in all searches
# DEPRECATED = warn on use, suggest replacement
# ARCHIVED   = hidden from search, kept for history
---

# ⚡ [SKILL HERO NAME]

> *One-line power statement — what does this skill DO in plain English?*

---

## 🎯 Purpose

What does this skill do? Why does it exist? What problem does it solve?

---

## 📥 Inputs

- **Input 1:** Description of what to provide
- **Input 2:** Description of what to provide
- **Input 3:** Description of what to provide

---

## 📤 Output Format

Describe the output format: markdown, JSON, bullet list, numbered steps, table, etc.

---

## 🔮 Prompt Block

```
PASTE YOUR EXACT PROMPT HERE.

Use [INPUT_VARIABLE] format for anything the user needs to fill in.

Example:
You are an expert in [TOPIC]. Analyse [INPUT_DATA] and provide [OUTPUT_TYPE].
```

---

## 💡 Example Usage

**Input:**
```
[Example of what you'd paste in]
```

**Output:**
```
[Example of what the AI returns]
```

---

## 🔗 Related Skills

- `SKILL_XXX` — Related Skill Name (why it pairs well)
- `SKILL_XXX` — Related Skill Name (why it pairs well)

---

## 📊 Skill Graph

```
Dependencies (must load first):
  SKILL_XXX → THIS SKILL → provides: [capability 1, capability 2]

Enables (load these next):
  THIS SKILL → SKILL_YYY (if building on top of this)
```

---

*Added by: @welshDog | Vault: HYPER-SKILLs-By-WelshDog*
*Template v2.0 — GoS-ready with dependency graph metadata*
