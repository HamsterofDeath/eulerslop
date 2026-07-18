#!/usr/bin/env python3
"""Project Euler Problem 936: Peerless Trees.

For planted trees, let A_d mark those whose root has final degree d.
The peerless condition gives

    A_d = x * MSET_(d-1)(A - A_d).

Vertex-rooted trees use one additional child.  In the dissymmetry
formula, an admissible edge always joins distinct degree classes, so
the directed-edge term is twice the unordered edge term and the
unrooted series is simply R-E.  The C++ implementation evaluates these
unlabelled multiset series coefficient by coefficient.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
