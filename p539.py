#!/usr/bin/env python3
from functools import lru_cache


MOD = 987654321


@lru_cache(maxsize=None)
def P(n):
    if n == 1:
        return 1
    m = n // 2
    return 2 * (m + 1 - P(m))


@lru_cache(maxsize=None)
def S(n):
    if n == 1:
        return 1
    m = n // 2
    paired = (m * (m + 3) - 2 * S(m)) % MOD
    if n % 2:
        return (1 + 2 * paired) % MOD
    return (1 + 2 * paired - P(n)) % MOD


def solve():
    assert P(1) == 1
    assert P(9) == 6
    assert P(1000) == 510
    assert S(1000) == 268271
    return S(10 ** 18)


if __name__ == "__main__":
    print(solve())
