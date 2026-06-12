#!/usr/bin/env python3
from collections import Counter
from math import atan2, gcd, pi


def C(n):
    angles = []
    rays = Counter()
    x = y = 1
    for _ in range(n):
        x = x * 1248 % 32323
        y = y * 8421 % 30103
        px, py = x - 16161, y - 15051
        angles.append(atan2(py, px))
        g = gcd(abs(px), abs(py))
        rays[(px // g, py // g)] += 1

    angles.sort()
    doubled = angles + [a + 2 * pi for a in angles]
    bad = 0
    j = 0
    for i in range(n):
        if j < i + 1:
            j = i + 1
        while j < i + n and doubled[j] - doubled[i] < pi - 1e-15:
            j += 1
        k = j - i - 1
        bad += k * (k - 1) // 2

    # The open-semicircle pass omits triples whose only separating half-plane
    # has two opposite boundary rays.  Those are exactly triples containing at
    # least one point from each ray in an opposite pair.
    boundary = 0
    seen = set()
    for ray, a in rays.items():
        if ray in seen:
            continue
        opposite = (-ray[0], -ray[1])
        b = rays.get(opposite, 0)
        if b:
            seen.add(ray)
            seen.add(opposite)
            boundary += a * b * (n - a - b)
            boundary += (a * (a - 1) // 2) * b + (b * (b - 1) // 2) * a

    return n * (n - 1) * (n - 2) // 6 - bad - boundary


def solve():
    assert C(8) == 20
    assert C(600) == 8950634
    assert C(40000) == 2666610948988
    return C(2_000_000)


if __name__ == "__main__":
    print(solve())
