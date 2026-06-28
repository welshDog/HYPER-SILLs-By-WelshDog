# HS-133 — ✂️ SHORTS ALCHEMIST — Long-Form → Shorts Repurposing Engine

---
skill_id: HS-133
hero_name: "SHORTS ALCHEMIST"
emoji: "✂️"
version: v1.0.0
status: ACTIVE
category: youtube
depends_on:
  - none  # standalone repurposing skill
provides:
  - shorts-clip-extraction
  - vertical-hook-rewrite
  - long-form-to-shorts-pipeline
related:
  - HS-127  # SIGNAL HUNTER — retention peaks mark the best clip candidates
  - HS-132  # THUMBNAIL DUELIST — Shorts still need a strong opening frame
graph_notes: "Mines a long-form video for self-contained 15-45s moments and rewrites each as a native vertical Short with its own hook — turning one upload into a week of top-of-funnel."
---
**Category:** `youtube/`
**Source:** Born-here — Shorts repurposing / multi-format distribution
**Version:** v1

---

## 🤔 What It Does

One long-form video is a quarry, not a single brick. This skill scans a transcript
(or chapter list) for **self-contained moments** — a payoff, a hot take, a
surprising stat — and rewrites each as a native **vertical Short** with its own
0-2s hook, on-screen text beats, and a loop-back ending. Shorts are top-of-funnel;
this turns one upload into a week of discovery surface.

---

## 🎯 Purpose

- **Who uses it:** Creators sitting on long-form back-catalogue with no Shorts pipeline.
- **When to use it:** Right after publishing long-form (or to revive old bangers).
- **What it unlocks:** 5-8 Shorts per long-form, each standalone, each pointing home.

---

## 📥 Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `transcript` | `string` | ✅ | Transcript or timestamped chapter list |
| `count` | `int` | ❌ | How many Shorts to extract (default 5) |
| `retention_peaks` | `string` | ❌ | Timestamps that held attention (from SIGNAL HUNTER) |

---

## 📤 Output Format

```
N clips, each: { source_timestamps, hook (0-2s), on_screen_text_beats[], spoken_line, loop_ending, suggested_caption }
```

---

## 🔮 Prompt Block

```
You are SHORTS ALCHEMIST. Mine a long-form transcript for vertical Shorts.

Rules:
1. Pick only SELF-CONTAINED moments — a viewer with zero context must get value in
   <45s. No "as I said earlier".
2. If retention_peaks are given, prioritise those timestamps (the audience already
   voted with their attention).
3. For each clip return: source timestamps, a 0-2s HOOK (curiosity or result),
   3-5 on-screen text beats, the core spoken line(s), a LOOP ending that nudges a
   rewatch or "full video in description", and a caption with 2-3 plain hashtags.
4. Vertical-first: assume 9:16, fast cuts, text-readable-on-mute.
Short bullets, ND-friendly, no fluff.
```

---

## 💡 Example Usage

```
transcript: <8-min "14 agents on one mini PC" transcript>
count: 6
retention_peaks: "1:12, 3:40, 5:05"
→ 6 standalone Shorts, each with its own hook + loop-back ending
```

---

## 🚨 Anti-patterns

- **Don't clip mid-thought** — if it needs the long video to make sense, skip it.
- **Don't reuse the long-form hook** — vertical needs its own 0-2s opener.
- **Don't bury the payoff** — Shorts front-load value, then loop.

---

## 🔗 Related Skills

- [[HS-127]] SIGNAL HUNTER — retention peaks = best clip candidates
- [[HS-132]] THUMBNAIL DUELIST — Shorts still need a strong opening frame
- [[HS-034]] BEAT ARCHITECT — beat structure helps spot self-contained moments

---

## 📋 THE PROMPT

> Copy this block into any AI session to activate the skill:

```text
Use skill HS-133 [SHORTS ALCHEMIST]. Mine my long-form transcript for N self-contained vertical Shorts, each with its own 0-2s hook, on-screen text beats, and a loop-back ending.
```
