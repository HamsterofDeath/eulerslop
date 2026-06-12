#!/usr/bin/env python3

MOD = 10 ** 9


def _matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) % MOD
             for j in range(n)] for i in range(n)]


def _matvec(a, v):
    return [sum(a[i][j] * v[j] for j in range(len(v))) % MOD
            for i in range(len(v))]


def T(n):
    if n == 0:
        return 1
    # State r=1..6 is the length of the longest suffix with all distinct
    # letters.  Repeating the letter d places back makes the new state d+1;
    # using a letter absent from the suffix increases r, except 6->7 is banned.
    trans = [[0] * 6 for _ in range(6)]
    for r in range(1, 7):
        for new_r in range(1, r + 1):
            trans[new_r - 1][r - 1] += 1
        if r < 6:
            trans[r][r - 1] += 7 - r

    v = [7, 0, 0, 0, 0, 0]
    e = n - 1
    while e:
        if e & 1:
            v = _matvec(trans, v)
        trans = _matmul(trans, trans)
        e >>= 1
    return sum(v) % MOD


def solve():
    assert T(7) == 818503
    return T(10 ** 12)


if __name__ == "__main__":
    print(solve())
