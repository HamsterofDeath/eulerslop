#!/usr/bin/env python3
"""Project Euler Problem 982: The Third Dice.

For each visible multiset s, let q_s be the probability that Bob chooses
the hidden die.  If Alice hides h and the largest visible value is m,
Bob's expected payment is

    m + q_s * (h - m).

For each rolled multiset t, introduce v_t, the minimum payment Alice can
force after seeing t.  The constraints

    v_t <= m + q_s * (h - m)

for every possible hidden die form a linear program.  Bob maximizes the
weighted sum of the v_t values, while 0 <= q_s <= 1.  The small LP is
solved exactly with a rational simplex tableau.
"""

from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import combinations_with_replacement
from math import factorial, prod


def simplex_maximum(
    constraints: list[list[Fraction]],
    bounds: list[Fraction],
    objective: list[Fraction],
) -> Fraction:
    """Maximize objective*x subject to constraints*x <= bounds, x >= 0."""
    row_count = len(constraints)
    variable_count = len(objective)
    column_count = variable_count + row_count

    tableau = [
        row + [Fraction(0)] * row_count + [bound]
        for row, bound in zip(constraints, bounds)
    ]
    for row_index in range(row_count):
        tableau[row_index][variable_count + row_index] = Fraction(1)
    tableau.append(
        [-coefficient for coefficient in objective]
        + [Fraction(0)] * row_count
        + [Fraction(0)]
    )

    while True:
        entering = next(
            (
                column
                for column in range(column_count)
                if tableau[-1][column] < 0
            ),
            None,
        )
        if entering is None:
            return tableau[-1][-1]

        leaving_options = [
            (tableau[row][-1] / tableau[row][entering], row)
            for row in range(row_count)
            if tableau[row][entering] > 0
        ]
        if not leaving_options:
            raise ValueError("unbounded linear program")
        _, leaving = min(leaving_options)

        pivot = tableau[leaving][entering]
        tableau[leaving] = [
            entry / pivot for entry in tableau[leaving]
        ]
        for row in range(row_count + 1):
            if row == leaving:
                continue
            multiplier = tableau[row][entering]
            if multiplier:
                tableau[row] = [
                    entry - multiplier * pivot_entry
                    for entry, pivot_entry in zip(
                        tableau[row], tableau[leaving]
                    )
                ]


def state_multiplicity(state: tuple[int, ...]) -> int:
    return factorial(len(state)) // prod(
        factorial(count) for count in Counter(state).values()
    )


def game_value(dice_count: int, side_count: int) -> Fraction:
    signals = list(
        combinations_with_replacement(
            range(1, side_count + 1), dice_count - 1
        )
    )
    signal_index = {signal: index for index, signal in enumerate(signals)}
    states = list(
        combinations_with_replacement(
            range(1, side_count + 1), dice_count
        )
    )

    signal_count = len(signals)
    variable_count = signal_count + len(states)
    constraints: list[list[Fraction]] = []
    bounds: list[Fraction] = []

    for state_index, state in enumerate(states):
        for hidden_index, hidden_value in enumerate(state):
            if (
                hidden_index > 0
                and hidden_value == state[hidden_index - 1]
            ):
                continue

            visible = state[:hidden_index] + state[hidden_index + 1 :]
            visible_payoff = max(visible)
            row = [Fraction(0)] * variable_count
            row[signal_index[visible]] = Fraction(
                visible_payoff - hidden_value
            )
            row[signal_count + state_index] = Fraction(1)
            constraints.append(row)
            bounds.append(Fraction(visible_payoff))

    for signal in range(signal_count):
        row = [Fraction(0)] * variable_count
        row[signal] = Fraction(1)
        constraints.append(row)
        bounds.append(Fraction(1))

    objective = [Fraction(0)] * signal_count + [
        Fraction(state_multiplicity(state)) for state in states
    ]
    weighted_value = simplex_maximum(constraints, bounds, objective)
    return weighted_value / side_count**dice_count


def solve() -> str:
    assert game_value(2, 6) == Fraction(145, 36)
    value = game_value(3, 6)
    with localcontext() as context:
        context.prec = 30
        decimal_value = Decimal(value.numerator) / value.denominator
        return f"{decimal_value:.6f}"


if __name__ == "__main__":
    print(solve())
