#!/usr/bin/env python3
"""Project Euler 794: compatible interval partitions."""

from decimal import Decimal, ROUND_HALF_UP, getcontext
from math import gcd


def common_denominator(limit: int) -> int:
    value = 1
    for n in range(1, limit + 1):
        value = value * n // gcd(value, n)
    return value


def extend_state(
    state: tuple[tuple[int, int], ...], bins: list[tuple[int, int]]
) -> list[tuple[tuple[int, int], ...]]:
    options = []
    for index, (left, right) in enumerate(state):
        choices = []
        for bin_index, (bin_left, bin_right) in enumerate(bins):
            new_left = max(left, bin_left)
            new_right = min(right, bin_right)
            if new_left < new_right:
                choices.append((bin_index, new_left, new_right))
        options.append((len(choices), index, choices))

    order = sorted(options)
    updated: list[tuple[int, int] | None] = [None] * len(state)
    out = []

    def search(position: int, used: int) -> None:
        if position == len(order):
            for bin_index, interval in enumerate(bins):
                if not (used >> bin_index) & 1:
                    complete = [entry for entry in updated if entry is not None]
                    out.append(tuple(complete + [interval]))
            return

        _, point_index, choices = order[position]
        for bin_index, new_left, new_right in choices:
            if not (used >> bin_index) & 1:
                updated[point_index] = (new_left, new_right)
                search(position + 1, used | (1 << bin_index))
                updated[point_index] = None

    search(0, 0)
    return out


def minimal_sum_units(limit: int) -> tuple[int, int]:
    denominator = common_denominator(limit)
    states = {((0, denominator),)}
    for size in range(2, limit + 1):
        bins = [
            (index * denominator // size, (index + 1) * denominator // size)
            for index in range(size)
        ]
        next_states = set()
        for state in states:
            next_states.update(extend_state(state, bins))
        states = next_states

    return min(sum(left for left, _ in state) for state in states), denominator


def rounded_minimum(limit: int) -> str:
    numerator, denominator = minimal_sum_units(limit)
    getcontext().prec = 40
    value = Decimal(numerator) / Decimal(denominator)
    return str(value.quantize(Decimal("0.000000000001"), rounding=ROUND_HALF_UP))


def solve() -> str:
    assert rounded_minimum(4) == "1.500000000000"
    return rounded_minimum(17)


if __name__ == "__main__":
    print(solve())
