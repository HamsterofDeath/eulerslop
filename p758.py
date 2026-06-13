#!/usr/bin/env python3
"""Project Euler 758: bucket pouring and Mersenne inverses."""

from math import gcd
from pathlib import Path

from _cpp_runner import run_cpp


def pouring_steps(a: int, b: int) -> int:
    best = None
    for sign in (1, -1):
        # a*x - b*y = sign, with x,y > 0.
        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1
        while r:
            q = old_r // r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s
            old_t, t = t, old_t - q * t
        x = old_s * sign
        y = -old_t * sign
        while x <= 0 or y <= 0:
            x += b
            y += a
        candidate = x + y
        best = candidate if best is None else min(best, candidate)
    return 2 * (best - 1)


def solve() -> int:
    assert gcd(3, 5) == 1 and pouring_steps(3, 5) == 4
    assert pouring_steps(7, 31) == 20
    assert pouring_steps(1234, 4321) == 2780
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
