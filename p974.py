#!/usr/bin/env python3
"""Project Euler Problem 974: Very Odd Numbers.

All allowed digits are nonzero, so numeric order is length followed by
lexicographic order.  A suffix-counting DP tracks the current remainder
modulo 105 and the parity mask of the five odd digit counts.  Counts by
length locate the requested block, after which standard lexicographic
unranking determines each digit.
"""

from functools import cache


DIGITS = (1, 3, 5, 7, 9)
MODULUS = 105
TARGET_MASK = (1 << len(DIGITS)) - 1
TARGET_INDEX = 10**16


@cache
def completion_count(
    remaining: int,
    parity_mask: int,
    remainder: int,
) -> int:
    if remaining == 0:
        return int(
            parity_mask == TARGET_MASK and remainder == 0
        )

    return sum(
        completion_count(
            remaining - 1,
            parity_mask ^ (1 << digit_index),
            (10 * remainder + digit) % MODULUS,
        )
        for digit_index, digit in enumerate(DIGITS)
    )


def very_odd_number(index: int) -> str:
    length = 1
    while True:
        count = completion_count(length, 0, 0)
        if index <= count:
            break
        index -= count
        length += 1

    parity_mask = 0
    remainder = 0
    result = []
    for position in range(length):
        remaining = length - position - 1
        for digit_index, digit in enumerate(DIGITS):
            next_mask = parity_mask ^ (1 << digit_index)
            next_remainder = (10 * remainder + digit) % MODULUS
            count = completion_count(
                remaining, next_mask, next_remainder
            )
            if index > count:
                index -= count
            else:
                result.append(str(digit))
                parity_mask = next_mask
                remainder = next_remainder
                break
        else:
            raise AssertionError("index exceeded the valid numbers")

    assert parity_mask == TARGET_MASK and remainder == 0
    return "".join(result)


def solve() -> str:
    assert very_odd_number(1) == "1117935"
    assert very_odd_number(1000) == "11137955115"
    return very_odd_number(TARGET_INDEX)


if __name__ == "__main__":
    print(solve())
