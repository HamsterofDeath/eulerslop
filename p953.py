#!/usr/bin/env python3
"""Project Euler Problem 953: Factorisation Nim.

Write n=a**2*d with d squarefree.  The Nim xor is zero exactly when the
prime factors of d xor to zero.  In such a set its largest prime equals
the xor of all smaller primes, so the C++ implementation enumerates only
the smaller-prime subset and reconstructs the final prime.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
