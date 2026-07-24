#!/usr/bin/env python3
"""Project Euler Problem 994: Counting Triangles.

The C++ solver counts pairwise-intersecting triples of segments and
subtracts degenerate triples whose three segments are concurrent.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
