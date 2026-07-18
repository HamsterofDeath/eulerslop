#!/usr/bin/env python3
"""Project Euler Problem 929: Odd-Run Compositions.

Odd runs of value v have generating function

    A_v = x**v / (1 - x**(2*v)).

The Smirnov-word transform for adjacent unequal runs then gives

    G(x) = 1 / (1 - sum_v A_v/(1+A_v)).

Its inner coefficients are divisor sums of signed Fibonacci numbers.
The C++ implementation builds those sums and uses fast formal-series
inversion to extract the coefficient of degree 100,000.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
