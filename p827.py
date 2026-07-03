#!/usr/bin/env python3
"""Project Euler 827: smallest integer in exactly n Pythagorean triples."""

from functools import lru_cache
from math import gcd, log
import random


MOD = 409_120_391
SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
INF = (float("inf"), 0)
random.seed(827)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in SMALL_PRIMES:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    while True:
        c = random.randrange(1, n - 1)
        x = random.randrange(2, n - 1)
        y = x
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d


@lru_cache(maxsize=None)
def factor_tuple(n: int) -> tuple[int, ...]:
    if n == 1:
        return ()
    if is_prime(n):
        return (n,)
    d = pollard_rho(n)
    return tuple(sorted(factor_tuple(d) + factor_tuple(n // d)))


@lru_cache(maxsize=None)
def factor_items(n: int) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for p in factor_tuple(n):
        counts[p] = counts.get(p, 0) + 1
    return tuple(sorted(counts.items()))


@lru_cache(maxsize=None)
def divisors(n: int) -> tuple[int, ...]:
    result = [1]
    for p, exponent in factor_items(n):
        next_result = []
        power = 1
        for _ in range(exponent + 1):
            next_result.extend(d * power for d in result)
            power *= p
        result = next_result
    return tuple(sorted(result))


def primes_mod_4(remainder: int, count: int) -> tuple[int, ...]:
    result = []
    candidate = 2
    while len(result) < count:
        if candidate % 4 == remainder and is_prime(candidate):
            result.append(candidate)
        candidate += 1
    return tuple(result)


PRIMES_1_MOD_4 = primes_mod_4(1, 80)
PRIMES_3_MOD_4 = primes_mod_4(3, 80)
LOGS_1_MOD_4 = tuple(log(p) for p in PRIMES_1_MOD_4)
LOGS_3_MOD_4 = tuple(log(p) for p in PRIMES_3_MOD_4)


@lru_cache(maxsize=None)
def min_product_for_count(
    divisor_count: int, prime_kind: int, prime_index: int, max_factor: int
) -> tuple[float, int]:
    if divisor_count == 1:
        return 0.0, 1
    if divisor_count % 2 == 0:
        return INF

    primes = PRIMES_1_MOD_4 if prime_kind == 1 else PRIMES_3_MOD_4
    logs = LOGS_1_MOD_4 if prime_kind == 1 else LOGS_3_MOD_4
    if prime_index >= len(primes):
        return INF

    best = INF
    for factor in divisors(divisor_count):
        if factor == 1:
            continue
        if factor > max_factor:
            break
        if factor % 2 == 0:
            continue
        tail_log, tail_mod = min_product_for_count(
            divisor_count // factor, prime_kind, prime_index + 1, factor
        )
        if tail_log == float("inf"):
            continue
        exponent = (factor - 1) // 2
        candidate = (
            exponent * logs[prime_index] + tail_log,
            pow(primes[prime_index], exponent, MOD) * tail_mod % MOD,
        )
        if candidate[0] < best[0]:
            best = candidate
    return best


def min_product(divisor_count: int, prime_kind: int) -> tuple[float, int]:
    if divisor_count == 1:
        return 0.0, 1
    return min_product_for_count(divisor_count, prime_kind, 0, divisor_count)


@lru_cache(maxsize=None)
def min_non_1_mod_4_product(count_factor: int) -> tuple[float, int]:
    if count_factor == 1:
        return 0.0, 1
    if count_factor % 2 == 0:
        return INF

    # Either use only primes 3 mod 4, or assign one odd factor to prime 2.
    best = min_product(count_factor, 3)
    for factor in divisors(count_factor):
        if factor == 1 or factor % 2 == 0:
            continue
        tail_log, tail_mod = min_product(count_factor // factor, 3)
        if tail_log == float("inf"):
            continue
        exponent = (factor + 1) // 2
        candidate = (
            exponent * log(2) + tail_log,
            pow(2, exponent, MOD) * tail_mod % MOD,
        )
        if candidate[0] < best[0]:
            best = candidate
    return best


def q_mod(target: int) -> int:
    # If B is the contribution from primes 1 mod 4 and E is the contribution
    # from the other primes, then B(E + 1) = 2(target + 1).
    total = 2 * (target + 1)
    best = INF
    for b_factor in divisors(target + 1):
        if b_factor % 2 == 0:
            continue
        e_factor = total // b_factor - 1
        if e_factor % 2 == 0:
            continue

        b_log, b_mod = min_product(b_factor, 1)
        e_log, e_mod = min_non_1_mod_4_product(e_factor)
        candidate = b_log + e_log, b_mod * e_mod % MOD
        if candidate[0] < best[0]:
            best = candidate
    return best[1]


def solve() -> int:
    assert q_mod(5) == 15
    assert q_mod(10) == 48
    assert q_mod(10**3) == 8_064_000
    return sum(q_mod(10**k) for k in range(1, 19)) % MOD


if __name__ == "__main__":
    print(solve())
