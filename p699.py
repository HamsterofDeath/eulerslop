#!/usr/bin/env python3
"""Project Euler 699: Triffle Numbers."""

from collections import deque
from math import gcd


LIMIT = 10**14


def _is_prime(n):
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small_primes:
        if n % p == 0:
            return n == p

    d = n - 1
    shifts = 0
    while d % 2 == 0:
        shifts += 1
        d //= 2

    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % n == 0:
            continue
        x = pow(base, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(shifts - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True


def _pollard_rho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    c = 1
    while True:
        x = 2
        y = 2
        divisor = 1

        while divisor == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            divisor = gcd(abs(x - y), n)

        if divisor != n:
            return divisor
        c += 1


_FACTOR_CACHE = {1: {}}


def _factor_into(n, factors):
    if n == 1:
        return
    if _is_prime(n):
        factors[n] = factors.get(n, 0) + 1
        return

    divisor = _pollard_rho(n)
    _factor_into(divisor, factors)
    _factor_into(n // divisor, factors)


def _factor(n):
    cached = _FACTOR_CACHE.get(n)
    if cached is not None:
        return cached.copy()

    original = n
    factors = {}
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p

    _factor_into(n, factors)
    _FACTOR_CACHE[original] = factors.copy()
    return factors


def _divisors(factors):
    result = [1]
    for p, exponent in factors.items():
        base = result[:]
        power = 1
        for _ in range(exponent):
            power *= p
            result.extend(d * power for d in base)
    return result


def _sigma_from_factors(factors):
    total = 1
    for p, exponent in factors.items():
        total *= (p ** (exponent + 1) - 1) // (p - 1)
    return total


def _v3(n):
    exponent = 0
    while n % 3 == 0:
        exponent += 1
        n //= 3
    return exponent


def _cofactors(c, limit):
    """Generate m <= limit, gcd(m, 3)=1, with m | c*sigma(m)."""
    c_factors = _factor(c)
    seen = set()
    valid = []
    queue = deque()

    def push(factors):
        m = 1
        for p, exponent in factors.items():
            m *= p**exponent

        if m > limit or m % 3 == 0 or m in seen:
            return

        sigma = _sigma_from_factors(factors)
        seen.add(m)
        queue.append((m, tuple(sorted(factors.items())), sigma))
        if c * sigma % m == 0:
            valid.append((m, sigma))

    for divisor in _divisors(c_factors):
        push(_factor(divisor))

    power = 2
    exponent = 1
    while power <= limit:
        push({2: exponent})
        exponent += 1
        power *= 2

    for p in c_factors:
        power = p
        exponent = 1
        while power <= limit:
            push({p: exponent})
            exponent += 1
            power *= p

    while queue:
        m, items, sigma = queue.popleft()
        factors = dict(items)

        for p in sorted(_factor(c * sigma)):
            if p == 3:
                continue

            multiplier = 1
            extra = 0
            while m * multiplier * p <= limit:
                multiplier *= p
                extra += 1
                next_factors = factors.copy()
                next_factors[p] = next_factors.get(p, 0) + extra
                push(next_factors)

    return valid


def solve():
    total = 0
    power_of_3 = 1

    for exponent in range(1, 30):
        power_of_3 *= 3
        c = (3 ** (exponent + 1) - 1) // 2
        limit = LIMIT // power_of_3

        cofactor_sum = sum(
            m for m, sigma in _cofactors(c, limit)
            if exponent > _v3(sigma)
        )
        total += power_of_3 * cofactor_sum

    return total


if __name__ == "__main__":
    print(solve())
