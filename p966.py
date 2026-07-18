#!/usr/bin/env python3
"""Project Euler Problem 966: Triangle Circle Intersection.

The C++ solver evaluates circle-triangle intersection area exactly from
the edge/circle crossings.  It maximizes the overlap under translation
with an analytic boundary-arc gradient and BFGS line search.  Similar
integer triangles are grouped by their primitive side-length triple;
their intersection areas then scale by the square of the common factor.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> str:
    return run_cpp(Path(__file__).with_suffix(".cpp")).strip()


if __name__ == "__main__":
    print(solve())
