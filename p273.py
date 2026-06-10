#!/usr/bin/env python3
# Problem 273: Sum of Squares
#
# The relevant N are squarefree products of the 16 primes p = 1 (mod 4) below
# 150. Each such prime splits in Z[i] as p = z * conj(z) with z = a + b*i.
# Every representation N = a^2 + b^2 (0 <= a <= b) of N = prod(p_j) comes from
# a product prod(z_j or conj(z_j)); the 2^k sign choices give every
# representation exactly twice (conjugate pairs), and a = min(|Re|, |Im|).
#
# Meet in the middle: split the 16 primes into two halves and enumerate all
# 3^8 = 6561 (subset, conjugation) products per half. Combining every pair
# (one product per half) enumerates every (subset of 16 primes, signs) exactly
# once, so the grand total of min(|Re|,|Im|) equals 2 * answer (the empty/empty
# pair contributes min(1,0) = 0). The inner combination is vectorised in numpy;
# all magnitudes stay below 2^63.

import numpy as np

def solve():
    # primes of the form 4k+1 below 150
    primes = [p for p in range(5, 150)
              if p % 4 == 1 and all(p % d for d in range(2, int(p ** 0.5) + 1))]

    # decompose p = a^2 + b^2
    zs = []
    for p in primes:
        a = 1
        while True:
            b2 = p - a * a
            b = int(b2 ** 0.5)
            if b * b == b2:
                zs.append((a, b))
                break
            a += 1

    def expand(zlist):
        # all products over subsets with each factor z or conj(z)
        prods = [(1, 0)]
        for (a, b) in zlist:
            new = list(prods)  # exclude this prime
            for (x, y) in prods:
                new.append((x * a - y * b, x * b + y * a))    # * (a + bi)
                new.append((x * a + y * b, y * a - x * b))    # * (a - bi)
            prods = new
        return prods

    A = expand(zs[:8])
    B = expand(zs[8:])
    bx = np.array([t[0] for t in B], dtype=np.int64)
    by = np.array([t[1] for t in B], dtype=np.int64)

    total = 0
    for (xa, ya) in A:
        x = np.abs(xa * bx - ya * by)
        y = np.abs(xa * by + ya * bx)
        total += int(np.minimum(x, y).sum())

    # every representation was counted twice (z and conj(z))
    return total // 2

if __name__ == "__main__":
    print(solve())
