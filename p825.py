#!/usr/bin/env python3
"""Project Euler 825: alternating cars on a circular track."""

from math import log, sqrt
import numpy as np


LIMIT = 10**14
SHIFT = (3 + sqrt(3)) / 6


def s_direct(n: int) -> float:
    """Solve the exact finite Markov recurrence for a single small n."""
    states = 2 * n
    matrix = np.eye(states)
    rhs = np.zeros(states)

    for gap in range(1, states + 1):
        row = gap - 1
        for move in (1, 2, 3):
            if move >= gap:
                rhs[row] += 1 / 3
            else:
                rhs[row] += 1 / 3
                next_gap = states - gap + move
                matrix[row, next_gap - 1] += 1 / 3

    first_win = np.linalg.solve(matrix, rhs)[n - 1]
    return 2 * first_win - 1


def digamma(x: float) -> float:
    """Enough of psi(x) for a 1e14 shifted harmonic sum in double precision."""
    total = 0.0
    while x < 50.0:
        total -= 1.0 / x
        x += 1.0

    inv = 1.0 / x
    inv2 = inv * inv
    correction = inv2 * (
        1 / 12
        - inv2
        * (
            1 / 120
            - inv2 * (1 / 252 - inv2 * (1 / 240 - inv2 * (5 / 660)))
        )
    )
    return total + log(x) - 0.5 * inv - correction


def shifted_harmonic(limit: int) -> float:
    return digamma(limit + 1 - SHIFT) - digamma(2 - SHIFT)


def solve() -> str:
    direct_t10 = sum(s_direct(n) for n in range(2, 11))
    assert f"{direct_t10:.8f}" == "2.38235282"

    correction = sum(s_direct(n) - 1.0 / (n - SHIFT) for n in range(2, 41))
    answer = shifted_harmonic(LIMIT) + correction
    return f"{answer:.8f}"


if __name__ == "__main__":
    print(solve())
