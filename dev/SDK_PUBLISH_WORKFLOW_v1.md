# HS-024 — 🚀 PUBLISH RITE — SDK Publish Workflow
**Version:** 1.0

**Category:** Dev / Publishing
**npm package:** `@w3lshdog/hyper-agent`
**Rescued From:** [HyperAgent-SDK](https://github.com/welshDog/HyperAgent-SDK) — `.Claude/skills/sdk-publish/SKILL.md`

> Full gated workflow for shipping `@w3lshdog/hyper-agent` to npm. **REFUSES if any safety gate fails.**

---

## 🚦 Pre-Flight Gates (ALL must pass)

```powershell
cd "H:\HyperAgent-SDK"
git status --porcelain          # 1. Clean working tree → empty output ✅
git rev-parse --abbrev-ref HEAD # 2. Must be on main ✅
npm test                        # 3. 57/57 green ✅
npm whoami                      # 4. Must be welshdog ✅
npm run test:templates          # 5. All templates valid ✅
```

---

## 📦 Bump Guide

| Change | Bump | Example |
|---|---|---|
| Bug fix only | `patch` | 0.3.0 → 0.3.1 |
| New feature, backward compat | `minor` | 0.3.1 → 0.4.0 |
| Breaking API change | `major` | 0.x.y → 1.0.0 |

---

## ⚡ The Ship Sequence

```powershell
cd "H:\HyperAgent-SDK"
git add -A
git commit -m "feat: <one-line summary>"
npm version minor             # or patch / major
git push --follow-tags
npm publish --access public   # MUST have --access public for scoped package

# Smoke test
npx @w3lshdog/hyper-agent@latest --version
```

---

## 🔧 Post-Ship Checklist

- [ ] Update `CLAUDE_CONTEXT.md` version table
- [ ] Update `hypercode-sdk` SKILL.md "Current State" snapshot
- [ ] If `hyper-agent-spec.json` changed → run `cross-repo-sync` skill
- [ ] Confirm `types/index.d.ts` reflects new API surface

---

## ❌ Hard Rules

- NEVER `--no-verify`
- NEVER amend a published commit
- NEVER force-push to main
- NEVER skip `--access public`
- NEVER bump major without asking Bro
- NEVER publish if `npm test` is red

*Rescued from HyperAgent-SDK — HYPER-SKILLs Vault by WelshDog 🐕⚡*
