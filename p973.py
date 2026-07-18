#!/usr/bin/env python3
"""Project Euler Problem 973: Random Dealings.

The expected occupation weight of a pile partition is the number of
distinct orderings of its parts.  Hence X(n) is the sum of the XOR of
the parts over all ordered compositions of n, except for the initial
all-ones composition.

For bit b, let D_b(n) be the signed sum over compositions, with a part
negative exactly when that bit is set.  The number of compositions with
odd bit parity is (2**(n-1)-D_b(n))/2.  Part signs have period 2**(b+1);
the composition recurrence is evaluated in O(n) with residue-prefix and
sliding-window sums.
"""

MODULUS = 1_000_000_007
LIMIT = 10_000
INVERSE_TWO = (MODULUS + 1) // 2


def range_sum(prefix: list[int], first: int, last: int) -> int:
    if first > last:
        return 0
    result = prefix[last]
    if first:
        result -= prefix[first - 1]
    return result % MODULUS


def signed_composition_sum(total: int, bit: int) -> int:
    half_period = 1 << bit
    period = 2 * half_period

    compositions = [0] * (total + 1)
    residue_prefix = [0] * (total + 1)
    prefix = [0] * (total + 1)
    compositions[0] = 1
    residue_prefix[0] = 1
    prefix[0] = 1

    for value in range(1, total + 1):
        # All residues initially have sign +1.
        first = max(0, value - period)
        signed_sum = range_sum(prefix, first, value - 1)

        # Residues half_period,...,period-1 have sign -1.
        if value >= half_period:
            negative_first = max(0, value - period + 1)
            negative_last = value - half_period
            signed_sum -= 2 * range_sum(
                prefix, negative_first, negative_last
            )
        compositions[value] = signed_sum % MODULUS

        residue_prefix[value] = compositions[value]
        if value >= period:
            residue_prefix[value] += residue_prefix[value - period]
        residue_prefix[value] %= MODULUS
        prefix[value] = (
            prefix[value - 1] + residue_prefix[value]
        ) % MODULUS

    return compositions[total]


def expected_score(total: int) -> int:
    composition_count = pow(2, total - 1, MODULUS)
    result = 0
    bit = 0
    while 1 << bit <= total:
        signed_sum = signed_composition_sum(total, bit)
        odd_count = (
            (composition_count - signed_sum) * INVERSE_TWO
            % MODULUS
        )
        result += (1 << bit) * odd_count
        bit += 1

    # The starting all-singleton composition is not scored.
    return (result - total % 2) % MODULUS


def solve() -> int:
    assert expected_score(2) == 2
    assert expected_score(4) == 14
    assert expected_score(10) == 1418
    return expected_score(LIMIT)


if __name__ == "__main__":
    print(solve())
