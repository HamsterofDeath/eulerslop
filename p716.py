#!/usr/bin/env python3
"""Project Euler 716: grid graph SCC sums."""

MOD = 1_000_000_007


def split_sums(length: int, overlap: bool) -> tuple[int, int]:
    """Return sums of single-orientation and both-orientation split counts.

    A directed rectangle cycle exists for a sign ``s`` when the row split has
    sign ``s`` on one side and ``1-s`` on the other, and similarly for columns.
    ``overlap`` means the split is around a vertex line, so the two sides share
    one sign position; otherwise it is between two adjacent positions.
    """

    powers = [1] * (length + 1)
    for i in range(1, length + 1):
        powers[i] = powers[i - 1] * 2 % MOD

    single_total = 0
    both_total = 0
    positions = range(length) if overlap else range(length - 1)
    for i in positions:
        if overlap:
            left = i + 1
            right = length - i
            single = powers[length] - powers[length - left] - powers[length - right]
            both = (
                powers[length]
                - 2 * powers[length - left]
                - 2 * powers[length - right]
                + 2
            )
        else:
            left = i + 1
            right = length - i - 1
            single = (powers[left] - 1) * (powers[right] - 1)
            both = (powers[left] - 2) * (powers[right] - 2)

        single_total = (single_total + single) % MOD
        both_total = (both_total + both) % MOD

    return single_total, both_total


def covered_sum(row_split: tuple[int, int], col_split: tuple[int, int]) -> int:
    single_rows, both_rows = row_split
    single_cols, both_cols = col_split
    return (2 * single_rows * single_cols - both_rows * both_cols) % MOD


def c_value(height: int, width: int) -> int:
    row_overlap = split_sums(height, True)
    row_disjoint = split_sums(height, False)
    col_overlap = split_sums(width, True)
    col_disjoint = split_sums(width, False)

    vertices = height * width * pow(2, height + width, MOD)
    horizontal_edges = covered_sum(row_overlap, col_disjoint)
    vertical_edges = covered_sum(row_disjoint, col_overlap)
    faces = covered_sum(row_disjoint, col_disjoint)
    return (vertices - horizontal_edges - vertical_edges + faces) % MOD


def solve() -> int:
    assert c_value(3, 3) == 408
    assert c_value(3, 6) == 4696
    assert c_value(10, 20) == 988_971_143
    return c_value(10_000, 20_000)


if __name__ == "__main__":
    print(solve())
