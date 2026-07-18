#!/usr/bin/env python3
"""Project Euler 911: Khinchin means of scaled Kempner numbers."""

import math


def truncation_continued_fraction(
    scale_exponent: int,
    final_series_index: int,
) -> list[int]:
    """Exact CF of 2^n sum_{i=0}^m 2^(-2^i)."""
    denominator_exponent = 1 << final_series_index
    numerator = sum(
        1 << (denominator_exponent - (1 << index))
        for index in range(final_series_index + 1)
    )

    # The unscaled numerator is odd, so multiplication by 2^n cancels
    # exactly n powers from the denominator.
    denominator = 1 << (
        denominator_exponent - scale_exponent
    )

    coefficients = []
    while denominator:
        quotient, remainder = divmod(numerator, denominator)
        coefficients.append(quotient)
        numerator, denominator = denominator, remainder
    return coefficients


def stable_prefix_statistics(
    first: list[int],
    second: list[int],
) -> tuple[float, int]:
    """Return log-product and length of their stable noninteger prefix."""
    common_length = 0
    while (
        common_length < min(len(first), len(second))
        and first[common_length] == second[common_length]
    ):
        common_length += 1

    return (
        sum(
            math.log(coefficient)
            for coefficient in first[1:common_length]
        ),
        common_length - 1,
    )


def log_limiting_mean(
    scale_exponent: int,
    base_level: int = 12,
) -> float:
    """Return log(k_infinity(rho_n)).

    The continued-fraction folding lemma makes each sufficiently late
    truncation preserve the preceding word and append a reflected block.
    For this series, successive appended stable blocks have the same
    multiset product.  Their log-product divided by their length is
    therefore the limiting logarithmic mean.
    """
    first = truncation_continued_fraction(
        scale_exponent,
        base_level,
    )
    second = truncation_continued_fraction(
        scale_exponent,
        base_level + 1,
    )
    third = truncation_continued_fraction(
        scale_exponent,
        base_level + 2,
    )

    first_log, first_length = stable_prefix_statistics(
        first,
        second,
    )
    second_log, second_length = stable_prefix_statistics(
        second,
        third,
    )
    return (
        (second_log - first_log)
        / (second_length - first_length)
    )


def exceptional_geometric_mean() -> float:
    logs = [
        log_limiting_mean(scale_exponent)
        for scale_exponent in range(51)
    ]
    return math.exp(sum(logs) / len(logs))


def solve() -> str:
    assert abs(
        math.exp(log_limiting_mean(2)) - 2.059767143907
    ) < 1e-12

    answer = exceptional_geometric_mean()
    independent_level_answer = math.exp(
        sum(
            log_limiting_mean(scale_exponent, 10)
            for scale_exponent in range(51)
        )
        / 51
    )
    assert abs(answer - independent_level_answer) < 1e-9
    return f"{answer:.6f}"


if __name__ == "__main__":
    print(solve())
