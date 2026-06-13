#!/usr/bin/env python3
import subprocess
import sys
import tempfile
from pathlib import Path


def solve():
    src = Path(__file__).with_name("p606.cpp")
    if not src.exists():
        raise FileNotFoundError(src)

    with tempfile.TemporaryDirectory(prefix="eulerslop_p606_") as tmpdir:
        exe = Path(tmpdir) / "solver"
        cmd = ["g++", "-O3", "-std=c++17", str(src), "-o", str(exe)]
        subprocess.run(cmd, check=True)
        result = subprocess.run(
            [str(exe)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
    return result.stdout.strip().splitlines()[-1].strip()


def main():
    print(solve())


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
