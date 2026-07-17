#!/usr/bin/env python3
"""Project Euler 857: count beautiful labelled graphs."""

from math import factorial


LIMIT = 10_000_000
MODULUS = 1_000_000_007

# Numbers of green/brown colourings of K_k without a monochromatic triangle.
# Ramsey's theorem R(3, 3) = 6 makes every larger block impossible.
BLOCK_COUNTS = (1, 2, 6, 18, 12)


def recurrence_term(
    initial: list[int],
    coefficients: list[int],
    index: int,
    modulus: int,
) -> int:
    """Evaluate a constant-coefficient recurrence using Kitamasa reduction."""
    order = len(coefficients)

    def combine(first: list[int], second: list[int]) -> list[int]:
        product = [0] * (2 * order - 1)
        for left_index, left in enumerate(first):
            for right_index, right in enumerate(second):
                degree = left_index + right_index
                product[degree] = (
                    product[degree] + left * right
                ) % modulus

        for degree in range(2 * order - 2, order - 1, -1):
            multiplier = product[degree]
            for lag, coefficient in enumerate(coefficients, 1):
                product[degree - lag] = (
                    product[degree - lag] + multiplier * coefficient
                ) % modulus
        return product[:order]

    result = [1] + [0] * (order - 1)
    power = [0, 1] + [0] * (order - 2)
    while index:
        if index & 1:
            result = combine(result, power)
        power = combine(power, power)
        index //= 2

    return sum(
        weight * value for weight, value in zip(result, initial)
    ) % modulus


def beautiful_graphs(vertices: int, modulus: int = MODULUS) -> int:
    """Return G(vertices) modulo modulus."""
    # A beautiful graph is an ordered sequence of undirected blocks.  Inside
    # a block all edges are green/brown with no monochromatic triangle;
    # edges between blocks have the unique red/blue orientation induced by
    # the block order.
    coefficients = [
        count * pow(factorial(size), modulus - 2, modulus) % modulus
        for size, count in enumerate(BLOCK_COUNTS, 1)
    ]

    # For a_n = G(n)/n!, the labelled-block recurrence is
    # a_n = sum_k (c_k/k!) a_(n-k).
    initial = [1]
    for index in range(1, len(coefficients)):
        initial.append(
            sum(
                coefficients[lag - 1] * initial[index - lag]
                for lag in range(1, index + 1)
            )
            % modulus
        )

    normalized = recurrence_term(
        initial, coefficients, vertices, modulus
    )
    vertex_factorial = 1
    for value in range(2, vertices + 1):
        vertex_factorial = vertex_factorial * value % modulus
    return normalized * vertex_factorial % modulus


def solve() -> int:
    assert beautiful_graphs(3) == 24
    assert beautiful_graphs(4) == 186
    assert (
        beautiful_graphs(15)
        == 12_472_315_010_483_328 % MODULUS
    )
    return beautiful_graphs(LIMIT)


if __name__ == "__main__":
    print(solve())
