#!/usr/bin/env python3
"""Project Euler Problem 999: Alternating Recurrence.

The recurrence has an alternating coefficient, so rescale it to the
constant-coefficient elliptic divisibility sequence

    W_n = sign(n) * 2^floor(n^2 / 4) * a_n,

where sign(n) = +1 for n = 1, 2 (mod 4) and -1 for n = 0, 3 (mod 4).
Substitution gives

    W_{n+2} * W_{n-2} = 4 * W_{n+1} * W_{n-1} + 4 * W_n^2,

with seeds W_0 = 0, W_1 = 1, W_2 = 2, W_3 = -4, W_4 = -32 (and the
usual antisymmetry W_{-n} = -W_n).

Elliptic divisibility sequences support doubling:

    W_{2m-1} = W_{m+1} * W_{m-1}^3 - W_{m-2} * W_m^3
    W_{2m}   = (W_m / W_2) * (W_{m+2} * W_{m-1}^2 - W_{m-2} * W_{m+1}^2)
    W_{2m+1} = W_{m+2} * W_m^3 - W_{m-1} * W_{m+1}^3

Each step halves the index, so W_n is computed in O(log n) modular
arithmetic.  The answer is recovered as

    a_n = sign(n) * W_n * 2^(-floor(n^2 / 4)).
"""

MODULUS = 1_234_567_891
INV_TWO = pow(2, -1, MODULUS)

BASE_BLOCKS = {
    1: [-2, -1, 0, 1, 2, -4, -32, -192],
    2: [-1, 0, 1, 2, -4, -32, -192, 3584],
    3: [0, 1, 2, -4, -32, -192, 3584, 77824],
    4: [1, 2, -4, -32, -192, 3584, 77824, 262144],
}


def block_around(n: int) -> list[int]:
    """Return [W_{n-3}, ..., W_{n+4}] modulo MODULUS."""
    if n in BASE_BLOCKS:
        return BASE_BLOCKS[n]
    m = n // 2
    block = block_around(m)
    doubled = []
    for offset in range(4):
        k = m - 1 + offset
        w = block[offset : offset + 5]  # W_{k-2}, ..., W_{k+2}
        doubled.append(
            (w[3] * w[1] ** 3 - w[0] * w[2] ** 3) % MODULUS  # W_{2k-1}
        )
        doubled.append(
            (w[2] * INV_TWO * (w[4] * w[1] ** 2 - w[0] * w[3] ** 2))
            % MODULUS  # W_{2k}
        )
    doubled.append(
        (w[4] * w[2] ** 3 - w[1] * w[3] ** 3) % MODULUS  # W_{2m+5}
    )
    start = 0 if n % 2 == 0 else 1
    return doubled[start : start + 8]


def sequence_value(n: int) -> int:
    w = block_around(n)[3]  # W_n
    exponent = (n * n) // 4
    scale = pow(INV_TWO, exponent % (MODULUS - 1), MODULUS)
    sign = 1 if n % 4 in (1, 2) else -1
    return sign * w * scale % MODULUS


def solve() -> int:
    return sequence_value(10**18 + 3)


if __name__ == "__main__":
    assert sequence_value(13) == 23321
    assert sequence_value(1003) == 231_906_014
    print(solve())
