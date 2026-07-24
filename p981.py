#!/usr/bin/env python3
"""Project Euler Problem 981: The Quaternion Group II.

A word is neutral exactly when its quaternion product is (-1)**length.
The product can be central only when X,Y,Z have the same parity.
Reordering to x**X y**Y z**Z shows that the positive-minus-negative
count is a q-multinomial evaluated at q=-1.  It is zero for three odd
counts.  For three even counts its magnitude is the multinomial of the
halved counts, with sign (-1)**((X+Y+Z)/2).
"""


MODULUS = 888_888_883
LIMIT = 88
MAXIMUM_COUNT = 3 * (LIMIT - 1) ** 3
INVERSE_TWO = (MODULUS + 1) // 2


factorials = [1] * (MAXIMUM_COUNT + 1)
for value in range(1, len(factorials)):
    factorials[value] = factorials[value - 1] * value % MODULUS

inverse_factorials = [1] * len(factorials)
inverse_factorials[-1] = pow(
    factorials[-1], MODULUS - 2, MODULUS
)
for value in range(MAXIMUM_COUNT, 0, -1):
    inverse_factorials[value - 1] = (
        inverse_factorials[value] * value % MODULUS
    )


def multinomial(first: int, second: int, third: int) -> int:
    return (
        factorials[first + second + third]
        * inverse_factorials[first]
        * inverse_factorials[second]
        * inverse_factorials[third]
        % MODULUS
    )


def neutral_count(first: int, second: int, third: int) -> int:
    if not (first % 2 == second % 2 == third % 2):
        return 0

    total = multinomial(first, second, third)
    if first % 2:
        return total * INVERSE_TWO % MODULUS

    difference = multinomial(
        first // 2, second // 2, third // 2
    )
    if (first + second + third) // 2 % 2:
        difference = -difference
    return (total + difference) * INVERSE_TWO % MODULUS


def solve() -> int:
    assert neutral_count(2, 2, 2) == 42
    assert neutral_count(8, 8, 8) == 4_732_773_210 % MODULUS

    even_cubes = [value**3 for value in range(0, LIMIT, 2)]
    odd_cubes = [value**3 for value in range(1, LIMIT, 2)]
    result = 0
    for cubes in (even_cubes, odd_cubes):
        for first in cubes:
            for second in cubes:
                for third in cubes:
                    result += neutral_count(first, second, third)
    return result % MODULUS


if __name__ == "__main__":
    print(solve())
