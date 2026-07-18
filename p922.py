"""Project Euler Problem 922: Young's Game.

An (a,b,k)-staircase is the disjoint-game value

    (b-a) + *(k-1),

where *n is a Nim heap.  The rectangular part of each step contributes the
integer b-a, while its triangular block frontier gives a heap of size k-1.

For an ordered tuple, Right wins when the integer parts sum positively, or
when they sum to zero and the heap XOR is nonzero. Symmetry under a <-> b
reduces the answer to (T+Z)/2-Z0, where Z counts zero integer sums and Z0 also
requires zero XOR.

A Walsh transform diagonalizes XOR. For each Walsh character, a Laurent
polynomial records counts by b-a; its m-th central coefficient supplies the
corresponding zero-sum count.
"""

from math import comb


MODULUS = 1_000_000_007
TARGET_DIAGRAMS = 8
TARGET_WEIGHT = 64


def polynomial_convolution(first: list[int], second: list[int]) -> list[int]:
    result = [0] * (len(first) + len(second) - 1)
    for first_index, first_value in enumerate(first):
        for second_index, second_value in enumerate(second):
            result[first_index + second_index] += first_value * second_value
    return [value % MODULUS for value in result]


def polynomial_square(polynomial: list[int]) -> list[int]:
    result = [0] * (2 * len(polynomial) - 1)
    for index, value in enumerate(polynomial):
        result[2 * index] += value * value
        for other_index in range(index + 1, len(polynomial)):
            result[index + other_index] += (
                2 * value * polynomial[other_index]
            )
    return [value % MODULUS for value in result]


def central_power_coefficient(polynomial: list[int], exponent: int) -> int:
    result = [1]
    power = [value % MODULUS for value in polynomial]

    while exponent:
        if exponent & 1:
            result = polynomial_convolution(result, power)
        exponent //= 2
        if exponent:
            power = polynomial_square(power)

    return result[(len(result) - 1) // 2]


def right_winning_tuples(diagram_count: int, weight_limit: int) -> int:
    maximum_difference = weight_limit - 3
    xor_size = 1
    while xor_size <= maximum_difference:
        xor_size *= 2

    transformed_zero_sums = []
    for character in range(xor_size):
        polynomial = [0] * (2 * maximum_difference + 1)

        for k in range(1, weight_limit - 1):
            sign = -1 if (character & (k - 1)).bit_count() & 1 else 1
            side_sum_limit = weight_limit - k

            for difference in range(
                -maximum_difference,
                maximum_difference + 1,
            ):
                # b-a=d and a+b<=L has floor((L-|d|)/2) solutions.
                count = (side_sum_limit - abs(difference)) // 2
                if count > 0:
                    polynomial[
                        difference + maximum_difference
                    ] += sign * count

        transformed_zero_sums.append(
            central_power_coefficient(polynomial, diagram_count)
        )

    zero_integer_sum = transformed_zero_sums[0]
    zero_integer_and_xor = (
        sum(transformed_zero_sums)
        * pow(xor_size, MODULUS - 2, MODULUS)
        % MODULUS
    )
    all_tuples = pow(comb(weight_limit, 3), diagram_count, MODULUS)

    return (
        (all_tuples + zero_integer_sum)
        * pow(2, MODULUS - 2, MODULUS)
        - zero_integer_and_xor
    ) % MODULUS


def solve() -> int:
    assert right_winning_tuples(2, 4) == 7
    assert right_winning_tuples(3, 9) == 314_104
    return right_winning_tuples(TARGET_DIAGRAMS, TARGET_WEIGHT)


if __name__ == "__main__":
    print(solve())
