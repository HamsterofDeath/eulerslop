#!/usr/bin/env python3
"""Project Euler 812: dynamical polynomials."""

from math import isqrt


MOD = 998_244_353
INV2 = (MOD + 1) // 2
DEGREE = 10_000


def primes_up_to(limit: int) -> list[int]:
    sieve = [True] * (limit + 1)
    sieve[:2] = [False, False]
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            for q in range(p * p, limit + 1, p):
                sieve[q] = False
    return [p for p, ok in enumerate(sieve) if ok]


def odd_orders_with_small_phi(limit: int) -> list[tuple[int, int]]:
    primes = [p for p in primes_up_to(limit + 1) if p % 2 == 1]
    result: list[tuple[int, int]] = []

    def search(start: int, value: int, phi: int) -> None:
        if value > 1:
            result.append((value, phi))
        for index in range(start, len(primes)):
            p = primes[index]
            if phi * (p - 1) > limit:
                break
            next_value = value * p
            next_phi = phi * (p - 1)
            while next_phi <= limit:
                search(index + 1, next_value, next_phi)
                next_value *= p
                next_phi *= p

    search(0, 1, 1)
    return result


def ramified_order_one_chain(limit: int) -> list[int]:
    # The order 2 factor maps to the order 4 factor with multiplicity two:
    # Psi_2(x^2 - 2) = x^2 = Psi_4(x)^2.
    plus = [0] * (limit + 1)
    minus = [0] * (limit + 1)
    plus[0] = minus[0] = 1

    size = 2
    while size <= limit:
        for i in range(size, limit + 1):
            plus[i] = (plus[i] + plus[i - size]) % MOD

        old = minus
        minus = old[:]
        for i in range(size, limit + 1):
            minus[i] = (old[i] - minus[i - size]) % MOD
        size *= 2

    result = [0] * (limit + 1)
    for i in range(limit + 1):
        result[i] = (plus[i] + minus[i]) * INV2 % MOD
        if i:
            result[i] = (result[i] + (plus[i - 1] - minus[i - 1]) * INV2) % MOD

    for i in range(1, limit + 1):
        result[i] = (result[i] + result[i - 1]) % MOD
    for i in range(2, limit + 1):
        result[i] = (result[i] + result[i - 2]) % MOD
    return result


def coefficient(limit: int) -> int:
    multiplicity = [0] * (limit + 1)
    for _, phi in odd_orders_with_small_phi(2 * limit):
        part = phi // 2
        while part <= limit:
            multiplicity[part] += 1
            part *= 2

    dp = ramified_order_one_chain(limit)
    for part, count in enumerate(multiplicity):
        if part == 0:
            continue
        for _ in range(count):
            for total in range(part, limit + 1):
                dp[total] = (dp[total] + dp[total - part]) % MOD
    return dp[limit]


def solve() -> int:
    assert coefficient(2) == 6
    assert coefficient(5) == 58
    assert coefficient(20) == 122_087
    return coefficient(DEGREE)


if __name__ == "__main__":
    print(solve())
