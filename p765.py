#!/usr/bin/env python3
"""Project Euler 765: optimal finite-horizon betting."""

from decimal import Decimal, ROUND_HALF_UP, getcontext
from math import comb


ROUNDS = 1000
TARGET = Decimal("1e12")
WIN_PROBABILITY = Decimal("0.6")
LOSS_PROBABILITY = Decimal("0.4")


def optimal_probability(rounds: int, target: Decimal) -> Decimal:
    getcontext().prec = 90
    budget = Decimal(1) / target
    fair_path_probability = Decimal(1) / (Decimal(2) ** rounds)
    answer = Decimal(0)

    for wins in range(rounds, -1, -1):
        paths = Decimal(comb(rounds, wins))
        fair_price = paths * fair_path_probability
        real_probability = (
            paths
            * (WIN_PROBABILITY**wins)
            * (LOSS_PROBABILITY ** (rounds - wins))
        )
        if fair_price <= budget:
            answer += real_probability
            budget -= fair_price
        else:
            answer += real_probability * (budget / fair_price)
            break

    return answer


def solve() -> str:
    value = optimal_probability(ROUNDS, TARGET)
    return str(value.quantize(Decimal("0.0000000001"), rounding=ROUND_HALF_UP))


if __name__ == "__main__":
    print(solve())
