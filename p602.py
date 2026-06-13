#!/usr/bin/env python3

MOD = 1_000_000_007


def coefficient(n: int, k: int) -> int:
    """Coefficient of p^k in (1-p)^(n+1) * sum_{r>=0} r^n p^r."""
    inv = [0] * (k + 1)
    if k:
        inv[1] = 1
    for i in range(2, k + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    total = 0
    choose = 1
    sign = 1
    top = n + 1

    for j in range(k + 1):
        base = k - j
        if base:
            term = choose * pow(base, n, MOD) % MOD
            total += term if sign > 0 else -term

        if j < k:
            choose = choose * (top - j) % MOD * inv[j + 1] % MOD
            sign = -sign

    return total % MOD


def solve() -> int:
    return coefficient(10_000_000, 4_000_000)


if __name__ == "__main__":
    print(solve())
