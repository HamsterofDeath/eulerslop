#!/usr/bin/env python3
"""Project Euler 853: Pisano periods equal to a prescribed value."""

from math import gcd


def fibonacci_pair(index: int, modulus: int) -> tuple[int, int]:
    """Return (F_index, F_(index+1)) modulo modulus by fast doubling."""
    if index == 0:
        return 0, 1 % modulus

    first, second = fibonacci_pair(index // 2, modulus)
    doubled = first * ((2 * second - first) % modulus) % modulus
    successor = (first * first + second * second) % modulus
    if index % 2:
        return successor, (doubled + successor) % modulus
    return doubled, successor


def factorize(number: int) -> dict[int, int]:
    factors = {}
    while number % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        number //= 2

    divisor = 3
    while divisor * divisor <= number:
        while number % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            number //= divisor
        divisor += 2
    if number > 1:
        factors[number] = 1
    return factors


def divisors(factors: dict[int, int]) -> list[int]:
    result = [1]
    for prime, exponent in factors.items():
        previous = result
        result = [
            divisor * prime_power
            for divisor in previous
            for prime_power in (prime**power for power in range(exponent + 1))
        ]
    return result


def is_identity(index: int, modulus: int) -> bool:
    return fibonacci_pair(index, modulus) == (0, 1 % modulus)


def has_exact_period(modulus: int, period: int) -> bool:
    """Test whether the Fibonacci transition matrix has this exact order."""
    if not is_identity(period, modulus):
        return False
    return all(
        not is_identity(period // prime, modulus)
        for prime in factorize(period)
    )


def sum_moduli(period: int, limit: int) -> int:
    # A period dividing k is equivalent to F_k = 0 and F_(k+1) = 1.
    first, second = 0, 1
    for _ in range(period):
        first, second = second, first + second
    common_modulus = gcd(first, second - 1)

    return sum(
        modulus
        for modulus in divisors(factorize(common_modulus))
        if modulus < limit and has_exact_period(modulus, period)
    )


def solve() -> int:
    assert sum_moduli(18, 50) == 57
    return sum_moduli(120, 1_000_000_000)


if __name__ == "__main__":
    print(solve())
