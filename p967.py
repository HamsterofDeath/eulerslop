#!/usr/bin/env python3
"""Project Euler Problem 967: B-Trivisible Numbers.

Work in Z[x]/(x**3-1).  For each prime p <= B, divisibility contributes
1 + (x**(p mod 3)-1)[p|n].  Expanding and summing over n replaces each
selected squarefree product d by floor(N/d).  The C++ DFS visits only
products d <= N and accumulates the residue-zero coefficient exactly.
The prime 3 is omitted because its expansion factor is identically one.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
