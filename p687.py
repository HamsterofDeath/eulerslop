#!/usr/bin/env python3
"""Project Euler 687: Shuffling Cards."""

from collections import defaultdict
from math import factorial


RANKS = 13
CARDS_PER_RANK = 4
PRIME_COUNTS = {2, 3, 5, 7, 11, 13}


def _perfect_rank_distribution():
    """Count rank sequences by how many ranks never appear adjacently."""
    good = [0] * (CARDS_PER_RANK + 1)
    bad = [0] * (CARDS_PER_RANK + 1)
    good[CARDS_PER_RANK] = RANKS

    # State: counts of still-good and already-bad ranks by remaining cards,
    # followed by the previous rank's status (0 none, 1 good, 2 bad) and
    # remaining-card count.  Ranks are labelled, but symmetric within bins.
    states = {(tuple(good), tuple(bad), 0, 0): 1}

    for _ in range(RANKS * CARDS_PER_RANK):
        next_states = defaultdict(int)
        for (good_state, bad_state, last_status, last_remaining), ways in states.items():
            good = list(good_state)
            bad = list(bad_state)

            for remaining in range(1, CARDS_PER_RANK + 1):
                count = good[remaining]
                if count == 0:
                    continue

                other_count = count - (
                    1 if last_status == 1 and last_remaining == remaining else 0
                )
                if other_count:
                    new_good = good.copy()
                    new_good[remaining] -= 1
                    new_good[remaining - 1] += 1
                    next_states[
                        (tuple(new_good), bad_state, 1, remaining - 1)
                    ] += ways * other_count

                if last_status == 1 and last_remaining == remaining:
                    new_good = good.copy()
                    new_bad = bad.copy()
                    new_good[remaining] -= 1
                    new_bad[remaining - 1] += 1
                    next_states[
                        (tuple(new_good), tuple(new_bad), 2, remaining - 1)
                    ] += ways

            for remaining in range(1, CARDS_PER_RANK + 1):
                count = bad[remaining]
                if count == 0:
                    continue

                other_count = count - (
                    1 if last_status == 2 and last_remaining == remaining else 0
                )
                if other_count:
                    new_bad = bad.copy()
                    new_bad[remaining] -= 1
                    new_bad[remaining - 1] += 1
                    next_states[
                        (good_state, tuple(new_bad), 2, remaining - 1)
                    ] += ways * other_count

                if last_status == 2 and last_remaining == remaining:
                    new_bad = bad.copy()
                    new_bad[remaining] -= 1
                    new_bad[remaining - 1] += 1
                    next_states[
                        (good_state, tuple(new_bad), 2, remaining - 1)
                    ] += ways

        states = next_states

    distribution = [0] * (RANKS + 1)
    for state, ways in states.items():
        distribution[state[0][0]] += ways

    return distribution


def solve():
    distribution = _perfect_rank_distribution()
    numerator = sum(distribution[count] for count in PRIME_COUNTS)
    denominator = sum(distribution)

    assert denominator == factorial(RANKS * CARDS_PER_RANK) // (
        factorial(CARDS_PER_RANK) ** RANKS
    )

    scale = 10**10
    rounded = (numerator * scale + denominator // 2) // denominator
    return f"{rounded // scale}.{rounded % scale:010d}"


if __name__ == "__main__":
    print(solve())
