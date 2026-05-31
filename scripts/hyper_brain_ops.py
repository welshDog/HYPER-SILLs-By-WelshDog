#!/usr/bin/env python3
"""
HS-114 🛠️ BRAIN OPS — Hyper Brain Infrastructure Maintenance CLI
welshDog 🐕 Llanelli, Wales

Usage:
    uv run scripts/hyper_brain_ops.py check-health [--restart-if-down] [--output FILE]
    uv run scripts/hyper_brain_ops.py generate-briefing [--output FILE]
    uv run scripts/hyper_brain_ops.py sync-github [--output FILE]
    uv run scripts/hyper_brain_ops.py fix-env
    uv run scripts/hyper_brain_ops.py report [--input-dir DIR]

Env vars required:
    GITHUB_PAT            - GitHub personal access token
    DISCORD_WEBHOOK_URL   - Discord webhook for status reports
    VAULT_PATH            - Absolute path to your Obsidian vault
    BRIEFING_API_URL      - (optional) default: http://localhost:8100
    DOCKER_CONTAINER      - (optional) default: hyper-brain
    GITHUB_REPOS          - (optional) comma-separated repos, default: welshDog repos
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

# ── Config from environment ──────────────────────────────────────────────────

GITHUB_PAT = os.environ.get("GITHUB_PAT", "")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
VAULT_PATH = Path(os.environ.get("VAULT_PATH", "./vault"))
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


# ── Helpers ───────────────────────────────────────────────────────────────────

def log(emoji: str, msg: str) -> None:
    print(f"{emoji}  {msg}", flush=True)


def write_output(path: str | None, data: dict) -> None:
    if not path:
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2))
    log("💾", f"Output written → {out}")


def github_get(endpoint: str) -> dict | list:
    """Single authenticated GitHub API GET with 1-second rate-limit delay."""
    url = f"https://api.github.com{endpoint}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {GITHUB_PAT}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    time.sleep(1)  # Respect 1 req/sec default
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


# ── Subcommand: check-health ──────────────────────────────────────────────────

def cmd_check_health(restart_if_down: bool, output: str | None) -> dict:
    result = {"timestamp": datetime.utcnow().isoformat(), "container": None, "api": None, "status": "unknown"}

    # 1. Docker container check
    try:
        proc = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Status}}", DOCKER_CONTAINER],
            capture_output=True, text=True, timeout=10,
        )
        container_status = proc.stdout.strip()
        result["container"] = container_status
        log("🐳", f"Container '{DOCKER_CONTAINER}' status: {container_status}")

        if container_status != "running":
            if restart_if_down:
                log("🔄", f"Container is {container_status}. Attempting restart...")
                subprocess.run(["docker", "restart", DOCKER_CONTAINER], timeout=30)
                result["container"] = "restarted"
                log("✅", "Container restarted. Waiting 5s for it to settle...")
                time.sleep(5)
            else:
                log("❌", "Container is not running. Run with --restart-if-down to auto-fix.")
    except FileNotFoundError:
        result["container"] = "docker_not_found"
        log("⚠️", "Docker CLI not found — skipping container check.")
    except Exception as e:
        result["container"] = f"error: {e}"
        log("❌", f"Container check failed: {e}")

    # 2. API health check
    try:
        req = urllib.request.Request(f"{BRIEFING_API_URL}/health")
        with urllib.request.urlopen(req, timeout=10) as resp:
            result["api"] = resp.status
            log("🌐", f"API health endpoint: HTTP {resp.status}")
    except urllib.error.URLError as e:
        result["api"] = f"unreachable: {e.reason}"
        log("❌", f"API unreachable: {e.reason}")
    except Exception as e:
        result["api"] = f"error: {e}"
        log("❌", f"API check failed: {e}")

    # Overall status
    container_ok = result["container"] in ("running", "restarted")
    api_ok = result["api"] == 200
    result["status"] = "healthy" if (container_ok and api_ok) else "degraded"
    log("📊", f"Overall status: {result['status']}")

    write_output(output, result)
    return result


# ── Subcommand: generate-briefing ─────────────────────────────────────────────

def cmd_generate_briefing(output: str | None) -> dict:
    result = {"timestamp": datetime.utcnow().isoformat(), "status": "unknown", "error": None, "file": None}

    try:
        log("🌅", f"Triggering briefing generation at {BRIEFING_API_URL}/briefing/generate ...")
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
            log("✅", f"Briefing generated: {result['file']}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode(errors="replace")
        result["status"] = "failed"
        result["error"] = f"HTTP {e.code}: {error_body[:500]}"
        log("❌", f"Briefing API error {e.code} — {error_body[:200]}")
        log("ℹ️", "Pipeline continues despite briefing failure.")
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)
        log("❌", f"Briefing generation exception: {e}")

    write_output(output, result)
    return result


# ── Subcommand: sync-github ───────────────────────────────────────────────────

def cmd_sync_github(output: str | None) -> dict:
    inbox = VAULT_PATH / "GitHub-Inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    result = {"timestamp": datetime.utcnow().isoformat(), "repos": {}, "total_issues_written": 0, "errors": []}

    for repo in GITHUB_REPOS:
        log("🔄", f"Syncing issues from {repo} ...")
        try:
            issues = github_get(f"/repos/{repo}/issues?state=open&per_page=50")
            written = 0
            for issue in issues:
                if "pull_request" in issue:  # Skip PRs
                    continue
                slug = repo.replace("/", "_")
                filename = inbox / f"{slug}__issue_{issue['number']}.md"
                content = (
                    f"# [{repo}] #{issue['number']} — {issue['title']}\n\n"
                    f"**State:** {issue['state']}  \n"
                    f"**URL:** {issue['html_url']}  \n"
                    f"**Created:** {issue['created_at']}  \n\n"
                    f"## Description\n\n{issue.get('body') or '_No description provided._'}\n\n"
                    f"---\n*Synced by HS-114 BRAIN OPS — {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC*\n"
                )
                filename.write_text(content, encoding="utf-8")
                written += 1
            result["repos"][repo] = {"issues_written": written, "status": "ok"}
            result["total_issues_written"] += written
            log("✅", f"{repo}: {written} issue(s) written to vault.")
        except urllib.error.HTTPError as e:
            if e.code == 403:
                msg = f"{repo}: GitHub rate limit hit — skipping."
            else:
                msg = f"{repo}: HTTP {e.code} error."
            result["repos"][repo] = {"status": "error", "error": msg}
            result["errors"].append(msg)
            log("⚠️", msg)
        except Exception as e:
            msg = f"{repo}: {e}"
            result["repos"][repo] = {"status": "error", "error": msg}
            result["errors"].append(msg)
            log("❌", msg)

    log("📥", f"Total issues written to vault: {result['total_issues_written']}")
    write_output(output, result)
    return result


# ── Subcommand: fix-env ────────────────────────────────────────────────────────

def cmd_fix_env() -> None:
    log("🔍", "Running environment diagnostics...\n")
    ok = True

    # GITHUB_PAT
    if GITHUB_PAT:
        log("✅", f"GITHUB_PAT is set ({len(GITHUB_PAT)} chars).")
    else:
        log("❌", "GITHUB_PAT is NOT set.")
        print("    ➡️  Fix: Add to your .env file → GITHUB_PAT=ghp_xxxxxxxxxxxxxxxx")
        ok = False

    # DISCORD_WEBHOOK_URL
    if DISCORD_WEBHOOK_URL:
        log("✅", "DISCORD_WEBHOOK_URL is set.")
    else:
        log("⚠️", "DISCORD_WEBHOOK_URL is NOT set — Discord reports will be skipped.")
        print("    ➡️  Fix: Add to your .env file → DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...")

    # VAULT_PATH
    if VAULT_PATH.exists():
        log("✅", f"VAULT_PATH exists: {VAULT_PATH}")
    else:
        log("❌", f"VAULT_PATH does NOT exist: {VAULT_PATH}")
        print(f"    ➡️  Fix: Create the directory or update VAULT_PATH env var.")
        ok = False

    # Docker
    try:
        proc = subprocess.run(["docker", "ps", "--filter", f"name={DOCKER_CONTAINER}", "--format", "{{.Names}}"],
                              capture_output=True, text=True, timeout=10)
        if DOCKER_CONTAINER in proc.stdout:
            log("✅", f"Docker container '{DOCKER_CONTAINER}' is running.")
        else:
            log("❌", f"Docker container '{DOCKER_CONTAINER}' is NOT running.")
            print(f"    ➡️  Fix: cd to your brain project and run: docker compose up -d")
            ok = False
    except FileNotFoundError:
        log("⚠️", "Docker CLI not found.")
        print("    ➡️  Fix: Install Docker Desktop (Windows) or docker on WSL/Linux.")

    # Port binding check
    try:
        req = urllib.request.Request(f"{BRIEFING_API_URL}/health")
        with urllib.request.urlopen(req, timeout=5) as resp:
            log("✅", f"API at {BRIEFING_API_URL} is reachable (HTTP {resp.status}).")
    except Exception:
        log("❌", f"API at {BRIEFING_API_URL} is NOT reachable.")
        print(f"    ➡️  Fix: Check your Docker volume mounts and that port 8100 is exposed.")
        ok = False

    print()
    if ok:
        log("🎉", "All critical env checks passed! Brain is ready.")
    else:
        log("🛑", "Some checks failed — see fix hints above.")
        sys.exit(1)


# ── Subcommand: report ────────────────────────────────────────────────────────

def cmd_report(input_dir: str) -> None:
    base = Path(input_dir)
    results = {}
    for name in ("health", "briefing", "sync"):
        fp = base / f"{name}.json"
        if fp.exists():
            results[name] = json.loads(fp.read_text())

    health = results.get("health", {})
    briefing = results.get("briefing", {})
    sync_r = results.get("sync", {})

    lines = [
        "🛠️ **BRAIN OPS STATUS REPORT**",
        f"🕐 {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
        "",
        f"🐳 Container: `{health.get('container', 'unknown')}` | API: `{health.get('api', 'unknown')}`",
        f"📊 Health: **{health.get('status', 'unknown').upper()}**",
        "",
        f"🌅 Morning Briefing: **{briefing.get('status', 'unknown').upper()}**",
    ]
    if briefing.get("error"):
        lines.append(f"   ⚠️ Error: `{briefing['error'][:120]}`")
    if briefing.get("file"):
        lines.append(f"   📄 File: `{briefing['file']}`")

    lines += [
        "",
        f"🔄 GitHub Sync: **{sync_r.get('total_issues_written', 0)} issues** written to vault",
    ]
    if sync_r.get("errors"):
        for err in sync_r["errors"]:
            lines.append(f"   ⚠️ {err}")

    lines += ["", "*HS-114 BRAIN OPS by welshDog 🐕⚡*"]
    message = "\n".join(lines)

    log("📣", "Status report:\n" + message)

    if not DISCORD_WEBHOOK_URL:
        log("⚠️", "DISCORD_WEBHOOK_URL not set — skipping Discord notification.")
        return

    time.sleep(1)  # Discord rate limit safety
    payload = json.dumps({"content": message}).encode()
    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            log("✅", f"Discord report sent! HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        log("⚠️", f"Discord webhook returned HTTP {e.code} — report not delivered.")
    except Exception as e:
        log("⚠️", f"Discord send failed: {e} — pipeline continues.")


# ── CLI entry point ───────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="hyper_brain_ops",
        description="🛠️ HS-114 BRAIN OPS — Hyper Brain Infrastructure Maintenance",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # check-health
    p_health = sub.add_parser("check-health", help="Ping Docker container + API health endpoint")
    p_health.add_argument("--restart-if-down", action="store_true", help="Auto-restart container if not running")
    p_health.add_argument("--output", default=None, help="Write result to JSON file")

    # generate-briefing
    p_brief = sub.add_parser("generate-briefing", help="Trigger morning briefing generation")
    p_brief.add_argument("--output", default=None, help="Write result to JSON file")

    # sync-github
    p_sync = sub.add_parser("sync-github", help="Sync open GitHub issues to vault inbox")
    p_sync.add_argument("--output", default=None, help="Write result to JSON file")

    # fix-env
    sub.add_parser("fix-env", help="Diagnose env vars, vault path, Docker, and port bindings")

    # report
    p_report = sub.add_parser("report", help="Send status report to Discord")
    p_report.add_argument("--input-dir", default="output", help="Directory containing health/briefing/sync JSON files")

    args = parser.parse_args()

    if args.command == "check-health":
        cmd_check_health(restart_if_down=args.restart_if_down, output=args.output)
    elif args.command == "generate-briefing":
        cmd_generate_briefing(output=args.output)
    elif args.command == "sync-github":
        cmd_sync_github(output=args.output)
    elif args.command == "fix-env":
        cmd_fix_env()
    elif args.command == "report":
        cmd_report(input_dir=args.input_dir)


if __name__ == "__main__":
    main()
