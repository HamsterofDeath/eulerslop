#!/usr/bin/env python3
"""Project Euler Problem 946: Continued Fraction of a Homography.

The C++ implementation applies the homographic continued-fraction
algorithm to (2*alpha+3)/(3*alpha+2).  Repeated states while consuming
each prime-length run of 1s are cycle-skipped, allowing the first
100,000,000 output coefficients to be summed directly.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
