#!/usr/bin/env python3
from sys import setrecursionlimit


N = 10**11
MOD = 1_000_000_007
PRECOMPUTE = 5_000_000
INV2 = (MOD + 1) // 2


def _totient_prefix(limit):
    phi = [0] * (limit + 1)
    phi[1] = 1
    primes = []
    composite = bytearray(limit + 1)

    for n in range(2, limit + 1):
        if not composite[n]:
            primes.append(n)
            phi[n] = n - 1
        for p in primes:
            m = n * p
            if m > limit:
                break
            composite[m] = 1
            if n % p == 0:
                phi[m] = phi[n] * p
                break
            phi[m] = phi[n] * (p - 1)

    total = 0
    for n in range(1, limit + 1):
        total = (total + phi[n]) % MOD
        phi[n] = total
    return phi


PHI_PREFIX = _totient_prefix(PRECOMPUTE)
PHI_SUM_CACHE = {}


def totient_sum(n):
    if n <= PRECOMPUTE:
        return PHI_PREFIX[n]
    cached = PHI_SUM_CACHE.get(n)
    if cached is not None:
        return cached

    total = (n % MOD) * ((n + 1) % MOD) * INV2 % MOD
    left = 2
    while left <= n:
        quotient = n // left
        right = n // quotient
        total -= ((right - left + 1) % MOD) * totient_sum(quotient)
        total %= MOD
        left = right + 1

    PHI_SUM_CACHE[n] = total
    return total


def friendly_pairs(limit):
    # gcd(p, q) = 2^t iff p=2^t a, q=2^t b and gcd(a, b)=1.
    # For each t, unordered coprime pairs a<b<=m are sum_{k=2..m} phi(k).
    total = 0
    power = 2
    while power <= limit:
        total += totient_sum(limit // power) - 1
        total %= MOD
        power <<= 1
    return total


def solve():
    assert friendly_pairs(10**2) == 1031
    assert friendly_pairs(10**6) == 321_418_433
    return friendly_pairs(N)


if __name__ == "__main__":
    setrecursionlimit(10_000)
    print(solve())
