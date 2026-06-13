#!/usr/bin/env python3
"""Project Euler 677: coloured degree-limited trees."""


LIMIT = 10_000
MOD = 1_000_000_007
INV2 = pow(2, MOD - 2, MOD)
INV6 = pow(6, MOD - 2, MOD)
INV24 = pow(24, MOD - 2, MOD)


def _constant(degree: int) -> int:
    return 1 if degree == 0 else 0


def _mset3_exact(series: list[int], square: list[int], degree: int) -> int:
    tripled = series[degree // 3] if degree % 3 == 0 else 0

    one_and_double = 0
    for doubled in range(1, degree // 2 + 1):
        single = degree - 2 * doubled
        if single >= 1:
            one_and_double = (one_and_double + series[single] * series[doubled]) % MOD

    cubed = 0
    for first in range(1, degree):
        cubed = (cubed + series[first] * square[degree - first]) % MOD

    return (cubed + 3 * one_and_double + 2 * tripled) * INV6 % MOD


def _mset_le2(series: list[int], square: list[int], degree: int) -> int:
    doubled = series[degree // 2] if degree % 2 == 0 else 0
    return (_constant(degree) + series[degree] + (square[degree] + doubled) * INV2) % MOD


def _mset_le3(series: list[int], square: list[int], degree: int) -> int:
    doubled = series[degree // 2] if degree % 2 == 0 else 0
    return (
        _constant(degree)
        + series[degree]
        + (square[degree] + doubled) * INV2
        + _mset3_exact(series, square, degree)
    ) % MOD


def _mset4_exact(series: list[int], square: list[int], degree: int) -> int:
    fourth = 0
    for first_pair in range(degree + 1):
        fourth = (fourth + square[first_pair] * square[degree - first_pair]) % MOD

    two_singles_and_double = 0
    for doubled in range(1, degree // 2 + 1):
        two_singles_and_double = (
            two_singles_and_double + series[doubled] * square[degree - 2 * doubled]
        ) % MOD

    two_doubles = square[degree // 2] if degree % 2 == 0 else 0

    single_and_triple = 0
    for tripled in range(1, degree // 3 + 1):
        single = degree - 3 * tripled
        if single >= 1:
            single_and_triple = (
                single_and_triple + series[single] * series[tripled]
            ) % MOD

    quadrupled = series[degree // 4] if degree % 4 == 0 else 0
    return (
        fourth
        + 6 * two_singles_and_double
        + 3 * two_doubles
        + 8 * single_and_triple
        + 6 * quadrupled
    ) * INV24 % MOD


def _mset_le4(series: list[int], square: list[int], degree: int) -> int:
    doubled = series[degree // 2] if degree % 2 == 0 else 0
    return (
        _constant(degree)
        + series[degree]
        + (square[degree] + doubled) * INV2
        + _mset3_exact(series, square, degree)
        + _mset4_exact(series, square, degree)
    ) % MOD


def g(size: int) -> int:
    red = [0] * (size + 1)
    blue = [0] * (size + 1)
    yellow = [0] * (size + 1)
    any_colour = [0] * (size + 1)
    not_yellow = [0] * (size + 1)
    any_square = [0] * (size + 1)
    not_yellow_square = [0] * (size + 1)

    for n in range(1, size + 1):
        degree = n - 1
        red[n] = _mset_le3(any_colour, any_square, degree)
        blue[n] = _mset_le2(any_colour, any_square, degree)
        yellow[n] = _mset_le2(not_yellow, not_yellow_square, degree)

        any_colour[n] = (red[n] + blue[n] + yellow[n]) % MOD
        not_yellow[n] = (red[n] + blue[n]) % MOD

        any_twice = 2 * any_colour[n]
        not_yellow_twice = 2 * not_yellow[n]
        max_partner = min(n - 1, size - n)
        for partner in range(1, max_partner + 1):
            target = n + partner
            any_square[target] = (
                any_square[target] + any_twice * any_colour[partner]
            ) % MOD
            not_yellow_square[target] = (
                not_yellow_square[target]
                + not_yellow_twice * not_yellow[partner]
            ) % MOD

        target = 2 * n
        if target <= size:
            any_square[target] = (any_square[target] + any_colour[n] ** 2) % MOD
            not_yellow_square[target] = (
                not_yellow_square[target] + not_yellow[n] ** 2
            ) % MOD

    degree = size - 1
    vertex_rooted = (
        _mset_le4(any_colour, any_square, degree)
        + _mset_le3(any_colour, any_square, degree)
        + _mset_le3(not_yellow, not_yellow_square, degree)
    ) % MOD

    yellow_yellow_edges = 0
    for left_size in range(1, size):
        yellow_yellow_edges = (
            yellow_yellow_edges + yellow[left_size] * yellow[size - left_size]
        ) % MOD

    directed_edges = (any_square[size] - yellow_yellow_edges) % MOD
    symmetric_edges = (red[size // 2] + blue[size // 2]) % MOD if size % 2 == 0 else 0
    return (vertex_rooted - (directed_edges - symmetric_edges) * INV2) % MOD


def solve() -> int:
    return g(LIMIT)


if __name__ == "__main__":
    print(solve())
