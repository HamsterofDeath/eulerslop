#!/usr/bin/env python3
from math import log


MOD = 1_000_000_007
INV2 = (MOD + 1) // 2
INV9 = pow(9, MOD - 2, MOD)
INV10 = pow(10, MOD - 2, MOD)


def _prime_limit(n: int) -> int:
    if n < 6:
        return 15
    return int(n * (log(n) + log(log(n)))) + 10


def _first_primes(n: int):
    if n <= 0:
        return

    limit = _prime_limit(n)

    while True:
        # Odd-only sieve.  Index i represents 2*i + 1.
        sieve = bytearray(b"\x01") * (limit // 2 + 1)
        sieve[0] = 0

        i = 1
        while True:
            p = 2 * i + 1
            if p * p > limit:
                break
            if sieve[i]:
                start = p * p // 2
                sieve[start::p] = b"\x00" * (((len(sieve) - 1 - start) // p) + 1)
            i += 1

        if 1 + sum(sieve) >= n:
            yield 2
            found = 1
            if found == n:
                return
            for i, is_prime in enumerate(sieve):
                if is_prime:
                    yield 2 * i + 1
                    found += 1
                    if found == n:
                        return

        limit *= 2


def _geometric_sums(x: int, count: int) -> tuple[int, int]:
    """Return sum x^q and sum q*x^q for 0 <= q < count, modulo MOD."""
    if count == 0:
        return 0, 0
    if x == 1:
        k = count % MOD
        return k, k * ((count - 1) % MOD) * INV2 % MOD

    x_to_k = pow(x, count, MOD)
    denominator = (1 - x) % MOD
    inv_denominator = pow(denominator, MOD - 2, MOD)

    total = (1 - x_to_k) * inv_denominator % MOD
    weighted = (
        (x - (count % MOD) * x_to_k + ((count - 1) % MOD) * x_to_k % MOD * x)
        * inv_denominator
        * inv_denominator
    ) % MOD
    return total, weighted


def _prime_digit_aggregates(prime_count: int) -> tuple[int, int, int, int, int]:
    length = digit_sum = weighted_digit_sum = 0
    inverse_power = 1
    inverse_digit_sum = inverse_weighted_digit_sum = 0

    for prime in _first_primes(prime_count):
        for ch in str(prime):
            digit = ord(ch) - ord("0")
            position = length + 1

            digit_sum = (digit_sum + digit) % MOD
            weighted_digit_sum = (weighted_digit_sum + digit * position) % MOD
            inverse_digit_sum = (inverse_digit_sum + digit * inverse_power) % MOD
            inverse_weighted_digit_sum = (
                inverse_weighted_digit_sum + digit * position * inverse_power
            ) % MOD

            inverse_power = inverse_power * INV10 % MOD
            length += 1

    return (
        length,
        digit_sum,
        weighted_digit_sum,
        inverse_digit_sum,
        inverse_weighted_digit_sum,
    )


def repeated_substring_sum(prime_count: int, repetitions: int) -> int:
    length, digit_sum, weighted_digit_sum, inverse_digit_sum, inverse_weighted = (
        _prime_digit_aggregates(prime_count)
    )

    total_length = length * repetitions
    repeat_ratio = pow(pow(10, length, MOD), MOD - 2, MOD)
    repeat_sum, repeat_weighted_sum = _geometric_sums(repeat_ratio, repetitions)

    positive_part = (
        pow(10, total_length, MOD)
        * (
            (length % MOD) * repeat_weighted_sum % MOD * inverse_digit_sum
            + repeat_sum * inverse_weighted
        )
    ) % MOD

    k = repetitions % MOD
    linear_part = (
        (length % MOD)
        * k
        % MOD
        * ((repetitions - 1) % MOD)
        % MOD
        * INV2
        % MOD
        * digit_sum
        + k * weighted_digit_sum
    ) % MOD

    return (positive_part - linear_part) * INV9 % MOD


def solve() -> int:
    return repeated_substring_sum(1_000_000, 10**12)


if __name__ == "__main__":
    print(solve())
