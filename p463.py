#!/usr/bin/env python3
from functools import lru_cache

MOD = 10 ** 9


@lru_cache(None)
def f(n):
    if n == 1:
        return 1
    if n == 3:
        return 3
    if n % 2 == 0:
        return f(n // 2)
    m = (n - 1) // 4
    if n % 4 == 1:
        return (2 * f(2 * m + 1) - f(m)) % MOD
    return (3 * f(2 * m + 1) - 2 * f(m)) % MOD


@lru_cache(None)
def odd_sum(n):
    """sum_{i=1..n} f(2i-1), modulo MOD."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    if n % 2 == 0:
        m = n // 2
        return (5 * odd_sum(m) - 3 * S(m - 1) - 1) % MOD
    m = n // 2
    return (odd_sum(2 * m) + 2 * f(2 * m + 1) - f(m)) % MOD


@lru_cache(None)
def S(n):
    if n <= 0:
        return 0
    if n % 2 == 0:
        m = n // 2
        return (S(m) + odd_sum(m)) % MOD
    return (S(n - 1) + f(n)) % MOD


def solve():
    assert S(8) == 22
    assert S(100) == 3604
    return S(3 ** 37)


if __name__ == "__main__":
    print(solve())
