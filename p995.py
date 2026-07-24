#!/usr/bin/env python3
"""Project Euler Problem 995: A Particular Pair of Polynomials.

The C++ solver minimizes each S(p) by dynamic programming over the
subgroups of the cyclic multiplicative group modulo p.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> str:
    return run_cpp(Path(__file__).with_suffix(".cpp")).strip()


if __name__ == "__main__":
    print(solve())
