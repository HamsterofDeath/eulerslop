#!/usr/bin/env python3
import re
from pathlib import Path

from _cpp_runner import run_cpp


def solve():
    output = run_cpp(
        Path(__file__).with_suffix(".cpp"),
        ("--no-validate", "--threads=1"),
    )
    match = re.search(r"S\(5000000\) = ([0-9]+)", output)
    if not match:
        raise RuntimeError(output)
    return match.group(1)


if __name__ == "__main__":
    print(solve())
