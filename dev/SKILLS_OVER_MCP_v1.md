# HS-129 — 🌐 SKILLS-OVER-MCP — Expose Skills as MCP Resources (SEP-2640)

---
skill_id: HS-129
hero_name: "SKILLS-OVER-MCP"
emoji: "🌐"
version: v1.0.0
status: ACTIVE
category: dev
depends_on:
  - DS-020  # PORTAL FORGE — the MCP server you're extending
provides:
  - mcp-resources-skill-surface
  - sep-2640-alignment
  - well-known-skill-discovery
related:
  - HS-128  # PLUGIN FORGE — ships this server inside a plugin
  - HS-073  # PULSE STREAM — adjacent MCP event patterns
graph_notes: "Exposes each skill as an MCP Resource (skill://ID) per the Skills-over-MCP working group (SEP-2640), so any SEP-2640-aware host discovers and reads skills natively, not via bespoke tools."
---
**Category:** `dev/`
**Source:** Born-here — modelcontextprotocol.io Skills-over-MCP charter / SEP-2640 (2026)
**Version:** v1

---

## 🤔 What It Does

The **Skills over MCP** working group (Anthropic + Nordstrom + Google + others)
standardised how agent skills are discovered and consumed through MCP. The current
direction (SEP-2640, Extensions Track) is **Resources-based**: skills are MCP
*Resources*, not custom tools. This skill adds that Resources surface to your server
so any standards-aware host can browse `skills://index` and read `skill://HS-NNN`
without learning your bespoke tool names.

---

## 🎯 Purpose

- **Who uses it:** Anyone running an MCP skill server who wants forward-compat.
- **When to use it:** Right after you have working tools — add Resources alongside them.
- **What it unlocks:** Native skill discovery across MCP clients; future SEP-2640 compliance.

---

## 📥 Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `registry` | `path` | ✅ | Source of truth listing your skills |
| `uri_scheme` | `string` | ❌ | Defaults to `skill://<ID>` |

---

## 📤 Output Format

```python
@mcp.resource("skills://index")        # browseable list of all skills
@mcp.resource("skill://{skill_id}")    # read one skill's markdown
```

---

## 🔮 Prompt Block

```
You are SKILLS-OVER-MCP. Add a SEP-2640-style Resources surface to an existing
FastMCP server WITHOUT removing its tools (back-compat).

Steps:
1. Add @mcp.resource("skills://index") returning a JSON list of {uri, id, hero_name,
   category, description}, skipping archived skills.
2. Add @mcp.resource("skill://{skill_id}") returning the skill's full markdown,
   with a Mercy-Message fallback when the ID is unknown.
3. Update the server `instructions` to advertise both resources.
4. Extend the smoke test to assert index count > 0 and a single skill reads back.

Rules:
- Keep existing tools untouched — Resources are additive.
- Resolve registry/file ID mismatches the same way the tools already do.
- Track SEP-2640; it's Extensions Track, so label it clearly as tracking-not-final.
```

---

## 💡 Example Usage

```python
# Host (SEP-2640-aware) lists resources:
#   skills://index            → 120 skills
#   skill://HS-100            → full CRADLE-TO-GRAVE markdown
res = await session.read_resource("skill://HS-100")
```

---

## 🚨 Anti-patterns

- **Don't delete your tools** — SEP-2640 is still in review; keep both surfaces.
- **Don't invent a parallel registry** — Resources read the same source of truth as tools.
- **Don't block on the spec finalising** — additive Resources are safe to ship today.

---

## 🔗 Related Skills

- [[HS-081]] PORTAL FORGE — the server you extend
- [[HS-128]] PLUGIN FORGE — bundle this server in a plugin
- [[HS-073]] PULSE STREAM — adjacent MCP streaming patterns

---

## 📋 THE PROMPT

> Copy this block into any AI session to activate the skill:

```text
Use skill HS-129 [SKILLS-OVER-MCP]. Add a SEP-2640 Resources surface (skills://index + skill://ID) to my FastMCP server alongside the existing tools, with a mercy fallback and an updated smoke test.
```
