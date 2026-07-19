#!/usr/bin/env python3
"""Project Euler Problem 981: The Quaternion Group II.

Interpret x, y, and z as the quaternion units i, j, and k.  A word is
neutral exactly when its quaternion product is (-1) ** len(word).

For fixed counts X, Y, Z, the product can be central only when the three
counts have the same parity.  Relative to the ordered word x^X y^Y z^Z,
each inversion changes the product's sign.  The difference between the
numbers of even- and odd-inversion multiset permutations is the Gaussian
multinomial evaluated at q = -1:

* it is zero when X, Y, Z are all odd;
* when they are all even, it is
  multinomial((X + Y + Z) / 2; X / 2, Y / 2, Z / 2).

The required inversion parity is
floor(X / 2) + floor(Y / 2) + floor(Z / 2), modulo 2.
"""

MODULUS = 888_888_883
LIMIT = 88
INVERSE_TWO = (MODULUS + 1) // 2


def factorial_tables(limit: int) -> tuple[list[int], list[int]]:
    factorial = [1] * (limit + 1)
    for value in range(1, limit + 1):
        factorial[value] = factorial[value - 1] * value % MODULUS

    inverse_factorial = [1] * (limit + 1)
    inverse_factorial[limit] = pow(factorial[limit], MODULUS - 2, MODULUS)
    for value in range(limit, 0, -1):
        inverse_factorial[value - 1] = (
            inverse_factorial[value] * value % MODULUS
        )
    return factorial, inverse_factorial


def neutral_count(
    x_count: int,
    y_count: int,
    z_count: int,
    factorial: list[int],
    inverse_factorial: list[int],
) -> int:
    if not (x_count % 2 == y_count % 2 == z_count % 2):
        return 0

    total_count = x_count + y_count + z_count
    all_words = factorial[total_count]
    all_words = all_words * inverse_factorial[x_count] % MODULUS
    all_words = all_words * inverse_factorial[y_count] % MODULUS
    all_words = all_words * inverse_factorial[z_count] % MODULUS

    signed_difference = 0
    if x_count % 2 == 0:
        signed_difference = factorial[total_count // 2]
        signed_difference *= inverse_factorial[x_count // 2]
        signed_difference %= MODULUS
        signed_difference *= inverse_factorial[y_count // 2]
        signed_difference %= MODULUS
        signed_difference *= inverse_factorial[z_count // 2]
        signed_difference %= MODULUS

    target_is_even = (
        x_count // 2 + y_count // 2 + z_count // 2
    ) % 2 == 0
    if target_is_even:
        return (all_words + signed_difference) * INVERSE_TWO % MODULUS
    return (all_words - signed_difference) * INVERSE_TWO % MODULUS


def solve() -> int:
    cubes = [value**3 for value in range(LIMIT)]
    maximum_total = 3 * cubes[-1]
    factorial, inverse_factorial = factorial_tables(maximum_total)

    assert (
        neutral_count(2, 2, 2, factorial, inverse_factorial) == 42
    )
    assert (
        neutral_count(8, 8, 8, factorial, inverse_factorial)
        == 4_732_773_210 % MODULUS
    )

    answer = 0
    for parity in (0, 1):
        same_parity_cubes = cubes[parity::2]
        for x_count in same_parity_cubes:
            for y_count in same_parity_cubes:
                for z_count in same_parity_cubes:
                    answer += neutral_count(
                        x_count,
                        y_count,
                        z_count,
                        factorial,
                        inverse_factorial,
                    )
        answer %= MODULUS
    return answer


if __name__ == "__main__":
    print(solve())
