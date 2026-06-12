#!/usr/bin/env python3
import numpy as np

def solve():
    # Wilson: (p-1)! = -1 (mod p).  Dividing down:
    #   (p-2)! = 1, (p-3)! = -1/2, (p-4)! = 1/6, (p-5)! = -1/24  (mod p)
    # so S(p) = -1 + 1 - 1/2 + 1/6 - 1/24 = (-12+4-1)/24 = -9/24 = -3/8 (mod p).
    # The inverse of 8 mod p is (1 + k*p)/8 with k = 8 - (p mod 8), since
    # p^-1 = p (mod 8) for odd p.  Everything vectorizes over a prime sieve.
    N = 10 ** 8
    sieve = np.ones(N, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    p = np.flatnonzero(sieve).astype(np.int64)
    p = p[p >= 5]

    k = 8 - (p & 7)
    inv8 = (1 + k * p) // 8
    s = p - (3 * inv8) % p          # (-3*inv8) mod p; 3*inv8 % p is never 0
    return int(s.sum())

if __name__ == "__main__":
    print(solve())
