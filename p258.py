#!/usr/bin/env python3
import numpy as np

# g_k = g_{k-2000} + g_{k-1999}, g_0..g_1999 = 1.  Find g_{10^18} mod 20092010.
#
# The recurrence has characteristic polynomial x^2000 - x - 1.  Compute
# x^N mod (x^2000 - x - 1) over Z_m by binary exponentiation; then
# g_N = sum_i c_i * g_i = sum_i c_i, since all initial terms are 1.
#
# Polynomial squaring uses np.convolve (int64 is safe: 2000 * (2*10^7)^2 < 2^63),
# and reduction uses x^(2000+h) = x^(h+1) + x^h.

MOD = 20092010
DEG = 2000


def reduce_poly(c):
    # c has length up to 2*DEG-1; fold the high part down.
    if len(c) <= DEG:
        out = np.zeros(DEG, dtype=np.int64)
        out[:len(c)] = c
        return out
    low = c[:DEG].copy()
    high = c[DEG:]
    h = len(high)
    low[:h] += high       # x^(2000+i) -> x^i
    low[1:h + 1] += high  # x^(2000+i) -> x^(i+1)
    return low % MOD


def polymul(a, b):
    return reduce_poly(np.convolve(a, b) % MOD)


def mul_x(c):
    # Multiply by x: shift up; x^2000 -> x + 1.
    out = np.empty(DEG, dtype=np.int64)
    out[1:] = c[:-1]
    top = c[-1]
    out[0] = top
    out[1] = (out[1] + top) % MOD
    return out


def solve():
    N = 10 ** 18
    # result = x^N mod (x^2000 - x - 1, MOD)
    res = np.zeros(DEG, dtype=np.int64)
    res[0] = 1
    for bit in bin(N)[2:]:
        res = polymul(res, res)
        if bit == '1':
            res = mul_x(res)
    return int(res.sum() % MOD)


if __name__ == "__main__":
    print(solve())
