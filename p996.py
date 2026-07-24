#!/usr/bin/env python3
"""Project Euler Problem 996: Overtakes.

A player with count zero never swaps, so zeroes split a count tuple into
independent positive runs.  A positive run is attainable exactly when
its sum is even and its largest entry is at most half that sum.  This is
the degree-sequence criterion for a loopless multigraph; a constructive
adjacent-swap induction realizes every such connected run.

For a positive run of length l and total 2t, inclusion-exclusion gives

    B_l(2t) = C(2t-1, l-1) - l*C(t-1, l-1).

Its generating function in y^t is U_l(y)/(1-y)^l.  Consequently the
generating function for all valid n-tuples is A_n(y)/(1-y)^n, where
A_n has degree only n.  The large day limit then needs just n+1
binomial coefficients.
"""

from math import comb
from typing import Optional


MODULUS = 1_234_567_891
PLAYERS = 123
DAYS = 4_567_891


def reduce_value(value: int, modulus: Optional[int]) -> int:
    return value if modulus is None else value % modulus


def add_polynomials(
    first: list[int], second: list[int], modulus: Optional[int]
) -> list[int]:
    result = [0] * max(len(first), len(second))
    for index, value in enumerate(first):
        result[index] += value
    for index, value in enumerate(second):
        result[index] += value
    if modulus is not None:
        result = [value % modulus for value in result]
    return result


def multiply_polynomials(
    first: list[int], second: list[int], modulus: Optional[int]
) -> list[int]:
    result = [0] * (len(first) + len(second) - 1)
    for first_degree, first_value in enumerate(first):
        for second_degree, second_value in enumerate(second):
            degree = first_degree + second_degree
            result[degree] += first_value * second_value
            if modulus is not None:
                result[degree] %= modulus
    return result


def multiply_by_one_minus_y(
    polynomial: list[int], modulus: Optional[int]
) -> list[int]:
    result = [0] * (len(polynomial) + 1)
    for degree, value in enumerate(polynomial):
        result[degree] += value
        result[degree + 1] -= value
    if modulus is not None:
        result = [value % modulus for value in result]
    return result


def block_numerator(
    length: int, modulus: Optional[int]
) -> list[int]:
    # Multiply sum_t C(2t-1,l-1)y^t by (1-y)^l, then
    # subtract l*y^l for the unique overlarge component.
    values = [
        (
            comb(2 * half_sum - 1, length - 1)
            if half_sum >= 1 and 2 * half_sum >= length
            else 0
        )
        for half_sum in range(length + 1)
    ]
    numerator = []
    for degree in range(length + 1):
        coefficient = sum(
            (-1) ** offset
            * comb(length, offset)
            * values[degree - offset]
            for offset in range(degree + 1)
        )
        numerator.append(reduce_value(coefficient, modulus))
    numerator[length] = reduce_value(
        numerator[length] - length, modulus
    )
    return numerator


def tuple_numerator(
    n: int, modulus: Optional[int]
) -> list[int]:
    block = [None] + [
        block_numerator(length, modulus)
        for length in range(1, n + 1)
    ]
    numerators = [[1]]

    for size in range(1, n + 1):
        # Start with a zero, or with a positive block.  A block shorter
        # than the tuple must be followed by one mandatory zero.
        current = multiply_by_one_minus_y(
            numerators[size - 1], modulus
        )
        for length in range(2, size):
            term = multiply_polynomials(
                block[length],
                numerators[size - length - 1],
                modulus,
            )
            current = add_polynomials(
                current,
                multiply_by_one_minus_y(term, modulus),
                modulus,
            )
        if size >= 2:
            current = add_polynomials(
                current, block[size], modulus
            )
        numerators.append(current)

    return numerators[n]


def count_tuples(
    n: int, days: int, modulus: Optional[int] = None
) -> int:
    numerator = tuple_numerator(n, modulus)
    half_limit = days // 2

    answer = 0
    for degree, coefficient in enumerate(numerator):
        if degree > half_limit:
            break
        # Dividing by (1-y)^(n+1) also sums all coefficients up to
        # the allowed number of overtakes.
        answer += coefficient * comb(
            half_limit - degree + n, n
        )
        if modulus is not None:
            answer %= modulus
    return answer


def solve() -> int:
    return count_tuples(PLAYERS, DAYS, MODULUS)


if __name__ == "__main__":
    assert count_tuples(3, 4) == 8
    assert count_tuples(12, 34) == 2_457_178_250
    print(solve())
