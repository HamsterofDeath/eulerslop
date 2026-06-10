#!/usr/bin/env python3
# Problem 274: Divisibility Multipliers
#
# Write n = 10q + d. Then f(n) = q + d*m and 10*f(n) - n = d*(10m - 1).
# f(n) is divisible by p for exactly the same n as n itself iff 10m = 1 (mod p),
# i.e. m is the modular inverse of 10 mod p (unique with 0 < m < p).
# Depending on p mod 10 the inverse is (k*p + 1)/10 with k in {9, 3, 7, 1}
# for p = 1, 3, 7, 9 (mod 10). Sum over all primes p < 10^7, p != 2, 5.

import numpy as np

def solve():
    LIMIT = 10 ** 7
    sieve = np.ones(LIMIT, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(LIMIT ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    p = np.nonzero(sieve)[0].astype(np.int64)
    p = p[(p != 2) & (p != 5)]

    r = p % 10
    # k such that k*p = -1 (mod 10), making (k*p + 1)/10 an integer.
    k = np.where(r == 1, 9, np.where(r == 3, 3, np.where(r == 7, 7, 1)))
    m = (k * p + 1) // 10
    return int(m.sum())

if __name__ == "__main__":
    print(solve())
