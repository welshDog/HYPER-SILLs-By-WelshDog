#!/usr/bin/env python3
"""
HS-114 🛠️ BRAIN OPS — Hyper Brain Infrastructure Maintenance CLI
welshDog 🐕 Llanelli, Wales

Hardened v1.1 — Gordon's patches applied:
  - Partial-success handling: every step writes its own status JSON; chain never halts
  - Rate-limit budget file: tracks GitHub API usage across runs
  - Vault Git contract: only commits when there are actual changes (git diff-index --quiet)
  - Full report: reads ALL 4 status files (health, briefing, sync, vault_commit)
  - Windows Task Scheduler wrapper script emitted via 'setup-task' subcommand

v1.2 — load_dotenv() fix:
  - Moved load_dotenv() to BEFORE config block so .env is loaded before os.environ.get() calls

Usage:
    uv run scripts/hyper_brain_ops.py fix-env
    uv run scripts/hyper_brain_ops.py check-health [--restart-if-down] [--output FILE]
    uv run scripts/hyper_brain_ops.py generate-briefing [--output FILE]
    uv run scripts/hyper_brain_ops.py sync-github [--output FILE]
    uv run scripts/hyper_brain_ops.py commit-vault [--output FILE]
    uv run scripts/hyper_brain_ops.py report [--input-dir DIR]
    uv run scripts/hyper_brain_ops.py setup-task [--hour INT] [--minute INT]

Env vars:
    GITHUB_PAT            — GitHub personal access token (required)
    DISCORD_WEBHOOK_URL   — Discord webhook URL (optional; skips Discord if absent)
    VAULT_PATH            — Absolute path to Obsidian vault (required)
    BRIEFING_API_URL      — default: http://localhost:8100
    DOCKER_CONTAINER      — default: hyper-brain
    GITHUB_REPOS          — comma-separated repo list (default: 4 welshDog repos)
    RATE_BUDGET_FILE      — path to rate-limit budget JSON (default: output/rate_limit_budget.json)
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ── Load .env FIRST — before any os.environ.get() calls ──────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed — fall back to real env vars

# ── Config ────────────────────────────────────────────────────────────────────

GITHUB_PAT          = os.environ.get("GITHUB_PAT", "")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
VAULT_PATH          = Path(os.environ.get("VAULT_PATH", "./vault"))
BRIEFING_API_URL    = os.environ.get("BRIEFING_API_URL", "http://localhost:8100")
DOCKER_CONTAINER    = os.environ.get("DOCKER_CONTAINER", "hyper-brain")
GITHUB_REPOS = [
    r.strip()
    for r in os.environ.get(
        "GITHUB_REPOS",
        "welshDog/HyperCode-V2.4,welshDog/HYPER-SILLs-By-WelshDog,welshDog/Hyper-Vibe-Coding-Course,welshDog/WelshDog-Mission-Control",
    ).split(",")
    if r.strip()
]
RATE_BUDGET_FILE = Path(os.environ.get("RATE_BUDGET_FILE", "output/rate_limit_budget.json"))


# ── Helpers ───────────────────────────────────────────────────────────────────

def log(emoji: str, msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {emoji}  {msg}", flush=True)


def write_output(path: str | None, data: dict) -> None:
    if not path:
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    data.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    out.write_text(json.dumps(data, indent=2))
    log("💾", f"Output written → {out}")


def _status_icon(status: str) -> str:
    mapping = {"ok": "✅", "success": "✅", "healthy": "✅", "partial": "⚠️",
               "degraded": "⚠️", "skipped": "⚠️", "failed": "❌", "error": "❌"}
    return mapping.get(status.lower(), "❓")


# ── Rate-limit budget ─────────────────────────────────────────────────────────

def _load_rate_budget() -> dict:
    if RATE_BUDGET_FILE.exists():
        try:
            b = json.loads(RATE_BUDGET_FILE.read_text())
            reset_at = datetime.fromisoformat(b.get("reset_at", "2000-01-01T00:00:00+00:00"))
            if datetime.now(timezone.utc) > reset_at:
                raise ValueError("expired")
            return b
        except Exception:
            pass
    return {
        "github_reads_used": 0,
        "github_reads_budget": 4800,
        "github_writes_used": 0,
        "github_writes_budget": 4800,
        "reset_at": "",
        "window_start": datetime.now(timezone.utc).isoformat(),
    }


def _save_rate_budget(budget: dict) -> None:
    RATE_BUDGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    RATE_BUDGET_FILE.write_text(json.dumps(budget, indent=2))


def _budget_ok(budget: dict, kind: str = "reads") -> bool:
    used = budget.get(f"github_{kind}_used", 0)
    total = budget.get(f"github_{kind}_budget", 4800)
    return used < total


# ── GitHub API helper ─────────────────────────────────────────────────────────

def github_get(endpoint: str, budget: dict) -> dict | list:
    """Authenticated GitHub API GET. Updates budget; raises on 403/429."""
    if not _budget_ok(budget, "reads"):
        raise RuntimeError("GitHub read budget exhausted for this hour — skipping.")
    url = f"https://api.github.com{endpoint}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {GITHUB_PAT}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    time.sleep(1)  # 1 req/sec default
    with urllib.request.urlopen(req, timeout=15) as resp:
        reset_ts = resp.headers.get("X-RateLimit-Reset")
        if reset_ts and not budget.get("reset_at"):
            budget["reset_at"] = datetime.fromtimestamp(int(reset_ts), tz=timezone.utc).isoformat()
        budget["github_reads_used"] = budget.get("github_reads_used", 0) + 1
        return json.loads(resp.read().decode())


# ── Subcommand: check-health ──────────────────────────────────────────────────

def cmd_check_health(restart_if_down: bool, output: str | None) -> dict:
    result = {
        "step": "check-health",
        "container": None, "api": None,
        "status": "unknown", "duration_s": None,
    }
    t0 = time.monotonic()

    try:
        proc = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Status}}", DOCKER_CONTAINER],
            capture_output=True, text=True, timeout=10,
        )
        container_status = proc.stdout.strip()
        result["container"] = container_status
        log("🐳", f"Container '{DOCKER_CONTAINER}': {container_status}")

        if container_status != "running":
            if restart_if_down:
                log("🔄", "Container not running — attempting restart...")
                subprocess.run(["docker", "restart", DOCKER_CONTAINER], timeout=30, check=True)
                result["container"] = "restarted"
                log("✅", "Restarted. Waiting 5s...")
                time.sleep(5)
            else:
                log("❌", "Container down. Pass --restart-if-down to auto-fix.")
    except FileNotFoundError:
        result["container"] = "docker_not_found"
        log("⚠️", "Docker CLI not found — skipping container check.")
    except Exception as e:
        result["container"] = f"error: {e}"
        log("❌", f"Container check failed: {e}")

    try:
        req = urllib.request.Request(f"{BRIEFING_API_URL}/health")
        with urllib.request.urlopen(req, timeout=10) as resp:
            result["api"] = resp.status
            log("🌐", f"API /health → HTTP {resp.status}")
    except urllib.error.URLError as e:
        result["api"] = f"unreachable: {e.reason}"
        log("❌", f"API unreachable: {e.reason}")
    except Exception as e:
        result["api"] = f"error: {e}"
        log("❌", f"API check error: {e}")

    container_ok = result["container"] in ("running", "restarted")
    api_ok = result["api"] == 200
    result["status"] = "healthy" if (container_ok and api_ok) else "degraded"
    result["duration_s"] = round(time.monotonic() - t0, 2)
    log("📊", f"Health: {result['status']} ({result['duration_s']}s)")

    write_output(output, result)
    return result


# ── Subcommand: generate-briefing ─────────────────────────────────────────────

def cmd_generate_briefing(output: str | None) -> dict:
    result = {
        "step": "generate-briefing",
        "status": "unknown", "error": None, "file": None, "duration_s": None,
    }
    t0 = time.monotonic()

    try:
        log("🌅", f"POST {BRIEFING_API_URL}/briefing/generate ...")
        req = urllib.request.Request(
            f"{BRIEFING_API_URL}/briefing/generate",
            data=b"{}",
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode())
            result["status"] = "success"
            result["file"] = body.get("file") or body.get("path")
            log("✅", f"Briefing generated → {result['file']}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode(errors="replace")
        result["status"] = "failed"
        result["error"] = f"HTTP {e.code}: {error_body[:500]}"
        log("❌", f"Briefing API HTTP {e.code} — {error_body[:200]}")
        log("ℹ️", "Pipeline continues — briefing failure is non-fatal.")
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)
        log("❌", f"Briefing exception: {e}")
        log("ℹ️", "Pipeline continues.")

    result["duration_s"] = round(time.monotonic() - t0, 2)
    write_output(output, result)
    return result


# ── Subcommand: sync-github ───────────────────────────────────────────────────

def cmd_sync_github(output: str | None) -> dict:
    inbox = VAULT_PATH / "GitHub-Inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    result = {
        "step": "sync-github",
        "repos": {}, "total_issues_written": 0,
        "errors": [], "status": "ok", "duration_s": None,
    }
    t0 = time.monotonic()
    budget = _load_rate_budget()

    for repo in GITHUB_REPOS:
        log("🔄", f"Syncing {repo} ...")
        try:
            issues = github_get(f"/repos/{repo}/issues?state=open&per_page=50", budget)
            written = 0
            for issue in issues:
                if "pull_request" in issue:
                    continue
                slug = repo.replace("/", "_")
                fname = inbox / f"{slug}__issue_{issue['number']}.md"
                content = (
                    f"# [{repo}] #{issue['number']} — {issue['title']}\n\n"
                    f"**State:** {issue['state']}  \n"
                    f"**URL:** {issue['html_url']}  \n"
                    f"**Created:** {issue['created_at']}  \n\n"
                    f"## Description\n\n{issue.get('body') or '_No description provided._'}\n\n"
                    f"---\n*Synced by HS-114 BRAIN OPS — "
                    f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC*\n"
                )
                fname.write_text(content, encoding="utf-8")
                written += 1
            result["repos"][repo] = {"issues_written": written, "status": "ok"}
            result["total_issues_written"] += written
            log("✅", f"{repo}: {written} issue(s) written.")
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                msg = f"{repo}: GitHub rate limit (HTTP {e.code}) — skipped gracefully."
                result["status"] = "partial"
            else:
                msg = f"{repo}: HTTP {e.code} error."
                result["status"] = "partial"
            result["repos"][repo] = {"status": "error", "error": msg}
            result["errors"].append(msg)
            log("⚠️", msg)
        except RuntimeError as e:
            msg = str(e)
            result["repos"][repo] = {"status": "skipped", "error": msg}
            result["errors"].append(msg)
            result["status"] = "partial"
            log("⚠️", msg)
        except Exception as e:
            msg = f"{repo}: {e}"
            result["repos"][repo] = {"status": "error", "error": msg}
            result["errors"].append(msg)
            result["status"] = "partial"
            log("❌", msg)

    _save_rate_budget(budget)
    log("📥", f"Total written: {result['total_issues_written']} | Budget used: {budget['github_reads_used']}")
    result["duration_s"] = round(time.monotonic() - t0, 2)
    write_output(output, result)
    return result


# ── Subcommand: commit-vault ──────────────────────────────────────────────────

def cmd_commit_vault(output: str | None) -> dict:
    result = {
        "step": "commit-vault",
        "status": "unknown", "committed": False,
        "message": None, "error": None, "duration_s": None,
    }
    t0 = time.monotonic()

    if not VAULT_PATH.exists():
        result["status"] = "skipped"
        result["error"] = f"VAULT_PATH does not exist: {VAULT_PATH}"
        log("⚠️", result["error"])
        write_output(output, result)
        return result

    git_dir = VAULT_PATH / ".git"
    if not git_dir.exists():
        result["status"] = "skipped"
        result["error"] = "Vault is not a Git repository — skipping commit."
        log("⚠️", result["error"])
        write_output(output, result)
        return result

    try:
        subprocess.run(
            ["git", "add", "-A"],
            cwd=VAULT_PATH, capture_output=True, check=True, timeout=30,
        )

        diff_check = subprocess.run(
            ["git", "diff-index", "--quiet", "HEAD", "--"],
            cwd=VAULT_PATH, capture_output=True, timeout=10,
        )

        if diff_check.returncode == 0:
            result["status"] = "skipped"
            result["message"] = "No changes to commit."
            log("ℹ️", "Vault: no changes since last commit — skipping.")
        else:
            commit_msg = f"ops: brain-ops sync {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=VAULT_PATH, capture_output=True, check=True, timeout=30,
            )
            result["status"] = "ok"
            result["committed"] = True
            result["message"] = commit_msg
            log("✅", f"Vault committed: {commit_msg}")

            try:
                subprocess.run(
                    ["git", "push"],
                    cwd=VAULT_PATH, capture_output=True, check=True, timeout=60,
                )
                log("✅", "Vault pushed to remote.")
            except Exception as push_err:
                log("⚠️", f"Push skipped (non-fatal): {push_err}")

    except subprocess.CalledProcessError as e:
        result["status"] = "failed"
        result["error"] = e.stderr.decode(errors="replace")[:300] if e.stderr else str(e)
        log("❌", f"Git command failed: {result['error']}")
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)
        log("❌", f"Vault commit error: {e}")

    result["duration_s"] = round(time.monotonic() - t0, 2)
    write_output(output, result)
    return result


# ── Subcommand: fix-env ────────────────────────────────────────────────────────

def cmd_fix_env() -> None:
    log("🔍", "Running environment diagnostics...\n")
    ok = True

    checks = [
        ("GITHUB_PAT",          bool(GITHUB_PAT),           f"GITHUB_PAT is set ({len(GITHUB_PAT)} chars).",           "Set in .env → GITHUB_PAT=ghp_xxxxxxxx",    True),
        ("DISCORD_WEBHOOK_URL", bool(DISCORD_WEBHOOK_URL),  "DISCORD_WEBHOOK_URL is set.",                              "Set in .env → DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...", False),
        ("VAULT_PATH",          VAULT_PATH.exists(),        f"VAULT_PATH exists: {VAULT_PATH}",                         f"Create it or update VAULT_PATH. Current: {VAULT_PATH}", True),
    ]

    for name, passed, ok_msg, fix_msg, critical in checks:
        if passed:
            log("✅", ok_msg)
        else:
            icon = "❌" if critical else "⚠️"
            log(icon, f"{name} issue detected.")
            print(f"    ➡️  Fix: {fix_msg}")
            if critical:
                ok = False

    try:
        proc = subprocess.run(
            ["docker", "ps", "--filter", f"name={DOCKER_CONTAINER}", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=10,
        )
        if DOCKER_CONTAINER in proc.stdout:
            log("✅", f"Docker container '{DOCKER_CONTAINER}' is running.")
        else:
            log("❌", f"Container '{DOCKER_CONTAINER}' NOT running.")
            print("    ➡️  Fix: docker compose up -d (from your brain project dir)")
            ok = False
    except FileNotFoundError:
        log("⚠️", "Docker CLI not found.")
        print("    ➡️  Fix: Install Docker Desktop (Windows) or docker on your system.")

    try:
        with urllib.request.urlopen(urllib.request.Request(f"{BRIEFING_API_URL}/health"), timeout=5) as resp:
            log("✅", f"API at {BRIEFING_API_URL} reachable (HTTP {resp.status}).")
    except Exception:
        log("❌", f"API at {BRIEFING_API_URL} NOT reachable.")
        print("    ➡️  Fix: Check Docker volume mounts and that port 8100 is exposed.")
        ok = False

    if (VAULT_PATH / ".git").exists():
        log("✅", "Vault is a Git repository.")
    else:
        log("⚠️", "Vault is NOT a Git repo — commit-vault step will be skipped.")
        print("    ➡️  Fix: cd into your vault and run: git init && git add -A && git commit -m 'init'")

    print()
    if ok:
        log("🎉", "All critical checks passed! Brain is ready to run.")
    else:
        log("🛑", "Some critical checks failed — fix above before running the chain.")
        sys.exit(1)


# ── Subcommand: report ────────────────────────────────────────────────────────

def cmd_report(input_dir: str) -> None:
    base = Path(input_dir)
    steps_order = [
        ("health",        "check-health",        "🐳 Health Check"),
        ("briefing",      "generate-briefing",   "🌅 Morning Briefing"),
        ("sync",          "sync-github",         "🔄 GitHub Sync"),
        ("vault_commit",  "commit-vault",        "📚 Vault Commit"),
    ]

    step_results: dict[str, dict] = {}
    for file_key, _, _ in steps_order:
        fp = base / f"{file_key}.json"
        if fp.exists():
            try:
                step_results[file_key] = json.loads(fp.read_text())
            except Exception:
                step_results[file_key] = {"status": "error", "error": "Malformed JSON"}
        else:
            step_results[file_key] = {"status": "no_data"}

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    lines = [
        "🛠️ **BRAIN OPS REPORT**",
        f"🕐 {now_str} UTC",
        "────────────────────────",
    ]

    all_ok = True
    for file_key, _, label in steps_order:
        r = step_results[file_key]
        s = r.get("status", "no_data")
        icon = _status_icon(s)
        duration = f" ({r['duration_s']}s)" if r.get("duration_s") else ""
        lines.append(f"{icon} **{label}**: `{s.upper()}`{duration}")

        if file_key == "health":
            c = r.get("container", "?")
            a = r.get("api", "?")
            lines.append(f"   └ container: `{c}` | api: `{a}`")
        elif file_key == "briefing":
            if r.get("file"):
                lines.append(f"   └ file: `{r['file']}`")
            if r.get("error"):
                lines.append(f"   └ ⚠️ `{str(r['error'])[:100]}`")
        elif file_key == "sync":
            lines.append(f"   └ {r.get('total_issues_written', 0)} issues written to vault")
            for err in r.get("errors", []):
                lines.append(f"   └ ⚠️ {err[:80]}")
        elif file_key == "vault_commit":
            if r.get("message"):
                lines.append(f"   └ `{r['message']}`")
            if r.get("error"):
                lines.append(f"   └ ⚠️ `{str(r['error'])[:80]}`")

        if s not in ("ok", "success", "healthy", "skipped", "no_data"):
            all_ok = False

    overall = "✅ ALL GOOD" if all_ok else "⚠️ CHECK ISSUES ABOVE"
    lines += [
        "────────────────────────",
        f"**Overall: {overall}**",
        "",
        "*HS-114 BRAIN OPS by welshDog 🐕⚡ — [HYPER-SILLs-By-WelshDog](https://github.com/welshDog/HYPER-SILLs-By-WelshDog)*",
    ]

    message = "\n".join(lines)
    log("📣", f"Status report:\n{message}")

    if not DISCORD_WEBHOOK_URL:
        log("⚠️", "DISCORD_WEBHOOK_URL not set — Discord skipped.")
        return

    time.sleep(1)
    payload = json.dumps({"content": message}).encode()
    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            log("✅", f"Discord report delivered! HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        log("⚠️", f"Discord HTTP {e.code} — report not delivered (non-fatal).")
    except Exception as e:
        log("⚠️", f"Discord send failed: {e} — pipeline continues.")


# ── Subcommand: setup-task ────────────────────────────────────────────────────

def cmd_setup_task(hour: int, minute: int) -> None:
    script_path = Path(__file__).resolve()
    bat_path = script_path.parent / "run_brain_ops_daily.bat"

    bat_content = f"""@echo off
REM HS-114 BRAIN OPS — Daily Mode Launcher
REM Generated by setup-task. Each step is independent (no ErrorActionPreference Stop).
REM Add VAULT_PATH, GITHUB_PAT, DISCORD_WEBHOOK_URL to your user env vars before running.

set OUTPUT_DIR=%~dp0..\\output

uv run "{script_path}" check-health --restart-if-down --output "%OUTPUT_DIR%\\health.json"
uv run "{script_path}" generate-briefing --output "%OUTPUT_DIR%\\briefing.json"
uv run "{script_path}" sync-github --output "%OUTPUT_DIR%\\sync.json"
uv run "{script_path}" commit-vault --output "%OUTPUT_DIR%\\vault_commit.json"
uv run "{script_path}" report --input-dir "%OUTPUT_DIR%"

exit /b 0
"""
    bat_path.write_text(bat_content, encoding="utf-8")
    log("✅", f"Launcher written → {bat_path}")

    ps_cmd = (
        f'$action = New-ScheduledTaskAction -Execute "{bat_path}"; '
        f'$trigger = New-ScheduledTaskTrigger -Daily -At {hour:02d}:{minute:02d}; '
        f'Register-ScheduledTask -TaskName "HyperBrainOpsDaily" -Action $action '
        f'-Trigger $trigger -RunLevel Highest -Force'
    )
    print("\n── Windows Task Scheduler Registration ──────────────────────────────")
    print("Run this in PowerShell (Admin) to register the daily task:\n")
    print(ps_cmd)
    print("\n────────────────────────────────────────────────────────────────────\n")
    log("ℹ️", f"Task will fire daily at {hour:02d}:{minute:02d}. Adjust -At if needed.")


# ── CLI entry point ───────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="hyper_brain_ops",
        description="🛠️ HS-114 BRAIN OPS — Hyper Brain Infrastructure Maintenance (v1.2)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_health = sub.add_parser("check-health", help="Ping Docker + API health endpoint")
    p_health.add_argument("--restart-if-down", action="store_true")
    p_health.add_argument("--output", default="output/health.json")

    p_brief = sub.add_parser("generate-briefing", help="Trigger morning briefing generation")
    p_brief.add_argument("--output", default="output/briefing.json")

    p_sync = sub.add_parser("sync-github", help="Sync open GitHub issues to vault GitHub-Inbox")
    p_sync.add_argument("--output", default="output/sync.json")

    p_commit = sub.add_parser("commit-vault", help="Git-commit vault changes (only if diff exists)")
    p_commit.add_argument("--output", default="output/vault_commit.json")

    sub.add_parser("fix-env", help="Diagnose env vars, vault path, Docker, port, and git")

    p_report = sub.add_parser("report", help="Send full BROski status report to Discord")
    p_report.add_argument("--input-dir", default="output")

    p_task = sub.add_parser("setup-task", help="Generate Windows Task Scheduler .bat + PS command")
    p_task.add_argument("--hour", type=int, default=7, help="Hour to trigger (24h, default: 7)")
    p_task.add_argument("--minute", type=int, default=0, help="Minute to trigger (default: 0)")

    p_search = sub.add_parser("skill-search", help="Semantic search the HYPER-SILLs vault")
    p_search.add_argument("query", nargs="+", help="What you're trying to do")
    p_search.add_argument("--limit", type=int, default=5)

    p_usage = sub.add_parser("analyze-skill-usage", help="Summarise .skill-memory usage + suggest improvements")

    p_prog = sub.add_parser("skill-progress", help="Dopamine progress tracker (achievements + streak)")

    args = parser.parse_args()

    if args.command == "check-health":
        cmd_check_health(restart_if_down=args.restart_if_down, output=args.output)
    elif args.command == "generate-briefing":
        cmd_generate_briefing(output=args.output)
    elif args.command == "sync-github":
        cmd_sync_github(output=args.output)
    elif args.command == "commit-vault":
        cmd_commit_vault(output=args.output)
    elif args.command == "fix-env":
        cmd_fix_env()
    elif args.command == "report":
        cmd_report(input_dir=args.input_dir)
    elif args.command == "setup-task":
        cmd_setup_task(hour=args.hour, minute=args.minute)
    elif args.command == "skill-search":
        cmd_skill_search(query=" ".join(args.query), limit=args.limit)
    elif args.command == "analyze-skill-usage":
        cmd_analyze_skill_usage()
    elif args.command == "skill-progress":
        cmd_skill_progress()


def cmd_skill_search(query: str, limit: int) -> None:
    """Semantic search over the vault (delegates to search_skills.py)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from search_skills import semantic_search
    except Exception as e:  # noqa: BLE001
        print(f"skill-search unavailable: {e}")
        return
    hits = semantic_search(query, limit=limit)
    if not hits:
        print(f"No stress — nothing matched '{query}'. Try different words.")
        return
    print(f"\nTop {len(hits)} for: {query}\n")
    for h in hits:
        print(f"  {h['id']}  {h['hero_name']}  (score {h['score']}, {h['category']})")
        print(f"      {h['description']}")
    print()


def cmd_analyze_skill_usage() -> None:
    """Read .skill-memory usage + suggest dependency/pack improvements."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from skill_memory import analyze
    except Exception as e:  # noqa: BLE001
        print(f"analyze-skill-usage unavailable: {e}")
        return
    report = analyze()
    print(report)


def cmd_skill_progress() -> None:
    """Dopamine progress tracker (delegates to progress_tracker.py)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from progress_tracker import compute, render, _write_snapshot
    except Exception as e:  # noqa: BLE001
        print(f"skill-progress unavailable: {e}")
        return
    s = compute()
    _write_snapshot(s)
    print(render(s))


if __name__ == "__main__":
    main()
