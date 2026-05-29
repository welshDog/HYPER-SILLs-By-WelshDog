# HS-026 — 🎓 GRADUATION GATE — Phase 4 Graduation Flow
**Version:** 1.0

**Category:** Dev / Graduation Pipeline
**Rescued From:** [HyperAgent-SDK](https://github.com/welshDog/HyperAgent-SDK) — `.Claude/skills/phase-4-graduation/SKILL.md`

> Use when: building/debugging the `graduate` CLI command, V2.4 trigger endpoint, badge assignment, portfolio URL, or Discord role/DM.

---

## 🔁 The 8-Step Pipeline

```
Bro runs: hyper-agent graduate 123456789

  1. CLI validates discord_id + reads env vars
  2. CLI builds source_id = "cli_graduate_<discord_id>_<timestamp>"
  3. CLI POSTs to $baseUrl/api/v1/graduate/trigger with X-Sync-Secret
  4. V2.4 verifies secret + checks: already graduated? (409 if yes)
  5. V2.4 awards 500 BROski$ tokens → writes to token_transactions
  6. V2.4 assigns "hyper-graduate" badge → writes to user_badges
  7. V2.4 generates portfolio_url + assigns Discord role + sends DM
  8. CLI prints celebration banner 🎉
```

---

## 🧾 CLI Contract

```javascript
POST ${baseUrl}/api/v1/graduate/trigger
Headers: Content-Type: application/json
         X-Sync-Secret: $env:SHOP_SYNC_SECRET  // ⚠️ Different from COURSE_SYNC_SECRET!
Body: {
  discord_id: "<arg>",
  source_id:  "cli_graduate_<discord_id>_<ts>",
  badge_slug: "hyper-graduate",
  tokens_awarded: 500    // override via --tokens N
}
// Response 200: { badge_slug, tokens_awarded, portfolio_url, discord_role_assigned }
// Response 409: { detail: "already graduated" }
```

---

## ⚡ Run It

```powershell
$env:HYPERCODE_API_URL = "http://localhost:8000"
$env:SHOP_SYNC_SECRET  = "<your-shared-secret>"

node cli/index.js graduate 123456789012345678
node cli/index.js graduate 123456789012345678 --tokens 1000
node cli/index.js graduate 123456789012345678 --json
```

---

## 🐛 Common Failures

| Symptom | Cause | Where to look |
|---|---|---|
| HTTP 401 | `SHOP_SYNC_SECRET` mismatch | env var on both sides |
| HTTP 404 | V2.4 route not registered | `HYPERCODE_API_URL`, V2.4 route table |
| `already graduated` unexpectedly | discord_id already in `user_badges` | V2.4 DB |
| `ECONNREFUSED` | V2.4 not running | `node cli/index.js status` |
| No Discord DM | Bot service down or DMs disabled | Discord bot container logs |

---

## 🧪 Tests To Add

Create `tests/graduate.test.js` covering:
- 200 happy path
- 409 idempotent replay
- 401 secret mismatch
- Network timeout

Update test baseline from 57 → new total.

*Rescued from HyperAgent-SDK — HYPER-SKILLs Vault by WelshDog 🐕⚡*
