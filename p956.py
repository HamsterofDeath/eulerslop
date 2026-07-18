#!/usr/bin/env python3
"""Project Euler Problem 956: Super Duper Sum.

For n=product(p**e), mark a divisor by x**Omega(d).  Its weighted
divisor polynomial is

    product_p (1 + p*x + ... + (p*x)**e).

A roots-of-unity filter at the m-th roots in the target finite field
extracts the coefficients whose degrees are divisible by m.  Each
factor is evaluated as a geometric sum by binary doubling.
"""

from math import isqrt


MODULUS = 999_999_001


def primes_through(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [
        value for value in range(2, limit + 1) if sieve[value]
    ]


def superduper_exponents(limit: int) -> list[tuple[int, int]]:
    result = []
    for prime in primes_through(limit):
        exponent = 0
        for factorial_index in range(1, limit + 1):
            quotient = factorial_index
            factorial_valuation = 0
            while quotient:
                quotient //= prime
                factorial_valuation += quotient
            exponent += (
                limit - factorial_index + 1
            ) * factorial_valuation
        result.append((prime, exponent))
    return result


def geometric_sum(base: int, terms: int, modulus: int) -> int:
    """Return 1+base+...+base**(terms-1) modulo modulus."""
    result_power = 1
    result_sum = 0
    block_power = base % modulus
    block_sum = 1

    while terms:
        if terms & 1:
            result_sum = (
                result_sum + result_power * block_sum
            ) % modulus
            result_power = result_power * block_power % modulus

        block_sum = (
            block_sum * (1 + block_power)
        ) % modulus
        block_power = block_power * block_power % modulus
        terms //= 2

    return result_sum


def distinct_prime_factors(value: int) -> list[int]:
    result = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            result.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        result.append(value)
    return result


def root_of_unity(order: int, modulus: int) -> int:
    assert (modulus - 1) % order == 0
    factors = distinct_prime_factors(order)

    candidate = 2
    while True:
        root = pow(candidate, (modulus - 1) // order, modulus)
        if (
            pow(root, order, modulus) == 1
            and all(
                pow(root, order // prime, modulus) != 1
                for prime in factors
            )
        ):
            return root
        candidate += 1


def filtered_divisor_sum(limit: int, divisor: int) -> int:
    exponents = superduper_exponents(limit)
    root = root_of_unity(divisor, MODULUS)

    total = 0
    root_power = 1
    for _ in range(divisor):
        evaluation = 1
        for prime, exponent in exponents:
            evaluation = (
                evaluation
                * geometric_sum(
                    prime * root_power % MODULUS,
                    exponent + 1,
                    MODULUS,
                )
                % MODULUS
            )
        total = (total + evaluation) % MODULUS
        root_power = root_power * root % MODULUS

    assert root_power == 1
    return total * pow(divisor, -1, MODULUS) % MODULUS


def solve() -> int:
    sample = 6_368_195_719_791_280
    assert filtered_divisor_sum(6, 6) == sample % MODULUS
    return filtered_divisor_sum(1000, 1000)


if __name__ == "__main__":
    print(solve())
