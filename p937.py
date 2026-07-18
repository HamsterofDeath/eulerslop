#!/usr/bin/env python3
"""Project Euler Problem 937: Factorial Partition.

Unique factorization in Z[sqrt(-2)] makes membership a Thue--Morse
sign on irreducible exponents:

    sign(z) = (-1)**sum(popcount(v_pi(z))).

For rational factorials, split primes p=1 or 3 (mod 8) occur as two
conjugate factors and cancel.  Only 2 and inert primes p=5 or 7
(mod 8) affect the sign.  The C++ implementation records every parity
change in their factorial valuations, then scans the factorials once.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
