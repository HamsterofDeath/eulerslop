#!/usr/bin/env python3
"""Project Euler 713: Turan's water heating system."""


def L(n):
    total = 0
    k = 1
    while k <= n:
        q = n // k
        last = n // q
        count = last - k + 1
        sum_k = (k + last) * count // 2
        total += count * n * q - sum_k * q * (q + 1) // 2
        k = last + 1
    return total


def solve():
    return L(10_000_000)


if __name__ == "__main__":
    print(solve())
