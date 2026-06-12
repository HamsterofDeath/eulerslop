#!/usr/bin/env python3

MOD = 1_000_000_007


def S(n):
    total = 0
    for k in range(1, n + 1):
        r = (1 - k * k) % MOD
        if r:
            total += r * (pow(r, n, MOD) - 1) * pow(r - 1, MOD - 2, MOD)
    return total % MOD


def solve():
    assert S(4) == 51160
    return S(10 ** 6)


if __name__ == "__main__":
    print(solve())
