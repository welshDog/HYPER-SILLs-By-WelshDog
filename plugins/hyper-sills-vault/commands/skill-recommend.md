---
description: Recommend the best HYPER-SILLs skills for a task you describe
argument-hint: <what you're trying to do>
---

The user wants to: **$ARGUMENTS**

1. Call the `recommend_for_task` MCP tool (from the `hyper-sills` server) with that description.
2. Show the top recommendations as `ID — 🦸 HERO NAME — why it fits`.
3. For the #1 pick, call `get_skill_graph(id)` to surface its prerequisite chain, then offer to
   load the whole bundle in Graph-of-Skills order (prereqs first).

Be encouraging and concrete — name the next single action, not a wall of options.
