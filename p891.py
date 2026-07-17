#!/usr/bin/env python3
"""Project Euler 891: ambiguous configurations of three clock hands."""

from itertools import permutations
from math import gcd


def ambiguity_sets() -> list[tuple[int, int]]:
    """Return (all projected times, fixed times) for each permutation type."""
    rates = (1, 12, 720)
    identity = (0, 1, 2)
    result: set[tuple[int, int]] = set()

    for permutation in permutations(range(3)):
        if permutation == identity:
            continue

        # Subtract the equation for hand zero from those for hands one
        # and two.  The kernel of this integer matrix on (R/Z)^2 is the
        # set of pairs (t,t') producing the same unlabeled reading.
        a = rates[1] - rates[0]
        b = -(rates[permutation[1]] - rates[permutation[0]])
        c = rates[2] - rates[0]
        d = -(rates[permutation[2]] - rates[permutation[0]])
        determinant = abs(a * d - b * c)

        projection_fibre = gcd(determinant, abs(b), abs(d))
        assert projection_fibre == 1
        projected_times = determinant

        # Setting t'=t leaves two one-variable congruences.
        fixed_times = gcd(abs(a + b), abs(c + d))
        result.add((projected_times, fixed_times))

    return sorted(result)


def ambiguous_moment_count() -> int:
    """Count the union of G_D minus G_f over the permutation types.

    Here G_m is the subgroup of R/Z consisting of multiples of 1/m.
    Intersections satisfy G_a intersection G_b = G_gcd(a,b), so two
    tiny inclusion-exclusion loops replace explicit rational sets.
    """
    sets = ambiguity_sets()
    result = 0

    for chosen_mask in range(1, 1 << len(sets)):
        chosen = [
            index
            for index in range(len(sets))
            if chosen_mask & (1 << index)
        ]
        common_order = 0
        for index in chosen:
            common_order = gcd(common_order, sets[index][0])

        intersection_size = 0
        for fixed_mask in range(1 << len(chosen)):
            order = common_order
            for position, index in enumerate(chosen):
                if fixed_mask & (1 << position):
                    order = gcd(order, sets[index][1])
            if fixed_mask.bit_count() % 2:
                intersection_size -= order
            else:
                intersection_size += order

        if len(chosen) % 2:
            result += intersection_size
        else:
            result -= intersection_size

    return result


def solve() -> int:
    return ambiguous_moment_count()


if __name__ == "__main__":
    print(solve())
