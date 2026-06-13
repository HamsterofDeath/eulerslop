#!/usr/bin/env python3
"""Project Euler 784: reciprocal pairs."""


TARGET = 2_000_000


def smallest_prime_factors(limit: int) -> list[int]:
    spf = list(range(limit + 1))
    for p in range(2, int(limit**0.5) + 1):
        if spf[p] == p:
            for multiple in range(p * p, limit + 1, p):
                if spf[multiple] == multiple:
                    spf[multiple] = p
    return spf


def prime_power_roots(prime: int, exponent: int) -> tuple[int, list[int]]:
    modulus = prime**exponent
    if prime != 2:
        return modulus, [1, modulus - 1]
    if exponent == 1:
        return modulus, [1]
    if exponent == 2:
        return modulus, [1, 3]
    half = 1 << (exponent - 1)
    return modulus, [1, modulus - 1, half - 1, half + 1]


def roots_modulo(number: int, spf: list[int]) -> list[int]:
    if number == 1:
        return [0]

    residues = [0]
    modulus = 1
    value = number
    while value > 1:
        prime = spf[value]
        exponent = 0
        while value % prime == 0:
            value //= prime
            exponent += 1

        prime_power, roots = prime_power_roots(prime, exponent)
        inverse = pow(modulus, -1, prime_power)
        combined = []
        for residue in residues:
            for root in roots:
                step = ((root - residue) * inverse) % prime_power
                combined.append(residue + modulus * step)
        residues = combined
        modulus *= prime_power

    return residues


def progression_contribution(first: int, step: int, last_limit: int) -> int:
    count = (last_limit - first) // step + 1
    sum_indices = count * (count - 1) // 2
    sum_square_indices = count * (count - 1) * (2 * count - 1) // 6
    square_sum = (
        count * first * first
        + 2 * first * step * sum_indices
        + step * step * sum_square_indices
    )
    return (square_sum - count) // step


def reciprocal_sum(limit: int) -> int:
    spf = smallest_prime_factors(limit // 2)
    total = 0
    for divisor in range(1, limit // 2 + 1):
        lower = 2 * divisor
        for residue in roots_modulo(divisor, spf):
            first = residue
            if first <= lower:
                first += ((lower - first) // divisor + 1) * divisor
            if first <= limit:
                total += progression_contribution(first, divisor, limit)
    return total


def solve() -> int:
    assert reciprocal_sum(5) == 59
    assert reciprocal_sum(100) == 697_317
    return reciprocal_sum(TARGET)


if __name__ == "__main__":
    print(solve())
