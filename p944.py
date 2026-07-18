#!/usr/bin/env python3
"""Project Euler Problem 944: Sum of Elevisors.

For a fixed x, count the subsets containing x and at least one of its
other multiples.  This turns the answer into a weighted floor-quotient
sum.  The C++ implementation evaluates it with the usual square-root
split and incremental powers of two.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
