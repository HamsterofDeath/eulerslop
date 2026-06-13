#!/usr/bin/env python3
"""Project Euler 669: Fibonacci-sum banquet seating."""

from functools import cache


TARGET_N_INDEX = 83
TARGET_POSITION = 10_000_000_000_000_000

BASE_INDEX = 5
BASE_PATH = (4, 1, 2, 3, 5)
BASE_EDGE_SYMBOLS = (1, 0, 1, 2)
MORPH = ((1, 2, 1), (0,), (1,))


def _fibonacci(limit: int) -> list[int]:
    fib = [0, 1, 1]
    for _ in range(3, limit + 1):
        fib.append(fib[-1] + fib[-2])
    return fib


FIB = _fibonacci(TARGET_N_INDEX + 1)
START = [0] * (TARGET_N_INDEX + 1)
HAS_PREFIX = [False] * (TARGET_N_INDEX + 1)
SYMBOL_COUNTS = [(0, 0, 0)] * (TARGET_N_INDEX + 1)

START[BASE_INDEX] = BASE_PATH[0]
SYMBOL_COUNTS[BASE_INDEX] = (1, 2, 1)
for m in range(BASE_INDEX + 1, TARGET_N_INDEX + 1):
    HAS_PREFIX[m] = 2 * START[m - 1] == FIB[m - 2]
    START[m] = FIB[m] - START[m - 1] if HAS_PREFIX[m] else START[m - 1]

    a_count, b_count, c_count = SYMBOL_COUNTS[m - 1]
    SYMBOL_COUNTS[m] = (
        b_count,
        2 * a_count + c_count + int(HAS_PREFIX[m]),
        a_count + 1,
    )


def _weighted_length(m: int, weights: tuple[int, int, int]) -> int:
    counts = SYMBOL_COUNTS[m]
    return counts[0] * weights[0] + counts[1] * weights[1] + counts[2] * weights[2]


def _locate_weighted(
    m: int,
    weights: tuple[int, int, int],
    position: int,
) -> tuple[int, int, int, tuple[int, int, int]]:
    """Locate a weighted position in the relative edge-label word for P_m.

    Edge labels in P_m only use Fibonacci indices m-1, m and m+1.  We encode
    them as symbols A=0, B=1, C=2.  From one Fibonacci order to the next the
    edge word is built by the morphism A->BCB, B->A, C->B, plus a small
    endpoint prefix every third order and a trailing C.
    """

    if m == BASE_INDEX:
        before = [0, 0, 0]
        for symbol in BASE_EDGE_SYMBOLS:
            width = weights[symbol]
            if position <= width:
                return sum(before) + 1, symbol, position, tuple(before)
            position -= width
            before[symbol] += 1
        raise ValueError("position outside base edge word")

    before = [0, 0, 0]
    if HAS_PREFIX[m]:
        width = weights[1]
        if position <= width:
            return 1, 1, position, (0, 0, 0)
        position -= width
        before[1] = 1

    old_weights = (2 * weights[1] + weights[2], weights[0], weights[1])
    middle_length = _weighted_length(m - 1, old_weights)
    if position <= middle_length:
        _, old_symbol, block_position, old_before = _locate_weighted(
            m - 1,
            old_weights,
            position,
        )
        before[0] += old_before[1]
        before[1] += 2 * old_before[0] + old_before[2]
        before[2] += old_before[0]

        for symbol in MORPH[old_symbol]:
            width = weights[symbol]
            if block_position <= width:
                return sum(before) + 1, symbol, block_position, tuple(before)
            block_position -= width
            before[symbol] += 1
        raise ValueError("position outside morphism block")

    position -= middle_length
    old_a, old_b, old_c = SYMBOL_COUNTS[m - 1]
    before[0] += old_b
    before[1] += 2 * old_a + old_c
    before[2] += old_a
    if position <= weights[2]:
        return sum(before) + 1, 2, position, tuple(before)
    raise ValueError("position outside edge word")


@cache
def _seat(m: int, position: int) -> int:
    if m == BASE_INDEX:
        return BASE_PATH[position - 1]

    has_prefix = HAS_PREFIX[m]
    if has_prefix:
        if position == 1:
            return FIB[m] - _seat(m - 1, 1)
        position -= 1

    if position == 1:
        return _seat(m - 1, 1)
    position -= 1

    body_length = FIB[m] - int(has_prefix) - 2
    if position > body_length:
        return FIB[m]

    edge_index, symbol, offset, _ = _locate_weighted(m - 1, (3, 1, 1), position)
    if symbol == 0:
        if offset == 1:
            return FIB[m] - _seat(m - 1, edge_index)
        if offset == 2:
            return FIB[m] - _seat(m - 1, edge_index + 1)
        return _seat(m - 1, edge_index + 1)
    return _seat(m - 1, edge_index + 1)


def solve() -> int:
    return _seat(TARGET_N_INDEX, TARGET_POSITION)


if __name__ == "__main__":
    print(solve())
