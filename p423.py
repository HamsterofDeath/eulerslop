#!/usr/bin/env python3
import numpy as np
from array import array

MOD = 1_000_000_007
L = 50_000_000


def solve():
    # A sequence of n throws is determined by the first value (6 ways) and, for
    # each of the n-1 following throws, whether it equals its predecessor (1 way)
    # or not (5 ways).  Hence exactly c equal adjacent pairs occur in
    # 6 * binom(n-1, c) * 5^(n-1-c) sequences, so
    #   C(n) = 6 * t_n,   t_n = sum_{c=0}^{pi(n)} binom(n-1, c) * 5^(n-1-c).
    # Pascal's rule gives, with k = pi(n),
    #   sum_{c=0}^{k} binom(n, c) 5^(n-c) = 6*t_n - binom(n-1, k) 5^(n-1-k),
    # and when n+1 is prime one extra term binom(n, k+1) 5^(n-1-k) is added.
    # We maintain t, B = binom(n-1, k) and pw = 5^(n-1-k) incrementally in O(L).

    # Sieve of Eratosthenes up to L (need primality of every n <= L).
    sieve = np.ones(L + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(L ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    is_prime = sieve.tobytes()
    del sieve

    # Modular inverses 1..L via the standard linear recurrence.
    typ = 'I' if array('I').itemsize == 4 else 'L'
    inv = array(typ, bytes(array(typ).itemsize * (L + 1)))
    inv[1] = 1
    M = MOD
    for i in range(2, L + 1):
        inv[i] = (M - M // i) * inv[M % i] % M

    t = 1   # t_1: pi(1)=0, single term binom(0,0)*5^0
    S = 1   # running sum of t_n
    B = 1   # binom(n-1, pi(n))
    pw = 1  # 5^(n-1-pi(n))
    k = 0   # pi(n)
    for n in range(1, L):
        U = (6 * t - B * pw) % M
        if is_prime[n + 1]:
            # pi increments: binom(n, k+1) = binom(n-1, k) * n / (k+1);
            # the exponent n-1-k is unchanged.
            k += 1
            B = B * n % M * inv[k] % M
            t = (U + B * pw) % M
        else:
            # binom(n, k) = binom(n-1, k) * n / (n-k); exponent grows by 1.
            B = B * n % M * inv[n - k] % M
            pw = pw * 5 % M
            t = U
        S += t  # t < MOD, L terms: fits comfortably in a Python int
    return 6 * S % M


if __name__ == "__main__":
    print(solve())
