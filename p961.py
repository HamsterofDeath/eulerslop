#!/usr/bin/env python3
"""Project Euler Problem 961: Removing Digits.

Only whether a digit is zero matters to the game.  Replace every
nonzero digit by 1; a binary pattern with k ones represents 9**k
decimal numbers.  After deleting one bit, leading zeroes are stripped
exactly as in the original game.

There are fewer than 2**18 canonical patterns of at most 18 digits, so
their normal-play outcomes can be memoized directly.
"""

from functools import cache


@cache
def is_winning(pattern: str) -> bool:
    if not pattern:
        return False

    for index in range(len(pattern)):
        child = (
            pattern[:index] + pattern[index + 1 :]
        ).lstrip("0")
        if not is_winning(child):
            return True
    return False


def count_winning(maximum_digits: int) -> int:
    result = 0

    for length in range(1, maximum_digits + 1):
        for bits in range(1 << (length - 1), 1 << length):
            pattern = format(bits, f"0{length}b")
            if is_winning(pattern):
                result += 9 ** bits.bit_count()

    return result


def solve() -> int:
    assert count_winning(2) == 18
    assert count_winning(4) == 1656
    return count_winning(18)


if __name__ == "__main__":
    print(solve())
