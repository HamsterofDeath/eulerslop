#!/usr/bin/env python3
"""Project Euler 678: differing exponents in Fermat-type equations."""

from pathlib import Path
import subprocess
import tempfile


def solve() -> int:
    source = Path(__file__).with_suffix(".cpp")
    with tempfile.TemporaryDirectory(prefix="p678_") as tmpdir:
        binary = Path(tmpdir) / "p678"
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(source), "-o", str(binary)],
            check=True,
        )
        return int(subprocess.check_output([str(binary)], text=True).strip())


if __name__ == "__main__":
    print(solve())
