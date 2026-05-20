# 🔒 Hyper Skill: OBSIDIAN_GIT_VAULT_v1
**Category:** Dev / Infrastructure  
**Version:** 1.0  
**Rescued From:** [BROski-Obsidian-Brain](https://github.com/welshDog/BROski-Obsidian-Brain-for-HyperFocus-z0ne) — `.claude/skills/obsidian-git-vault/SKILL.md`

> Level 10 — Vault Immortal. Trigger when: "vault not committing", "git conflict in vault", "lost a note", "Obsidian Git", "auto-commit", "vault sync".

---

## ⚙️ How It Works

```
Every 10 mins:
git add -A  →  git commit -m "vault: auto-commit <timestamp>"  →  git push
```

Push fail = logs to Obsidian notice tray but doesn't block — local commits still happen.

---

## ✅ Verify It's Running

In Obsidian: `Cmd+P → "Obsidian Git: Show status"` — should show recent auto-commits.

---

## 📋 Canonical Plugin Config

```json
{
  "autoCommitInterval": 10,
  "autoPushInterval": 10,
  "autoPullInterval": 0,
  "commitMessage": "vault: auto-commit {{date}}",
  "pullBeforePush": true
}
```

---

## 💾 Recovering A Lost Note

```powershell
cd H:\BROski-Obsidian-Brain-for-HyperFocus-z0ne

# Find when a file existed
git log --all --follow -- "HYPERFOCUS_ZONE/01-Projects/<file>.md"

# Show contents at a specific commit
git show <commit>:HYPERFOCUS_ZONE/01-Projects/<file>.md

# Restore file
git checkout <commit> -- HYPERFOCUS_ZONE/01-Projects/<file>.md

# Find any deleted file ever
git log --all --diff-filter=D --summary | Select-String "<filename>"
```

---

## 🖥️ Multi-Machine Rule

**ALWAYS pull first when switching machines.**
```
Machine A finishes → auto-push
Machine B starts → MANUAL PULL FIRST → work → auto-push
```

---

## 🚑 Common Failures

| Symptom | Fix |
|---|---|
| Vault not committed in hours | Open Obsidian, check plugin status |
| Push fails: "non-fast-forward" | Manual pull first |
| Conflict markers in a note | Resolve in VS Code/terminal, commit |
| "Not a git repository" | `git init` at repo root, push to remote |

---

## ⚠️ Hard Rules

- Pull before working on a 2nd machine — every time
- Don't disable auto-commit — vault immortality depends on it
- Don't commit `.env` files
- Resolve conflicts in VS Code/terminal, NOT Obsidian editor
- `.obsidian/` IS committed — plugins/hotkeys travel with vault
- Push to remote — local-only = one disk failure away from gone

*Rescued from BROski-Obsidian-Brain-for-HyperFocus-z0ne — HYPER-SKILLs Vault by WelshDog 🐕⚡*
