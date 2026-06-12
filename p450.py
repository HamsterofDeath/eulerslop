#!/usr/bin/env python3
import numpy as np
from math import gcd, isqrt

# Math: with g = gcd(R, r), p = (R-r)/g, q = r/g (coprime, p > q since 2r < R),
# a point of the hypocycloid is x+iy = (R-r) e^{it} + r e^{-i(p/q)t}.  If
# sin t, cos t are rational and x, y are integers, then e^{it} and e^{i(p/q)t}
# are rational points of the unit circle, hence so is zeta = e^{it/q}
# (gcd(p,q)=1).  Conversely every rational zeta on the unit circle yields a
# candidate point P = g*p*zeta^q + g*q*conj(zeta)^p, and C(R,r) is exactly the
# set of those P that are Gaussian integers.
#
# Every rational point of the unit circle is zeta = i^k * w^2 / N(w) with w a
# primitive Gaussian integer of odd norm (k = 0..3).  Since gcd(w, conj(w))=1,
# P is a Gaussian integer iff w^p | g*q and w^q | g*p, i.e. for every prime
# power l^e || N(w):  e*p <= v_l(g)+v_l(q)  and  e*q <= v_l(g)+v_l(p).
# (Only primes l = 1 mod 4 can divide N(w); the condition forces l | g and in
# fact l^2 | g*..., so nontrivial denominators need l^2 <= g <= N/3.)
#
# w = 1 gives the four "trivial" points (zeta = 1, i, -1, -i), present for all
# (R, r); their |x|+|y| sum has a closed form depending only on the parities of
# p, q and (p-q) mod 4, which reduces to v2/odd-part-mod-4 data of a = r and
# b = R-r without needing the gcd.  That trivial part is summed with numpy in
# O(N).  Pairs admitting nontrivial denominators are rare; they are generated
# by looping over (l, e, p, q) and multiples of l^max(ep-v_l(q), eq-v_l(p)),
# then each such pair gets its full point set enumerated exactly (with dedup).

def _trivial_S(R, r):
    # Sum of |x|+|y| over the 4 points from zeta in {1,-1,i,-i}.
    g = gcd(R, r)
    p = (R - r) // g
    q = r // g
    if p & 1 and q & 1:
        return 4 * R - 4 * r if (p - q) % 4 == 0 else 4 * R
    return 4 * R - 2 * r


def _trivial_total(N):
    # Sum of _trivial_S(R, r) over all 3 <= R <= N, 1 <= r, 2r < R.
    if N < 3:
        return 0
    R = np.arange(3, N + 1, dtype=np.int64)
    part1 = int(np.sum(4 * R * ((R - 1) // 2)))
    # U = sum over pairs of r * c, with c determined by a = r, b = R - r:
    # c = 1 if v2(a) != v2(b); c = 2 if v2 equal and odd parts agree mod 4;
    # c = 0 otherwise (then S_trivial = 4R).
    amax = (N - 1) // 2
    a = np.arange(1, amax + 1, dtype=np.int64)
    v = np.log2(a & -a).astype(np.int64)        # v2(a), exact (powers of 2)
    odd = a >> v
    m = odd & 3
    tX = (N - a) >> v
    same_v = (tX - (tX >> 1)) - (odd - (odd >> 1))   # b in (a, N-a], v2(b)=v
    count1 = (N - 2 * a) - same_v
    FX = np.where(tX >= m, (tX - m) // 4 + 1, 0)
    Fa = (odd - m) // 4 + 1
    count2 = FX - Fa                                  # same v2 and odd mod 4
    U = int(np.sum(a * (count1 + 2 * count2)))
    return part1 - 2 * U


def _vl(n, l):
    v = 0
    while n % l == 0:
        n //= l
        v += 1
    return v


def _gen_special(N):
    # All (R, r) pairs that admit some denominator D > 1.
    pairs = set()
    lim = isqrt(N // 3) + 1
    sieve = bytearray([1]) * (lim + 1)
    primes4 = []
    for i in range(2, lim + 1):
        if sieve[i]:
            for j in range(i * i, lim + 1, i):
                sieve[j] = 0
            if i % 4 == 1:
                primes4.append(i)
    for l in primes4:
        if 3 * l * l > N:
            break
        e = 1
        while l ** (2 * e) * 3 <= N:
            p = 2
            while True:
                hit = False
                for q in range(1, p):
                    if gcd(p, q) != 1:
                        continue
                    mreq = max(e * p - _vl(q, l), e * q - _vl(p, l), 1)
                    s = p + q
                    base = l ** mreq
                    if base * s > N:
                        continue
                    hit = True
                    for j in range(1, N // (base * s) + 1):
                        g = base * j
                        pairs.add((g * s, g * q))
                # lower bound on m for any q < p+1 only grows with p
                lb = max(e * (p + 1) - _vl_cap(p + 1, l), 1)
                if not hit and l ** lb * (p + 2) > N:
                    break
                p += 1
            e += 1
    return pairs


def _vl_cap(p, l):
    # max possible v_l(q) for q < p
    v = 0
    x = l
    while x < p:
        v += 1
        x *= l
    return v


def _gmul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def _gpow(z, n):
    r = (1, 0)
    while n:
        if n & 1:
            r = _gmul(r, z)
        z = _gmul(z, z)
        n >>= 1
    return r


_ROT = (
    lambda x, y: (x, y),
    lambda x, y: (-y, x),
    lambda x, y: (-x, -y),
    lambda x, y: (y, -x),
)


def _full_S(R, r, spf, gprime):
    # Exact S(R, r): enumerate every valid zeta, dedupe points, sum |x|+|y|.
    g = gcd(R, r)
    p = (R - r) // g
    q = r // g
    # factor g, keep primes 1 mod 4 with a valid exponent
    cands = []
    x = g
    while x > 1:
        l = spf[x]
        beta = 0
        while x % l == 0:
            x //= l
            beta += 1
        if l % 4 == 1:
            emax = min((beta + _vl(q, l)) // p, (beta + _vl(p, l)) // q)
            if emax >= 1:
                cands.append((l, emax, gprime[l]))
    ws = [(1, 0)]
    for l, emax, pi in cands:
        cpi = (pi[0], -pi[1])
        new = []
        for w in ws:
            new.append(w)
            f1, f2 = pi, cpi
            for _ in range(emax):
                new.append(_gmul(w, f1))
                new.append(_gmul(w, f2))
                f1 = _gmul(f1, pi)
                f2 = _gmul(f2, cpi)
        ws = new
    gp, gq = g * p, g * q
    pts = set()
    for w in ws:
        D = w[0] * w[0] + w[1] * w[1]
        w2q = _gpow(w, 2 * q)
        cw2p = _gpow((w[0], -w[1]), 2 * p)
        Dpq = D ** (p - q)
        Dp = D ** p
        t1 = (gp * Dpq * w2q[0], gp * Dpq * w2q[1])
        t2 = (gq * cw2p[0], gq * cw2p[1])
        for k in range(4):
            a1 = _ROT[(k * q) & 3](*t1)
            a2 = _ROT[(-k * p) & 3](*t2)
            nx, ny = a1[0] + a2[0], a1[1] + a2[1]
            assert nx % Dp == 0 and ny % Dp == 0
            pts.add((nx // Dp, ny // Dp))
    return sum(abs(px) + abs(py) for px, py in pts)


def T(N):
    total = _trivial_total(N)
    specials = _gen_special(N)
    if specials:
        lim = max(gcd(R, r) for R, r in specials)
        spf = np.zeros(lim + 1, dtype=np.int32)
        for i in range(2, lim + 1):
            if spf[i] == 0:
                spf[i:lim + 1:i] = np.where(
                    spf[i:lim + 1:i] == 0, i, spf[i:lim + 1:i])
        spf = spf.tolist()
        gprime = {}
        for l in range(5, isqrt(lim) + 2):
            if l % 4 == 1 and all(l % d for d in range(2, isqrt(l) + 1)):
                for aa in range(1, isqrt(l) + 1):
                    bb = isqrt(l - aa * aa)
                    if aa * aa + bb * bb == l:
                        gprime[l] = (aa, bb)
                        break
        for R, r in specials:
            total += _full_S(R, r, spf, gprime) - _trivial_S(R, r)
    return total


def solve():
    return T(10 ** 6)


if __name__ == "__main__":
    print(solve())
