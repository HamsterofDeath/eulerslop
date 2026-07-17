#!/usr/bin/env python3
"""Project Euler 866: expected number-caterpillar product."""


PIECES = 100
MODULUS = 987_654_319


def expected_product(piece_count: int, modulus: int | None = None) -> int:
    """Return the expected product for a caterpillar of the given length."""
    # Let E_n be the expected product, with E_0 = 1.  Condition on the
    # position of the final piece.  If it leaves i pieces on the left, the
    # two sides are independent caterpillars whose placement orders can be
    # interleaved in binomial(n - 1, i) ways.  Dividing the resulting
    # weighted permutation count by n! cancels that binomial coefficient.
    # The final factor H_n = n(2n - 1) then gives
    #
    #     E_n = (2n - 1) * sum(E_i E_(n-1-i), 0 <= i < n).
    values = [1]
    for length in range(1, piece_count + 1):
        value = (2 * length - 1) * sum(
            values[left] * values[length - 1 - left]
            for left in range(length)
        )
        if modulus is not None:
            value %= modulus
        values.append(value)
    return values[piece_count]


def solve() -> int:
    assert expected_product(4) == 994
    return expected_product(PIECES, MODULUS)


if __name__ == "__main__":
    print(solve())
