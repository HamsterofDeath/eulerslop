#!/usr/bin/env python3
"""Project Euler 829: binary factor tree shapes."""

from functools import lru_cache
from math import isqrt


def first_primes(count: int) -> list[int]:
    primes = []
    candidate = 2
    while len(primes) < count:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes


@lru_cache(maxsize=None)
def factor_tuple(n: int) -> tuple[tuple[int, int], ...]:
    result = []
    p = 2
    while p * p <= n:
        exponent = 0
        while n % p == 0:
            exponent += 1
            n //= p
        if exponent:
            result.append((p, exponent))
        p += 1 if p == 2 else 2
    if n > 1:
        result.append((n, 1))
    return tuple(result)


@lru_cache(maxsize=None)
def divisors(factors: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    result = [1]
    for p, exponent in factors:
        next_result = []
        power = 1
        for _ in range(exponent + 1):
            next_result.extend(d * power for d in result)
            power *= p
        result = next_result
    return tuple(sorted(result))


def multiply_factors(
    left: tuple[tuple[int, int], ...], right: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, int], ...]:
    result = dict(left)
    for p, exponent in right:
        result[p] = result.get(p, 0) + exponent
    return tuple(sorted(result.items()))


def is_closest_split(left: int, right: int, factors: tuple[tuple[int, int], ...]) -> bool:
    root = isqrt(left * right)
    for divisor in divisors(factors):
        if divisor > left:
            return divisor > root
    return True


@lru_cache(maxsize=None)
def tree_shape(n: int):
    factors = factor_tuple(n)
    if sum(exponent for _, exponent in factors) == 1:
        return "P"

    root = isqrt(n)
    left = max(d for d in divisors(factors) if 1 < d <= root)
    return (tree_shape(left), tree_shape(n // left))


def double_factorial(n: int) -> int:
    result = 1
    for value in range(n, 0, -2):
        result *= value
    return result


def candidate_function(limit: int):
    primes = first_primes(limit)

    @lru_cache(maxsize=None)
    def candidates(shape):
        if shape == "P":
            return tuple((p, ((p, 1),)) for p in primes)

        by_value = {}
        for left, left_factors in candidates(shape[0]):
            for right, right_factors in candidates(shape[1]):
                if left > right:
                    continue
                factors = multiply_factors(left_factors, right_factors)
                if is_closest_split(left, right, factors):
                    by_value.setdefault(left * right, factors)
        return tuple((value, by_value[value]) for value in sorted(by_value)[:limit])

    return candidates


def combine_all(left_candidates, right_candidates):
    by_value = {}
    for left, left_factors in left_candidates:
        for right, right_factors in right_candidates:
            if left > right:
                continue
            factors = multiply_factors(left_factors, right_factors)
            if is_closest_split(left, right, factors):
                by_value.setdefault(left * right, factors)
    return tuple((value, by_value[value]) for value in sorted(by_value))


def solve() -> int:
    shapes = {n: tree_shape(double_factorial(n)) for n in range(2, 32)}
    candidates80 = candidate_function(80)
    candidates150 = candidate_function(150)

    values = {}
    for n in range(2, 32):
        if n == 28:
            values[n] = candidates150(shapes[n])[0][0]
        elif n == 31:
            left_shape, right_shape = shapes[n]
            left_candidates = candidates150(left_shape)
            right_candidates = combine_all(
                candidates150(right_shape[0]), candidates150(right_shape[1])
            )

            roots = []
            for left, left_factors in left_candidates:
                for right, right_factors in right_candidates:
                    if left > right:
                        continue
                    factors = multiply_factors(left_factors, right_factors)
                    if is_closest_split(left, right, factors):
                        roots.append(left * right)
            values[n] = min(roots)
        else:
            values[n] = candidates80(shapes[n])[0][0]

    assert values[9] == 72
    return sum(values.values())


if __name__ == "__main__":
    print(solve())
