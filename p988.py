#!/usr/bin/env python3
"""Project Euler Problem 988: Non-attacking Frogs.

The positive integers unreachable from zero are exactly the gaps of the
two-generator numerical semigroup.  Each gap has a unique representation

    ab - ia - jb > 0,  i,j >= 1.

The difference between two gaps is reachable precisely when their
(i,j) cells are comparable coordinatewise.  A non-attacking configuration
therefore corresponds to an antichain in the Ferrers diagram below
ia + jb = ab.

Scanning rows in increasing i, an antichain chooses at most one cell per
row, and chosen j values strictly decrease.  The DP stores the last j,
the number of partial antichains, and their total frog-location sum.
"""


def configuration_totals(first_jump: int, second_jump: int) -> tuple[int, int]:
    # The sentinel last column first_jump represents the empty antichain.
    counts = [0] * (first_jump + 1)
    location_sums = [0] * (first_jump + 1)
    counts[first_jump] = 1

    product = first_jump * second_jump
    for row in range(1, second_jump):
        row_height = (
            product - first_jump * row - 1
        ) // second_jump
        next_counts = counts[:]
        next_sums = location_sums[:]

        for previous_column in range(1, first_jump + 1):
            maximum_column = min(row_height, previous_column - 1)
            for column in range(1, maximum_column + 1):
                location = (
                    product
                    - first_jump * row
                    - second_jump * column
                )
                next_counts[column] += counts[previous_column]
                next_sums[column] += (
                    location_sums[previous_column]
                    + counts[previous_column] * location
                )

        counts, location_sums = next_counts, next_sums

    return sum(counts), sum(location_sums)


def solve() -> int:
    assert configuration_totals(3, 5) == (7, 23)
    assert configuration_totals(5, 13)[1] == 16_336
    return configuration_totals(19, 53)[1]


if __name__ == "__main__":
    print(solve())
