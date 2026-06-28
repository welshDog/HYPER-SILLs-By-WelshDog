# HS-134 — 🔁 SIGNAL-TO-SCRIPT LOOP — Analytics → Next Video Script

---
skill_id: HS-134
hero_name: "SIGNAL-TO-SCRIPT LOOP"
emoji: "🔁"
version: v1.0.0
status: ACTIVE
category: youtube
depends_on:
  - HS-127  # SIGNAL HUNTER — consumes its diagnosis as the loop's input
provides:
  - analytics-to-script-pipeline
  - data-driven-hook-writing
  - content-feedback-loop
related:
  - HS-133  # SHORTS ALCHEMIST — the new script can be Shorts-first
  - HS-132  # THUMBNAIL DUELIST — script and packaging are designed together
graph_notes: "Closes the creator feedback loop: takes SIGNAL HUNTER's diagnosis of the last video and outputs the next video's title, hook, and beat outline — so every upload teaches the next."
---
**Category:** `youtube/`
**Source:** Born-here — data-driven content loop
**Version:** v1

---

## 🤔 What It Does

Most creators analyse a video, nod, and forget. This skill **closes the loop**: it
takes the diagnosis from SIGNAL HUNTER (what worked, where retention dipped, packaging
match) and turns it into the *next* video's blueprint — a title, a result-first hook,
and a beat-by-beat outline that fixes last video's weak spots while doubling down on
what held attention. Every upload becomes training data for the next.

---

## 🎯 Purpose

- **Who uses it:** Creators who want compounding improvement, not random uploads.
- **When to use it:** Immediately after a SIGNAL HUNTER debug, while signal is fresh.
- **What it unlocks:** A self-improving content cadence — data in, script out.

---

## 📥 Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `diagnosis` | `string` | ✅ | SIGNAL HUNTER output (or your own metrics summary) |
| `next_topic` | `string` | ❌ | Topic for the next video (else suggest one) |
| `format` | `string` | ❌ | long-form / Shorts-first (default long-form) |

---

## 📤 Output Format

```
{ next_title, hook_10s, beat_outline[] (with pattern-interrupt markers), packaging_brief, what_to_repeat, what_to_fix }
```

---

## 🔮 Prompt Block

```
You are SIGNAL-TO-SCRIPT LOOP. Turn last video's analytics into next video's script.

Input: a diagnosis (retention dips, CTR status, packaging match, what worked).
Output the NEXT video's blueprint:
1. WHAT TO REPEAT — name the moments that held attention; bake them in again.
2. WHAT TO FIX — each retention dip → a concrete structural change (earlier payoff,
   pattern interrupt, cut the slow intro, etc.).
3. NEXT TITLE + 10s HOOK — result-first, ND-friendly, matches what the video delivers.
4. BEAT OUTLINE — 5-8 beats with a pattern-interrupt marker every ~90s.
5. PACKAGING BRIEF — one-line title+thumbnail direction (hand to THUMBNAIL DUELIST).
If format is Shorts-first, structure beats for 9:16 and front-load the payoff.
Short bullets, honest, celebrate the wins too.
```

---

## 💡 Example Usage

```
diagnosis: <SIGNAL HUNTER output: CTR ok, big dip at 0:45 slow intro, strong at 3:10 demo>
next_topic: "self-hosting the agent stack"
→ next title + hook + 6-beat outline that kills the slow intro and leads with a demo
```

---

## 🚨 Anti-patterns

- **Don't ignore what worked** — fixing dips while dropping your strengths is a net loss.
- **Don't write the script before the packaging** — design title/hook/thumbnail together.
- **Don't loop on noise** — if the last video had <500 views, gather more signal first.

---

## 🔗 Related Skills

- [[HS-127]] SIGNAL HUNTER — produces the diagnosis this consumes
- [[HS-132]] THUMBNAIL DUELIST — receives the packaging brief
- [[HS-133]] SHORTS ALCHEMIST — the next script can be Shorts-first

---

## 📋 THE PROMPT

> Copy this block into any AI session to activate the skill:

```text
Use skill HS-134 [SIGNAL-TO-SCRIPT LOOP]. Take my last video's SIGNAL HUNTER diagnosis and output the next video's title, 10s hook, and beat outline — repeating what worked and fixing each retention dip.
```
