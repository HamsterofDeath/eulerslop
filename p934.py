#!/usr/bin/env python3
"""Project Euler Problem 934: Unlucky Primes.

To survive prime p, an integer must have residue 0, 7, 14, ... modulo
p.  The C++ implementation combines these allowed residues by CRT
while their primorial modulus is at most N.  Once the modulus exceeds
N, each surviving residue identifies at most one actual integer, and
the shrinking survivor list is filtered directly by later primes.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
