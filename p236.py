#!/usr/bin/env python3
from math import gcd

# Supplies: A = (5248, 1312, 2624, 5760, 3936), B = (640, 1888, 3776, 3776, 5664)
# Ratio classes (B'_i/A'_i in lowest terms):
#   product 1:        5/41   (A=41*128, B=5*128)
#   products 2,3,5:  59/41   (A=41*{32,64,96}, B=59*{32,64,96})
#   product 4:       59/90   (A=90*64,  B=59*64)
# Totals: SA=18880, SB=15744, SB/SA = 246/295.
#
# Conditions for m = u/v (>1, lowest terms):
#   per product:  b_i/a_i = m*B_i/A_i = u*B'_i/(v*A'_i) = p_c/q_c (reduced),
#                 so (a_i, b_i) = k_i*(q_c, p_c), 1 <= k_i <= K_i = min(A_i//q_c, B_i//p_c)
#   totals:       Sa/SA = m*Sb/SB  ->  246*v*Sa = 295*u*Sb
#                 ->  sum_i k_i*(246*v*q_c - 295*u*p_c) = 0
# Products 2,3,5 share (p,q), so their k's collapse to one sum s in a contiguous range,
# leaving a 3-variable bounded linear Diophantine existence check.

A1, B1 = 5248, 640
A2, B2 = 1312, 1888
A3, B3 = 2624, 3776
A5, B5 = 3936, 5664
A4, B4 = 5760, 3776


def exists2(a, b, n, x1, x2, y1, y2):
    """Does a*x + b*y == n have a solution with x in [x1,x2], y in [y1,y2]?"""
    if x1 > x2 or y1 > y2:
        return False
    if a == 0 and b == 0:
        return n == 0
    if a == 0:
        return n % b == 0 and y1 <= n // b <= y2
    if b == 0:
        return n % a == 0 and x1 <= n // a <= x2
    g = gcd(a, b)
    if n % g:
        return False
    a, b, n = a // g, b // g, n // g
    # y in [y1,y2]  =>  a*x = n - b*y lies in [lo_ax, hi_ax]
    t1, t2 = n - b * y1, n - b * y2
    lo_ax, hi_ax = (t1, t2) if t1 <= t2 else (t2, t1)
    if a > 0:
        xl, xh = -((-lo_ax) // a), hi_ax // a
    else:
        aa = -a
        xl, xh = -(hi_ax // aa), (-lo_ax) // aa
    lo, hi = max(x1, xl), min(x2, xh)
    if lo > hi:
        return False
    step = abs(b)
    if step == 1:
        return True
    # need a*x ≡ n (mod |b|)
    r = (n * pow(a % step, -1, step)) % step
    first = lo + ((r - lo) % step)
    return first <= hi


def feasible(u, v):
    """Check whether m = u/v admits valid spoilage counts."""
    # class {2,3,5}: ratio 59/41 (cheapest reject first)
    g2 = gcd(59 * u, 41 * v)
    q2, p2 = 41 * v // g2, 59 * u // g2
    if q2 > A2 or p2 > B2:
        return False
    # class {1}: ratio 5/41
    g1 = gcd(5 * u, 41 * v)
    q1, p1 = 41 * v // g1, 5 * u // g1
    if q1 > A1 or p1 > B1:
        return False
    # class {4}: ratio 59/90
    g4 = gcd(59 * u, 90 * v)
    q4, p4 = 90 * v // g4, 59 * u // g4
    if q4 > A4 or p4 > B4:
        return False

    K1 = min(A1 // q1, B1 // p1)
    K2 = min(A2 // q2, B2 // p2)
    K3 = min(A3 // q2, B3 // p2)
    K5 = min(A5 // q2, B5 // p2)
    K4 = min(A4 // q4, B4 // p4)

    w1 = 246 * v * q1 - 295 * u * p1
    w2 = 246 * v * q2 - 295 * u * p2
    w4 = 246 * v * q4 - 295 * u * p4
    # need k1*w1 + s*w2 + k4*w4 == 0 with k1 in [1,K1], s in [3,K2+K3+K5], k4 in [1,K4]
    if w1 > 0 and w2 > 0 and w4 > 0:
        return False
    if w1 < 0 and w2 < 0 and w4 < 0:
        return False
    triples = sorted(
        [(K1, w1, 1, K1), (K2 + K3 + K5 - 2, w2, 3, K2 + K3 + K5), (K4, w4, 1, K4)]
    )
    _, wa, alo, ahi = triples[0]
    _, wb, blo, bhi = triples[1]
    _, wc, clo, chi = triples[2]
    for t in range(alo, ahi + 1):
        if exists2(wb, wc, -wa * t, blo, bhi, clo, chi):
            return True
    return False


def candidates():
    """All (u, v) that can pass the per-product bounds, split by 41|u and 59|v.

    From products 2 (and 1, 4): q <= A and p <= B force
      41|u? no,  59|v? no  -> u, v <= 32
      41|u yes,  59|v no   -> u = 41u' (u'<=32), v <= 1312
      41|u no,   59|v yes  -> u <= 1888, v = 59v' (v'<=32)
      both                 -> u = 41u' (u'<=640), v = 59v' (v'<=444)  [via product 1]
    """
    for u in range(2, 33):
        for v in range(1, 33):
            yield u, v
    for up in range(1, 33):
        u = 41 * up
        for v in range(1, 1313):
            if v % 59:
                yield u, v
    for vp in range(1, 33):
        v = 59 * vp
        for u in range(2, 1889):
            if u % 41:
                yield u, v
    for up in range(1, 641):
        u = 41 * up
        for vp in range(1, 445):
            yield u, 59 * vp


def solve():
    valid = []
    for u, v in candidates():
        if u <= v or gcd(u, v) != 1:
            continue
        if feasible(u, v):
            valid.append((u, v))
    # sanity: the problem states there are 35 such m, the smallest being 1476/1475
    assert len(valid) == 35, len(valid)
    assert min(valid, key=lambda f: f[0] / f[1]) == (1476, 1475)
    u, v = max(valid, key=lambda f: f[0] / f[1])
    return f"{u}/{v}"


if __name__ == "__main__":
    print(solve())
