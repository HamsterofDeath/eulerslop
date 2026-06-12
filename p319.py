#!/usr/bin/env python3
import numpy as np

def solve():
    # The two conditions x_{i-1} < x_i and x_i^j < (x_j+1)^i say exactly that
    # the half-open intervals [x_i^(1/i), (x_i+1)^(1/i)) have a common point c,
    # i.e. x_i = floor(c^i) for some real c; x_1 = 2 forces c in [2,3).
    # So t(n) = number of distinct tuples (floor(c^1),...,floor(c^n)), c in [2,3),
    # which is 1 + #{distinct c in (2,3) with c^i integer for some i <= n}.
    # With S_i = {c in (2,3): c^i in Z} (|S_i| = 3^i - 2^i - 1) and
    # S_i ∩ S_j = S_gcd(i,j), Mobius inversion over the divisor lattice gives
    #   t(n) = 1 + sum_{d=1}^{n} (3^d - 2^d - 1) * M(n // d)
    # where M is the Mertens function.  We evaluate M at all values floor(n/d)
    # by sieving mu up to 10^7 and using the standard O(n^(2/3)) recursion
    #   M(x) = 1 - sum_{k=2}^{x} M(x // k).
    n = 10 ** 10
    MOD = 10 ** 9

    # --- Mertens: sieve of mu up to L, prefix sums ---
    L = 10 ** 7
    mu = np.ones(L + 1, dtype=np.int8)
    is_comp = np.zeros(L + 1, dtype=bool)
    for p in range(2, int(L ** 0.5) + 1):
        if not is_comp[p]:
            is_comp[p * p::p] = True
            mu[p::p] *= -1
            mu[p * p::p * p] = 0
    # remaining primes > sqrt(L): flip sign for their multiples
    for p in range(int(L ** 0.5) + 1, L + 1):
        if not is_comp[p]:
            mu[p::p] *= -1
    mu[0] = 0
    mert = np.cumsum(mu, dtype=np.int64)

    cache = {}

    def M(x):
        if x <= L:
            return int(mert[x])
        if x in cache:
            return cache[x]
        res = 1
        k = 2
        while k <= x:
            q = x // k
            k2 = x // q  # largest k with same quotient
            res -= (k2 - k + 1) * M(q)
            k = k2 + 1
        cache[x] = res
        return res

    # --- main sum, in blocks of constant q = n // d ---
    MOD2 = 2 * MOD
    total = 0
    a = 1
    while a <= n:
        q = n // a
        b = n // q
        # sum_{d=a}^{b} 3^d = (3^(b+1) - 3^a)/2 : compute mod 2*MOD, halve
        s3 = (pow(3, b + 1, MOD2) - pow(3, a, MOD2)) % MOD2
        s3 = (s3 // 2) % MOD
        s2 = (pow(2, b + 1, MOD) - pow(2, a, MOD)) % MOD
        blocksum = (s3 - s2 - (b - a + 1)) % MOD
        total = (total + M(q) * blocksum) % MOD
        a = b + 1
    return (total + 1) % MOD  # +1 for the initial tuple at c = 2

if __name__ == "__main__":
    print(solve())
