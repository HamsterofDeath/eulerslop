#!/usr/bin/env python3

MOD = 10 ** 9


def f(n):
    if n % 10 == 0:
        return 0
    x = 0
    while True:
        y = pow(n, x, MOD)
        if y == x:
            return x
        x = y


def solve():
    assert f(4) == 411728896
    assert f(10) == 0
    assert f(157) == 743757
    assert sum(f(n) for n in range(2, 1001)) == 442530011399
    return sum(f(n) for n in range(2, 10 ** 6 + 1))


if __name__ == "__main__":
    print(solve())
