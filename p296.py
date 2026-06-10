#!/usr/bin/env python3
import numpy as np

# Angle bisector / circumcircle tangent geometry.
#
# With sides a = BC, b = CA, c = AB (a <= b <= c):
# the tangent-chord angle at C equals angle A, so line n through B makes
# angle A with CB; in triangle CBE (E on the bisector of C) the sine rule
# gives BE = a*sin(C/2)/sin(A + C/2), which is exactly the length BD of the
# bisector foot D on AB (since sin(A + C/2) = sin(B + C/2)).
# Hence BE = a*c/(a+b), and BE integral  <=>  (a+b) | a*c.
#
# Write g = gcd(a, b), a = g*a', b = g*b', s' = a' + b' (gcd(a', s') = 1).
# Then (a+b) | a*c  <=>  s' | c, so c = k*s' with:
#   b <= c           <=>  k >= ceil(g*b'/s') = g - floor(g*a'/s')
#   c < a + b        <=>  k <= g - 1
#   a + b + c <= N   <=>  g + k <= M := N // s'
# So the number of valid c for fixed (g, a', s') is
#   max(0, min(g-1, M-g) - g + 1 + floor(g*a'/s')).
# Sum this over all s', coprime a' <= s'/2 and g >= 2 (vectorized with numpy).


def solve():
    N = 100000
    total = 0

    # Smallest-prime-factor sieve for fast coprime masks.
    lim = N // 3 + 1
    spf = np.zeros(lim, dtype=np.int32)
    for p in range(2, lim):
        if spf[p] == 0:
            spf[p::p] = np.where(spf[p::p] == 0, p, spf[p::p])

    for sp in range(2, N // 3 + 1):
        M = N // sp
        if M < 3:
            break
        # a' in [1, sp//2] coprime to sp, via the prime factors of sp.
        half = sp // 2
        mask = np.ones(half + 1, dtype=bool)
        m = sp
        while m > 1:
            p = int(spf[m])
            mask[p::p] = False
            while m % p == 0:
                m //= p
        A = np.flatnonzero(mask[1:]).astype(np.int32) + 1
        if A.size == 0:
            continue

        G = np.arange(2, M, dtype=np.int32)
        # base(g) = min(g-1, M-g) - g + 1   (independent of a')
        base = np.minimum(G - 1, M - G) - G + 1
        # counts(g, a') = max(0, base(g) + floor(g*a'/sp))
        mat = np.multiply.outer(G, A) // sp
        mat += base[:, None]
        np.maximum(mat, 0, out=mat)
        total += int(mat.sum(dtype=np.int64))

    return total


if __name__ == "__main__":
    print(solve())
