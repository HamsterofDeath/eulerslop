#!/usr/bin/env python3
import numpy as np
from math import isqrt

def icbrt(x):
    c = round(x ** (1.0 / 3.0))
    while c * c * c > x:
        c -= 1
    while (c + 1) ** 3 <= x:
        c += 1
    return c

def d3_sum(m):
    # D3(m) = #{(a,b,c) : a*b*c <= m} = sum_{k<=m} d_3(k), computed in
    # O(m^(2/3)) by splitting ordered triples by the shape of sorted (a,b,c):
    #   D3 = 6*#{a<b<c} + 3*#{a=b<c} + 3*#{a<b=c} + #{a=b=c}.
    if m <= 0:
        return 0
    A = icbrt(m)
    t4 = A                                            # a = b = c
    a = np.arange(1, A + 1, dtype=np.int64)
    t2 = int((m // (a * a) - a).sum())                # a = b < c
    b = np.arange(2, isqrt(m) + 1, dtype=np.int64)
    t3 = int(np.minimum(b - 1, m // (b * b)).sum())   # a < b = c
    # a < b < c: for each a, b runs to isqrt(m//a) and contributes
    # m//(a*b) - b choices of c; flatten the (a,b) pairs in chunks.
    q = m // a
    bs = np.sqrt(q.astype(np.float64)).astype(np.int64)
    bs += (bs + 1) ** 2 <= q
    bs -= bs * bs > q                                 # bs = isqrt(m//a)
    lens = np.maximum(bs - a, 0)
    cum = np.concatenate(([0], np.cumsum(lens)))
    t1 = 0
    CHUNK = 1 << 24
    i = 0
    while i < A:
        jj = int(np.searchsorted(cum, cum[i] + CHUNK))
        jj = min(max(jj - 1, i + 1), A)
        tot = int(cum[jj] - cum[i])
        if tot:
            ls = lens[i:jj]
            aa = np.repeat(a[i:jj], ls)
            bb = (np.arange(tot, dtype=np.int64)
                  - np.repeat(cum[i:jj] - cum[i], ls)
                  + np.repeat(a[i:jj] + 1, ls))
            t1 += int((m // (aa * bb)).sum()) - int(bb.sum())
        i = jj
    return 6 * t1 + 3 * t2 + 3 * t3 + t4

def solve():
    # g(n) counts pairs x<=y with lcm(x,y)<=n.  Ordered pairs with lcm = k
    # number d(k^2), so ordered pairs with lcm<=n total D2(n) = sum d(k^2)
    # and g(n) = (D2(n) + n) / 2 (the n diagonal pairs are self-paired).
    # d(k^2) = sum_{d|k} 2^omega(d) and 2^omega = mu^2 * 1, mu^2(a) =
    # sum_{t^2|a} mu(t), hence d(.^2) summed is a triple Dirichlet 1*1*1
    # twisted by squares:  D2(n) = sum_{t<=sqrt(n)} mu(t) * D3(n // t^2).
    n = 10 ** 12
    L = isqrt(n)

    # Mobius sieve up to L with cumulative sums (Mertens) for block sums.
    mu = np.ones(L + 1, dtype=np.int64)
    prime = np.ones(L + 1, dtype=bool)
    prime[:2] = False
    for p in range(2, isqrt(L) + 1):
        if prime[p]:
            prime[p * p::p] = False
    for p in np.flatnonzero(prime):
        p = int(p)
        mu[p::p] *= -1
        mu[p * p::p * p] = 0
    mert = np.concatenate(([0], np.cumsum(mu[1:])))  # mert[t] = sum mu(1..t)

    d2 = 0
    t = 1
    while t <= L:
        m = n // (t * t)
        t2 = min(isqrt(n // m), L)      # all t' in [t, t2] share n//t'^2 = m
        coef = int(mert[t2] - mert[t - 1])
        if coef:
            d2 += coef * d3_sum(m)
        t = t2 + 1
    return (d2 + n) // 2

if __name__ == "__main__":
    print(solve())
