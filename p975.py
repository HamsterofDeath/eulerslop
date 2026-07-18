#!/usr/bin/env python3
"""Project Euler Problem 975: A Winding Path.

The derivative of H_ab factors into sine and cosine terms, giving every
critical point explicitly.  The C++ solver splits each H into monotone
branches and traces the unique endpoint component through pairs of
branches.  Whenever one coordinate crosses a turning point, the other
reverses along its current branch.  Summing the absolute critical-height
changes gives the path's total vertical variation.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> str:
    return run_cpp(Path(__file__).with_suffix(".cpp")).strip()


if __name__ == "__main__":
    print(solve())
