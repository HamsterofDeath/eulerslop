#!/usr/bin/env python3
from functools import lru_cache


MOD = 123454321
DIGITS = "123432"
CYCLE_MOD = 10 ** 6 % MOD


def _digits_mod(text):
    value = 0
    for ch in text:
        value = (10 * value + int(ch)) % MOD
    return value


def _first_period():
    pos = 0
    chunks = []
    for target in range(1, 16):
        start = pos
        total = 0
        text = []
        while total < target:
            ch = DIGITS[pos]
            text.append(ch)
            total += int(ch)
            pos = (pos + 1) % len(DIGITS)
        chunks.append((start, "".join(text)))
    return chunks


PERIOD = _first_period()


@lru_cache(maxsize=None)
def _geom(n):
    # For R = 10^6, return:
    # R^n, sum_{k=0}^{n-1} R^k, and sum_{k=0}^{n-1} (n-k)R^k.
    if n == 0:
        return 1, 0, 0
    if n == 1:
        return CYCLE_MOD, 1, 1

    a = n // 2
    b = n - a
    pow_a, sum_a, weighted_a = _geom(a)
    pow_b, sum_b, weighted_b = _geom(b)
    return (
        pow_a * pow_b % MOD,
        (sum_a + pow_a * sum_b) % MOD,
        (weighted_a + b * sum_a + pow_a * weighted_b) % MOD,
    )


def S(limit):
    total = 0
    for residue, (pos, suffix) in enumerate(PERIOD, start=1):
        if limit < residue:
            continue
        cycles = (limit - residue) // 15
        block = "".join(DIGITS[(pos + i) % len(DIGITS)] for i in range(6))
        _, _, weighted = _geom(cycles)
        total += _digits_mod(block) * pow(10, len(suffix), MOD) * weighted
        total += _digits_mod(suffix) * (cycles + 1)
    return total % MOD


def solve():
    assert S(11) == 36120
    assert S(1000) == 18232686
    return S(10 ** 14)


if __name__ == "__main__":
    print(solve())
