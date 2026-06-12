#!/usr/bin/env python3
import numpy as np
from math import isqrt

def solve():
    # Steiner chain: invert about a limit point of the coaxal pencil of C_in
    # (diameter b) and C_out (diameter a+b+c); their inversive distance is
    #   delta = (R^2 + r^2 - d^2)/(2Rr) = 1 + 2ac/(b(a+b+c)),
    # and a closed chain of k non-overlapping circles exists iff
    # delta = (1+sin^2(pi/k))/(1-sin^2(pi/k)), i.e. ac/(b(a+b+c)) = tan^2(pi/k).
    # For rational a,b,c Niven's theorem allows only k = 3, 4, 6, i.e.
    #   ac = m*b*(a+b+c) with m in {3, 1, 1/3}.
    # Counting ordered (a,c) for fixed b:
    #   m=1:   (a-b)(c-b) = 2b^2        -> d(2 b^2) solutions
    #   m=3:   (a-3b)(c-3b) = 12b^2     -> d(12 b^2) solutions
    #   m=1/3: (3a-b)(3c-b) = 4b^2 with both factors = -b (mod 3)
    # (negative-factor branches are impossible by size).  With chi the
    # character mod 3 and g = 1*chi:  for 3 J b the m=1/3 count is
    # (d(4b^2) - chi(b) g(b^2))/2, and for b = 3^e m it is (2e-1) d(4m^2).
    # So with S2(x) = sum_{b<=x} d(b^2) (computed as sum mu(d) D3(x/d^2)),
    # everything reduces to S2 at points n/(2^i 3^j) plus one character sum
    # B(n) = sum chi(b) g(b^2) = sum_{3Jd} mu(d) sum_{3Jm} Dchi(n/(d^2 m)).
    n = 10 ** 9
    sq = isqrt(n)

    # Moebius sieve up to sqrt(n)
    mu = np.ones(sq + 1, dtype=np.int64)
    primes = []
    is_comp = bytearray(sq + 1)
    for i in range(2, sq + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > sq:
                break
            is_comp[i * p] = 1
            if i % p == 0:
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]

    # --- d3 (3-dim divisor function) prefix table up to L3, via sorted triples
    L3 = min(n, 6_000_000)
    d3 = np.zeros(L3 + 1, dtype=np.int32)
    a = 1
    while a * a * a <= L3:
        d3[a * a * a] += 1                          # a=b=c
        if a * a * (a + 1) <= L3:
            d3[a * a * (a + 1):: a * a] += 3        # a=b<c
        bmax = isqrt(L3 // a)
        if bmax > a:
            bs = np.arange(a + 1, bmax + 1)
            d3[a * bs * bs] += 3                    # a<b=c (distinct indices)
            for b in range(a + 1, bmax + 1):
                ab = a * b
                if ab * (b + 1) <= L3:
                    d3[ab * (b + 1):: ab] += 6      # a<b<c
        a += 1
    D3_small = np.cumsum(d3, dtype=np.int64)
    del d3

    d3_memo = {}

    def D3(x):
        # sum_{t<=x} d_3(t)
        if x <= L3:
            return int(D3_small[x])
        r = d3_memo.get(x)
        if r is not None:
            return r
        total = 0
        a = 1
        while a * a * a <= x:
            xa = x // a
            B = isqrt(xa)
            if B > a:
                bs = np.arange(a + 1, B + 1)
                total += 6 * int((xa // bs - bs).sum())   # a<b<c
                total += 3 * (B - a)                      # a<b=c
            cnt = x // (a * a) - a                        # a=b<c
            if cnt > 0:
                total += 3 * cnt
            total += 1                                    # a=b=c
            a += 1
        d3_memo[x] = total
        return total

    s2_memo = {}

    def S2(y):
        # sum_{b<=y} d(b^2) = sum_{d<=sqrt(y)} mu(d) D3(y // d^2)
        if y <= 0:
            return 0
        r = s2_memo.get(y)
        if r is not None:
            return r
        s = isqrt(y)
        ds = np.arange(1, s + 1)
        args = y // (ds * ds)
        big = args > L3
        total = 0
        for d in ds[big]:
            m = int(mu[d])
            if m:
                total += m * D3(y // (int(d) * int(d)))
        total += int((mu[1:s + 1][~big] * D3_small[args[~big]]).sum())
        s2_memo[y] = total
        return total

    # 2-adic / 3-adic Dirichlet correction coefficients (derived by inversion):
    # d(2 b^2):  2-part coeffs  2*(-1)^j           (and odd part d(m^2))
    # d(4 b^2):  2-part coeffs  3, -4, 4, -4, ...
    # d(12 b^2): both corrections combined
    # A-inversion (strip 3-part of d(4 b^2)): v = 1, -3, 4, -4, 4, ...
    def c2(i):
        return 3 if i == 0 else 4 * (-1 if i % 2 else 1)

    def v3(e):
        return 1 if e == 0 else (-3 if e == 1 else 4 * (-1 if e % 2 else 1))

    # Sum1 = sum_{b<=n} d(2 b^2)
    sum1 = 0
    j, p2 = 0, 1
    while p2 <= n:
        sum1 += 2 * (-1) ** j * S2(n // p2)
        j += 1
        p2 *= 2

    # Sum2 = sum_{b<=n} d(12 b^2)
    sum2 = 0
    i, p2 = 0, 1
    while p2 <= n:
        j, p3 = 0, 1
        while p2 * p3 <= n:
            sum2 += c2(i) * 2 * (-1) ** j * S2(n // (p2 * p3))
            j += 1
            p3 *= 3
        i += 1
        p2 *= 2

    u_memo = {}

    def U(x):
        # sum_{b<=x} d(4 b^2)
        r = u_memo.get(x)
        if r is None:
            r = 0
            i, p2 = 0, 1
            while p2 <= x:
                r += c2(i) * S2(x // p2)
                i += 1
                p2 *= 2
            u_memo[x] = r
        return r

    a_memo = {}

    def A(x):
        # sum_{b<=x, 3 J b} d(4 b^2)
        r = a_memo.get(x)
        if r is None:
            r = 0
            e, p3 = 0, 1
            while p3 <= x:
                r += v3(e) * U(x // p3)
                e += 1
                p3 *= 3
            a_memo[x] = r
        return r

    # --- Dchi(z) = sum_{t<=z} chi(t) d(t), chi the nontrivial character mod 3
    LC = min(n, 6_000_000)
    dt = np.zeros(LC + 1, dtype=np.int32)
    for i in range(1, isqrt(LC) + 1):
        dt[i * i:: i] += 2
        dt[i * i] -= 1
    w = dt.astype(np.int64)
    del dt
    w[0::3] = 0
    w[2::3] *= -1
    Dchi_small = np.cumsum(w)
    del w

    dchi_memo = {}

    def Dchi(z):
        if z <= LC:
            return int(Dchi_small[z])
        r = dchi_memo.get(z)
        if r is not None:
            return r
        # hyperbola: 2 * sum_{m<=sqrt(z)} chi(m) X(z//m) - X(sqrt(z))^2,
        # X(t) = sum_{i<=t} chi(i) = [t % 3 == 1]
        s = isqrt(z)
        ms = np.arange(1, s + 1)
        chi = np.zeros(s + 1, dtype=np.int64)
        chi[1::3] = 1
        chi[2::3] = -1
        x_vals = (z // ms) % 3 == 1
        r = 2 * int((chi[1:] * x_vals).sum()) - (1 if s % 3 == 1 else 0)
        dchi_memo[z] = r
        return r

    def F(y):
        # sum_{m<=y, 3 J m} Dchi(y // m)
        s = isqrt(y)
        total = 0
        # m <= s : direct values
        mcut = min(s, y // LC) if y > LC else 0
        for m in range(1, mcut + 1):
            if m % 3:
                total += Dchi(y // m)
        if s > mcut:
            ms = np.arange(mcut + 1, s + 1)
            vals = Dchi_small[y // ms]
            vals[ms % 3 == 0] = 0
            total += int(vals.sum())
        # m > s : group by v = y // m, v runs 1 .. y//(s+1)
        vtop = y // (s + 1)
        if vtop >= 1:
            vs = np.arange(1, vtop + 1)
            hi = y // vs
            lo = y // (vs + 1)
            cnt = (hi - hi // 3) - (lo - lo // 3)
            total += int((cnt * Dchi_small[vs]).sum())
        return total

    # B(n) = sum_{b<=n} chi(b) g(b^2)   (g = 1 * chi; vanishes for 3|b)
    B = 0
    for d in range(1, sq + 1):
        m = int(mu[d])
        if m and d % 3:
            B += m * F(n // (d * d))

    # assemble:  T(n) = sum d(2b^2) + sum d(12b^2)
    #            + (A(n) - B)/2                      (m=1/3, 3 J b)
    #            + sum_{e>=1} (2e-1) A(n // 3^e)     (m=1/3, 3^e || b)
    part3 = A(n) - B
    assert part3 % 2 == 0
    total = sum1 + sum2 + part3 // 2
    e, p3 = 1, 3
    while p3 <= n:
        total += (2 * e - 1) * A(n // p3)
        e += 1
        p3 *= 3
    return total

if __name__ == "__main__":
    print(solve())
