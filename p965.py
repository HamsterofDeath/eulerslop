#!/usr/bin/env python3
"""Project Euler Problem 965: Expected Minimal Fractional Value.

On a gap a/b < c/d between consecutive fractions of the Farey sequence
of order N, f_N(x)=b*x-a.  The gap has length 1/(b*d), so its integral
is 1/(2*b*d**2).  Farey neighbours have exactly the ordered coprime
denominator pairs b,d <= N with b+d>N.  The C++ solver sums those pairs,
combining the two orientations.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> str:
    return run_cpp(Path(__file__).with_suffix(".cpp")).strip()


if __name__ == "__main__":
    print(solve())
