#!/usr/bin/env python3
"""Claude Code PostToolUse hook: auto-deploy when a lesson HTML file is written.

Reads the hook payload from stdin. If the written file is a lesson HTML file
(a `.html` inside any `lessons/` folder), it rebuilds the index pages, commits,
and pushes so the change goes live on GitHub Pages. Always exits 0 so a network
or git hiccup never blocks the editing session; details go to deploy.log.
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / ".claude" / "deploy.log"


def log(msg: str) -> None:
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True, timeout=120
    )


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    p = file_path.replace("\\", "/")
    if not (p.endswith(".html") and "/lessons/" in p):
        return  # not a lesson; nothing to deploy

    try:
        run("python3", str(ROOT / "build_site.py"))
        run("git", "add", "-A")
        status = run("git", "status", "--porcelain")
        if not status.stdout.strip():
            log("no changes to deploy")
            return
        name = Path(file_path).name
        run("git", "commit", "-m", f"Publish lesson: {name}")
        push = run("git", "push")
        if push.returncode == 0:
            log(f"deployed {name}")
        else:
            log(f"committed {name}, push failed: {push.stderr.strip()}")
    except Exception as exc:  # never break the session
        log(f"error: {exc}")


if __name__ == "__main__":
    main()
    sys.exit(0)
