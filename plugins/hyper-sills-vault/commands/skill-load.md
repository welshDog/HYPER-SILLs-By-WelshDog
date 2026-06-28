---
description: Load a HYPER-SILLs skill by ID (e.g. HS-100) and apply it
argument-hint: <skill-id>
---

Load the HYPER-SILLs skill: **$ARGUMENTS**

1. Call the `load_skill` MCP tool (from the `hyper-sills` server) with the skill ID.
   If the ID is not found, call `search_skills` with the user's text and offer the closest match
   in a warm, no-blame way (Mercy Message style — "No stress, that exact ID isn't here, but...").
2. Call `get_skill_graph(id)` and load any `depends_on` skills first (Graph-of-Skills load order):
   prerequisites → this skill → optionally `related` skills for context.
3. Apply the skill's Prompt Block to the user's current task.
