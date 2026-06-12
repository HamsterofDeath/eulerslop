#!/usr/bin/env python3

from functools import lru_cache

import numpy as np


@lru_cache(maxsize=None)
def expected_time(maximum, minimum):
    later_times = list(range(minimum + 5, maximum + 6))
    probability = 1.0 / len(later_times)
    residual_limit = maximum + 5

    def caught_index(residual):
        return residual - 1

    def ahead_index(residual):
        return residual_limit + residual - 1

    both_caught = 2 * residual_limit
    both_ahead = both_caught + 1
    size = both_ahead + 1

    matrix = np.eye(size)
    rhs = np.zeros(size)

    for residual in range(1, residual_limit + 1):
        row = caught_index(residual)
        for next_time in later_times:
            rhs[row] += probability * min(next_time, residual)
            if next_time == residual:
                matrix[row, both_caught] -= probability
            else:
                matrix[row, ahead_index(abs(next_time - residual))] -= probability

        row = ahead_index(residual)
        for next_time in later_times:
            if next_time < residual:
                rhs[row] += probability * next_time
            elif next_time == residual:
                rhs[row] += probability * next_time
                matrix[row, both_ahead] -= probability
            else:
                rhs[row] += probability * residual
                matrix[row, caught_index(next_time - residual)] -= probability

    row = both_caught
    for first in later_times:
        for second in later_times:
            p = probability * probability
            rhs[row] += p * min(first, second)
            if first == second:
                matrix[row, both_caught] -= p
            else:
                matrix[row, ahead_index(abs(first - second))] -= p

    row = both_ahead
    for leader in later_times:
        for trailer in later_times:
            p = probability * probability
            if leader < trailer:
                rhs[row] += p * leader
            elif leader == trailer:
                rhs[row] += p * leader
                matrix[row, both_ahead] -= p
            else:
                rhs[row] += p * trailer
                matrix[row, caught_index(leader - trailer)] -= p

    solution = np.linalg.solve(matrix, rhs)

    first_times = list(range(minimum, maximum + 1))
    first_probability = 1.0 / len(first_times)
    total = 0.0
    for first in first_times:
        for second in first_times:
            p = first_probability * first_probability
            total += p * min(first, second)
            if first == second:
                total += p * solution[both_caught]
            else:
                total += p * solution[ahead_index(abs(first - second))]

    return float(total)


def s(limit):
    return sum(expected_time(m, n) for m in range(2, limit + 1) for n in range(1, m))


def solve():
    assert f"{expected_time(60, 30):.2f}" == "1036.15"
    assert f"{s(5):.2f}" == "7722.82"
    return f"{s(100):.2f}"


if __name__ == "__main__":
    print(solve())
