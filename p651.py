#!/usr/bin/env python3
from functools import lru_cache
from math import comb, gcd


MOD = 1_000_000_007


def factorize(n):
    factors = []
    exponent = 0
    while n % 2 == 0:
        n //= 2
        exponent += 1
    if exponent:
        factors.append((2, exponent))

    p = 3
    while p * p <= n:
        exponent = 0
        while n % p == 0:
            n //= p
            exponent += 1
        if exponent:
            factors.append((p, exponent))
        p += 2
    if n > 1:
        factors.append((n, 1))
    return factors


@lru_cache(maxsize=None)
def divisors_with_phi(n):
    items = [(1, 1)]
    for p, exponent in factorize(n):
        expanded = []
        power = 1
        for k in range(exponent + 1):
            phi_factor = 1 if k == 0 else power - power // p
            for divisor, phi_value in items:
                expanded.append((divisor * power, phi_value * phi_factor))
            power *= p
        items = expanded
    return tuple(sorted(items))


def reflection_types(n):
    """Return (count, fixed_cycles, two_cycles) for reflections of an n-cycle."""
    if n % 2:
        return ((n, 1, (n - 1) // 2),)
    return ((n // 2, 2, (n - 2) // 2), (n // 2, 0, n // 2))


def exact_colourings(cycles, colours):
    total = 0
    for omitted in range(colours + 1):
        term = comb(colours, omitted) * pow(colours - omitted, cycles, MOD)
        total += -term if omitted % 2 else term
    return total % MOD


def f(colours, a, b):
    a_rotations = divisors_with_phi(a)
    b_rotations = divisors_with_phi(b)
    a_reflections = reflection_types(a)
    b_reflections = reflection_types(b)

    fixed_cache = {}

    def fixed(cycles):
        if cycles not in fixed_cache:
            fixed_cache[cycles] = exact_colourings(cycles, colours)
        return fixed_cache[cycles]

    total = 0

    for len_a, count_a in a_rotations:
        cycles_a = a // len_a
        for len_b, count_b in b_rotations:
            cycles = cycles_a * (b // len_b) * gcd(len_a, len_b)
            total += count_a * count_b * fixed(cycles)

    for len_a, count_a in a_rotations:
        cycles_a = a // len_a
        for count_b, fixed_b, pairs_b in b_reflections:
            cycles = cycles_a * (fixed_b + pairs_b * gcd(len_a, 2))
            total += count_a * count_b * fixed(cycles)

    for count_a, fixed_a, pairs_a in a_reflections:
        for len_b, count_b in b_rotations:
            cycles = (b // len_b) * (fixed_a + pairs_a * gcd(len_b, 2))
            total += count_a * count_b * fixed(cycles)

    for count_a, fixed_a, pairs_a in a_reflections:
        for count_b, fixed_b, pairs_b in b_reflections:
            cycles = (
                fixed_a * fixed_b
                + fixed_a * pairs_b
                + pairs_a * fixed_b
                + 2 * pairs_a * pairs_b
            )
            total += count_a * count_b * fixed(cycles)

    return total % MOD * pow(4 * a * b, MOD - 2, MOD) % MOD


def solve():
    fib = [0, 1]
    for _ in range(2, 41):
        fib.append(fib[-1] + fib[-2])

    return sum(f(i, fib[i - 1], fib[i]) for i in range(4, 41)) % MOD


if __name__ == "__main__":
    print(solve())
