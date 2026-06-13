#!/usr/bin/env python3
"""Project Euler 719: Number Splitting."""


LIMIT = 10**12


def _can_split_to(square: int, target: int) -> bool:
    digits = str(square)

    def search(position: int, remaining: int, pieces: int) -> bool:
        if position == len(digits):
            return remaining == 0 and pieces >= 2

        value = 0
        for end in range(position, len(digits)):
            value = 10 * value + ord(digits[end]) - 48
            if value > remaining:
                break
            if search(end + 1, remaining - value, pieces + 1):
                return True
        return False

    return search(0, target, 0)


def T(limit: int) -> int:
    root_limit = int(limit**0.5)
    while (root_limit + 1) * (root_limit + 1) <= limit:
        root_limit += 1
    while root_limit * root_limit > limit:
        root_limit -= 1

    total = 0
    for root in range(2, root_limit + 1):
        if root % 9 not in (0, 1):
            continue
        square = root * root
        if _can_split_to(square, root):
            total += square
    return total


def solve():
    return T(LIMIT)


if __name__ == "__main__":
    print(solve())
