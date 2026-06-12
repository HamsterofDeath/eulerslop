#!/usr/bin/env python3
from functools import lru_cache

MOD = 10 ** 9


def _hit(k, i, j):
    if i == j:
        return 0
    if i < j:
        return (j - i) * (i + j - 2)
    return (i - j) * (2 * k - i - j)


def _E(n, k, a, b, c):
    pos = (a, b, c)

    @lru_cache(None)
    def f(r, s, d, cur):
        t = 3 - s - d
        if r == 1:
            return _hit(k, pos[cur], pos[s]) + _hit(k, pos[s], pos[d])
        return (
            f(r - 1, s, t, cur)
            + _hit(k, pos[t], pos[s])
            + _hit(k, pos[s], pos[d])
            + f(r - 1, t, d, d)
        )

    return f(n, 0, 2, 1)


def solve():
    assert _E(2, 5, 1, 3, 5) == 60
    assert _E(3, 20, 4, 9, 17) == 2358

    states = [(s, d, cur) for s in range(3) for d in range(3) if s != d
              for cur in range(3)]
    index = {state: i for i, state in enumerate(states)}

    coeffs = []
    for s, d, cur in states:
        v = [0] * 9
        v[cur * 3 + s] += 1
        v[s * 3 + d] += 1
        coeffs.append(v)

    ans = 0
    k = a = b = c = 1
    for n in range(1, 10001):
        k = k * 10 % MOD
        a = a * 3 % MOD
        b = b * 6 % MOD
        c = c * 9 % MOD
        costs = [0] * 9
        costs[0 * 3 + 1] = (b - a) * (a + b - 2) % MOD
        costs[0 * 3 + 2] = (c - a) * (a + c - 2) % MOD
        costs[1 * 3 + 2] = (c - b) * (b + c - 2) % MOD
        costs[1 * 3 + 0] = (b - a) * (2 * k - a - b) % MOD
        costs[2 * 3 + 0] = (c - a) * (2 * k - a - c) % MOD
        costs[2 * 3 + 1] = (c - b) * (2 * k - b - c) % MOD

        target = coeffs[index[(0, 2, 1)]]
        ans = (ans + sum(x * y for x, y in zip(target, costs))) % MOD

        nxt = []
        for s, d, cur in states:
            t = 3 - s - d
            left = coeffs[index[(s, t, cur)]]
            right = coeffs[index[(t, d, d)]]
            v = [(left[i] + right[i]) % MOD for i in range(9)]
            v[t * 3 + s] = (v[t * 3 + s] + 1) % MOD
            v[s * 3 + d] = (v[s * 3 + d] + 1) % MOD
            nxt.append(v)
        coeffs = nxt

    return ans


if __name__ == "__main__":
    print(solve())
