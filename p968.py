#!/usr/bin/env python3
"""Project Euler Problem 968: 5D Summation.

The ten pair bounds define a five-dimensional lattice polytope.  The
C++ solver perturbs each integral upper bound outward by a distinct
fraction below one, preserving its lattice points while making the
polytope simple.  Brion's theorem then expresses its weighted generating
function as the sum of its vertex-cone generating functions.  All cone
determinants for this facet matrix are only 1, 4, or 16, so their
fundamental parallelepipeds can be enumerated directly and exactly.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
