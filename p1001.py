#!/usr/bin/env python3
"""Project Euler Problem 1001: Connections I.

A chosen set of value pairs is connectable iff the arcs drawn above the row
do not cross, i.e. the chosen intervals [l_v, r_v] form a laminar family.
The C++ solver counts laminar families via
    F(l, r) = 1 + sum_{l <= l_v, r_v <= r} B_v * F(r_v + 1, r)
    B_v     = F(l_v + 1, r_v - 1)
processing the left ends a = l_v + 1 in decreasing order so each needed
sequence F(a, *) costs a single O(2n) pass.
"""

from pathlib import Path

from _cpp_runner import run_cpp

DATA = Path(__file__).resolve().parent / "1001_input.txt"


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), args=(str(DATA),)))


if __name__ == "__main__":
    print(solve())
