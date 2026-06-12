#!/usr/bin/env python3
from math import isqrt


def _small_primes(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * ((limit - p * p) // p + 1)
    return [p for p in range(limit + 1) if sieve[p]]


SMALL_PRIMES = _small_primes(50000)


def _is_prime(n):
    for p in SMALL_PRIMES:
        if p * p > n:
            return True
        if n % p == 0:
            return False
    return True


def _power_sum(k, n, mod):
    # F_k(x)=sum_{i<=x} i^k is a degree k+1 polynomial.  Since mod > k+1,
    # interpolate it from F_k(0),...,F_k(k+1) at x=n mod mod.
    degree = k + 1
    x = n % mod
    if x <= degree:
        return sum(pow(i, k, mod) for i in range(1, x + 1)) % mod

    y = [0] * (degree + 1)
    acc = 0
    for i in range(1, degree + 1):
        acc = (acc + pow(i, k, mod)) % mod
        y[i] = acc

    pref = [1] * (degree + 2)
    for i in range(degree + 1):
        pref[i + 1] = pref[i] * (x - i) % mod
    suff = [1] * (degree + 2)
    for i in range(degree, -1, -1):
        suff[i] = suff[i + 1] * (x - i) % mod
    fact = [1] * (degree + 1)
    for i in range(1, degree + 1):
        fact[i] = fact[i - 1] * i % mod

    total = 0
    for i, yi in enumerate(y):
        num = pref[i] * suff[i + 1] % mod
        den = fact[i] * fact[degree - i] % mod
        term = yi * num % mod * pow(den, mod - 2, mod) % mod
        total += -term if (degree - i) & 1 else term
    return total % mod


def _S(k, n, mod):
    return ((n + 1) % mod * _power_sum(k, n, mod)
            - _power_sum(k + 1, n, mod)) % mod


def solve():
    assert _S(4, 100, 1_000_000_007) == 35375333830 % 1_000_000_007
    primes = [p for p in range(2_000_000_000, 2_000_002_001) if _is_prime(p)]
    return sum(_S(10000, 10 ** 12, p) for p in primes)


if __name__ == "__main__":
    print(solve())
