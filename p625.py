#!/usr/bin/env python3
from functools import lru_cache


MOD = 998244353
N = 10**11
LIMIT = 5_000_000
INV2 = (MOD + 1) // 2


def totient_prefix(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for multiple in range(p, limit + 1, p):
                phi[multiple] -= phi[multiple] // p

    total = 0
    for i in range(1, limit + 1):
        total = (total + phi[i]) % MOD
        phi[i] = total
    return phi


PHI_PREFIX = totient_prefix(LIMIT)


def triangle(n):
    return (n % MOD) * ((n + 1) % MOD) % MOD * INV2 % MOD


@lru_cache(maxsize=None)
def sum_phi(n):
    if n <= LIMIT:
        return PHI_PREFIX[n]

    total = triangle(n)
    left = 2
    while left <= n:
        quotient = n // left
        right = n // quotient
        total -= ((right - left + 1) % MOD) * sum_phi(quotient)
        total %= MOD
        left = right + 1
    return total


def solve(n=N):
    # gcd(a,b) = sum_{d|a,b} phi(d). Symmetry gives
    # 2G(n)-n(n+1)/2 = sum_{a,b<=n} gcd(a,b).
    total = 0
    left = 1
    while left <= n:
        quotient = n // left
        right = n // quotient
        block = (sum_phi(right) - sum_phi(left - 1)) % MOD
        total = (total + block * (quotient % MOD) * (quotient % MOD)) % MOD
        left = right + 1

    return (total + triangle(n)) * INV2 % MOD


if __name__ == "__main__":
    print(solve())
