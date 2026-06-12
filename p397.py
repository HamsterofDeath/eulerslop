#!/usr/bin/env python3
import numpy as np

# The chord between points with x-coords u, v on y = x^2/k has slope (u+v)/k.
# For a triangle a < b < c, take the interior angle at one vertex; writing the
# signed tangent of the angle between the two rays (the sign flips when the
# vertex lies between its neighbours) and setting it to tan 45 = 1 gives, with
# s, t the two chord x-sums:
#   angle at A: (a+b-k)(a+c+k) = -2k^2
#   angle at B: (a+b+k)(b+c-k) = -2k^2      (B is the middle vertex)
#   angle at C: (a+c-k)(b+c+k) = -2k^2
# Each is m*n = -2k^2 with m = -d < 0, n = e > 0 forced (d*e = 2k^2 implies
# d+e >= 2*sqrt(2)*k > 2k, which is exactly the ordering constraint a<b<c).
# For a fixed divisor pair the remaining freedom is one integer translation
# variable confined to an intersection of intervals:
#   type A: count a in [max(-X, e-k-X), min(X, floor((k-d-1)/2))]
#   type B: with s1=-d-k, s2=e+k, count b in
#           [max(s2-X, floor(s1/2)+1), min(s1+X, floor((s2-1)/2))]
# and type C equals type A summed over the swapped pair (d,e)->(e,d), so
# N1 = sum over k, d|2k^2 of (2*A + B) counts every 45-degree angle once.
#
# Triangles with two 45-degree angles (right isosceles) are counted twice, so
# subtract them once.  Right angle at vertex v with neighbours u, w means
# (u+v)(w+v) = -k^2; writing u+v = d*x^2, w+v = -d*y^2 (gcd(x,y)=1, k = d*x*y,
# decomposition unique) the equal-legs condition |u-v| sqrt(1+((u+v)/k)^2) =
# |w-v| sqrt(1+((w+v)/k)^2) reduces to (u+v)(u-v)^2 = -(w+v)(w-v)^2 and yields
#   v = d(x^3-y^3)/(2(x+y))   or   v = d(x^3+y^3)/(2(x-y))  (x != y),
# so per coprime (x, y) the valid d form an arithmetic progression cut by the
# linear box constraints |v|, |u|, |w| <= X -- an O(1) count.


def n1_count(K, X):
    # smallest-prime-factor sieve for fast factorisation of every k
    spf_np = np.arange(K + 1, dtype=np.int64)
    p = 2
    while p * p <= K:
        if spf_np[p] == p:
            sl = spf_np[p * p::p]
            np.minimum(sl, p, out=sl)
        p += 1
    spf = spf_np.tolist()

    def flush(dlist, kvals, counts):
        dd = np.array(dlist, dtype=np.int64)
        kk = np.repeat(np.array(kvals, dtype=np.int64),
                       np.array(counts, dtype=np.int64))
        ee = (2 * kk * kk) // dd
        cA = np.minimum(X, (kk - dd - 1) >> 1) - np.maximum(-X, ee - kk - X) + 1
        np.maximum(cA, 0, out=cA)
        s1 = -dd - kk
        s2 = ee + kk
        cB = np.minimum(s1 + X, (s2 - 1) >> 1) - np.maximum(s2 - X, (s1 >> 1) + 1) + 1
        np.maximum(cB, 0, out=cB)
        return int((2 * cA + cB).sum())

    total = 0
    dlist, kvals, counts = [], [], []
    for k in range(1, K + 1):
        # divisors of 2*k^2 from the factorisation of k
        m = k
        e2 = 1
        while m & 1 == 0:
            m >>= 1
            e2 += 2
        divs = [1 << j for j in range(e2 + 1)]
        while m > 1:
            p = spf[m]
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            pw = []
            q = 1
            for _ in range(2 * e):
                q *= p
                pw.append(q)
            divs += [D * q for q in pw for D in divs]
        dlist += divs
        kvals.append(k)
        counts.append(len(divs))
        if len(dlist) >= (1 << 22):
            total += flush(dlist, kvals, counts)
            dlist, kvals, counts = [], [], []
    if dlist:
        total += flush(dlist, kvals, counts)
    return total


def n2_count(K, X):
    # right isosceles triangles, parametrised by coprime (x, y) with xy <= K
    res = 0
    x0 = 1
    while x0 <= K:
        x1, s = x0, 0
        while x1 <= K and s + K // x1 <= (1 << 22):
            s += K // x1
            x1 += 1
        x1 = max(x1, x0 + 1)
        xr = np.arange(x0, x1, dtype=np.int64)
        cnts = K // xr
        xs = np.repeat(xr, cnts)
        offs = np.repeat(np.concatenate(([0], np.cumsum(cnts)[:-1])), cnts)
        ys = np.arange(int(cnts.sum()), dtype=np.int64) - offs + 1
        msk = np.gcd(xs, ys) == 1
        xs, ys = xs[msk], ys[msk]
        dmax = K // (xs * ys)
        x2, y2 = xs * xs, ys * ys
        x3, y3 = x2 * xs, y2 * ys
        # case v = d(x^3-y^3)/(2(x+y)): d multiple of M/gcd(M,t), bounded by
        # |v|<=X, |u|<=X, |w|<=X (all linear in d)
        M = 2 * (xs + ys)
        t = x3 - y3
        m0 = M // np.gcd(M, t)
        XM = X * M
        D = dmax.copy()
        c1 = np.abs(t)
        np.minimum(D, np.where(c1 > 0, XM // np.maximum(c1, 1), D), out=D)
        np.minimum(D, XM // (x3 + 2 * x2 * ys + y3), out=D)  # |u| bound
        np.minimum(D, XM // (x3 + 2 * xs * y2 + y3), out=D)  # |w| bound
        res += int((D // m0).sum())
        # case v = d(x^3+y^3)/(2(x-y)), x != y
        nz = xs != ys
        x_, y_ = xs[nz], ys[nz]
        x2_, y2_, x3_, y3_ = x2[nz], y2[nz], x3[nz], y3[nz]
        M2 = 2 * np.abs(x_ - y_)
        t2 = x3_ + y3_
        m0 = M2 // np.gcd(M2, t2)
        XM2 = X * M2
        D = dmax[nz].copy()
        np.minimum(D, XM2 // t2, out=D)
        c2 = np.abs(x3_ - 2 * x2_ * y_ - y3_)
        np.minimum(D, np.where(c2 > 0, XM2 // np.maximum(c2, 1), D), out=D)
        c3 = np.abs(x3_ + 2 * x_ * y2_ - y3_)
        np.minimum(D, np.where(c3 > 0, XM2 // np.maximum(c3, 1), D), out=D)
        res += int((D // m0).sum())
        x0 = x1
    return res


def F(K, X):
    return n1_count(K, X) - n2_count(K, X)


def solve():
    assert F(1, 10) == 41 and F(10, 100) == 12492  # statement test values
    return F(10 ** 6, 10 ** 9)


if __name__ == "__main__":
    print(solve())
