#!/usr/bin/env python3
"""Project Euler Problem 955: Finding Triangles.

Immediately after a triangular value T_m, the first differences are
1, 2, 3, ..., so the value k steps later is T_m+T_k.  Writing
T_m+T_k=T_l and factoring the resulting difference of squares gives

    u*v = m*(m+1),
    k = (v-u-1)/2,
    l = (u+v-1)/2.

Here u and v must have opposite parity.  The next triangular hit uses
the closest nontrivial factor pair, found after factoring m and m+1.
"""

from math import gcd, isqrt


MILLER_RABIN_BASES = (
    2,
    325,
    9375,
    28178,
    450775,
    9780504,
    1795265022,
)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if value % prime == 0:
            return value == prime

    odd_part = value - 1
    power_of_two = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        power_of_two += 1

    for base in MILLER_RABIN_BASES:
        if base % value == 0:
            continue
        witness = pow(base, odd_part, value)
        if witness in (1, value - 1):
            continue
        for _ in range(power_of_two - 1):
            witness = witness * witness % value
            if witness == value - 1:
                break
        else:
            return False
    return True


def pollard_rho(value: int) -> int:
    if value % 2 == 0:
        return 2
    if value % 3 == 0:
        return 3

    constant = 1
    while True:
        first = second = 2
        divisor = 1
        while divisor == 1:
            first = (first * first + constant) % value
            second = (second * second + constant) % value
            second = (second * second + constant) % value
            divisor = gcd(abs(first - second), value)
        if divisor != value:
            return divisor
        constant += 1


def factor_integer(value: int, factors: dict[int, int]) -> None:
    if value == 1:
        return
    if is_prime(value):
        factors[value] = factors.get(value, 0) + 1
        return

    divisor = pollard_rho(value)
    factor_integer(divisor, factors)
    factor_integer(value // divisor, factors)


def divisors(factors: dict[int, int]) -> list[int]:
    result = [1]
    for prime, exponent in factors.items():
        previous = result[:]
        prime_power = 1
        for _ in range(exponent):
            prime_power *= prime
            result.extend(
                divisor * prime_power for divisor in previous
            )
    return result


def next_triangle_hit(index: int) -> tuple[int, int]:
    factors: dict[int, int] = {}
    factor_integer(index, factors)
    factor_integer(index + 1, factors)

    product = index * (index + 1)
    root = isqrt(product)
    lower = max(
        divisor
        for divisor in divisors(factors)
        if (
            divisor <= root
            and divisor != index
            and (divisor + product // divisor) % 2 == 1
        )
    )
    upper = product // lower

    steps = (upper - lower - 1) // 2
    next_index = (lower + upper - 1) // 2
    return steps, next_index


def triangle_hit(number: int) -> tuple[int, int]:
    sequence_index = 0
    triangle_index = 2

    for _ in range(1, number):
        steps, triangle_index = next_triangle_hit(triangle_index)
        sequence_index += steps

    triangle_value = triangle_index * (triangle_index + 1) // 2
    return sequence_index, triangle_value


def solve() -> int:
    assert triangle_hit(10) == (2964, 1_439_056)
    return triangle_hit(70)[0]


if __name__ == "__main__":
    print(solve())
