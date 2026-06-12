#!/usr/bin/env python3

MOD = 999999937


def _binom_small(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    num = den = 1
    for i in range(1, k + 1):
        num = num * (n - k + i) % MOD
        den = den * i % MOD
    return num * pow(den, MOD - 2, MOD) % MOD


def _binom_lucas(n, k):
    res = 1
    while n or k:
        ni, ki = n % MOD, k % MOD
        if ki > ni:
            return 0
        res = res * _binom_small(ni, ki) % MOD
        n //= MOD
        k //= MOD
    return res


def C(n, m, d):
    # x^n mod (x-1)^m is the Taylor truncation:
    # sum_{j=0}^{m-1} binom(n,j)(x-1)^j.
    # The x^d coefficient is
    #   binom(n,d) * sum_{t=0}^{m-1-d} (-1)^t binom(n-d,t)
    # = +/- binom(n,d) * binom(n-d-1,m-1-d).
    return _binom_lucas(n, d) * _binom_lucas(n - d - 1, m - d - 1) % MOD


def solve():
    assert C(6, 3, 1) == 24
    assert C(100, 10, 4) == 227197811615775 % MOD
    return C(10 ** 13, 10 ** 12, 10 ** 4)


if __name__ == "__main__":
    print(solve())
