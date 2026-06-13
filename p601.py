#!/usr/bin/env python3
from math import gcd


def solve() -> int:
    total = 0
    lcm = 1

    for s in range(1, 32):
        next_lcm = lcm * (s + 1) // gcd(lcm, s + 1)
        limit = 4**s

        # streak(n) >= s iff n == 1 mod lcm(2, ..., s).
        # Exclude n = 1, and subtract those whose streak is at least s + 1.
        total += (limit - 2) // lcm - (limit - 2) // next_lcm
        lcm = next_lcm

    return total


if __name__ == "__main__":
    print(solve())
