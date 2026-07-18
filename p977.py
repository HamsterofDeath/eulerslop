#!/usr/bin/env python3
"""Project Euler Problem 977: Iterated Functions.

Taking y=1 shows that the condition is equivalent to f(x)=f**x(1), so
f is determined by the tail and cycle of the orbit of 1.  Consistency
forces the early tail labels and assigns cycle labels to fixed residue
classes modulo the cycle length.  Reindexing the resulting count by
M=n-t+1=qL+r makes complete remainder ranges geometric.  The C++ solver
sums them in O(n log n), with O(n) work for the t=0,1 boundary cases.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
