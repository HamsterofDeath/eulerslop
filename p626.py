#!/usr/bin/env python3
from collections import Counter
from math import factorial, gcd


MOD = 1_001_001_011
N = 20


def partitions(n, minimum=1):
    if n == 0:
        yield ()
        return

    for first in range(minimum, n + 1):
        for rest in partitions(n - first, first):
            yield (first, *rest)


def centralizer_size(cycle_type):
    counts = Counter(cycle_type)
    result = 1
    for length, amount in counts.items():
        result *= length**amount * factorial(amount)
    return result


def gf2_rank(rows):
    basis = {}
    rank = 0
    for row in rows:
        value = row
        while value:
            bit = value.bit_length() - 1
            if bit in basis:
                value ^= basis[bit]
            else:
                basis[bit] = value
                rank += 1
                break
    return rank


def flip_average_exponent(row_cycles, column_cycles):
    row_count = len(row_cycles)
    column_count = len(column_cycles)
    cell_orbits = 0
    equations = []

    for i, row_length in enumerate(row_cycles):
        for j, column_length in enumerate(column_cycles):
            common = gcd(row_length, column_length)
            cell_orbits += common

            mask = 0
            if (column_length // common) & 1:
                mask ^= 1 << i
            if (row_length // common) & 1:
                mask ^= 1 << (row_count + j)
            if mask:
                equations.append(mask)

    nullity = row_count + column_count - gf2_rank(equations)
    return cell_orbits - row_count - column_count + nullity


def solve(n=N):
    cycle_types = []
    for part in partitions(n):
        inverse_z = pow(centralizer_size(part), MOD - 2, MOD)
        cycle_types.append((part, inverse_z))

    total = 0
    for row_cycles, row_weight in cycle_types:
        for column_cycles, column_weight in cycle_types:
            exponent = flip_average_exponent(row_cycles, column_cycles)
            total += row_weight * column_weight * pow(2, exponent, MOD)
            total %= MOD
    return total


if __name__ == "__main__":
    print(solve())
