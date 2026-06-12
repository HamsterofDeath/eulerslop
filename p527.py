#!/usr/bin/env python3
from functools import lru_cache
from math import log


EULER_GAMMA = 0.5772156649015328606


@lru_cache(maxsize=None)
def _binary_total(n):
    if n == 0:
        return 0
    left = (n - 1) // 2
    right = n - 1 - left
    return n + _binary_total(left) + _binary_total(right)


def B(n):
    return _binary_total(n) / n


def _harmonic(n):
    if n < 1000:
        return sum(1 / k for k in range(1, n + 1))
    x = float(n)
    return log(x) + EULER_GAMMA + 1 / (2 * x) - 1 / (12 * x * x)


def R(n):
    # Random pivots form a random binary-search tree.  The successful-search
    # mean depth is 2(n+1)H_n/n - 3.
    return 2 * (n + 1) * _harmonic(n) / n - 3


def solve():
    assert f"{B(6):.8f}" == "2.33333333"
    assert f"{R(6):.8f}" == "2.71666667"
    return f"{R(10 ** 10) - B(10 ** 10):.8f}"


if __name__ == "__main__":
    print(solve())
