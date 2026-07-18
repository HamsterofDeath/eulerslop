#!/usr/bin/env python3
"""Project Euler Problem 951: A Game of Chance.

Let P_i be the probability that the player about to play wins from the
suffix starting at i, and put Q_i = 2*P_i-1.  Prepending a card gives

    Q_new = -Q_i                    if the colours differ,
    Q_new = -(Q_i + Q_(i+1)) / 2   if the colours agree.

For a suffix of length L, scaling both Q values by 2**(L-1) makes every
state integral.  The dynamic program below builds decks right-to-left
while tracking the two scaled values, the first colour, and the number
of red cards.  A full deck is fair exactly when its first scaled value
is zero.
"""

from collections import defaultdict


State = tuple[int, int, int, int]


def count_fair(n: int) -> int:
    total_length = 2 * n

    # (first colour, scaled Q_i, scaled Q_(i+1), red count)
    states: dict[State, int] = {
        (0, 1, -1, 0): 1,
        (1, 1, -1, 1): 1,
    }

    for length in range(2, total_length + 1):
        remaining = total_length - length
        following: dict[State, int] = defaultdict(int)

        for (colour, current_q, next_q, reds), count in states.items():
            different_colour = 1 - colour
            different_reds = reds + different_colour
            if different_reds <= n <= different_reds + remaining:
                state = (
                    different_colour,
                    -2 * current_q,
                    2 * current_q,
                    different_reds,
                )
                following[state] += count

            same_reds = reds + colour
            if same_reds <= n <= same_reds + remaining:
                state = (
                    colour,
                    -(current_q + next_q),
                    2 * current_q,
                    same_reds,
                )
                following[state] += count

        states = following

    return sum(
        count
        for (_, current_q, _, _), count in states.items()
        if current_q == 0
    )


def solve() -> int:
    assert count_fair(2) == 4
    assert count_fair(8) == 11892
    return count_fair(26)


if __name__ == "__main__":
    print(solve())
