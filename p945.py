#!/usr/bin/env python3
"""Project Euler Problem 945: XOR-products.

Integers are polynomials over F_2 under XOR-product.  The equation is
solvable exactly when x*a*b is a square.  The C++ implementation finds
the unique square-free representative of every polynomial's class and
matches the frequencies of classes D and x*D.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
