#!/usr/bin/env python3

from collections import Counter
from math import gcd


def primes_upto(limit):
    sieve = [True] * (limit + 1)
    primes = []
    for n in range(2, limit + 1):
        if sieve[n]:
            primes.append(n)
            for multiple in range(n * n, limit + 1, n):
                sieve[multiple] = False
    return primes


def factorial_prime_exponents(limit):
    result = []
    for prime in primes_upto(limit):
        power = prime
        exponent = 0
        while power <= limit:
            exponent += limit // power
            power *= prime
        result.append((prime, exponent))
    return result


def build_ratio_counts(group):
    counts = Counter({(1, 1): 1})
    for _, exponent in group:
        choices = []
        for used in range(exponent + 1):
            numerator = used + 1
            denominator = exponent - used + 1
            divisor = gcd(numerator, denominator)
            choices.append((numerator // divisor, denominator // divisor))

        next_counts = Counter()
        for (numerator, denominator), count in counts.items():
            for choice_num, choice_den in choices:
                new_num = numerator * choice_num
                new_den = denominator * choice_den
                divisor = gcd(new_num, new_den)
                next_counts[(new_num // divisor, new_den // divisor)] += count
        counts = next_counts
    return counts


def count_equal_divisor_factor_pairs(limit):
    items = factorial_prime_exponents(limit)

    left = []
    right = []
    left_raw = 1
    right_raw = 1
    for item in sorted(items, key=lambda entry: entry[1] + 1, reverse=True):
        choices = item[1] + 1
        if left_raw <= right_raw:
            left.append(item)
            left_raw *= choices
        else:
            right.append(item)
            right_raw *= choices

    left_counts = build_ratio_counts(left)
    right_counts = build_ratio_counts(right)

    ordered = 0
    for (numerator, denominator), count in left_counts.items():
        ordered += count * right_counts.get((denominator, numerator), 0)

    # 100! is not a square, so complementing the divisor exponents pairs every
    # valid assignment with a distinct assignment in the opposite order.
    return ordered // 2


def solve():
    assert count_equal_divisor_factor_pairs(10) == 3
    return str(count_equal_divisor_factor_pairs(100))


if __name__ == "__main__":
    print(solve())
