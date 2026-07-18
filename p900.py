#!/usr/bin/env python3
"""Project Euler 900: losing thresholds for the many-pile game."""

MODULUS = 900_497_239


def losing_offset(n: int) -> int:
    """Return t(n).

    For a position with r piles, total T, and minimum m, every next
    minimum from 1 through min(m, floor((T-m)/r)) is attainable.
    If ell(T) is the smallest losing minimum for total T, induction gives

        ell(T) = lowbit(T + [r is even])

    whenever that low bit is at most floor(T/r), and no losing minimum
    otherwise.

    Here r=n+1.  Applying the criterion to the total after the first move
    shows that n^2+k+(n mod 2) must first become divisible by a power of
    two greater than n.
    """
    power = 1 << n.bit_length()
    return (-n * n - (n & 1)) % power


def block_sum(bit_length: int, modulus: int) -> int:
    """Sum t(n) for 2^(b-1) <= n < 2^b, modulo modulus."""
    if bit_length == 1:
        return 0
    if bit_length == 2:
        return 2 % modulus

    b = bit_length
    return (
        pow(2, 2 * b - 2, modulus)
        + pow(2, b + (b - 3) // 2, modulus)
        - pow(2, b, modulus)
    ) % modulus


def sum_offsets(exponent: int, modulus: int = MODULUS) -> int:
    """Return S(exponent) modulo modulus."""
    # The endpoint n=2^exponent has t(n)=0.
    return sum(
        block_sum(bit_length, modulus)
        for bit_length in range(1, exponent + 1)
    ) % modulus


def solve() -> int:
    assert [losing_offset(n) for n in range(1, 8)] == [
        0, 0, 2, 0, 6, 4, 6
    ]
    assert sum_offsets(10, 10**20) == 361_522
    return sum_offsets(10_000)


if __name__ == "__main__":
    print(solve())
