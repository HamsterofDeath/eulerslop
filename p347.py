#!/usr/bin/env python3
import numpy as np

def solve():
    # M(p,q,N) = largest p^a * q^b <= N (a,b >= 1) for distinct primes p < q.
    # All M(p,q,N) are distinct (unique factorization), so S(N) is just the sum
    # over all prime pairs p < q with p*q <= N.
    N = 10 ** 7

    # Sieve primes up to N//2 (largest possible q is paired with p = 2).
    limit = N // 2
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    primes = np.flatnonzero(sieve)
    primes_list = primes.tolist()

    total = 0
    for i, p in enumerate(primes_list):
        if p * p >= N:
            break
        K = N // p
        # all primes q with p < q <= N // p
        hi = int(np.searchsorted(primes, K, side="right"))
        for q in primes_list[i + 1:hi]:
            best = 0
            pa = p
            while pa * q <= N:
                m = pa * q
                while m * q <= N:  # raise the power of q as far as possible
                    m *= q
                if m > best:
                    best = m
                pa *= p  # try a higher power of p
            total += best
    return total

if __name__ == "__main__":
    print(solve())
