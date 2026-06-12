#!/usr/bin/env python3
import numpy as np
from math import isqrt

# A grid-line cut of a w x h sheet into two pieces that reassemble into another
# rectangle is necessarily a staircase cut with some number of steps k:
#   family 1: if k | w and (k+1) | h, we get  w(k+1)/k  x  hk/(k+1)
#   family 2: if (k+1) | w and k | h, we get  wk/(k+1)  x  h(k+1)/k
# F(w,h) = number of distinct unordered targets != {w,h}.  Writing w = ku,
# h = (k+1)v (family 1) the move is (ku,(k+1)v) -> ((k+1)u, kv).
#
# Let I(N) = sum over h<=w<=N of (#family-1 k's + #family-2 k's).  This
# overcounts G(N) by:
#  * targets congruent to the source: only family 2 can do this, exactly when
#    w/h = (q+1)/q in lowest terms, i.e. (w,h) = ((q+1)t, qt); total count
#    sum_{m>=2} floor(N/m) = D2(N) - N  (D2 = divisor summatory function).
#  * the same target produced by two different representations.  Within
#    family 1 targets are distinct (their long side w(k+1)/k > w determines k)
#    and never collide with the source, so duplicates are either
#      (a) family 1 (k) vs family 2 (k'): solving the equations forces
#          w = k(k'+1)d, h = (k+1)k'd, and h<=w forces k'<=k; count
#          D_A = #{(k,j,d): kjd <= N, 2 <= j <= k+1}   (j = k'+1)
#      (b) family 2 (k1) vs family 2 (k2), k1<k2: forces
#          w = (k1+1)(k2+1)e, h = k1k2e; count
#          D_B = #{(a,b,e): abe <= N, 2 <= a < b}      (a,b = k_i+1)
#    Each duplicated target appears at most twice, so subtract D_A + D_B once.
#    Splitting D_A at j = k+1 and pairing #{2<=j<=k} with D_B, the union is
#    all triples with both small factors >= 2 plus the j=k+1 diagonal:
#      D_A + D_B = (D3(N) - 2*D2(N) + N) + W,   W = sum_k floor(N/(k(k+1)))
#    where D3(N) = #{xyz <= N} (3-dimensional divisor summatory function).
# Altogether:
#   G(N) = I(N) - (D2(N) - N) - (D3(N) - 2*D2(N) + N + W)
#        = I(N) + D2(N) - D3(N) - W.

def icbrt(n):
    x = int(round(n ** (1.0 / 3)))
    while x * x * x > n:
        x -= 1
    while (x + 1) ** 3 <= n:
        x += 1
    return x

def D2(N):
    # #{(x,y): xy <= N} by the hyperbola method.
    K = isqrt(N)
    i = np.arange(1, K + 1, dtype=np.int64)
    return 2 * int((N // i).sum()) - K * K

def D3(N):
    # #{(x,y,z): xyz <= N} via the sorted-triple decomposition
    # D3 = 6*#{x<y<z} + 3*#{x=y<z} + 3*#{x<y=z} + #{x=y=z}.
    K = isqrt(N)
    xs = np.arange(1, K + 1, dtype=np.int64)
    B = int(np.maximum(N // (xs * xs) - xs, 0).sum())      # x = y < z
    ys = np.arange(2, K + 1, dtype=np.int64)
    C = int(np.minimum(ys - 1, N // (ys * ys)).sum())      # x < y = z
    A = 0                                                  # x < y < z
    x = 1
    while x * (x + 1) * (x + 2) <= N:
        ymax = isqrt(N // x)
        if ymax > x:
            y = np.arange(x + 1, ymax + 1, dtype=np.int64)
            A += int((N // (x * y) - y).sum())
        x += 1
    return 6 * A + 3 * B + 3 * C + icbrt(N)

def G(N):
    K = isqrt(N)
    # I(N): family 1 contributes, per k, #{(i,j): (k+1)j <= ki <= N}
    #   = sum_{i<=N//k} floor(ki/(k+1)), and floor(ki/(k+1)) = i - ceil(i/(k+1));
    # family 2 contributes sum_{i<=N//(k+1)} floor((k+1)i/k) with
    #   floor((k+1)i/k) = i + floor(i/k).  Both inner sums have O(1) closed forms.
    I = 0
    for k in range(1, K + 1):
        M = N // k
        q, r = divmod(M, k + 1)
        I += M * (M + 1) // 2 - ((k + 1) * q * (q + 1) // 2 + r * (q + 1))
        M2 = N // (k + 1)
        q2, r2 = divmod(M2, k)
        I += M2 * (M2 + 1) // 2 + k * q2 * (q2 - 1) // 2 + q2 * (r2 + 1)
    # For k > sqrt(N) the ceil/floor corrections collapse (N//k < k), leaving
    # M(M-1)/2 resp. M'(M'+1)/2 with M = N//k, M' = N//(k+1): sum by quotient
    # blocks (family 2 re-indexed by m = k+1, so it starts one index later).
    m = K + 1
    while m <= N:
        v = N // m
        hi = N // v
        cnt = hi - m + 1
        I += cnt * (v * (v - 1) // 2)
        I += (cnt - (1 if m == K + 1 else 0)) * (v * (v + 1) // 2)
        m = hi + 1
    ks = np.arange(1, K + 1, dtype=np.int64)
    ks = ks[ks * (ks + 1) <= N]
    W = int((N // (ks * (ks + 1))).sum())
    return I + D2(N) - D3(N) - W

def F_brute(w, h):
    # Direct enumeration of staircase moves, for validating the formula.
    targets = set()
    for k in range(1, max(w, h) + 1):
        if w % k == 0 and h % (k + 1) == 0:
            a, b = (w // k) * (k + 1), (h // (k + 1)) * k
            targets.add((max(a, b), min(a, b)))
        if w % (k + 1) == 0 and h % k == 0:
            a, b = (w // (k + 1)) * k, (h // k) * (k + 1)
            targets.add((max(a, b), min(a, b)))
    targets.discard((w, h))
    return len(targets)

def solve():
    # Sanity checks against the values given in the statement.
    assert F_brute(2, 1) == 0 and F_brute(2, 2) == 1
    assert F_brute(9, 4) == 3 and F_brute(9, 8) == 2
    assert G(137) == sum(F_brute(w, h) for w in range(1, 138)
                         for h in range(1, w + 1))
    assert G(10) == 55
    assert G(10 ** 3) == 971745
    assert G(10 ** 5) == 9992617687
    return G(10 ** 12) % 10 ** 8

if __name__ == "__main__":
    print(solve())
