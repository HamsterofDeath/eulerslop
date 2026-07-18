#!/usr/bin/env python3
"""Project Euler Problem 971: Modular Polynomial Composition.

For p=5k-4, put r=(p-1)/5.  Every nonzero x has a state z=x**r
among the five fifth roots of unity, and f sends

    x -> x*(1+z),  z -> z*(1+z)**r.

Thus x is periodic exactly when its five-root state is cyclic in this
five-node map.  Every cyclic state represents r field elements.  The
C++ solver sieves p <= 10**8 and constructs this tiny map for each
prime congruent to one modulo five.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
