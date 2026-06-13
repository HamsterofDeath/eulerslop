#!/usr/bin/env python3
"""Project Euler 636: factorial representations with distinct bases."""

from collections import Counter, defaultdict
from math import factorial, gcd


MOD = 1_000_000_007
N = 1_000_000
EXPONENTS = (1, 2, 2, 3, 3, 3, 4, 4, 4, 4)
LABEL_GROUP_SIZE = factorial(2) * factorial(3) * factorial(4)
INV_LABEL_GROUP_SIZE = pow(LABEL_GROUP_SIZE, MOD - 2, MOD)
INV_SMALL = [0] + [pow(n, MOD - 2, MOD) for n in range(1, len(EXPONENTS) + 1)]


def lcm(a, b):
    return a // gcd(a, b) * b


def primes_upto(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    root = int(limit**0.5)
    for n in range(2, root + 1):
        if sieve[n]:
            start = n * n
            sieve[start : limit + 1 : n] = b"\x00" * (((limit - start) // n) + 1)
    return (n for n in range(limit + 1) if sieve[n])


def factorial_prime_exponent_counts(n):
    counts = Counter()
    for prime in primes_upto(n):
        remaining = n
        exponent = 0
        while remaining:
            remaining //= prime
            exponent += remaining
        counts[exponent] += 1
    return dict(counts)


def partition_weight_coefficients():
    coefficients = defaultdict(int)
    blocks = []

    def visit(index):
        if index == len(EXPONENTS):
            weights = tuple(sorted(sum(EXPONENTS[i] for i in block) for block in blocks))
            mobius = 1
            for block in blocks:
                size = len(block)
                mobius *= (-1) ** (size - 1) * factorial(size - 1)
            coefficients[weights] += mobius
            return

        for block in blocks:
            block.append(index)
            visit(index + 1)
            block.pop()

        blocks.append([index])
        visit(index + 1)
        blocks.pop()

    visit(0)

    # Since many primes divide N! exactly once, any surviving block system must
    # contain a weight-1 variable; all others have zero contribution.
    return [(weights, coeff % MOD) for weights, coeff in coefficients.items() if coeff and 1 in weights]


def representation_counts(weights, targets):
    variable_count = len(weights)
    period = 1
    for weight in weights:
        period = lcm(period, weight)

    max_needed = variable_count * period - 1
    ways = [0] * (max_needed + 1)
    ways[0] = 1
    for weight in weights:
        for value in range(weight, max_needed + 1):
            ways[value] = (ways[value] + ways[value - weight]) % MOD

    differences_by_residue = {}
    for residue in {target % period for target in targets}:
        values = [ways[residue + step * period] for step in range(variable_count)]
        differences = []
        while values:
            differences.append(values[0])
            values = [(values[i + 1] - values[i]) % MOD for i in range(len(values) - 1)]
        differences_by_residue[residue] = differences

    result = {}
    for target in targets:
        quotient, residue = divmod(target, period)
        value = 0
        binomial = 1
        for degree, difference in enumerate(differences_by_residue[residue]):
            if degree:
                binomial = binomial * ((quotient - degree + 1) % MOD) % MOD
                binomial = binomial * INV_SMALL[degree] % MOD
            value = (value + difference * binomial) % MOD
        result[target] = value
    return result


def solve(n=N):
    exponent_counts = factorial_prime_exponent_counts(n)
    targets = tuple(exponent_counts)

    total = 0
    for weights, coefficient in partition_weight_coefficients():
        counts = representation_counts(weights, targets)
        product = 1
        for exponent, amount in exponent_counts.items():
            product = product * pow(counts[exponent], amount, MOD) % MOD
        total = (total + coefficient * product) % MOD

    return total * INV_LABEL_GROUP_SIZE % MOD


def main():
    print(solve())


if __name__ == "__main__":
    main()
