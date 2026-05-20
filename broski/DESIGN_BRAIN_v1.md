# 🎨 Hyper Skill: DESIGN_BRAIN_v1
**Category:** Broski / Design  
**Version:** 1.0  
**Rescued From:** [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) — `.claude/skills/design-brain/SKILL.md`

> Trigger when: building/redesigning UI, reviewing frontend code, creating animations, "make this slick", "premium this up", "too basic", "more hacker vibe".

---

## 🎛️ Three Design Dials

Set at start of every task. Defaults shown.

```
VARIANCE  [1–5]  How far from safe default layout    Default: 3
MOTION    [1–5]  Animation intensity + cinematic feel Default: 2
DENSITY   [1–5]  Packed UI (1=airy, 5=packed)        Default: 2
```

| Surface | Variance | Motion | Density |
|---|---|---|---|
| Landing page / hero | 4 | 3 | 1 |
| BROski$ dNFT UI | 5 | 4 | 2 |
| Token economy dashboard | 3 | 2 | 3 |
| Course lesson page | 2 | 1 | 3 |
| Agent Mission Control | 3 | 2 | 4 |
| Internal admin tool | 1 | 1 | 4 |

---

## 🎨 HyperCode Base Palette

```
Background:  #0a0a0a  (OLED black)
Surface:     #111111  (cards, panels)
Surface+1:   #1a1a1a  (elevated, modals)
Border:      rgba(255,255,255,0.06)
Text:        #e8e8e8
Text muted:  #888888
Accent:      #7c3aed  (BROski purple)
Accent warm: #f59e0b  (BROski gold — wins)
Accent neon: #22d3ee  (cyan — live stats)
Success:     #10b981
Danger:      #ef4444
```

**Typography:** Headings = `font-mono` NEVER Inter alone. Body = `font-sans`. Data = `font-mono`.

**Motion:** 150ms micro | 300ms transitions | 500ms entrances. Easing: `cubic-bezier(0.16, 1, 0.3, 1)`. Hardware-accel ONLY: `transform`, `opacity`.

---

## 🚫 Anti-Slop Blacklist (BANNED patterns)

- ❌ 3-column marketing grid (icon + heading + paragraph)
- ❌ Hero gradient blob + centered text + 2 CTAs
- ❌ Purple-to-blue gradient on CTAs ("AI purple")
- ❌ `transition-all` (layout thrashing)
- ❌ Hover scale >1.05 on cards
- ❌ Generic Shadcn/Radix zero customisation
- ❌ `rounded-full` on every button/badge
- ❌ Emoji in headings (🚀 Your Journey Starts Here)
- ❌ Entrance spam (fade-in on literally everything)

---

## 🔧 Two Modes

**BUILD MODE** — New UI from scratch  
→ Layer 1 (taste) + Layer 2 (Emil micro-interactions)  
→ Output: React/Tailwind code + design rationale

**AUDIT MODE** — Reviewing/improving existing UI  
→ Layer 1 (taste) + Layer 3 (Impeccable audit)  
→ Output: score /10 + critical fixes + polish wins

---

## 🧠 ND Design Principles (always baked in)

- Scannable hierarchy — clear F/Z reading pattern
- One primary action per screen
- Progress always visible (loading states, step indicators)
- Error messages are human (never "Error 422")
- Reward moments — wins deserve micro-celebration
- Never hide info behind hover on mobile

---

## 📦 Output Format

### Build Mode
```
## 🎛️ Design Settings
[Variance X | Motion Y | Density Z — why]

## 🎨 Design Decisions
[3-5 bullets: choices + why]

## ⚡ Code
[Full component, ready to paste]

## 🔮 Next Level
[1-2 optional enhancements]
```

### Audit Mode
```
## 🔍 Audit Score: [X/10]
## 🚨 Critical Fixes [≤3]
## ⚠️ Polish Wins [≤4]
## ✅ What's Working
## 🔮 Elevation Moves [only if score ≥ 7]
```

---

*Rescued from BROski-Obsidian-Brain-for-HyperFocus-z0ne — HYPER-SKILLs Vault by WelshDog 🐕⚡*
