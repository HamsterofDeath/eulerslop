#!/usr/bin/env python3
"""Project Euler Problem 928: Cribbage.

A hand is represented by its multiplicity (0 through 4) at each rank,
weighted by the corresponding choices of suits.  Splitting after rank
9 is especially useful: a fifteen contains either only low cards, or
one of the ten-valued cards together with a low-card subset worth 5.

The C++ implementation aggregates the 5**9 low-rank configurations by
their score balance, subset counts, and unfinished run.  It then joins
those states to the 5**4 configurations of 10, Jack, Queen, and King.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
