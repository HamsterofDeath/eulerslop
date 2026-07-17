#!/usr/bin/env python3
"""Project Euler 858: sum the LCMs of all subsets of {1, ..., N}."""

from math import gcd, isqrt


LIMIT = 800
MODULUS = 1_000_000_007


def primes_up_to(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [value for value in range(2, limit + 1) if sieve[value]]


def multiples_mask(divisor: int, limit: int) -> int:
    mask = 0
    for multiple in range(divisor, limit + 1, divisor):
        mask |= 1 << (multiple - 1)
    return mask


def exact_lcm_sum(limit: int) -> int:
    """Small independent DP used to check the supplied examples."""
    counts = {1: 1}
    for value in range(1, limit + 1):
        next_counts = counts.copy()
        for current_lcm, count in counts.items():
            new_lcm = current_lcm * value // gcd(current_lcm, value)
            next_counts[new_lcm] = next_counts.get(new_lcm, 0) + count
        counts = next_counts
    return sum(value * count for value, count in counts.items())


def lcm_subset_sum(limit: int, modulus: int = MODULUS) -> int:
    """Return G(limit) modulo modulus by prime-power inclusion-exclusion."""
    primes = primes_up_to(limit)
    root = isqrt(limit)
    small_primes = [prime for prime in primes if prime <= root]
    large_primes = [prime for prime in primes if prime > root]

    exponents = {}
    universal_lcm = 1
    for prime in primes:
        exponent = 0
        prime_power = prime
        while prime_power <= limit:
            exponent += 1
            prime_power *= prime
        exponents[prime] = exponent
        universal_lcm = (
            universal_lcm * pow(prime, exponent, modulus)
        ) % modulus

    powers_of_two = [1] * (limit + 1)
    for index in range(1, limit + 1):
        powers_of_two[index] = 2 * powers_of_two[index - 1] % modulus

    # A number <= limit contains at most one prime greater than sqrt(limit).
    # Its multiples are prime*k for a small multiplier k.
    maximum_multiplier = limit // (root + 1)
    prefix_masks = [
        (1 << length) - 1
        for length in range(maximum_multiplier + 1)
    ]
    inverse_two = pow(2, modulus - 2, modulus)
    inverse_powers_of_two = [1] * (maximum_multiplier + 1)
    for index in range(1, maximum_multiplier + 1):
        inverse_powers_of_two[index] = (
            inverse_powers_of_two[index - 1] * inverse_two
        ) % modulus

    # For p^e || lcm(1,...,N), expanding
    #   p^v/p^e = 1 - sum_{r=v+1}^e phi(p^r)/p^e
    # gives one "not selected", or one forbidden prime-power, per prime.
    small_options = []
    for prime in small_primes:
        exponent = exponents[prime]
        inverse_max_power = pow(
            pow(prime, exponent, modulus), modulus - 2, modulus
        )
        options = [(0, 0, 1)]
        prime_power = 1
        for power in range(1, exponent + 1):
            prime_power *= prime
            covered_numbers = multiples_mask(prime_power, limit)
            covered_multipliers = multiples_mask(
                prime_power, maximum_multiplier
            )
            totient = pow(prime, power - 1, modulus) * (prime - 1)
            weight = -totient * inverse_max_power % modulus
            options.append(
                (covered_numbers, covered_multipliers, weight)
            )
        small_options.append(options)

    large_weights = [
        (
            prime,
            (prime - 1) * pow(prime, modulus - 2, modulus) % modulus,
        )
        for prime in large_primes
    ]
    large_cache = {}

    def large_prime_product(multiplier_mask: int) -> int:
        cached = large_cache.get(multiplier_mask)
        if cached is not None:
            return cached

        product = 1
        for prime, weight in large_weights:
            multiple_count = limit // prime
            already_covered = (
                multiplier_mask & prefix_masks[multiple_count]
            ).bit_count()
            newly_forbidden = multiple_count - already_covered
            factor = (
                1
                - weight * inverse_powers_of_two[newly_forbidden]
            ) % modulus
            product = product * factor % modulus

        large_cache[multiplier_mask] = product
        return product

    total = 0

    def search(
        index: int,
        number_mask: int,
        multiplier_mask: int,
        coefficient: int,
    ) -> None:
        nonlocal total
        if index == len(small_options):
            free_numbers = limit - number_mask.bit_count()
            contribution = coefficient * powers_of_two[free_numbers]
            contribution %= modulus
            contribution *= large_prime_product(multiplier_mask)
            total = (total + contribution) % modulus
            return

        for add_numbers, add_multipliers, weight in small_options[index]:
            search(
                index + 1,
                number_mask | add_numbers,
                multiplier_mask | add_multipliers,
                coefficient * weight % modulus,
            )

    search(0, 0, 0, 1)
    return universal_lcm * total % modulus


def solve() -> int:
    assert exact_lcm_sum(5) == 528
    assert exact_lcm_sum(20) == 8_463_108_648_960
    return lcm_subset_sum(LIMIT)


if __name__ == "__main__":
    print(solve())
