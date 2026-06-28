---
description: Search the HYPER-SILLs vault by keyword, category, or tag
argument-hint: <keywords> [category]
---

Search the HYPER-SILLs skill vault for skills matching: **$ARGUMENTS**

Use the `search_skills` MCP tool (from the `hyper-sills` server) with the keywords above.
If the user named a category (`agents`, `dev`, `broski`, `youtube`), pass it as the `category` filter.

Present the results as a short list: `ID — 🦸 HERO NAME — description (category)`.
For the single best match, also call `get_skill_graph(id)` and show its `depends_on` so the
user knows which prerequisite skills to load first. Keep it scannable — this vault is built
for ADHD brains.
