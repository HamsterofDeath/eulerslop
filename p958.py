#!/usr/bin/env python3
"""Project Euler Problem 958: Euclid's Labour.

The subtraction count is the sum of the Euclidean quotients minus one.
The C++ implementation searches continued-fraction prefixes by quotient
sum.  Once a prefix reaches moderate size, the target numerator fixes
the suffix's second continuant modulo the prefix numerator, so only a
short arithmetic progression of exact suffix candidates remains.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
