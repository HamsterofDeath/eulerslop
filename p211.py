#!/usr/bin/env python3
"""Project Euler 211: Divisor Square Sum.

Find the sum of all n, 0 < n < 64,000,000, such that sigma_2(n) (the sum of
the squares of the divisors of n) is a perfect square.

Uses a segmented sieve with numpy: for each divisor d <= sqrt(n) the pair
(d, n/d) contributes d^2 + (n/d)^2 (counting d^2 once when n = d^2).
"""
import math

import numpy as np


def solve():
    limit = 64_000_000  # exclusive upper bound for n
    seg_size = 1 << 22  # 4M entries per segment keeps memory modest

    total = 0
    for lo in range(1, limit, seg_size):
        hi = min(lo + seg_size, limit)
        size = hi - lo
        sig = np.zeros(size, dtype=np.int64)

        # For each small divisor d, add d^2 + k^2 to every n = d*k in the
        # segment with k >= d (so each divisor pair is counted once).
        for d in range(1, math.isqrt(hi - 1) + 1):
            n0 = max(d * d, ((lo + d - 1) // d) * d)
            if n0 >= hi:
                continue
            ks = np.arange(n0 // d, (hi - 1) // d + 1, dtype=np.int64)
            sig[n0 - lo:size:d] += d * d + ks * ks
            # n = d*d added d^2 twice; correct it.
            if lo <= d * d < hi:
                sig[d * d - lo] -= d * d

        # Perfect-square test: sigma2 < 7e15 < 2^53, so float sqrt is close;
        # accept r-1..r+1 as candidates, then verify exactly.
        r = np.rint(np.sqrt(sig.astype(np.float64))).astype(np.int64)
        mask = (r * r == sig) | ((r + 1) * (r + 1) == sig) | ((r - 1) * (r - 1) == sig)
        for idx in np.nonzero(mask)[0]:
            s = int(sig[idx])
            root = math.isqrt(s)
            if root * root == s:
                total += lo + int(idx)

    return total


if __name__ == "__main__":
    print(solve())
