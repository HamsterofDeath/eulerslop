#!/usr/bin/env python3
"""Project Euler Problem 972: Hyperbolic Plane.

Lift (x,y) to (x,y,1+x**2+y**2).  Equations of both diameters and
circles orthogonal to the unit circle become homogeneous planes through
the origin in these coordinates.  For each first point P, the C++ solver
groups every other point Q by the primitive cross product v(P) x v(Q).
A group of g other points contributes g*(g-1) ordered choices of Q,R.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
