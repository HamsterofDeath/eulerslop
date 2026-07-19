#!/usr/bin/env python3
"""Project Euler Problem 990: Addition Equations.

The C++ solver works from the units column towards the most-significant
column.  Its state records the numbers still contributing digits on each
side and the carry difference between the two sums.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
