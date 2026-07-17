#!/usr/bin/env python3
"""Project Euler 852: optimal sequential testing of coins.

The continuation score after a coin is revealed depends on its true type, not
on the guess, so it separates from the current round's testing decision.  For
each possible prior probability of an unfair coin, solve the resulting
infinite-horizon Bayesian stopping problem by backward induction, then combine
those one-coin values over the random depletion of the box.
"""

from math import gcd


MAX_TOSSES = 180


def stop_value(unfair_probability: float) -> float:
    if unfair_probability >= 0.5:
        return 70.0 * unfair_probability - 50.0
    return 20.0 - 70.0 * unfair_probability


def coin_value(
    unfair: int,
    total: int,
    powers_of_three: list[float],
    inverse_powers_of_two: list[float],
    max_tosses: int,
) -> float:
    """Optimal expected round score for prior P(unfair)=unfair/total."""
    if unfair == 0 or unfair == total:
        return 20.0

    initial_odds = unfair / (total - unfair)
    next_row = [0.0] * (max_tosses + 2)
    current_row = [0.0] * (max_tosses + 2)

    base_odds = initial_odds * inverse_powers_of_two[max_tosses]
    for heads in range(max_tosses + 1):
        odds = base_odds * powers_of_three[heads]
        posterior = odds / (1.0 + odds)
        next_row[heads] = stop_value(posterior)

    for tosses in range(max_tosses - 1, -1, -1):
        base_odds = initial_odds * inverse_powers_of_two[tosses]
        for heads in range(tosses + 1):
            odds = base_odds * powers_of_three[heads]
            posterior = odds / (1.0 + odds)
            head_probability = 0.5 + 0.25 * posterior
            continue_value = (
                -1.0
                + head_probability * next_row[heads + 1]
                + (1.0 - head_probability) * next_row[heads]
            )
            current_row[heads] = max(
                stop_value(posterior), continue_value
            )
        next_row, current_row = current_row, next_row

    return next_row[0]


def expected_score(coins_of_each_type: int, max_tosses: int = MAX_TOSSES) -> float:
    powers_of_three = [1.0] * (max_tosses + 1)
    inverse_powers_of_two = [1.0] * (max_tosses + 1)
    for index in range(1, max_tosses + 1):
        powers_of_three[index] = 3.0 * powers_of_three[index - 1]
        inverse_powers_of_two[index] = 0.5 * inverse_powers_of_two[index - 1]

    priors = set()
    for unfair in range(coins_of_each_type + 1):
        for fair in range(coins_of_each_type + 1):
            total = unfair + fair
            if total:
                divisor = gcd(unfair, total)
                priors.add((unfair // divisor, total // divisor))

    round_value = {
        prior: coin_value(
            *prior,
            powers_of_three,
            inverse_powers_of_two,
            max_tosses,
        )
        for prior in priors
    }

    value = [
        [0.0] * (coins_of_each_type + 1)
        for _ in range(coins_of_each_type + 1)
    ]
    for total in range(1, 2 * coins_of_each_type + 1):
        lower = max(0, total - coins_of_each_type)
        upper = min(coins_of_each_type, total)
        for unfair in range(lower, upper + 1):
            fair = total - unfair
            divisor = gcd(unfair, total)
            immediate = round_value[(unfair // divisor, total // divisor)]
            continuation = 0.0
            if unfair:
                continuation += unfair / total * value[unfair - 1][fair]
            if fair:
                continuation += fair / total * value[unfair][fair - 1]
            value[unfair][fair] = immediate + continuation

    return value[coins_of_each_type][coins_of_each_type]


def solve() -> str:
    assert f"{expected_score(1):.6f}" == "20.558591"
    return f"{expected_score(50):.6f}"


if __name__ == "__main__":
    print(solve())
