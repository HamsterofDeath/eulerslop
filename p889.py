#!/usr/bin/env python3
"""Project Euler 889: a sparse-bit formula for the blancmange sum."""

from math import comb


MODULUS = 1_000_062_031


def blancmange_integer(k: int, t: int, exponent: int, modulus: int) -> int:
    """Return F(k,t,exponent) modulo modulus."""
    set_bit_positions: list[int] = []
    numerator = 0
    for block in range(exponent + 1):
        coefficient = comb(exponent, block)
        assert coefficient.bit_length() <= t
        numerator = (
            numerator
            + coefficient * pow(2, t * block, modulus)
        ) % modulus
        for bit in range(coefficient.bit_length()):
            if coefficient & (1 << bit):
                set_bit_positions.append(t * block + bit)

    set_bit_positions.sort()
    assert len(set_bit_positions) == len(set(set_bit_positions))
    bit_length = set_bit_positions[-1] + 1
    assert bit_length <= k

    # For q=2^k+1, the distances s(2^n p/q) repeat after k terms.
    # Put c=k-n and low_c=p mod 2^c.  After multiplying away q and
    # powers of two, each cut contributes
    #
    #   q*low_c-p                 if bit c-1 is zero,
    #   q*(2^c-low_c)+p           if bit c-1 is one.
    #
    # The least-significant one is the sole boundary exception and uses
    # the first line; this changes the final signed count by two.
    low = 0
    cut_sum = 0
    previous_set_bit = -1
    for position in set_bit_positions:
        zero_gap = position - previous_set_bit - 1
        cut_sum = (cut_sum + zero_gap * low) % modulus

        bit_value = pow(2, position, modulus)
        low = (low + bit_value) % modulus
        cut_sum = (cut_sum + 2 * bit_value - low) % modulus
        previous_set_bit = position

    # All cuts above the numerator's top bit have low_c=p.
    cut_sum = (
        cut_sum + (k - bit_length) * numerator
    ) % modulus

    quotient = (pow(2, k, modulus) + 1) % modulus
    signed_cut_count = 2 * len(set_bit_positions) - k - 2
    return (
        quotient * cut_sum
        + numerator * signed_cut_count
    ) % modulus


def solve() -> int:
    assert blancmange_integer(3, 1, 1, MODULUS) == 42
    assert blancmange_integer(13, 3, 3, MODULUS) == 23_093_880
    assert (
        blancmange_integer(103, 13, 6, MODULUS)
        == 878_922_518
    )
    return blancmange_integer(
        10**18 + 31,
        10**14 + 31,
        62,
        MODULUS,
    )


if __name__ == "__main__":
    print(solve())
