#!/usr/bin/env python3
"""Project Euler Problem 950: The Pirate Problem.

The C++ implementation follows the backward-induction equilibrium.
Pirates who would die after rejecting a proposal vote for it freely;
survivors require their future coins plus the integral premium implied
by the additional deaths.  Accepted proposals therefore update only
the cheapest future allocations, which can be kept as a histogram.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
