#!/usr/bin/env python3
"""Project Euler 833: triangular products via Pell powers."""

from math import gcd


LIMIT = 10**35
MOD = 136_101_521


def pell_y(n: int, x: int, cap: int | None = None) -> int:
    """Y coordinate of (x + y sqrt(D))^n when y starts at 1."""
    if n == 0:
        return 0
    y0, y1 = 0, 1
    for _ in range(1, n):
        y0, y1 = y1, 2 * x * y1 - y0
        if cap is not None and y1 > cap:
            return y1
    return y1


def family_value(a: int, u: int, v: int, cap: int | None = None) -> int:
    x = 2 * a + 1
    triangle = a * (a + 1) // 2
    yu = pell_y(u, x, cap)
    if cap is not None and triangle * yu > cap:
        return cap + 1
    yv = pell_y(v, x, cap)
    value = triangle * yu * yv
    if cap is not None and value > cap:
        return cap + 1
    return value


def max_base(limit: int, u: int, v: int) -> int:
    if family_value(1, u, v, limit) > limit:
        return 0

    lo, hi = 1, 2
    while family_value(hi, u, v, limit) <= limit:
        hi *= 2

    lo = hi // 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if family_value(mid, u, v, limit) <= limit:
            lo = mid
        else:
            hi = mid - 1
    return lo


def comb_small(n: int, r: int) -> int:
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    result = 1
    for i in range(1, r + 1):
        result = result * (n - r + i) // i
    return result


def family_sum(limit: int, u: int, v: int, modulus: int) -> int:
    last = max_base(limit, u, v)
    if last == 0:
        return 0

    # For fixed coprime exponents (u, v), T_a * Y_u(2a+1) * Y_v(2a+1)
    # is a degree u+v polynomial in a. Finite differences sum it at huge a.
    degree = u + v
    diffs = [family_value(a, u, v) % modulus for a in range(degree + 1)]
    total = 0
    for k in range(degree + 1):
        total = (total + diffs[0] * (comb_small(last + 1, k + 1) % modulus)) % modulus
        diffs = [(diffs[i + 1] - diffs[i]) % modulus for i in range(len(diffs) - 1)]
    return total


def summed(limit: int, modulus: int) -> int:
    total = 0
    u = 1
    while family_value(1, u, u + 1, limit) <= limit:
        v = u + 1
        while True:
            if gcd(u, v) == 1:
                if family_value(1, u, v, limit) > limit:
                    break
                total = (total + family_sum(limit, u, v, modulus)) % modulus
            v += 1
        u += 1
    return total


def solve() -> int:
    exact_modulus = 10**30
    assert summed(100, exact_modulus) == 155
    assert summed(10**5, exact_modulus) == 1_479_802
    assert summed(10**9, exact_modulus) == 241_614_948_794
    return summed(LIMIT, MOD)


if __name__ == "__main__":
    print(solve())
