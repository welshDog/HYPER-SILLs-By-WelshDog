#!/usr/bin/env python3
"""HS-114 BRAIN OPS — Hyper Brain Infrastructure Manager
Version: 2.0.0 (Gordon-hardened: partial-success, rate budget, vault-git contract)
Usage: uv run scripts/hyper_brain_ops.py <subcommand> [options]
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

# ---------------------------------------------------------------------------
# Config — loaded from environment variables
# ---------------------------------------------------------------------------

VAULT_PATH = Path(os.environ.get("VAULT_PATH", ""))
GITHUB_PAT = os.environ.get("GITHUB_PAT", "")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
BRIEFING_API_URL = os.environ.get("BRIEFING_API_URL", "http://localhost:8100")
DOCKER_CONTAINER = os.environ.get("DOCKER_CONTAINER", "hyper-brain")
GITHUB_REPOS = [
    r.strip()
    for r in os.environ.get(
        "GITHUB_REPOS",
        "welshDog/HYPER-SILLs-By-WelshDog,welshDog/HyperFocusZone,welshDog/BROski,welshDog/HyperCodeAI",
    ).split(",")
    if r.strip()
]

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_FILE = OUTPUT_DIR / "ops.log"
RATE_BUDGET_FILE = OUTPUT_DIR / "rate_budget.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] {msg}"
    print(line)
    with LOG_FILE.open("a") as f:
        f.write(line + "\n")


def write_status(output_path: str | None, status: dict) -> None:
    if output_path:
        Path(output_path).write_text(json.dumps(status, indent=2))
        log(f"Status written → {output_path}")


def load_rate_budget() -> dict:
    if RATE_BUDGET_FILE.exists():
        try:
            data = json.loads(RATE_BUDGET_FILE.read_text())
            reset_at = datetime.fromisoformat(data.get("reset_at", ""))
            if datetime.now(timezone.utc) < reset_at:
                return data
        except Exception:
            pass
    # Fresh budget (GitHub authenticated = 5000 req/hr)
    from datetime import timedelta
    reset_at = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    budget = {"github_reads_used": 0, "github_reads_budget": 5000, "reset_at": reset_at}
    RATE_BUDGET_FILE.write_text(json.dumps(budget, indent=2))
    return budget


def save_rate_budget(budget: dict) -> None:
    RATE_BUDGET_FILE.write_text(json.dumps(budget, indent=2))


def github_get(url: str) -> dict | None:
    """Single GitHub API GET with rate limiting and budget tracking."""
    budget = load_rate_budget()
    if budget["github_reads_used"] >= budget["github_reads_budget"]:
        log("⚠️  GitHub rate budget exhausted — skipping request")
        return None
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_PAT:
        headers["Authorization"] = f"Bearer {GITHUB_PAT}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            budget["github_reads_used"] += 1
            save_rate_budget(budget)
            time.sleep(1)  # 1 req/sec
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code in (403, 429):
            log(f"⚠️  GitHub rate limit hit ({e.code}) — skipping")
        else:
            log(f"❌  GitHub HTTP error {e.code} for {url}")
        return None
    except Exception as ex:
        log(f"❌  GitHub request failed: {ex}")
        return None


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_fix_env(args) -> dict:
    """Diagnose environment: vault path, Docker, port, tokens."""
    log("🔍 Running environment doctor...")
    checks = {}
    start = time.time()

    # Vault path
    if VAULT_PATH and VAULT_PATH.exists():
        checks["vault_path"] = {"ok": True, "detail": str(VAULT_PATH)}
        log(f"✅ Vault path exists: {VAULT_PATH}")
    else:
        checks["vault_path"] = {"ok": False, "detail": f"Not found: {VAULT_PATH}"}
        log(f"❌ Vault path NOT found: {VAULT_PATH}")

    # GitHub PAT
    if GITHUB_PAT:
        checks["github_pat"] = {"ok": True, "detail": "Set"}
        log("✅ GITHUB_PAT is set")
    else:
        checks["github_pat"] = {"ok": False, "detail": "GITHUB_PAT not set"}
        log("❌ GITHUB_PAT not set")

    # Discord webhook
    if DISCORD_WEBHOOK_URL:
        checks["discord_webhook"] = {"ok": True, "detail": "Set"}
        log("✅ DISCORD_WEBHOOK_URL is set")
    else:
        checks["discord_webhook"] = {"ok": False, "detail": "DISCORD_WEBHOOK_URL not set"}
        log("⚠️  DISCORD_WEBHOOK_URL not set — report step will be skipped")

    # Docker container
    try:
        result = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Status}}", DOCKER_CONTAINER],
            capture_output=True, text=True, timeout=10
        )
        status = result.stdout.strip()
        if status == "running":
            checks["docker"] = {"ok": True, "detail": f"{DOCKER_CONTAINER} is running"}
            log(f"✅ Docker container '{DOCKER_CONTAINER}' is running")
        else:
            checks["docker"] = {"ok": False, "detail": f"{DOCKER_CONTAINER} status: {status}"}
            log(f"⚠️  Docker container '{DOCKER_CONTAINER}' status: {status}")
    except FileNotFoundError:
        checks["docker"] = {"ok": False, "detail": "Docker not found in PATH"}
        log("❌ Docker not found in PATH")
    except Exception as ex:
        checks["docker"] = {"ok": False, "detail": str(ex)}
        log(f"❌ Docker check failed: {ex}")

    # API port
    try:
        req = urllib.request.Request(f"{BRIEFING_API_URL}/health", method="GET")
        with urllib.request.urlopen(req, timeout=5):
            checks["api_port"] = {"ok": True, "detail": f"{BRIEFING_API_URL} reachable"}
            log(f"✅ API reachable at {BRIEFING_API_URL}")
    except Exception:
        checks["api_port"] = {"ok": False, "detail": f"{BRIEFING_API_URL} unreachable"}
        log(f"⚠️  API not reachable at {BRIEFING_API_URL} (container may be starting)")

    duration = round(time.time() - start, 2)
    all_ok = all(v["ok"] for v in checks.values())
    status_obj = {"command": "fix-env", "ok": all_ok, "duration": duration, "checks": checks}
    write_status(args.output, status_obj)
    return status_obj


def cmd_check_health(args) -> dict:
    """Ping Docker container and API health endpoint."""
    log("🏥 Checking brain health...")
    start = time.time()
    container_ok = False
    api_ok = False

    # Docker
    try:
        result = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Status}}", DOCKER_CONTAINER],
            capture_output=True, text=True, timeout=10
        )
        container_ok = result.stdout.strip() == "running"
        if container_ok:
            log(f"✅ Container '{DOCKER_CONTAINER}' is running")
        else:
            log(f"⚠️  Container '{DOCKER_CONTAINER}' is NOT running")
            if args.restart_if_down:
                log(f"🔄 Attempting restart of '{DOCKER_CONTAINER}'...")
                subprocess.run(["docker", "restart", DOCKER_CONTAINER], timeout=30)
                time.sleep(10)
                result2 = subprocess.run(
                    ["docker", "inspect", "--format", "{{.State.Status}}", DOCKER_CONTAINER],
                    capture_output=True, text=True, timeout=10
                )
                container_ok = result2.stdout.strip() == "running"
                log(f"{'✅' if container_ok else '❌'} Container after restart: {result2.stdout.strip()}")
    except Exception as ex:
        log(f"❌ Docker check failed: {ex}")

    # API
    try:
        req = urllib.request.Request(f"{BRIEFING_API_URL}/health", method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            api_ok = resp.status == 200
            log(f"✅ API health endpoint OK (HTTP {resp.status})")
    except Exception as ex:
        log(f"⚠️  API health check failed: {ex}")

    duration = round(time.time() - start, 2)
    ok = container_ok and api_ok
    status_obj = {
        "command": "check-health", "ok": ok, "duration": duration,
        "container_running": container_ok, "api_healthy": api_ok
    }
    write_status(args.output, status_obj)
    return status_obj


def cmd_generate_briefing(args) -> dict:
    """Trigger POST /briefing/generate and verify file appears in vault."""
    log("📝 Generating morning briefing...")
    start = time.time()
    ok = False
    detail = ""
    briefing_file = None

    try:
        data = json.dumps({}).encode()
        req = urllib.request.Request(
            f"{BRIEFING_API_URL}/briefing/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read())
            detail = body.get("message", str(body))
            log(f"✅ Briefing API responded: {detail}")

            # Verify file landed in vault
            if VAULT_PATH:
                briefings_dir = VAULT_PATH / "Briefings"
                briefings_dir.mkdir(parents=True, exist_ok=True)
                today = datetime.now().strftime("%Y-%m-%d")
                matches = list(briefings_dir.glob(f"*{today}*.md"))
                if matches:
                    briefing_file = str(matches[0])
                    ok = True
                    log(f"✅ Briefing file found: {briefing_file}")
                else:
                    ok = True  # API succeeded even if we can't verify file yet
                    detail += " (file not yet detected in vault — check Briefings/ folder)"
                    log(f"⚠️  Briefing file for {today} not yet detected in {briefings_dir}")
            else:
                ok = True
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        detail = f"HTTP {e.code}: {body_text[:300]}"
        log(f"❌ Briefing API error: {detail}")
    except Exception as ex:
        detail = str(ex)
        log(f"❌ Briefing generation failed: {ex}")

    duration = round(time.time() - start, 2)
    status_obj = {
        "command": "generate-briefing", "ok": ok, "duration": duration,
        "detail": detail, "briefing_file": briefing_file
    }
    write_status(args.output, status_obj)
    return status_obj


def cmd_sync_github(args) -> dict:
    """Pull open issues from configured repos and write to vault GitHub-Inbox."""
    log(f"🔄 Syncing GitHub issues from {len(GITHUB_REPOS)} repos...")
    start = time.time()
    total_synced = 0
    total_issues = 0
    repo_results = {}

    inbox_dir = None
    if VAULT_PATH:
        inbox_dir = VAULT_PATH / "GitHub-Inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)

    for repo in GITHUB_REPOS:
        log(f"  → Fetching issues from {repo}...")
        url = f"https://api.github.com/repos/{repo}/issues?state=open&per_page=50"
        issues = github_get(url)
        if issues is None:
            repo_results[repo] = {"ok": False, "synced": 0, "detail": "Rate limited or API error"}
            continue

        synced = 0
        for issue in issues:
            if "pull_request" in issue:  # skip PRs
                continue
            total_issues += 1
            if inbox_dir:
                safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in issue["title"])[:60]
                fname = f"{repo.replace('/', '_')}__#{issue['number']}_{safe_title}.md"
                content = (
                    f"---\n"
                    f"repo: {repo}\n"
                    f"issue_number: {issue['number']}\n"
                    f"title: \"{issue['title']}\"\n"
                    f"state: {issue['state']}\n"
                    f"url: {issue['html_url']}\n"
                    f"synced_at: {datetime.now(timezone.utc).isoformat()}\n"
                    f"---\n\n"
                    f"# {issue['title']}\n\n"
                    f"{issue.get('body', '') or '_No description provided._'}\n"
                )
                (inbox_dir / fname).write_text(content, encoding="utf-8")
                synced += 1

        repo_results[repo] = {"ok": True, "synced": synced, "total": len([i for i in issues if "pull_request" not in i])}
        total_synced += synced
        log(f"  ✅ {repo}: {synced} issues synced")

    duration = round(time.time() - start, 2)
    all_ok = all(v["ok"] for v in repo_results.values())
    partial = not all_ok and any(v["ok"] for v in repo_results.values())

    status_obj = {
        "command": "sync-github",
        "ok": all_ok,
        "partial": partial,
        "duration": duration,
        "total_synced": total_synced,
        "total_issues": total_issues,
        "repos": repo_results
    }
    write_status(args.output, status_obj)
    return status_obj


def cmd_report(args) -> dict:
    """Read all status JSONs and send ONE emoji table to Discord."""
    log("📊 Building status report...")
    start = time.time()

    status_files = {
        "check-health": OUTPUT_DIR / "health_status.json",
        "generate-briefing": OUTPUT_DIR / "briefing_status.json",
        "sync-github": OUTPUT_DIR / "sync_status.json",
    }

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"🧠 **BRAIN OPS — {ts} BST**"]

    for name, path in status_files.items():
        if path.exists():
            try:
                data = json.loads(path.read_text())
                ok = data.get("ok", False)
                partial = data.get("partial", False)
                duration = data.get("duration", "?")
                emoji = "✅" if ok else ("⚠️" if partial else "❌")
                detail = ""
                if name == "sync-github":
                    synced = data.get("total_synced", 0)
                    total = data.get("total_issues", 0)
                    detail = f" ({synced}/{total} issues)"
                elif not ok:
                    detail = f" — {data.get('detail', 'unknown error')[:80]}"
                lines.append(f"{emoji} {name}: {'OK' if ok else ('PARTIAL' if partial else 'FAILED')} ({duration}s){detail}")
            except Exception as ex:
                lines.append(f"⚠️ {name}: could not read status ({ex})")
        else:
            lines.append(f"⏭️ {name}: not run")

    message = "\n".join(lines)
    log(f"\n{message}")

    ok = False
    if DISCORD_WEBHOOK_URL:
        try:
            time.sleep(1)  # Respect Discord rate limit
            payload = json.dumps({"content": message}).encode()
            req = urllib.request.Request(
                DISCORD_WEBHOOK_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                ok = resp.status in (200, 204)
                log(f"✅ Discord report sent (HTTP {resp.status})")
        except urllib.error.HTTPError as e:
            log(f"❌ Discord webhook error HTTP {e.code} — check DISCORD_WEBHOOK_URL")
        except Exception as ex:
            log(f"❌ Discord report failed: {ex}")
    else:
        log("⏭️  DISCORD_WEBHOOK_URL not set — skipping Discord delivery")
        ok = True  # Not a failure if webhook not configured

    duration = round(time.time() - start, 2)
    status_obj = {"command": "report", "ok": ok, "duration": duration, "message": message}
    write_status(args.output, status_obj)
    return status_obj


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="hyper_brain_ops",
        description="🧠 HS-114 BRAIN OPS — Hyper Brain Infrastructure Manager"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # fix-env
    p_fix = sub.add_parser("fix-env", help="Diagnose environment")
    p_fix.add_argument("--output", help="Write status JSON to this path")

    # check-health
    p_health = sub.add_parser("check-health", help="Ping Docker + API")
    p_health.add_argument("--output", help="Write status JSON to this path")
    p_health.add_argument("--restart-if-down", action="store_true", help="Restart container if unhealthy")

    # generate-briefing
    p_brief = sub.add_parser("generate-briefing", help="Trigger briefing generation API")
    p_brief.add_argument("--output", help="Write status JSON to this path")

    # sync-github
    p_sync = sub.add_parser("sync-github", help="Pull GitHub issues into vault")
    p_sync.add_argument("--output", help="Write status JSON to this path")

    # report
    p_report = sub.add_parser("report", help="Send status report to Discord")
    p_report.add_argument("--output", help="Write status JSON to this path")

    args = parser.parse_args()

    dispatch = {
        "fix-env": cmd_fix_env,
        "check-health": cmd_check_health,
        "generate-briefing": cmd_generate_briefing,
        "sync-github": cmd_sync_github,
        "report": cmd_report,
    }

    result = dispatch[args.command](args)
    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
