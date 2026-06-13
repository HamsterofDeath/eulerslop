#!/usr/bin/env python3
"""Project Euler 746: two-present Secret Santa seating."""


MOD = 1_000_000_007
LIMIT = 2021


def factorials(limit: int) -> tuple[list[int], list[int]]:
    fact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (limit + 1)
    inv_fact[limit] = pow(fact[limit], MOD - 2, MOD)
    for i in range(limit, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD
    return fact, inv_fact


FACT, INV_FACT = factorials(4 * LIMIT)


def choose(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    return FACT[n] * INV_FACT[k] % MOD * INV_FACT[n - k] % MOD


def block_placements(n: int, blocks: int) -> int:
    if blocks == 0:
        return 1
    return (
        4
        * n
        * FACT[blocks - 1]
        * choose(4 * n - 3 * blocks - 1, blocks - 1)
    ) % MOD


def m_value(n: int) -> int:
    if n == 1:
        return 0
    total = 0
    for together in range(n + 1):
        term = (
            choose(n, together)
            * 2
            * block_placements(n, together)
            * pow(4, together, MOD)
            * FACT[2 * n - 2 * together]
            * FACT[2 * n - 2 * together]
        ) % MOD
        if together % 2:
            total -= term
        else:
            total += term
    return total % MOD


def solve() -> int:
    assert m_value(1) == 0
    assert m_value(2) == 896
    assert m_value(3) == 890880
    assert m_value(10) == 170717180
    assert sum(m_value(k) for k in range(2, 11)) % MOD == 399291975
    return sum(m_value(k) for k in range(2, LIMIT + 1)) % MOD


if __name__ == "__main__":
    print(solve())
