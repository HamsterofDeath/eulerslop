#!/usr/bin/env python3
import numpy as np
from bisect import bisect_right
from math import gcd


def _factor(m):
    # trial-division factorization (all m here are small or smooth)
    f = {}
    d = 2
    while d * d <= m:
        while m % d == 0:
            f[d] = f.get(d, 0) + 1
            m //= d
        d += 1 if d == 2 else 2
    if m > 1:
        f[m] = f.get(m, 0) + 1
    return f


def _carmichael(m):
    lam = 1
    for p, e in _factor(m).items():
        if p == 2:
            v = 1 if e == 1 else (2 if e == 2 else 2 ** (e - 2))
        else:
            v = (p - 1) * p ** (e - 1)
        lam = lam * v // gcd(lam, v)
    return lam


def _order(a, m):
    # multiplicative order of a mod m (gcd(a, m) == 1)
    if m == 1:
        return 1
    t = _carmichael(m)
    for q in _factor(t):
        while t % q == 0 and pow(a, t // q, m) == 1:
            t //= q
    return t


def _S(n):
    if n == 1:
        return 1  # only station (0, 0)
    # strip factors of 2 (resp. 3): 2^i mod n is periodic for i >= v2(n)
    # with period ord_{n/2^v2}(2), similarly for 3^i.
    a2, m2 = 0, n
    while m2 % 2 == 0:
        m2 //= 2
        a2 += 1
    b3, m3 = 0, n
    while m3 % 3 == 0:
        m3 //= 3
        b3 += 1
    o2, o3 = _order(2, m2), _order(3, m3)
    T = o2 * o3 // gcd(o2, o3)
    pre = max(a2, b3)
    L = min(2 * n + 1, pre + T)  # i = 0..L-1 hits every distinct station

    # generate (2^i mod n, 3^i mod n) in numpy blocks: each block is the
    # previous one multiplied by 2^B (resp. 3^B) mod n; pack into one key
    # so that sorting by key == sorting by x then y.
    B = 1 << 15
    head = min(B, L)
    xs, ys = [0] * head, [0] * head
    cx = cy = 1 % n
    for i in range(head):
        xs[i], ys[i] = cx, cy
        cx = cx * 2 % n
        cy = cy * 3 % n
    xb = np.array(xs, dtype=np.int64)
    yb = np.array(ys, dtype=np.int64)
    s2, s3 = pow(2, B, n), pow(3, B, n)
    blocks = []
    done = 0
    while done < L:
        take = min(B, L - done)
        blocks.append(xb[:take] * (n + 1) + yb[:take])
        done += take
        if done < L:
            xb = xb * s2 % n
            yb = yb * s3 % n
    keys = np.unique(np.concatenate(blocks))  # dedupe + sort by (x, y)

    # longest non-decreasing subsequence of y (patience sorting)
    tails = []
    for y in (keys % (n + 1)).tolist():
        j = bisect_right(tails, y)
        if j == len(tails):
            tails.append(y)
        else:
            tails[j] = y
    return len(tails)


def solve():
    return sum(_S(k ** 5) for k in range(1, 31))


if __name__ == "__main__":
    print(solve())
