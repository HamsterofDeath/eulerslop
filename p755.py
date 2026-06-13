#!/usr/bin/env python3
"""Project Euler 755: Fibonacci subset sums."""

from functools import cache


TARGET = 10**13


def build_fibonacci(limit: int) -> tuple[list[int], list[int]]:
    fib = [1, 2]
    while fib[-1] <= limit:
        fib.append(fib[-1] + fib[-2])
    prefix = [0]
    for value in fib:
        prefix.append(prefix[-1] + value)
    return fib, prefix


FIB, PREFIX = build_fibonacci(TARGET)


@cache
def count_with_first_terms(terms: int, limit: int) -> int:
    if limit < 0:
        return 0
    if terms == 0:
        return 1
    if limit >= PREFIX[terms]:
        return 1 << terms
    return count_with_first_terms(terms - 1, limit) + count_with_first_terms(
        terms - 1, limit - FIB[terms - 1]
    )


def s_value(limit: int) -> int:
    terms = 0
    while terms < len(FIB) and FIB[terms] <= limit:
        terms += 1
    return count_with_first_terms(terms, limit)


def solve() -> int:
    assert s_value(100) == 415
    assert s_value(10**4) == 312807
    return s_value(TARGET)


if __name__ == "__main__":
    print(solve())
