#!/usr/bin/env python3
"""Project Euler Problem 976: XO Game.

Strip lengths have the strategy-equivalence classes: all lengths 1 mod
4 form one class, all lengths 3 mod 4 form another, and every even
length is its own class.  For even k, X wins unless every class occurs
an even number of times.  For odd k, X wins exactly when the only class
with odd multiplicity is the 1 mod 4 class.

Even/odd class multiplicities are extracted from products of
(1-x)^(-u)(1+x)^(-v).  Their coefficients obey a second-order
recurrence, which the C++ solver evaluates through K modulo 1234567891.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
