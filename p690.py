#!/usr/bin/env python3
"""Project Euler 690: Tom and Jerry."""


MOD = 1_000_000_007
N = 2019
INV2 = (MOD + 1) // 2


def _add(a, b):
    return [(x + y) % MOD for x, y in zip(a, b)]


def _sub(a, b):
    return [(x - y) % MOD for x, y in zip(a, b)]


def _mul(a, b):
    result = [0] * (N + 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b[: N + 1 - i]):
            if y:
                result[i + j] = (result[i + j] + x * y) % MOD
    return result


def _inverse_series(poly):
    result = [0] * (N + 1)
    result[0] = pow(poly[0], MOD - 2, MOD)
    for n in range(1, N + 1):
        total = 0
        for i in range(1, n + 1):
            total = (total + poly[i] * result[n - i]) % MOD
        result[n] = -total * result[0] % MOD
    return result


def _compose_x_squared(poly):
    result = [0] * (N + 1)
    for i, value in enumerate(poly):
        if 2 * i <= N:
            result[2 * i] = value
    return result


def _lobster_tree_counts():
    partitions = [0] * (N + 1)
    partitions[0] = 1
    for part in range(1, N + 1):
        for total in range(part, N + 1):
            partitions[total] = (partitions[total] + partitions[total - part]) % MOD

    # A is the decoration of a spine vertex by arbitrary depth-at-most-2 branches.
    any_decoration = [0] * (N + 1)
    for n in range(1, N + 1):
        any_decoration[n] = partitions[n - 1]

    passive_only = [0] * (N + 1)
    for n in range(1, N + 1):
        passive_only[n] = 1

    exactly_one_active = [0] * (N + 1)
    for n in range(3, N + 1):
        exactly_one_active[n] = n - 2

    endpoint_decoration = _sub(any_decoration, passive_only)
    singleton_core = _sub(endpoint_decoration, exactly_one_active)

    empty_core = [0] * (N + 1)
    empty_core[1] = 1
    for n in range(2, N + 1):
        empty_core[n] = n // 2

    denominator = [0] * (N + 1)
    denominator[0] = 1
    for i in range(1, N + 1):
        denominator[i] = -any_decoration[i] % MOD

    oriented_paths = _mul(
        _mul(endpoint_decoration, endpoint_decoration),
        _inverse_series(denominator),
    )

    squared_any = _compose_x_squared(any_decoration)
    squared_endpoint = _compose_x_squared(endpoint_decoration)
    one_plus_any = any_decoration[:]
    one_plus_any[0] = 1

    squared_denominator = [0] * (N + 1)
    squared_denominator[0] = 1
    for i in range(1, N + 1):
        squared_denominator[i] = -squared_any[i] % MOD

    symmetric_paths = _mul(
        _mul(squared_endpoint, one_plus_any),
        _inverse_series(squared_denominator),
    )

    counts = [0] * (N + 1)
    for i in range(N + 1):
        path_count = (oriented_paths[i] + symmetric_paths[i]) * INV2
        counts[i] = (empty_core[i] + singleton_core[i] + path_count) % MOD
    return counts


def solve():
    lobster_counts = _lobster_tree_counts()
    inverses = [0] * (N + 2)
    for n in range(1, N + 2):
        inverses[n] = pow(n, MOD - 2, MOD)

    forests = [0] * (N + 1)
    forests[0] = 1
    for size in range(1, N + 1):
        max_multiplicity = N // size
        choices = [1] * (max_multiplicity + 1)
        for multiplicity in range(1, max_multiplicity + 1):
            choices[multiplicity] = (
                choices[multiplicity - 1]
                * (lobster_counts[size] + multiplicity - 1)
                * inverses[multiplicity]
            ) % MOD

        next_forests = forests[:]
        for base_size, ways in enumerate(forests):
            if ways == 0:
                continue
            for multiplicity in range(1, max_multiplicity + 1):
                total_size = base_size + multiplicity * size
                if total_size > N:
                    break
                next_forests[total_size] = (
                    next_forests[total_size] + ways * choices[multiplicity]
                ) % MOD
        forests = next_forests

    return forests[N]


if __name__ == "__main__":
    print(solve())
