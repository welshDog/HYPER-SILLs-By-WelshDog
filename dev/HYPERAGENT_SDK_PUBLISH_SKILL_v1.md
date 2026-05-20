# 📦 Hyper Skill: HYPERAGENT_SDK_PUBLISH_SKILL_v1
**Category:** Dev / SDK Publishing
**Rescued From:** [HyperAgent-SDK](https://github.com/welshDog/HyperAgent-SDK) — `.agents/skills/hyperagent-sdk-publish/SKILL.md`

> Use when: adding new agent interfaces, bumping SDK version, publishing to npm, or syncing SDK changes across the 5-repo ecosystem.

---

## ⚡ Development Flow

1. Make changes in `src/`
2. Run tests:
```powershell
npm test
```
3. Build:
```powershell
npm run build
```
4. Check exports are correct in `dist/`

---

## 🚀 Version Bump + Publish

```powershell
# 1. Bump version
npm version patch   # or minor / major

# 2. Publish (MUST use --access public — scoped package!)
npm publish --access public

# 3. Update dependant repos
# In HyperCode-V2.4 and Hyper-Vibe-Coding-Course:
npm install @welshdog/hyperagent-sdk@latest
```

---

## 📋 Agent Interface Rules

- Every agent **must** implement the base `HyperAgent` interface
- Agents are write-once, deploy-anywhere across the ecosystem
- **Never break existing interface contracts — add, don't remove**

---

## ✅ Success Criteria

- All tests pass before publish
- New version visible on npm
- Dependent repos updated and building without errors

---

## 🔑 Key Env Vars

- `NPM_TOKEN` — for publishing to npm

---

## 🔗 Related Skills
- `dev/SDK_PUBLISH_WORKFLOW_v1.md` (HS-024) — full gated publish flow with safety checks
- `dev/CROSS_REPO_SYNC_v1.md` (HS-023) — syncing contracts across 3 repos after publish

*Rescued from HyperAgent-SDK — HYPER-SKILLs Vault by WelshDog 🐕⚡*
