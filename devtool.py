#!/usr/bin/env python3

import argparse, subprocess, sys, json
from pathlib import Path

def run(cmd, cwd=None):
    print(f"[+] {' '.join(cmd)}")
    if subprocess.run(cmd, cwd=cwd).returncode:
        sys.exit(1)

def init_repo(name):
    p = Path(name); p.mkdir(exist_ok=True)
    run(["git", "init", "-b", "main"], cwd=p)
    (p / "README.md").write_text(f"# {name}\n\nInternal dev tool demo.\n")
    run(["git", "add", "."], cwd=p)
    run(["git", "commit", "-m", "init"], cwd=p)

def trigger_ci(project_id, token_path="~/.ci-token"):
    tok_file = Path(token_path).expanduser()
    if not tok_file.exists():
        print("[-] CI token not found"); return
    token = tok_file.read_text().strip()
    print(f"[+] Triggering CI for {project_id} with token {token[:4]}***")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("init");  p1.add_argument("name")
    p2 = sub.add_parser("ci");    p2.add_argument("project_id")
    args = ap.parse_args()
    {"init": init_repo, "ci": trigger_ci}[args.cmd](**vars(args))
