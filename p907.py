#!/usr/bin/env python3
"""Project Euler 907: stacking all cups into one tower."""

from functools import lru_cache

MODULUS = 1_000_000_007
INITIAL_COUNTS = [2, 2, 6, 12, 16, 22, 36, 58, 82]
RECURRENCE = [2, -3, 5, -4, 4, -3, 1, -1]


def direct_count(cup_count: int) -> int:
    """Enumerate small towers directly.

    Read a tower from bottom to top.  If the current cup is upright, a
    nesting step goes to the next smaller cup; if it is inverted, it goes
    to the next larger cup.  A base-to-base or rim-to-rim step changes
    the size by two and flips the orientation.  Requiring one linear
    sequence also enforces the stated ban on a rim-to-rim branch.
    """
    full_mask = (1 << cup_count) - 1

    @lru_cache(None)
    def extend(last: int, used_mask: int, inverted: bool) -> int:
        if used_mask == full_mask:
            return 1

        result = 0
        for following in (
            last - 2,
            last - 1,
            last + 1,
            last + 2,
        ):
            if not 0 <= following < cup_count:
                continue
            if used_mask & (1 << following):
                continue

            difference = following - last
            next_mask = used_mask | (1 << following)
            if abs(difference) == 2:
                result += extend(
                    following,
                    next_mask,
                    not inverted,
                )
            elif difference == 1 and inverted:
                result += extend(
                    following,
                    next_mask,
                    inverted,
                )
            elif difference == -1 and not inverted:
                result += extend(
                    following,
                    next_mask,
                    inverted,
                )

        return result

    return sum(
        extend(start, 1 << start, inverted)
        for start in range(cup_count)
        for inverted in (False, True)
    )


def matrix_multiply(
    left: list[list[int]],
    right: list[list[int]],
) -> list[list[int]]:
    size = len(left)
    return [
        [
            sum(
                left[row][middle] * right[middle][column]
                for middle in range(size)
            )
            % MODULUS
            for column in range(size)
        ]
        for row in range(size)
    ]


def tower_count(cup_count: int) -> int:
    """Return S(cup_count) modulo MODULUS.

    A two-vertex frontier enumeration of the Hamiltonian tower sequence
    gives

      G(x) = (2x-2x^2+8x^3-4x^4+8x^5-4x^6+2x^7-2x^9)
             / ((1+x^2)^2 (1-2x+x^2-x^3+x^4)).

    The denominator yields RECURRENCE from n=10 onward.
    """
    if cup_count <= len(INITIAL_COUNTS):
        return INITIAL_COUNTS[cup_count - 1]

    order = len(RECURRENCE)
    transition = [
        [coefficient % MODULUS for coefficient in RECURRENCE],
        *[
            [
                int(column == row - 1)
                for column in range(order)
            ]
            for row in range(1, order)
        ],
    ]
    power = [
        [int(row == column) for column in range(order)]
        for row in range(order)
    ]

    exponent = cup_count - len(INITIAL_COUNTS)
    while exponent:
        if exponent & 1:
            power = matrix_multiply(power, transition)
        transition = matrix_multiply(transition, transition)
        exponent //= 2

    state_at_nine = INITIAL_COUNTS[1:][::-1]
    return sum(
        power[0][index] * state_at_nine[index]
        for index in range(order)
    ) % MODULUS


def solve() -> int:
    assert direct_count(4) == tower_count(4) == 12
    assert direct_count(8) == tower_count(8) == 58
    assert tower_count(20) == 5_560
    return tower_count(10**7)


if __name__ == "__main__":
    print(solve())
