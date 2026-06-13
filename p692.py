#!/usr/bin/env python3
"""Project Euler 692: Siegbert and Jo."""

from bisect import bisect_right
from functools import cache


LIMIT = 23_416_728_348_467_685


def _fibonacci_numbers(limit):
    numbers = [1, 2]
    while numbers[-1] < limit:
        numbers.append(numbers[-1] + numbers[-2])
    return tuple(numbers)


FIBONACCI = _fibonacci_numbers(LIMIT)


@cache
def _summatory_minimal_winning_take(limit):
    if limit <= 0:
        return 0

    index = bisect_right(FIBONACCI, limit) - 1
    largest = FIBONACCI[index]
    remainder = limit - largest

    # H(n) is the smallest Fibonacci summand in the Zeckendorf form of n.
    return (
        _summatory_minimal_winning_take(largest - 1)
        + largest
        + _summatory_minimal_winning_take(remainder)
    )


def solve():
    return _summatory_minimal_winning_take(LIMIT)


if __name__ == "__main__":
    print(solve())
