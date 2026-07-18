#!/usr/bin/env python3
"""Project Euler 902: sum of ranks of conjugated cycle powers."""

from math import factorial, gcd

MODULUS = 1_000_000_007


def rank_sum(m: int) -> int:
    """Return P(m) modulo 1,000,000,007.

    The permutation sigma is the disjoint union of one cycle of every
    length 1 through m.  In the Lehmer-code formula

        rank(q) = 1 + sum_{i<j} [q(j)<q(i)] (n-i)!,

    a pair whose elements lie in cycles of lengths a and b repeats every
    lcm(a,b) powers.  During one period, its two rotated offsets (u,v)
    visit exactly the pairs satisfying

        u-v = initial_u-initial_v (mod gcd(a,b)).

    Comparison counts for every pair of cycles and every such residue
    can therefore be precomputed in O(n^2) total time.
    """
    if m == 1:
        return 1

    n = m * (m + 1) // 2
    inverse_multiplier = pow(MODULUS, -1, n)

    # tau^{-1}(value), with residue zero represented by index n.
    inverse_tau = [0] * (n + 1)
    for value in range(1, n + 1):
        index = inverse_multiplier * (value - 1) % n
        inverse_tau[value] = index or n

    cycle_length = [0] * (n + 1)
    cycle_offset = [0] * (n + 1)
    cycle_start = [0] * (m + 1)
    for length in range(1, m + 1):
        start = length * (length - 1) // 2 + 1
        cycle_start[length] = start
        for offset in range(length):
            cycle_length[start + offset] = length
            cycle_offset[start + offset] = offset

    gcd_table = [[0] * (m + 1) for _ in range(m + 1)]
    comparison_counts = [[None] * (m + 1) for _ in range(m + 1)]

    for a in range(1, m + 1):
        positions_a = [
            inverse_tau[cycle_start[a] + offset]
            for offset in range(a)
        ]
        for b in range(1, m + 1):
            positions_b = [
                inverse_tau[cycle_start[b] + offset]
                for offset in range(b)
            ]
            common_divisor = gcd(a, b)
            gcd_table[a][b] = common_divisor
            counts = [0] * common_divisor

            for offset_a, position_a in enumerate(positions_a):
                for offset_b, position_b in enumerate(positions_b):
                    if position_b < position_a:
                        counts[
                            (offset_a - offset_b) % common_divisor
                        ] += 1

            comparison_counts[a][b] = counts

    element_info = []
    for index in range(1, n + 1):
        value = MODULUS * index % n + 1
        element_info.append(
            (cycle_length[value], cycle_offset[value])
        )

    power_count = factorial(m) % MODULUS
    period_factors = [[0] * (m + 1) for _ in range(m + 1)]
    for a in range(1, m + 1):
        for b in range(1, m + 1):
            period = a // gcd_table[a][b] * b
            period_factors[a][b] = (
                power_count * pow(period, MODULUS - 2, MODULUS)
            ) % MODULUS

    factorials = [1] * (n + 1)
    for value in range(1, n + 1):
        factorials[value] = factorials[value - 1] * value % MODULUS

    answer = power_count
    for first_index in range(n - 1):
        a, offset_a = element_info[first_index]
        count_rows = comparison_counts[a]
        gcd_row = gcd_table[a]
        factor_row = period_factors[a]
        inversion_count = 0

        for second_index in range(first_index + 1, n):
            b, offset_b = element_info[second_index]
            inversion_count += (
                factor_row[b]
                * count_rows[b][
                    (offset_a - offset_b) % gcd_row[b]
                ]
            )

        answer += (
            factorials[n - first_index - 1]
            * (inversion_count % MODULUS)
        )
        answer %= MODULUS

    return answer


def solve() -> int:
    assert rank_sum(2) == 4
    assert rank_sum(3) == 780
    assert rank_sum(4) == 38_810_300
    return rank_sum(100)


if __name__ == "__main__":
    print(solve())
