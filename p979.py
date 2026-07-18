#!/usr/bin/env python3
"""Project Euler Problem 979: Heptagon Hopping.

The tile-adjacency graph is the 7-regular triangular {3,7} tiling.
The C++ solver builds concentric triangulated disks combinatorially:
each old boundary edge receives one shared outer vertex, then private
fan vertices complete every old vertex to degree seven.  A closed walk
of length 20 stays inside radius 10, where ordinary adjacency DP counts
all returns exactly.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
