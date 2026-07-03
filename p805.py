#!/usr/bin/env python3
"""Project Euler 805: shifted leading digit multiples."""

from functools import lru_cache
from math import gcd, isqrt


MOD = 1_000_000_007


def primes_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [p for p in range(limit + 1) if sieve[p]]


PRIMES = primes_to(10_000)


@lru_cache(maxsize=None)
def factor(n: int) -> tuple[tuple[int, int], ...]:
    result = []
    x = n
    for p in PRIMES:
        if p * p > x:
            break
        if x % p == 0:
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            result.append((p, e))
    if x > 1:
        result.append((x, 1))
    return tuple(result)


@lru_cache(maxsize=None)
def order10(modulus: int) -> int | None:
    if modulus == 1:
        return 1
    if gcd(modulus, 10) != 1:
        return None

    phi = modulus
    for p, _ in factor(modulus):
        phi = phi // p * (p - 1)

    order = phi
    for p, _ in factor(phi):
        while order % p == 0 and pow(10, order // p, modulus) == 1:
            order //= p
    return order


def leading_digit_is_valid(p: int, q: int, leading: int, digits: int) -> bool:
    if digits < 8 and p * 10 ** (digits - 1) < q:
        return False

    upper_coeff = 10 * q - (leading + 1) * p
    if upper_coeff >= 0:
        return True
    if digits >= 8:
        return False
    return leading * q > (-upper_coeff) * 10 ** (digits - 1)


def n_mod_for_ratio(p: int, q: int) -> int:
    if p >= 10 * q:
        return 0

    denominator = 10 * q - p
    best: tuple[int, int, int] | None = None
    for leading in range(1, 10):
        reduced = denominator // gcd(denominator, leading)
        digits = order10(reduced)
        if digits is None:
            continue
        if not leading_digit_is_valid(p, q, leading, digits):
            continue

        value = leading * q
        value %= MOD
        value *= pow(10, digits, MOD) - 1
        value %= MOD
        value *= pow(denominator, MOD - 2, MOD)
        value %= MOD
        candidate = (digits, leading, value)
        if best is None or candidate[:2] < best[:2]:
            best = candidate
    return 0 if best is None else best[2]


def t_value(limit: int) -> int:
    total = 0
    for u in range(1, limit + 1):
        p = u**3
        for v in range(1, limit + 1):
            if gcd(u, v) == 1:
                total += n_mod_for_ratio(p, v**3)
    return total % MOD


def solve() -> int:
    assert n_mod_for_ratio(3, 1) == 142857
    assert n_mod_for_ratio(1, 10) == 10
    assert n_mod_for_ratio(2, 1) == 0
    assert t_value(3) == 262429173
    return t_value(200)


if __name__ == "__main__":
    print(solve())
