#!/usr/bin/env python3
import numpy as np


def expected_turns(card_count, rolls, tolerance=1e-13, max_iterations=10_000):
    """Solve the optimal stopping MDP by Bellman iteration."""
    state_count = 1 << card_count
    winning_state = state_count - 1
    states = np.arange(state_count, dtype=np.int32)

    move_tables = []
    for x, y in rolls:
        choices = {1 << (x - 1), 1 << (y - 1), 1 << (x + y - 1)}
        move_tables.append(np.vstack([states ^ bit for bit in choices]))

    values = np.zeros(state_count, dtype=np.float64)
    roll_weight = 1.0 / len(move_tables)

    for _ in range(max_iterations):
        previous = values
        values = np.ones(state_count, dtype=np.float64)
        for moves in move_tables:
            values += previous[moves].min(axis=0) * roll_weight
        values[winning_state] = 0.0

        if np.max(np.abs(values - previous)) < tolerance:
            return values[0]
    raise RuntimeError("Bellman iteration did not converge")


def solve():
    coin_rolls = [(x, y) for x in (1, 2) for y in (1, 2)]
    assert f"{expected_turns(4, coin_rolls):.6f}" == "5.673651"

    dice_rolls = [(x, y) for x in range(1, 7) for y in range(1, 7)]
    return f"{expected_turns(12, dice_rolls):.6f}"


if __name__ == "__main__":
    print(solve())
