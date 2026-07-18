#!/usr/bin/env python3
"""Project Euler Problem 969: Kangaroo Hopping.

The renewal equation gives

    H(n) = sum((-1)^j * (n-j)^j / j! * alpha^(n-j),
               j=0,...,n-1).

For j >= 1, j! divides m^j exactly when m is divisible by every prime
up to j: each prime valuation of j! is positive but strictly below j.
Thus the integral coefficients for fixed j are indexed by multiples of
the primorial through j.  That primorial exceeds 10**18 at 53, leaving
only small-degree power sums, evaluated modulo MOD by interpolation.
"""

MODULUS = 1_000_000_007
LIMIT = 10**18
MAXIMUM_DEGREE = 60


factorials = [1] * (MAXIMUM_DEGREE + 1)
for index in range(1, len(factorials)):
    factorials[index] = factorials[index - 1] * index % MODULUS

inverse_factorials = [1] * len(factorials)
inverse_factorials[-1] = pow(
    factorials[-1], MODULUS - 2, MODULUS
)
for index in range(len(factorials) - 1, 0, -1):
    inverse_factorials[index - 1] = (
        inverse_factorials[index] * index % MODULUS
    )


def power_sum(exponent: int, limit: int) -> int:
    """Return sum(k**exponent, k=1..limit) modulo MODULUS."""
    degree = exponent + 1
    values = [0] * (degree + 1)
    for point in range(1, degree + 1):
        values[point] = (
            values[point - 1] + pow(point, exponent, MODULUS)
        ) % MODULUS

    argument = limit % MODULUS
    if argument <= degree:
        return values[argument]

    prefix = [1] * (degree + 2)
    suffix = [1] * (degree + 2)
    for point in range(degree + 1):
        prefix[point + 1] = (
            prefix[point] * (argument - point) % MODULUS
        )
    for point in range(degree, -1, -1):
        suffix[point] = (
            suffix[point + 1] * (argument - point) % MODULUS
        )

    result = 0
    for point, value in enumerate(values):
        term = value * prefix[point] % MODULUS
        term = term * suffix[point + 1] % MODULUS
        term = term * inverse_factorials[point] % MODULUS
        term = term * inverse_factorials[degree - point] % MODULUS
        if (degree - point) % 2:
            result -= term
        else:
            result += term
    return result % MODULUS


def is_prime(number: int) -> bool:
    return number >= 2 and all(
        number % divisor
        for divisor in range(2, int(number**0.5) + 1)
    )


def coefficient_sum(limit: int) -> int:
    result = limit % MODULUS  # j=0
    primorial = 1

    for exponent in range(1, MAXIMUM_DEGREE):
        if is_prime(exponent):
            primorial *= exponent
        if primorial + exponent > limit:
            break

        multiple_count = (limit - exponent) // primorial
        coefficient = (
            pow(primorial % MODULUS, exponent, MODULUS)
            * inverse_factorials[exponent]
            % MODULUS
        )
        contribution = (
            coefficient * power_sum(exponent, multiple_count)
            % MODULUS
        )
        if exponent % 2:
            result -= contribution
        else:
            result += contribution
    return result % MODULUS


def solve() -> int:
    assert coefficient_sum(10) == 43
    return coefficient_sum(LIMIT)


if __name__ == "__main__":
    print(solve())
