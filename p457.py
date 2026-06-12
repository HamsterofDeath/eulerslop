#!/usr/bin/env python3
from math import isqrt


def _primes_upto(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * ((limit - p * p) // p + 1)
    return [p for p in range(limit + 1) if sieve[p]]


def _sqrt_mod(a, p):
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    q = p - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while t != 1:
        i = 1
        tt = t * t % p
        while tt != 1:
            tt = tt * tt % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * c % p
        r = r * b % p
    return r


def R(p):
    if p in (2, 13):
        return 0
    r = _sqrt_mod(13, p)
    if r is None:
        return 0

    # Lift r^2 == 13 (mod p) to rr^2 == 13 (mod p^2).
    t = (-((r * r - 13) // p) * pow(2 * r, -1, p)) % p
    rr = r + t * p
    mod = p * p
    inv2 = (mod + 1) // 2
    return min((3 + rr) * inv2 % mod, (3 - rr) * inv2 % mod)


def solve():
    return sum(R(p) for p in _primes_upto(10 ** 7))


if __name__ == "__main__":
    print(solve())
