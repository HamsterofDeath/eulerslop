#!/usr/bin/env python3
"""Project Euler Problem 963: Removing Trits.

Every one-number game has an uptimal expansion.  After deleting all
ternary 2s, the remaining binary word determines its dyadic part.  The
parity of the 2s determines its star part.  Before the first 1, each 0
adds an uptimal coefficient equal to the number of preceding 2s.

The C++ solver groups equal expansions, then groups all unordered
two-number paper values.  A fair setting uses the same value on both
ordered papers, so a value occurring c times contributes c**2.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
