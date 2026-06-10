#!/usr/bin/env python3
"""Project Euler 201: Subsets with a unique sum.

Find the sum of all integers which are the sum of exactly one of the
50-element subsets of S = {1^2, 2^2, ..., 100^2}.

Dynamic programming over (number of elements picked, subset sum), with
counts saturated at 2 (we only care about "exactly once" vs "more than
once").  Each layer is stored as two big-integer bitmasks per subset
size k: bit s of once[k] means "sum s reachable with >= 1 subsets of
size k", bit s of twice[k] means "reachable with >= 2 subsets".
Big-int shifts/ors make the inner loop fast.
"""

K = 50
N = 100


def solve():
    once = [0] * (K + 1)
    twice = [0] * (K + 1)
    once[0] = 1  # sum 0 with the empty subset, exactly one way

    for i in range(1, N + 1):
        v = i * i
        for k in range(min(i, K), 0, -1):
            shifted_once = once[k - 1] << v
            twice[k] |= (twice[k - 1] << v) | (once[k] & shifted_once)
            once[k] |= shifted_once

    unique = once[K] & ~twice[K]
    bits = bin(unique)[2:]
    n = len(bits)
    return sum(n - 1 - i for i, c in enumerate(bits) if c == '1')


if __name__ == "__main__":
    print(solve())
