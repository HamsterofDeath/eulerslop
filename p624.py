#!/usr/bin/env python3
"""Project Euler 624: HH stopping time divisibility via a two-state chain."""


MOD = 1_000_000_009
N = 10**18


def mat_mul(left, right, mod):
    a, b, c, d = left
    e, f, g, h = right
    return (
        (a * e + b * g) % mod,
        (a * f + b * h) % mod,
        (c * e + d * g) % mod,
        (c * f + d * h) % mod,
    )


def mat_pow(matrix, exponent, mod):
    result = (1, 0, 0, 1)
    while exponent:
        if exponent & 1:
            result = mat_mul(result, matrix, mod)
        matrix = mat_mul(matrix, matrix, mod)
        exponent >>= 1
    return result


def stopping_probability_residue(period, mod):
    inv2 = (mod + 1) // 2
    transition = (inv2, inv2, inv2, 0)

    full_block = mat_pow(transition, period, mod)
    final_toss = mat_pow(transition, period - 1, mod)

    # h = (0, 1/2)^T is the absorption probability on the next toss from each
    # non-absorbed state. Sum v*(I-A^period)^-1*A^(period-1)*h for v=(1,0).
    c0 = final_toss[1] * inv2 % mod
    c1 = final_toss[3] * inv2 % mod

    a, b, c, d = full_block
    determinant = ((1 - a) * (1 - d) - b * c) % mod
    numerator = ((1 - d) * c0 + b * c1) % mod
    return numerator * pow(determinant, -1, mod) % mod


def solve(period=N, prime=MOD):
    residue = stopping_probability_residue(period, prime)
    return residue if residue else prime


if __name__ == "__main__":
    print(solve())
