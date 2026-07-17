#!/usr/bin/env python3
"""Project Euler 865: count digit strings reducible by deleting triples."""

from math import comb


LIMIT = 10_000
MODULUS = 998_244_353


def triplicate_count(
    maximum_digits: int,
    alphabet_size: int = 10,
    modulus: int | None = None,
) -> int:
    """Count reducible strings with a nonzero first symbol."""
    triplets = maximum_digits // 3
    if triplets == 0:
        return 0
    branches = alphabet_size - 1

    # The directed Cayley graph of the free product of alphabet_size copies
    # of C_3 is a tree of oriented triangles.  If A counts branch excursions
    # and E counts returns at the root (x marks three input symbols), then
    #
    #     A = 1 + (q-1)xA^3,    E = (q-1)A/(q-A).
    #
    # Hence [x^m]A is a scaled ternary Catalan number, and the second identity
    # gives the convolution recurrence below.
    branch_coefficients = [0] * (triplets + 1)
    return_coefficients = [0] * (triplets + 1)
    branch_coefficients[0] = 1
    return_coefficients[0] = 1

    if modulus is None:
        result = 0
        for index in range(1, triplets + 1):
            branch_coefficients[index] = (
                branches**index
                * comb(3 * index, index)
                // (2 * index + 1)
            )
            convolution = sum(
                branch_coefficients[left]
                * return_coefficients[index - left]
                for left in range(1, index + 1)
            )
            assert convolution % branches == 0
            return_coefficients[index] = (
                branch_coefficients[index] + convolution // branches
            )
            valid = (
                return_coefficients[index] * branches // alphabet_size
            )
            result += valid
        return result

    factorials = [1] * (3 * triplets + 1)
    for value in range(1, len(factorials)):
        factorials[value] = factorials[value - 1] * value % modulus
    inverse_factorials = [1] * len(factorials)
    inverse_factorials[-1] = pow(
        factorials[-1], modulus - 2, modulus
    )
    for value in range(len(factorials) - 1, 0, -1):
        inverse_factorials[value - 1] = (
            inverse_factorials[value] * value
        ) % modulus

    inverse_branches = pow(branches, modulus - 2, modulus)
    leading_factor = (
        branches * pow(alphabet_size, modulus - 2, modulus) % modulus
    )
    branch_power = 1
    result = 0

    for index in range(1, triplets + 1):
        branch_power = branch_power * branches % modulus
        branch_coefficients[index] = (
            branch_power
            * factorials[3 * index]
            % modulus
            * inverse_factorials[index]
            % modulus
            * inverse_factorials[2 * index]
            % modulus
            * pow(2 * index + 1, modulus - 2, modulus)
            % modulus
        )
        convolution = sum(
            branch_coefficients[left]
            * return_coefficients[index - left]
            for left in range(1, index + 1)
        ) % modulus
        return_coefficients[index] = (
            branch_coefficients[index]
            + convolution * inverse_branches
        ) % modulus
        result += leading_factor * return_coefficients[index]
        result %= modulus

    return result


def solve() -> int:
    assert triplicate_count(6) == 261
    assert triplicate_count(30) == 5_576_195_181_577_716
    return triplicate_count(LIMIT, modulus=MODULUS)


if __name__ == "__main__":
    print(solve())
