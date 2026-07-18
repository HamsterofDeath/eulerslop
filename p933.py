#!/usr/bin/env python3
"""Project Euler Problem 933: Paper Cutting.

The Grundy value of a w-by-h rectangle is the mex of the xor of the
four pieces from each cut.  For fixed w, every child has smaller width.
Once those smaller-width sequences are constant beyond height T, the
current option set is constant beyond 2T as well.

In that stable range every cut whose two heights are at least T is
winning.  Thus C(w,h) is eventually affine in h, with slope w-1.  The
C++ implementation evaluates only the short transient and sums the
remaining million-height tail arithmetically.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
