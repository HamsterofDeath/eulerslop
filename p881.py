#!/usr/bin/env python3
"""Project Euler 881: minimize a divisor-lattice level width."""

from math import comb, prod


TARGET = 10_000


def first_primes(count: int) -> list[int]:
    primes: list[int] = []
    candidate = 2
    while len(primes) < count:
        if all(candidate % prime for prime in primes if prime * prime <= candidate):
            primes.append(candidate)
        candidate += 1
    return primes


def extend_coefficients(coefficients: list[int], exponent: int) -> list[int]:
    """Multiply a coefficient list by 1+x+...+x^exponent."""
    result = [0] * (len(coefficients) + exponent)
    window_sum = 0
    for degree in range(len(result)):
        if degree < len(coefficients):
            window_sum += coefficients[degree]
        if degree - exponent - 1 >= 0:
            window_sum -= coefficients[degree - exponent - 1]
        result[degree] = window_sum
    return result


def maximum_level_size(exponents: list[int]) -> int:
    coefficients = [1]
    for exponent in exponents:
        coefficients = extend_coefficients(coefficients, exponent)
    return max(coefficients)


def smallest_number(target: int) -> int:
    """Find the least n whose widest divisor-lattice level reaches target.

    If n has prime exponents e_i, the sizes of its levels are the
    coefficients of

        product_i (1+x+...+x^e_i).

    For a fixed exponent multiset, the least n assigns nonincreasing
    exponents to increasing primes.  The DFS therefore enumerates every
    relevant exponent partition exactly once and prunes as soon as its
    partial integer reaches the best complete candidate.
    """
    prime_count = 1
    while comb(prime_count, prime_count // 2) < target:
        prime_count += 1
    primes = first_primes(prime_count)

    # All exponents equal to one give an immediate valid upper bound.
    best = prod(primes)

    def search(
        prime_index: int,
        maximum_exponent: int,
        value: int,
        coefficients: list[int],
    ) -> None:
        nonlocal best
        if max(coefficients) >= target:
            best = min(best, value)
            return
        if prime_index >= prime_count:
            return

        prime = primes[prime_index]
        prime_power = 1
        for exponent in range(1, maximum_exponent + 1):
            prime_power *= prime
            next_value = value * prime_power
            if next_value >= best:
                break
            search(
                prime_index + 1,
                exponent,
                next_value,
                extend_coefficients(coefficients, exponent),
            )

    search(0, best.bit_length(), 1, [1])
    return best


def solve() -> int:
    assert maximum_level_size([1, 1]) == 2
    assert maximum_level_size([4, 2, 1, 1]) == 12
    return smallest_number(TARGET)


if __name__ == "__main__":
    print(solve())
