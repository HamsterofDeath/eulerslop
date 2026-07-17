#!/usr/bin/env python3
"""Project Euler 884: summatory greedy cube subtraction."""


LIMIT = 10**17


def integer_cube_root(number: int) -> int:
    root = int(number ** (1 / 3))
    while (root + 1) ** 3 <= number:
        root += 1
    while root**3 > number:
        root -= 1
    return root


def summatory_steps(limit: int) -> int:
    """Return S(limit).

    On the interval n=k^3+r, 0 <= r < (k+1)^3-k^3, the first
    subtraction leaves r.  Hence a full interval contributes

        delta_k + S(delta_k),  delta_k=3k^2+3k+1.

    The table stores prefix sums of those full-interval contributions.
    Since cbrt(delta_k) < k (apart from harmless initial boundary
    cases), its entries can be built in increasing order.
    """
    if limit <= 1:
        return 0

    largest_cube_index = integer_cube_root(limit - 1)
    interval_prefix = [0] * (largest_cube_index + 1)

    def evaluate(argument: int) -> int:
        result = 0
        while argument > 1:
            cube_index = integer_cube_root(argument - 1)
            result += interval_prefix[cube_index - 1]

            partial_length = argument - cube_index**3
            result += partial_length
            argument = partial_length
        return result

    for cube_index in range(1, largest_cube_index + 1):
        interval_length = (
            3 * cube_index * cube_index + 3 * cube_index + 1
        )
        interval_prefix[cube_index] = (
            interval_prefix[cube_index - 1]
            + interval_length
            + evaluate(interval_length)
        )

    return evaluate(limit)


def solve() -> int:
    assert summatory_steps(100) == 512
    return summatory_steps(LIMIT)


if __name__ == "__main__":
    print(solve())
