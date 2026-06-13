#!/usr/bin/env python3
"""Project Euler 731: decimal digits of a sparse series."""


TARGET = 10**16
DIGITS = 10
MOD = 10**DIGITS


def extract(position: int) -> str:
    powers = []
    power = 1
    while power * 3 <= position + DIGITS - 1:
        power *= 3
        powers.append(power)

    exponent_count = len(powers)
    denominator = 3**exponent_count
    modulus = MOD * denominator
    numerator = 0

    for index, power_of_three in enumerate(powers, start=1):
        decimal_shift = position + DIGITS - 1 - power_of_three
        numerator += pow(10, decimal_shift, modulus) * 3 ** (exponent_count - index)
        numerator %= modulus

    return f"{(numerator // denominator) % MOD:0{DIGITS}d}"


def solve() -> str:
    assert extract(100) == "4938271604"
    assert extract(10**8) == "2584642393"
    return extract(TARGET)


if __name__ == "__main__":
    print(solve())
