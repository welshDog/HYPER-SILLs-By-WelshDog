# HS-069 — 💚 MERCY MESSAGE — ND-First Error Messages Template


---
skill_id: HS-069
hero_name: "MERCY MESSAGE"
emoji: "💚"
version: v1.0
category: broski
depends_on:
  - HS-002  # SIX_LAWS_OF_AGENTS — Law 3 (EXPLAIN SIMPLY) drives ND-first messaging
provides:
  - nd-first-error-template
  - empathy-first-pattern
  - recovery-cue-language
related:
  - HS-036  # ANALOGY ARSENAL — analogies soften the error explanation
  - HS-010  # THE AESTHETE — error message tone aligns with design voice
graph_notes: "Non-judgmental error message template for ADHD/ND users — empathy first, then diagnosis, then next step."
---
**Category:** `broski/`  
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §1 Principle 3  
**Version:** v1  

---

## 🤔 What It Does

Replaces cold, confusing error messages with clear, kind, neurodivergent-friendly ones. Follows the **What / Why / How** format. Every error tells the user exactly what happened, why, and how to fix it. Designed for ADHD + dyslexia — no jargon, no wall of text.

---

## ❌ vs ✅ Examples

```
❌ BAD:
"SyntaxError: unexpected token at line 42"

✅ GOOD:
⚠️ Syntax Error on Line 42

What happened: Missing closing bracket
Why: The function on line 38 has an opening '{' but no closing '}'
How to fix: Add '}' at the end of line 41

Need help? Ask BROski: 'Explain this error'
```

---

## 🏗️ The Template

```
⚠️ {Error Type} {Location if applicable}

What happened: {Plain language description}
Why: {Root cause in simple terms}
How to fix: {Actionable steps}

{Optional: Example of correct usage}

Need help? {Where to get help}
```

---

## 🐍 Python Implementation

```python
def create_friendly_error(
    error_type: str,
    location: str = None,
    what: str = "",
    why: str = "",
    how_to_fix: str = "",
    example: str = None
) -> str:
    message = f"⚠️ {error_type}"
    if location:
        message += f" in {location}"
    message += "\n\n"
    if what:
        message += f"What happened: {what}\n"
    if why:
        message += f"Why: {why}\n"
    if how_to_fix:
        message += f"How to fix: {how_to_fix}\n"
    if example:
        message += f"\nExample:\n{example}\n"
    message += "\nNeed help? Ask BROski: 'Explain this error'"
    return message
```

---

## 🎯 THE PROMPT

```
Convert this error message to ND-friendly format:

[PASTE RAW ERROR HERE]

Output format:
⚠️ [Error Type] on [Location]

What happened: [plain English]
Why: [simple root cause]
How to fix: [exact steps]

Need help? Ask BROski: 'Explain this error'
```

---

## ✅ ND-Friendly UI Requirements

- Clear structure — headings, bullets, short paragraphs
- Visual hierarchy — size + color guide attention
- Progress indicators — always show "where am I?"
- Plain language — no jargon unless defined
- Low cognitive load — one task at a time
- Focus preservation — minimise interruptions

---

## 🔗 Related Skills
- HS-071 Fail Gracefully + Fallback Chain
- HS-075 Agent Decision Framework Matrix
