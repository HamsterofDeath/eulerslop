"""Project Euler Problem 918: Recursive Sequence Sum.

Pairing adjacent terms makes the prefix sum telescope:

    S(2m)   = 4 - a_m
    S(2m+1) = 4 - 3*a_(m+1).

The pair (a_n, a_(n+1)) can itself be found by following the binary digits of
n, so the trillion-term prefix needs only logarithmic work.
"""

from functools import cache


TARGET = 10**12


@cache
def adjacent_terms(index: int) -> tuple[int, int]:
    """Return (a_index, a_(index+1))."""
    if index == 1:
        return 1, 2

    lower, upper = adjacent_terms(index // 2)
    odd_term = lower - 3 * upper
    if index % 2:
        return odd_term, 2 * upper
    return 2 * lower, odd_term


def prefix_sum(limit: int) -> int:
    half = limit // 2
    if limit % 2 == 0:
        return 4 - adjacent_terms(half)[0]
    return 4 - 3 * adjacent_terms(half + 1)[0]


def solve() -> int:
    assert prefix_sum(10) == -13
    return prefix_sum(TARGET)


if __name__ == "__main__":
    print(solve())
