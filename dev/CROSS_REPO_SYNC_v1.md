# HS-023 — 🔗 REPO BRIDGE — Cross-Repo Sync
**Category:** Dev / Cross-Repo Contracts
**Rescued From:** [HyperAgent-SDK](https://github.com/welshDog/HyperAgent-SDK) — `.Claude/skills/cross-repo-sync/SKILL.md`

> Use when: changing manifest schema, adding/changing fields, modifying the Course→V2.4 token sync payload, the graduate API shape, or whenever "the three repos drifted".

---

## 📋 The Three Contracts

| Contract | Canonical (SDK) | Mirrored in V2.4 | Mirrored in Course |
|---|---|---|---|
| Agent manifest schema | `hyper-agent-spec.json` | Validator / agent registry | Agent submission UI |
| `awardFromCourse` payload | `cli/client.js` | `POST /api/v1/economy/award-from-course` | Edge function |
| `graduate` payload | `cli/commands/graduate.js` | `POST /api/v1/graduate/trigger` | Graduation trigger |

---

## ⚡ SDK Changes First — Then Mirror

1. Land change in SDK (with bumped tests + types)
2. Open both sister repos
3. Mirror in V2.4 (server side)
4. Mirror in Course (consumer side)
5. End-to-end test the round trip
6. Bump SDK version + ship via `sdk-publish` skill

---

## 🔍 Drift Detection (quick audit)

```powershell
# 1. Read SDK source of truth
cd "H:\HyperAgent-SDK"
Get-Content hyper-agent-spec.json | Select-String '"required"|"port"|"mcp_compatible"'

# 2. Find V2.4 mirror
cd "H:\HyperStation zone\HyperCode\HyperCode-V2.4"

# 3. Find Course mirror
cd "H:\the hyper vibe coding hub"
```

---

## 📏 Versioning Discipline

- **Additive** (new optional field) → MINOR bump
- **Breaking** (removed field / type change) → MAJOR bump + migration notes in `AGENT_SYNC_NOTES.md`
- Update all three repos in the same week — don't let drift compound

---

## 🧪 Round-Trip Test (awardFromCourse)

```powershell
$env:HYPERCODE_API_URL  = "http://localhost:8000"
$env:COURSE_SYNC_SECRET = "<the-shared-secret>"
node -e "require('H:/HyperAgent-SDK/cli/client').awardFromCourse({sourceId:'test_'+Date.now(),discordId:'123456789012345678',tokens:1,reason:'sync test'}).then(r=>console.log('OK',r))"
# Expected: OK { source_id, awarded: 1, coins_balance, xp_balance, level }
```

*Rescued from HyperAgent-SDK — HYPER-SKILLs Vault by WelshDog 🐕⚡*
