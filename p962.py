#!/usr/bin/env python3
"""Project Euler Problem 962: Angular Bisector and Tangent 2.

Coordinates give CE**2=a**3*((a+b)**2-c**2)/(b*(a+b)**2).
After reducing a:b and separating squarefree kernels, every solution
has a unique parametrization by two coprime square-class pairs and a
scale.  The C++ implementation enumerates the primitive parameters and
counts all admissible scales arithmetically.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
