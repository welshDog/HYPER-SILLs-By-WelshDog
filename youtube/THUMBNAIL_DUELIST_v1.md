# HS-132 — 🥊 THUMBNAIL DUELIST — Title + Thumbnail A/B Testing

---
skill_id: HS-132
hero_name: "THUMBNAIL DUELIST"
emoji: "🥊"
version: v1.0.0
status: ACTIVE
category: youtube
depends_on:
  - HS-127  # SIGNAL HUNTER — analytics tell you WHICH videos need new packaging
provides:
  - title-thumbnail-ab-test
  - packaging-variant-generator
  - ctr-decision-framework
related:
  - HS-034  # BEAT ARCHITECT — packaging must match the video's promise
  - HS-036  # ANALOGY ARSENAL — analogies sharpen thumbnail concepts
graph_notes: "Generates competing title+thumbnail variants and a decision rule to pick the winner — the packaging layer that SIGNAL HUNTER's CTR diagnosis feeds into."
---
**Category:** `youtube/`
**Source:** Born-here — YouTube packaging / A-B testing practice
**Version:** v1

---

## 🤔 What It Does

Click-through rate is decided in the first half-second by **packaging** — the
title + thumbnail pair. This skill stops you guessing: it generates 3 distinct
packaging variants per video (different angles, not cosmetic tweaks), predicts
which audience each pulls, and gives a clear rule for declaring a winner once
YouTube's built-in A/B test (Test & Compare) returns data.

---

## 🎯 Purpose

- **Who uses it:** Creators whose impressions are fine but CTR is low.
- **When to use it:** Before publishing, and again whenever SIGNAL HUNTER flags low CTR.
- **What it unlocks:** Variant packaging + a non-emotional pick rule (no "I like B" bias).

---

## 📥 Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `topic` | `string` | ✅ | What the video actually delivers |
| `audience` | `string` | ✅ | Who it's for (e.g. ND devs) |
| `current_ctr` | `string` | ❌ | If re-packaging an existing video |

---

## 📤 Output Format

```
3 variants, each: { angle, title (<=60 chars), thumbnail_concept, who_it_pulls }
+ decision_rule: minimum impressions before calling it + winner threshold
```

---

## 🔮 Prompt Block

```
You are THUMBNAIL DUELIST. Generate competing packaging for one video.

Given topic, audience (and optional current CTR), return EXACTLY 3 variants that
differ by ANGLE, not wording:
  A = curiosity/open-loop   B = result/benefit   C = identity/"this is for you"
For each: title (<=60 chars, no clickbait you can't pay off), a thumbnail concept
(subject + 2-4 words of on-image text + emotion), and who it pulls.

Then give a DECISION RULE:
- Run YouTube Test & Compare with all 3.
- Don't judge before N impressions (suggest a number for this channel size).
- Pick the variant with the highest CTR *only if* it also holds AVD (a high-CTR
  thumbnail that tanks retention is a mismatch — reject it).
Be honest, ND-friendly, short bullets first.
```

---

## 💡 Example Usage

```
topic: "How I run 14 AI agents on one mini PC"
audience: neurodivergent devs + self-hosters
current_ctr: 2.1%
→ A "Open loop", B "Result", C "Identity" variants + 'wait for 1k impressions' rule
```

---

## 🚨 Anti-patterns

- **Don't A/B cosmetic tweaks** — font colour changes teach you nothing; test angles.
- **Don't crown a high-CTR thumbnail that kills retention** — that's a promise you broke.
- **Don't call a winner on 50 impressions** — wait for signal, not noise.

---

## 🔗 Related Skills

- [[HS-127]] SIGNAL HUNTER — diagnoses WHICH videos need re-packaging
- [[HS-034]] BEAT ARCHITECT — packaging must match the video's structure/promise
- [[HS-036]] ANALOGY ARSENAL — sharper thumbnail concepts

---

## 📋 THE PROMPT

> Copy this block into any AI session to activate the skill:

```text
Use skill HS-132 [THUMBNAIL DUELIST]. Generate 3 angle-distinct title+thumbnail variants for my video plus a decision rule for picking the winner from YouTube Test & Compare.
```
