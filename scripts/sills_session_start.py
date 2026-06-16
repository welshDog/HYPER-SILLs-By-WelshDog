#!/usr/bin/env python3
"""HyperFocus Z0ne - HYPER-SILLs Session Start Hook.

Writes a .focus_session_start marker, checks .env, pyproject.toml,
and skills-registry.json.  Pings the briefing API if running.
Exits 0 on pass, 1 on hard failure.
"""

import socket
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESSION_FILE = ROOT / ".focus_session_start"


def _briefing_reachable() -> bool:
    try:
        s = socket.create_connection(("127.0.0.1", 8100), timeout=2)
        s.close()
        return True
    except OSError:
        return False


def main() -> int:
    now = datetime.now()
    print("\n[SESSION START] HyperFocus Z0ne -- HYPER-SILLs")
    print("-" * 40)
    print("   Time    : " + now.strftime("%Y-%m-%d %H:%M:%S"))

    SESSION_FILE.write_text(now.isoformat())

    env_ok = (ROOT / ".env").exists()
    pyproject_ok = (ROOT / "pyproject.toml").exists()
    registry_ok = (ROOT / "skills-registry.json").exists()
    briefing_ok = _briefing_reachable()

    print("   .env            : " + ("PASS found" if env_ok else "WARN missing (.env)"))
    print("   pyproject.toml  : " + ("PASS found" if pyproject_ok else "WARN pyproject.toml missing"))
    print("   skills-registry : " + ("PASS found" if registry_ok else "FAIL skills-registry.json missing"))
    print("   briefing :8100  : " + ("PASS reachable" if briefing_ok else "WARN offline (brain agents not running)"))
    print()

    if not registry_ok:
        print("FAIL  Session start FAILED -- skills-registry.json not found.\n")
        return 1

    print("PASS  SILLs session started. BROski forever! Let's build!\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
