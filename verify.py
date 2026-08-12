#!/usr/bin/env python3
"""Verify Project Euler solutions against known_answers.md.

Computed answers are cached in our_answers.md, so each solution runs only
once; later invocations just compare the cached table. Solutions missing
from the cache (e.g. newly added pNNN.py files) are run and added.

Usage:
    verify.py            run uncached solutions, then compare everything
    verify.py 12 54      force re-run of p012 and p054 (then compare)
    verify.py --all      force re-run of every solution
"""
import re
import shlex
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).parent
KNOWN = ROOT / "known_answers.md"
OURS = ROOT / "our_answers.md"
TIMEOUT = 300
MEMORY_LIMIT_KB = 10_000_000_000 // 1024

def load_table(path):
    table = {}
    if path.exists():
        for line in path.read_text().splitlines():
            m = re.match(r"^(\d+)\. (.+)$", line.strip())
            if m:
                table[int(m.group(1))] = m.group(2).strip()
    return table

def save_table(table):
    lines = [f"{n}. {table[n]}" for n in sorted(table)]
    OURS.write_text("\n".join(lines) + "\n")

def run_one(n):
    script = ROOT / f"p{n:03d}.py"
    cmd = (
        f"ulimit -v {MEMORY_LIMIT_KB}; "
        f"exec {shlex.quote(sys.executable)} {shlex.quote(str(script))}"
    )
    try:
        r = subprocess.run(["bash", "-lc", cmd], capture_output=True,
                           text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return n, "TIMEOUT", ""
    if r.returncode != 0:
        return n, "ERROR", r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""
    out = r.stdout.strip().splitlines()
    return n, "OK", out[-1].strip() if out else ""

def main():
    known = load_table(KNOWN)
    ours = load_table(OURS)
    problems = sorted(int(p.stem[1:]) for p in ROOT.glob("p[0-9][0-9][0-9]*.py"))

    args = sys.argv[1:]
    if "--all" in args:
        to_run = problems
    else:
        forced = {int(a) for a in args}
        to_run = [n for n in problems if n in forced or n not in ours]

    broken = {}
    if to_run:
        print(f"running {len(to_run)} solution(s): "
              + ", ".join(f"p{n:03d}" for n in to_run), flush=True)
        with ThreadPoolExecutor(max_workers=12) as ex:
            futures = {ex.submit(run_one, n): n for n in to_run}
            for fut in as_completed(futures):
                n, status, value = fut.result()
                if status == "OK":
                    ours[n] = value
                else:
                    ours.pop(n, None)
                    broken[n] = (status, value)
                    print(f"p{n:03d}: {status} {value}", flush=True)
        save_table(ours)

    failed = dict(broken)
    for n in problems:
        if n in failed:
            continue
        if n not in ours:
            failed[n] = ("MISSING", "")
        elif ours[n] != known.get(n):
            failed[n] = ("MISMATCH", f"got={ours[n]!r} expected={known.get(n)!r}")
            print(f"p{n:03d}: MISMATCH {failed[n][1]}", flush=True)

    print(f"\n{len(problems) - len(failed)}/{len(problems)} verified")
    if failed:
        print("failed:", ", ".join(f"p{n:03d} ({failed[n][0]})" for n in sorted(failed)))
        sys.exit(1)

if __name__ == "__main__":
    main()
