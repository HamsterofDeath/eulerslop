#!/usr/bin/env python3
"""Project Euler 671: coloured loop tilings."""

from collections import defaultdict


MOD = 1_000_004_321
K = 10
N = 10_004_003_002_001
OTHER = -1


def _category(top: int, bottom: int, special: int) -> tuple[int, int, int]:
    top_cat = top if top < special else OTHER
    bottom_cat = bottom if bottom < special else OTHER
    if top_cat == OTHER and bottom_cat == OTHER:
        return top_cat, bottom_cat, int(top == bottom)
    return top_cat, bottom_cat, 0


def _representative(category: tuple[int, int, int], special: int) -> tuple[int, int]:
    top_cat, bottom_cat, same_other = category
    if top_cat == OTHER and bottom_cat == OTHER:
        return (special, special) if same_other else (special, special + 1)
    top = special if top_cat == OTHER else top_cat
    bottom = special if bottom_cat == OTHER else bottom_cat
    return top, bottom


def _category_transitions(
    state: tuple[int, tuple[int, int, int], int, int],
    colours: int,
    special: int,
) -> dict[tuple[int, tuple[int, int, int], int, int], int]:
    top_rem, category, bottom_rem, previous_vertical_edge = state
    top_colour, bottom_colour = _representative(category, special)
    out = defaultdict(int)

    def row_options(remaining: int, old_colour: int) -> list[tuple[int, int, bool]]:
        if remaining:
            return [(remaining - 1, old_colour, False)]
        return [
            (length - 1, new_colour, True)
            for new_colour in range(colours)
            if new_colour != old_colour
            for length in (1, 2, 3)
        ]

    if top_rem == 0 and bottom_rem == 0:
        for colour in range(colours):
            if colour != top_colour and colour != bottom_colour:
                out[(0, _category(colour, colour, special), 0, 0)] += 1

    for next_top_rem, next_top_colour, top_starts in row_options(top_rem, top_colour):
        for next_bottom_rem, next_bottom_colour, bottom_starts in row_options(
            bottom_rem, bottom_colour
        ):
            if next_top_colour == next_bottom_colour:
                continue
            if top_starts and bottom_starts and previous_vertical_edge:
                continue
            next_category = _category(next_top_colour, next_bottom_colour, special)
            out[(next_top_rem, next_category, next_bottom_rem, 1)] += 1

    return out


def _build_matrix(colours: int, special: int, mod: int) -> tuple[list[tuple], list[list[int]]]:
    categories = {
        _category(top, bottom, special)
        for top in range(colours)
        for bottom in range(colours)
    }
    states = []
    for top_rem in range(3):
        for bottom_rem in range(3):
            for previous_vertical_edge in (0, 1):
                for category in categories:
                    top_colour, bottom_colour = _representative(category, special)
                    if previous_vertical_edge:
                        if top_colour == bottom_colour:
                            continue
                    elif not (
                        top_rem == 0 and bottom_rem == 0 and top_colour == bottom_colour
                    ):
                        continue
                    states.append((top_rem, category, bottom_rem, previous_vertical_edge))

    index = {state: i for i, state in enumerate(states)}
    matrix = [[0] * len(states) for _ in states]
    for state, i in index.items():
        for next_state, count in _category_transitions(state, colours, special).items():
            matrix[i][index[next_state]] = count % mod

    return states, matrix


def _mat_mul(left: list[list[int]], right: list[list[int]], mod: int) -> list[list[int]]:
    size = len(left)
    product = [[0] * size for _ in range(size)]
    for i, row in enumerate(left):
        product_row = product[i]
        for k, value in enumerate(row):
            if value == 0:
                continue
            right_row = right[k]
            for j, other in enumerate(right_row):
                if other:
                    product_row[j] = (product_row[j] + value * other) % mod
    return product


def _mat_pow(matrix: list[list[int]], exponent: int, mod: int) -> list[list[int]]:
    size = len(matrix)
    result = [[0] * size for _ in range(size)]
    for i in range(size):
        result[i][i] = 1

    while exponent:
        if exponent & 1:
            result = _mat_mul(result, matrix, mod)
        exponent >>= 1
        if exponent:
            matrix = _mat_mul(matrix, matrix, mod)

    return result


def _marked_loop_count(colours: int, length: int, mod: int) -> int:
    states_one, matrix_one = _build_matrix(colours, 1, mod)
    power_one = _mat_pow(matrix_one, length, mod)
    start_one = (0, _category(0, 0, 1), 0, 0)
    total = colours * power_one[states_one.index(start_one)][states_one.index(start_one)]

    states_two, matrix_two = _build_matrix(colours, 2, mod)
    power_two = _mat_pow(matrix_two, length, mod)
    two_index = {state: i for i, state in enumerate(states_two)}
    diagonal_sum = 0
    for top_rem in range(3):
        for bottom_rem in range(3):
            state = (top_rem, _category(0, 1, 2), bottom_rem, 1)
            i = two_index[state]
            diagonal_sum += power_two[i][i]

    total += colours * (colours - 1) * diagonal_sum
    return total % mod


def solve() -> int:
    # The requested circumference is prime, and one-column marked loops do not
    # exist. Burnside's lemma therefore reduces rotation classes to trace(T^N)/N.
    marked = _marked_loop_count(K, N, MOD)
    return marked * pow(N % MOD, -1, MOD) % MOD


if __name__ == "__main__":
    print(solve())
