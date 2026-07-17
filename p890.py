#!/usr/bin/env python3
"""Project Euler 890: binary sections of the partition generating function."""


MODULUS = 1_000_000_007
COEFFICIENT_BYTES = 9
COEFFICIENT_BASE = 1 << (8 * COEFFICIENT_BYTES)


def packed_convolution(left: list[int], right: list[int]) -> list[int]:
    """Convolve two short modular polynomials using one integer product.

    Nine bytes per coefficient leave enough space for the unreduced sum
    of at most 2183 products below MODULUS^2, so base digits cannot carry
    into one another.
    """
    maximum_raw_coefficient = (
        min(len(left), len(right)) * (MODULUS - 1) ** 2
    )
    assert maximum_raw_coefficient < COEFFICIENT_BASE

    packed_left = int.from_bytes(
        b"".join(
            coefficient.to_bytes(COEFFICIENT_BYTES, "little")
            for coefficient in left
        ),
        "little",
    )
    packed_right = int.from_bytes(
        b"".join(
            coefficient.to_bytes(COEFFICIENT_BYTES, "little")
            for coefficient in right
        ),
        "little",
    )

    coefficient_count = len(left) + len(right) - 1
    raw_product = (packed_left * packed_right).to_bytes(
        coefficient_count * COEFFICIENT_BYTES,
        "little",
    )
    return [
        int.from_bytes(
            raw_product[
                index * COEFFICIENT_BYTES:
                (index + 1) * COEFFICIENT_BYTES
            ],
            "little",
        )
        % MODULUS
        for index in range(coefficient_count)
    ]


def binary_partition_count(number: int) -> int:
    """Return p(number) modulo MODULUS.

    Let P(x)=product_j (1-x^(2^j))^-1, so

        P(x) = P(x^2)/(1-x).

    After processing low binary digits, a section of P has the form
    P(x)Q(x)/(1-x)^R.  Its even or odd section increments R and replaces
    Q by the matching parity coefficients of

        Q(x)(1+x)^(R+1).

    Once every digit is consumed, the requested coefficient is Q(0).
    """
    numerator = [1]
    binomial_row = [1, 1]  # Coefficients of (1+x)^(R+1), initially R=0.

    while number:
        parity = number & 1
        product = packed_convolution(numerator, binomial_row)
        numerator = product[parity::2]
        number >>= 1

        binomial_row = (
            [1]
            + [
                (binomial_row[index - 1] + binomial_row[index])
                % MODULUS
                for index in range(1, len(binomial_row))
            ]
            + [1]
        )

    return numerator[0]


def solve() -> int:
    assert binary_partition_count(7) == 6
    assert binary_partition_count(7**7) == 144_548_435
    return binary_partition_count(7**777)


if __name__ == "__main__":
    print(solve())
