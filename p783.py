#!/usr/bin/env python3
"""Project Euler 783: urn expectation."""


def expected_square_sum(turns: int, batch: int) -> float:
    after_mean = 0.0
    after_second = 0.0
    draw = 2 * batch
    total = 0.0
    correction = 0.0

    for turn in range(1, turns + 1):
        population = batch * (turns - turn + 2)
        before_mean = after_mean + batch
        before_second = after_second + 2 * batch * after_mean + batch * batch

        variance_factor = draw * (population - draw) / (population - 1)
        linear = variance_factor / population
        quadratic = (draw / population) ** 2 - variance_factor / (population * population)
        contribution = linear * before_mean + quadratic * before_second

        y = contribution - correction
        subtotal = total + y
        correction = (subtotal - total) - y
        total = subtotal

        kept = population - draw
        if kept == 0:
            after_mean = 0.0
            after_second = 0.0
        else:
            keep_variance_factor = kept * (population - kept) / (population - 1)
            keep_linear = keep_variance_factor / population
            keep_quadratic = (kept / population) ** 2 - keep_variance_factor / (
                population * population
            )
            after_mean = kept / population * before_mean
            after_second = keep_linear * before_mean + keep_quadratic * before_second

    return total


def solve() -> int:
    assert abs(expected_square_sum(2, 2) - 9.6) < 1e-12
    return int(expected_square_sum(1_000_000, 10) + 0.5)


if __name__ == "__main__":
    print(solve())
