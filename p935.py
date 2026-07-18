#!/usr/bin/env python3
"""Project Euler Problem 935: Rolling Square.

Periodic rolling states are indexed by primitive positive pairs.  A
pair with sum q returns after either 2q-2 or 2q steps.  Thus, for
N=2K, all Farey layers through K are complete and only layer K+1 needs
classification.

The longer return occurs when that layer's rotation fraction lies in
the critical contact interval [3/4, rho].  The C++ implementation sums
the complete totient layers and counts coprime numerators in this one
interval by inclusion-exclusion.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
