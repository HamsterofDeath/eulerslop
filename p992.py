#!/usr/bin/env python3
"""Project Euler Problem 992: Another Frog Jumping.

For a fixed final stone t, flow conservation uniquely determines the
numbers L_i and R_i of left and right crossings of every edge i.
Journeys are Euler trails of that directed path multigraph.

The directed BEST theorem counts them as

    arborescences(t) * product_v (out(v)-1+[v=t])!
    ------------------------------------------------,
                   product_i L_i! R_i!

where a path has product(R_i for i<=t, L_i for i>t)
arborescences directed towards t.
"""


MODULUS = 987_898_789
N = 500
K_VALUES = (1, 10, 100, 1_000, 10_000)


def factorial_tables(limit: int) -> tuple[list[int], list[int]]:
    factorial = [1] * (limit + 1)
    for value in range(1, limit + 1):
        factorial[value] = factorial[value - 1] * value % MODULUS

    inverse_factorial = [1] * (limit + 1)
    inverse_factorial[limit] = pow(
        factorial[limit], MODULUS - 2, MODULUS
    )
    for value in range(limit, 0, -1):
        inverse_factorial[value - 1] = (
            inverse_factorial[value] * value % MODULUS
        )
    return factorial, inverse_factorial


def journey_count(
    n: int,
    k: int,
    factorial: list[int],
    inverse_factorial: list[int],
) -> int:
    answer = 0

    for finish in range(n + 1):
        left = [0] * (n + 1)
        right = [0] * (n + 1)
        left[1] = k - 1

        for edge in range(1, n + 1):
            right[edge] = left[edge] + (edge <= finish)
            if edge < n:
                right_arrivals = right[edge]
                left[edge + 1] = k + edge - right_arrivals

        # An entirely unused suffix is outside the Euler trail's support.
        # This only matters for tiny generic inputs (not for n=500), but
        # makes the formula include the empty n=1, k=1 journey correctly.
        support_end = n
        while (
            support_end > 0
            and left[support_end] + right[support_end] == 0
        ):
            support_end -= 1

        trails = 1
        for edge in range(1, support_end + 1):
            tree_choices = (
                right[edge] if edge <= finish else left[edge]
            )
            trails = trails * tree_choices % MODULUS
            trails = trails * inverse_factorial[left[edge]] % MODULUS
            trails = trails * inverse_factorial[right[edge]] % MODULUS

        for stone in range(support_end + 1):
            out_degree = 0
            if stone > 0:
                out_degree += left[stone]
            if stone < support_end:
                out_degree += right[stone + 1]
            factorial_index = out_degree - 1 + (stone == finish)
            if factorial_index < 0:
                trails = 0
                break
            trails = trails * factorial[factorial_index] % MODULUS

        answer = (answer + trails) % MODULUS

    return answer


def solve() -> int:
    factorial, inverse_factorial = factorial_tables(max(K_VALUES) + N)
    return sum(
        journey_count(N, k, factorial, inverse_factorial)
        for k in K_VALUES
    ) % MODULUS


if __name__ == "__main__":
    sample_factorial, sample_inverse = factorial_tables(20)
    assert journey_count(3, 2, sample_factorial, sample_inverse) == 17
    assert journey_count(6, 1, sample_factorial, sample_inverse) == 1320
    assert (
        journey_count(6, 5, sample_factorial, sample_inverse)
        == 16_793_280
    )
    print(solve())
