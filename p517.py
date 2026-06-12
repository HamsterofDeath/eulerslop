#!/usr/bin/env python3
from math import isqrt


MOD = 1_000_000_007


def ceil_k_sqrt_n(k, n):
    square = k * k * n
    root = isqrt(square)
    return root if root * root == square else root + 1


def prime_sieve(limit):
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[0:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if is_prime[p]:
            start = p * p
            is_prime[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return is_prime


def factorial_tables(limit):
    factorial = [1] * (limit + 1)
    inverse_factorial = [1] * (limit + 1)
    for i in range(1, limit + 1):
        factorial[i] = factorial[i - 1] * i % MOD

    inverse_factorial[limit] = pow(factorial[limit], MOD - 2, MOD)
    for i in range(limit, 0, -1):
        inverse_factorial[i - 1] = inverse_factorial[i] * i % MOD
    return factorial, inverse_factorial


def make_choose(limit):
    factorial, inverse_factorial = factorial_tables(limit)

    def choose(n, k):
        if k < 0 or k > n:
            return 0
        return factorial[n] * inverse_factorial[k] % MOD * inverse_factorial[n - k] % MOD

    return choose


def G(n, choose):
    total = 0
    for j in range(isqrt(n) + 4):
        i = n + 1 - ceil_k_sqrt_n(j + 1, n)
        if i >= 1:
            total += choose(i + j - 1, j)

        if j >= 1:
            low = n - ceil_k_sqrt_n(j + 1, n) + 1
            high = n - ceil_k_sqrt_n(j, n)
            if high >= 0 and low <= high:
                low = max(low, 0)
                total += choose(high + j, j) - choose(low + j - 1, j)

        total %= MOD
    return total


def solve():
    choose = make_choose(10_010_000)
    assert G(90, choose) == 7_564_511

    is_prime = prime_sieve(10_010_000)
    total = 0
    for p in range(10_000_001, 10_010_000):
        if is_prime[p]:
            total = (total + G(p, choose)) % MOD
    return total


if __name__ == "__main__":
    print(solve())
