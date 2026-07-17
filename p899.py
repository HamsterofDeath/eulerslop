#!/usr/bin/env python3
"""Project Euler 899: losing thresholds in the two-pile game."""


def losing_pair_count(limit: int) -> int:
    """Return L(limit).

    For x <= y, every move produces a split of y.  Induction on x+y
    shows that the losing positions are exactly

        y odd,  1 <= x <= 2^v2(y+1)-1.

    Summing over y=2j-1 reduces the answer to the valuation sum
    sum_{j<=m} 2^v2(j).  Diagonal pairs are subtracted once after
    reflecting the off-diagonal pairs.
    """
    half_count = (limit + 1) // 2
    valuation_sum = 0
    power = 1
    while power <= half_count:
        exact_count = (
            half_count // power - half_count // (2 * power)
        )
        valuation_sum += power * exact_count
        power *= 2

    diagonal_count = (limit + 1).bit_length() - 1
    return (
        4 * valuation_sum
        - 2 * half_count
        - diagonal_count
    )


def solve() -> int:
    assert losing_pair_count(7) == 21
    assert losing_pair_count(7**2) == 221
    return losing_pair_count(7**17)


if __name__ == "__main__":
    print(solve())
