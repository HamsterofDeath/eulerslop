#!/usr/bin/env python3
"""Project Euler 843: periods of the circular neighbour-difference map."""

from functools import lru_cache
from math import isqrt, lcm
import random


random.seed(843)


def degree(poly: int) -> int:
    return poly.bit_length() - 1


def poly_divmod(a: int, b: int) -> tuple[int, int]:
    q = 0
    db = degree(b)
    while a and degree(a) >= db:
        shift = degree(a) - db
        q ^= 1 << shift
        a ^= b << shift
    return q, a


def poly_div_exact(a: int, b: int) -> int:
    q, r = poly_divmod(a, b)
    assert r == 0
    return q


def poly_mod(a: int, modulus: int) -> int:
    return poly_divmod(a, modulus)[1]


def poly_gcd(a: int, b: int) -> int:
    while b:
        a, b = b, poly_mod(a, b)
    return a


def poly_mul_mod(a: int, b: int, modulus: int) -> int:
    result = 0
    a = poly_mod(a, modulus)
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if degree(a) >= degree(modulus):
            a = poly_mod(a, modulus)
    return poly_mod(result, modulus)


def poly_pow_mod(a: int, exponent: int, modulus: int) -> int:
    result = 1
    a = poly_mod(a, modulus)
    while exponent:
        if exponent & 1:
            result = poly_mul_mod(result, a, modulus)
        exponent >>= 1
        if exponent:
            a = poly_mul_mod(a, a, modulus)
    return result


def divisors(n: int) -> list[int]:
    result = []
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            result.append(d)
            if d * d != n:
                result.append(n // d)
    return sorted(result)


@lru_cache(maxsize=None)
def odd_cyclotomic(order: int) -> int:
    # Over GF(2), x^order - 1 is x^order + 1.
    poly = (1 << order) | 1
    for d in divisors(order):
        if d < order:
            poly = poly_div_exact(poly, odd_cyclotomic(d))
    return poly


def equal_degree_factors(poly: int, factor_degree: int) -> list[int]:
    if poly == 1:
        return []
    if degree(poly) == factor_degree:
        return [poly]
    if factor_degree == 1:
        factors = []
        for linear in (0b10, 0b11):
            g = poly_gcd(poly, linear)
            if g != 1:
                factors.append(g)
                poly = poly_div_exact(poly, g)
        assert poly == 1
        return factors

    while True:
        candidate = random.randrange(2, 1 << degree(poly))
        trace = 0
        term = candidate
        for _ in range(factor_degree):
            trace ^= term
            term = poly_mul_mod(term, term, poly)
        g = poly_gcd(poly, trace)
        if g != 1 and g != poly:
            return equal_degree_factors(g, factor_degree) + equal_degree_factors(
                poly_div_exact(poly, g), factor_degree
            )


def squarefree_factors(poly: int) -> list[int]:
    factors = []
    remaining = poly
    h = 0b10
    factor_degree = 1

    while remaining != 1 and 2 * factor_degree <= degree(remaining):
        h = poly_mul_mod(h, h, remaining)
        g = poly_gcd(remaining, h ^ 0b10)
        if g != 1:
            factors.extend(equal_degree_factors(g, factor_degree))
            remaining = poly_div_exact(remaining, g)
            h = poly_mod(h, remaining) if remaining != 1 else 0
        factor_degree += 1

    if remaining != 1:
        factors.append(remaining)
    return factors


def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small_primes:
        if n % p == 0:
            return n == p

    d = n - 1
    shift = 0
    while d % 2 == 0:
        d //= 2
        shift += 1
    for base in small_primes:
        x = pow(base, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(shift - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
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


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def factor_integer(n: int, factors: list[int]) -> None:
    if n == 1:
        return
    if is_probable_prime(n):
        factors.append(n)
        return
    d = pollard_rho(n)
    factor_integer(d, factors)
    factor_integer(n // d, factors)


@lru_cache(maxsize=None)
def component_orders(root_order: int) -> tuple[int, ...]:
    orders = []
    eigenvalue = (1 << 1) ^ (1 << (root_order - 1))
    for factor in squarefree_factors(odd_cyclotomic(root_order)):
        order = (1 << degree(factor)) - 1
        prime_factors: list[int] = []
        factor_integer(order, prime_factors)
        for p in set(prime_factors):
            while order % p == 0 and poly_pow_mod(eigenvalue, order // p, factor) == 1:
                order //= p
        orders.append(order)
    return tuple(sorted(orders))


def periods_for_size(size: int) -> set[int]:
    two_power = 0
    odd_part = size
    while odd_part % 2 == 0:
        two_power += 1
        odd_part //= 2

    periods = {1}
    for root_order in divisors(odd_part):
        if root_order == 1:
            continue
        for odd_order in component_orders(root_order):
            choices = [1] + [odd_order * (1 << b) for b in range(two_power + 1)]
            periods = {lcm(period, choice) for period in periods for choice in choices}
    return periods


def s_value(limit: int) -> int:
    possible_periods = set()
    for size in range(3, limit + 1):
        possible_periods.update(periods_for_size(size))
    return sum(possible_periods)


def solve() -> int:
    assert s_value(6) == 6
    assert s_value(30) == 20381
    return s_value(100)


if __name__ == "__main__":
    print(solve())
