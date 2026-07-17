#!/usr/bin/env python3
"""Project Euler 856: expected wait for consecutive equal card ranks."""

from collections import defaultdict
from decimal import Decimal, localcontext


def expected_draws(ranks: int, copies_per_rank: int) -> Decimal:
    """Return the expected stopping draw for the given deck."""
    # counts[r] is the number of ranks with r cards remaining.  The final
    # component records how many cards remain in the rank drawn most recently.
    initial = (0,) * copies_per_rank + (ranks, -1)

    with localcontext() as context:
        context.prec = 40
        states = {initial: Decimal(1)}
        expectation = Decimal(0)
        deck_size = ranks * copies_per_rank

        # E[T] = sum_{k=0}^{deck_size-1} P(T > k).
        for drawn in range(deck_size):
            expectation += sum(states.values(), Decimal(0))
            remaining_cards = Decimal(deck_size - drawn)
            next_states = defaultdict(Decimal)

            for state, probability in states.items():
                counts = list(state[: copies_per_rank + 1])
                last_remaining = state[-1]

                for remaining in range(1, copies_per_rank + 1):
                    eligible_ranks = counts[remaining]
                    if last_remaining == remaining:
                        eligible_ranks -= 1
                    if eligible_ranks == 0:
                        continue

                    next_counts = counts.copy()
                    next_counts[remaining] -= 1
                    next_counts[remaining - 1] += 1
                    next_state = tuple(next_counts) + (remaining - 1,)
                    ways = eligible_ranks * remaining
                    next_states[next_state] += (
                        probability * ways / remaining_cards
                    )

            states = next_states

        return +expectation


def solve() -> str:
    assert expected_draws(1, 4) == 2
    assert expected_draws(2, 2) == 3
    return f"{expected_draws(13, 4):.8f}"


if __name__ == "__main__":
    print(solve())
