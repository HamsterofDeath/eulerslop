#!/usr/bin/env python3
"""Project Euler 830: binomial sum modulo three prime cubes."""

from math import comb, factorial


N = 10**18
PRIMES = (83, 89, 97)
MODULI = tuple(p**3 for p in PRIMES)
MODULUS = MODULI[0] * MODULI[1] * MODULI[2]


def v_p_factorial(n: int, p: int) -> int:
    total = 0
    while n:
        n //= p
        total += n
    return total


def stirling2_mod(n: int, k: int, p: int) -> int:
    modulus = p**3
    valuation = v_p_factorial(k, p)
    numerator_modulus = p ** (3 + valuation)

    numerator = 0
    for i in range(k + 1):
        term = comb(k, i) * pow(i, n, numerator_modulus)
        numerator += -term if (k - i) % 2 else term
    numerator %= numerator_modulus

    p_power = p**valuation
    assert numerator % p_power == 0
    unit = (factorial(k) // p_power) % modulus
    return numerator // p_power * pow(unit, -1, modulus) % modulus


def falling_mod_and_valuation(n: int, k: int, p: int) -> tuple[int, int]:
    modulus = p**3
    value = 1
    valuation = 0

    for offset in range(k):
        term = n - offset
        if term == 0:
            return 0, valuation
        while term % p == 0:
            valuation += 1
            term //= p
        value = value * (term % modulus) % modulus

    if valuation >= 3:
        return 0, valuation
    return value * (p**valuation) % modulus, valuation


def s_mod_prime_cube(n: int, p: int) -> int:
    modulus = p**3
    total = 0

    for k in range(1, min(n + 1, 5 * p)):
        falling, valuation = falling_mod_and_valuation(n, k, p)
        if valuation >= 3:
            break
        total += (
            stirling2_mod(n, k, p)
            * falling
            * pow(2, n - k, modulus)
        )
        total %= modulus
    return total


def crt(residues: list[int], moduli: tuple[int, ...]) -> int:
    value = 0
    modulus = 1
    for residue, next_modulus in zip(residues, moduli):
        step = (residue - value) % next_modulus
        step = step * pow(modulus, -1, next_modulus) % next_modulus
        value += modulus * step
        modulus *= next_modulus
    return value


def solve_for(n: int) -> int:
    residues = [s_mod_prime_cube(n, p) for p in PRIMES]
    return crt(residues, MODULI)


def solve() -> int:
    assert solve_for(10) == 142_469_423_360
    return solve_for(N)


if __name__ == "__main__":
    print(solve())
