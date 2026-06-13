#!/usr/bin/env python3
"""Project Euler 646: Bound Divisors."""

from bisect import bisect_left, bisect_right


MOD = 1_000_000_007


def _primes_up_to(limit: int) -> list[int]:
    sieve = [True] * (limit + 1)
    if limit >= 0:
        sieve[0] = False
    if limit >= 1:
        sieve[1] = False

    for number in range(2, int(limit**0.5) + 1):
        if sieve[number]:
            for multiple in range(number * number, limit + 1, number):
                sieve[multiple] = False
    return [number for number, is_prime in enumerate(sieve) if is_prime]


def _factorial_prime_exponents(n: int) -> list[tuple[int, int]]:
    factors = []
    for prime in _primes_up_to(n):
        exponent = 0
        power = prime
        while power <= n:
            exponent += n // power
            power *= prime
        factors.append((prime, exponent))
    return factors


def _choose_split(factors: list[tuple[int, int]]) -> int:
    divisor_counts = [exponent + 1 for _, exponent in factors]
    total = 1
    for count in divisor_counts:
        total *= count

    best_index = 0
    best_worst_side = total
    left_count = 1
    for index in range(len(factors) + 1):
        if index:
            left_count *= divisor_counts[index - 1]
        right_count = total // left_count
        worst_side = max(left_count, right_count)
        if worst_side < best_worst_side:
            best_worst_side = worst_side
            best_index = index
    return best_index


def _prime_power_options(
    factors: list[tuple[int, int]], upper_bound: int
) -> list[list[tuple[int, int]]]:
    all_options = []
    for prime, exponent in factors:
        options = []
        value = 1
        signed_value = 1
        signed_prime = (MOD - prime) % MOD
        for _ in range(exponent + 1):
            options.append((value, signed_value))
            if value > upper_bound // prime:
                break
            value *= prime
            signed_value = (signed_value * signed_prime) % MOD
        all_options.append(options)
    return all_options


def _build_products(
    options_by_prime: list[list[tuple[int, int]]], upper_bound: int
) -> list[tuple[int, int]]:
    products = [(1, 1)]
    for options in options_by_prime:
        next_products = []
        for base_value, base_weight in products:
            max_factor = upper_bound // base_value
            for factor_value, factor_weight in options:
                if factor_value > max_factor:
                    break
                next_products.append(
                    (base_value * factor_value, base_weight * factor_weight % MOD)
                )
        products = next_products
    return products


def liouville_factorial_sum_mod(n: int, low: int, high: int) -> int:
    if low > high:
        return 0

    factors = _factorial_prime_exponents(n)
    split = _choose_split(factors)
    left_factors = factors[:split]
    right_factors = factors[split:]

    right_products = _build_products(_prime_power_options(right_factors, high), high)
    right_products.sort(key=lambda item: item[0])

    right_values = [value for value, _ in right_products]
    prefix_weights = [0] * (len(right_products) + 1)
    running = 0
    for index, (_, weight) in enumerate(right_products, 1):
        running = (running + weight) % MOD
        prefix_weights[index] = running

    left_options = _prime_power_options(left_factors, high)
    answer = 0

    def visit_left(index: int, value: int, weight: int) -> None:
        nonlocal answer
        if index == len(left_options):
            min_right = (low + value - 1) // value
            max_right = high // value
            if min_right <= max_right:
                start = bisect_left(right_values, min_right)
                end = bisect_right(right_values, max_right)
                if start < end:
                    answer = (
                        answer
                        + weight * (prefix_weights[end] - prefix_weights[start])
                    ) % MOD
            return

        max_factor = high // value
        for factor_value, factor_weight in left_options[index]:
            if factor_value > max_factor:
                break
            visit_left(
                index + 1,
                value * factor_value,
                weight * factor_weight % MOD,
            )

    visit_left(0, 1, 1)
    return answer


def solve() -> int:
    return liouville_factorial_sum_mod(70, 10**20, 10**60)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
