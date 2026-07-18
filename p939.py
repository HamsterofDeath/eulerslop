#!/usr/bin/env python3
"""Project Euler Problem 939: A Pile of Problems.

A size-r pile on A's side has canonical game

    (r-1)*up + (r mod 2)*star;

on B's side only the up coefficient changes sign.  If U is the total
up coefficient and s the star parity, A wins whoever starts exactly
for U>=2, or U=1 with s=0.

Side-swap symmetry turns the count into
(all - count(U=0))/2 - count(U=1,s=1).  The C++ implementation obtains
these boundary counts from partitions indexed by stones, part count,
and odd-part parity.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
