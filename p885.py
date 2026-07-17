#!/usr/bin/env python3
"""Project Euler 885: sum numbers formed by sorting decimal digits."""

from math import comb


MODULUS = 1_123_455_689


def digit_sort_sum(digits: int, modulus: int | None = None) -> int:
    """Return S(digits), optionally reduced modulo modulus.

    Pad every integer below 10^digits with leading zeros.  For a fixed
    nonzero digit j, let c be its multiplicity and h the number of
    larger digits.  Its block in the sorted result contributes

        j * 10^h * (10^c-1)/9.

    The remaining positions independently contain one of the j digits
    0,...,j-1, while each of the h positions contains one of 9-j larger
    digits.
    """
    result = 0
    for digit in range(1, 10):
        for multiplicity in range(1, digits + 1):
            digit_block = digit * (10**multiplicity - 1) // 9
            for larger_count in range(digits - multiplicity + 1):
                smaller_count = digits - multiplicity - larger_count
                arrangements = (
                    comb(digits, multiplicity)
                    * comb(digits - multiplicity, larger_count)
                    * (9 - digit) ** larger_count
                    * digit**smaller_count
                )
                result += (
                    arrangements
                    * digit_block
                    * 10**larger_count
                )
                if modulus is not None:
                    result %= modulus
    return result


def solve() -> int:
    assert digit_sort_sum(1) == 45
    assert digit_sort_sum(5) == 1_543_545_675
    return digit_sort_sum(18, MODULUS)


if __name__ == "__main__":
    print(solve())
