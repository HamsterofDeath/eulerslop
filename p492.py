#!/usr/bin/env python3
from math import isqrt


def _small_primes(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * ((limit - p * p) // p + 1)
    return [p for p in range(limit + 1) if sieve[p]]


BASE_PRIMES = _small_primes(40000)


def _primes_interval(lo, hi):
    mark = bytearray(b"\x01") * (hi - lo + 1)
    for p in BASE_PRIMES:
        if p * p > hi:
            break
        start = max(p * p, ((lo + p - 1) // p) * p)
        mark[start - lo:hi - lo + 1:p] = b"\x00" * ((hi - start) // p + 1)
    return [lo + i for i, ok in enumerate(mark) if ok]


def _mul(x, y, mod):
    a, b = x
    c, d = y
    return ((a * c + 117 * b * d) % mod, (a * d + b * c) % mod)


def _a_mod_prime(p, n):
    # b_n = 6a_n+5 gives b_{n+1}=b_n^2-2, b_1=11.  If alpha is a root of
    # z^2-11z+1, then b_n=alpha^(2^(n-1))+alpha^(-2^(n-1)).
    order = p - 1 if pow(117, (p - 1) // 2, p) == 1 else p + 1
    exponent = pow(2, n - 1, order)
    inv2 = (p + 1) // 2
    base = (11 * inv2 % p, inv2)  # (11 + sqrt(117)) / 2
    res = (1, 0)
    while exponent:
        if exponent & 1:
            res = _mul(res, base, p)
        base = _mul(base, base, p)
        exponent >>= 1
    b = 2 * res[0] % p
    return (b - 5) * pow(6, -1, p) % p


def B(x, y, n):
    return sum(_a_mod_prime(p, n) for p in _primes_interval(x, x + y))


def solve():
    assert _a_mod_prime(1_000_000_007, 6) == 203064689
    assert _a_mod_prime(1_000_000_007, 100) == 456482974
    assert B(10 ** 9, 10 ** 3, 10 ** 3) == 23674718882
    assert B(10 ** 9, 10 ** 3, 10 ** 15) == 20731563854
    return B(10 ** 9, 10 ** 7, 10 ** 15)


if __name__ == "__main__":
    print(solve())
