# HS-027 — 📋 TEST HERALD — Test Status Report
**Category:** Dev / Testing
**Rescued From:** [HyperAgent-SDK](https://github.com/welshDog/HyperAgent-SDK) — `.Claude/skills/test-status-report/SKILL.md`

> Use when: "test report", "are tests green", "run the suite", or before/after publishing.

---

## ▶️ Run It

```powershell
cd "H:\HyperAgent-SDK"
npm test 2>&1 | Tee-Object -FilePath "$env:TEMP\hyper-test-output.log"
```

---

## 📊 Expected Baseline (v0.3.0)

```
tests/validate.test.js   21/21 ✅
tests/registry.test.js   15/15 ✅
tests/init.test.js        7/7  ✅
tests/client.test.js     14/14 ✅
────────────────────────────────
TOTAL                    57/57 ✅
```

---

## 🏷️ Report Format (BROski badge style)

```
🧪 HyperAgent-SDK Test Report
📅 Run: 2026-MM-DD | ⏱️ Duration: X.XXs | 🏷️ v0.3.0 | 🌿 main

✅ validate.test.js   21/21
✅ registry.test.js   15/15
✅ init.test.js        7/7
✅ client.test.js     14/14
──────────────────────────
🎯 STATUS: ALL GREEN ✅
```

---

## ⚡ Quick One-Shot Badge

```powershell
cd "H:\HyperAgent-SDK"
$out = npm test 2>&1
if ($LASTEXITCODE -eq 0) {
  $count = ($out | Select-String '# tests (\d+)').Matches.Groups[1].Value
  Write-Host "✅ $count/$count GREEN" -ForegroundColor Green
} else {
  Write-Host "❌ Failing — run full report" -ForegroundColor Red
}
```

---

## ❌ Hard Rules

- Never claim green without actually running
- Never trim failures — show all
- Always include version + commit + branch
- If TOTAL drops below 57 → that's a regression

---

## 🔗 Pairs With
- `sdk-publish` — pre-flight gate 3
- `phase-4-graduation` — update baseline when adding `tests/graduate.test.js`
- `token-sync-debug` — when `tests/client.test.js` regresses

*Rescued from HyperAgent-SDK — HYPER-SKILLs Vault by WelshDog 🐕⚡*
