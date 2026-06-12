#!/usr/bin/env python3
from math import isqrt

MOD = 1_000_000_007


def _primes_upto(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            sieve[p * p:n + 1:p] = b"\x00" * ((n - p * p) // p + 1)
    return [p for p in range(n + 1) if sieve[p]]


def _factor_exponents_factorial(n):
    out = []
    for p in _primes_upto(n):
        e = 0
        q = p
        while q <= n:
            e += n // q
            q *= p
        out.append(e)
    return out


def _factor_exponents(n):
    out = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out.append(e)
        p += 1
    if n > 1:
        out.append(1)
    return out


def _partitions(n, max_part=None):
    if max_part is None or max_part > n:
        max_part = n
    if n == 0:
        yield {}
        return
    if max_part == 0:
        return
    for m in range(n // max_part + 1):
        for rest in _partitions(n - m * max_part, max_part - 1):
            if m:
                rest = rest.copy()
                rest[max_part] = m
            yield rest


def W_from_exponents(exponents, k):
    inv = [0] + [pow(i, MOD - 2, MOD) for i in range(1, k + 1)]
    invfact = [1] * (k + 1)
    fact = 1
    for i in range(1, k + 1):
        fact = fact * i % MOD
        invfact[i] = pow(fact, MOD - 2, MOD)

    multiplicity = {}
    for e in exponents:
        multiplicity[e] = multiplicity.get(e, 0) + 1
    max_e = max(multiplicity, default=0)

    ans = 0
    for blocks in _partitions(k):
        weight = 1
        sign = 0
        sizes = []
        for s, m in blocks.items():
            sign += (s - 1) * m
            weight = weight * pow(inv[s], m, MOD) % MOD * invfact[m] % MOD
            sizes.extend([s] * m)
        if sign & 1:
            weight = -weight % MOD

        coeff = [0] * (max_e + 1)
        coeff[0] = 1
        for s in sizes:
            new = coeff[:]
            for r in range(s, max_e + 1):
                new[r] = (new[r] + new[r - s]) % MOD
            coeff = new

        prod = 1
        for e, count in multiplicity.items():
            prod = prod * pow(coeff[e], count, MOD) % MOD
            if prod == 0:
                break
        ans = (ans + weight * prod) % MOD
    return ans


def solve():
    assert W_from_exponents(_factor_exponents(144), 4) == 7
    assert W_from_exponents(_factor_exponents_factorial(100), 10) == 287549200
    return W_from_exponents(_factor_exponents_factorial(10000), 30)


if __name__ == "__main__":
    print(solve())
