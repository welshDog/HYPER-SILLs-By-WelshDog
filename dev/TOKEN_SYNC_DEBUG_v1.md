# HS-025 — 🪙 COIN MENDER — Token Sync Debug
**Category:** Dev / Debugging
**Rescued From:** [HyperAgent-SDK](https://github.com/welshDog/HyperAgent-SDK) — `.Claude/skills/token-sync-debug/SKILL.md`

> Use when: `awardFromCourse` failing, 401 from V2.4, token sync broken, course not awarding tokens, duplicate replay, or any `AwardFromCourseError`.

---

## 🌳 Error Code Decision Tree

| `code` | Meaning | Fix |
|---|---|---|
| `BROWSER_FORBIDDEN` | Called from browser bundle | Move to server-side only |
| `MISSING_SECRET` | `COURSE_SYNC_SECRET` not set | Set env var on both sides |
| `INVALID_SOURCE_ID` etc | Validation failure | Check field limits below |
| `NO_FETCH` | Node < 18 | Upgrade Node or pass custom fetch |
| `TIMEOUT` | Request > 5000ms | Check if V2.4 is up, bump `timeoutMs` |
| `NETWORK` | Fetch threw before response | Check `baseUrl`, check V2.4 running |
| `BAD_STATUS` 401 | Secret mismatch | See §7 checklist |
| `BAD_STATUS` 4xx/5xx | Other server error | See §8 table |
| Returns `{ duplicate: true }` | 409 idempotent replay — **NOT an error** ✅ | Expected — treat as success |

---

## 📏 Field Limits

| Field | Constraint |
|---|---|
| `sourceId` | non-empty string, ≤128 chars |
| `discordId` | non-empty string, ≤32 chars |
| `tokens` | integer, 1..10000 |
| `reason` | optional string, ≤255 chars |

---

## 🔑 §7 — 401 Secret Mismatch Checklist

1. Is `COURSE_SYNC_SECRET` set in calling env?
2. Does it match V2.4's value **exactly**? (whitespace + trailing newline matters)
3. Did V2.4's secret recently rotate?
4. Is any proxy stripping custom headers?
5. Are you hitting the right environment (local vs staging)?

```powershell
# Verify round-trip
$secret = $env:COURSE_SYNC_SECRET
curl -X POST "$env:HYPERCODE_API_URL/api/v1/economy/award-from-course" `
  -H "Content-Type: application/json" `
  -H "X-Sync-Secret: $secret" `
  -d '{"source_id":"debug_test","discord_id":"123456789012345678","tokens":1,"reason":"debug"}'
```

---

## 🧪 Run Tests to Verify Helper

```powershell
cd "H:\HyperAgent-SDK"
node --test tests/client.test.js  # → expect 14 pass
```

If tests pass → helper is fine, issue is environmental.
If tests fail → fix `cli/client.js`, then ship via `sdk-publish`.

*Rescued from HyperAgent-SDK — HYPER-SKILLs Vault by WelshDog 🐕⚡*
