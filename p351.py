#!/usr/bin/env python3
import numpy as np


def solve():
    # By the hexagon's 6-fold symmetry, consider one sextant.  The points of
    # ring k (a regular hexagon of side k) split into 6 edges of k points
    # each; an edge's points are a*(k-j) + b*j for j = 0..k-1 with a, b the
    # two basis vectors spanning the sextant.  Such a point is visible from
    # the center iff gcd(k-j, j) = gcd(k, j) = 1, so each edge has phi(k)
    # visible points and k - phi(k) hidden ones.  Hence
    #   H(n) = 6 * sum_{k=1..n} (k - phi(k)) = 6 * (n(n+1)/2 - Phi(n))
    # where Phi is the totient summatory function, computed sublinearly via
    #   Phi(n) = n(n+1)/2 - sum_{d=2..n} Phi(n // d)
    # with the small values sieved directly.
    N = 10 ** 8
    L = 5 * 10 ** 6  # sieve limit for direct phi values

    phi = np.arange(L + 1, dtype=np.int64)
    for p in range(2, L + 1):
        if phi[p] == p:  # p is prime
            phi[p::p] -= phi[p::p] // p
    csum = np.cumsum(phi)  # csum[m] = Phi(m) for m <= L

    memo = {}

    def Phi(n):
        if n <= L:
            return int(csum[n])
        if n in memo:
            return memo[n]
        res = n * (n + 1) // 2
        i = 2
        while i <= n:
            q = n // i
            j = n // q  # largest i' with n // i' == q
            res -= (j - i + 1) * Phi(q)
            i = j + 1
        memo[n] = res
        return res

    return 6 * (N * (N + 1) // 2 - Phi(N))


if __name__ == "__main__":
    print(solve())
