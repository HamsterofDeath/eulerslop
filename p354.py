#!/usr/bin/env python3
import numpy as np
from math import isqrt

def solve():
    # Hexagon cells of side 1: the centres form a triangular lattice with
    # nearest-neighbour distance sqrt(3), so the squared centre distances are
    # L^2 = 3*(x^2 + xy + y^2), i.e. n = L^2/3 is an Eisenstein norm.
    # Classically the number of lattice points of norm n is
    #   B(L) = 6 * prod_{p | n, p == 1 (mod 3)} (e_p + 1)
    # provided every prime q == 2 (mod 3) divides n to an even power
    # (otherwise B = 0); the power of 3 in n is irrelevant.
    # B(L) = 450  <=>  prod (e_p + 1) = 75.  Factoring 75 into parts >= 2
    # gives the exponent multisets below for distinct primes == 1 (mod 3);
    # the rest of n is a free cofactor k = 3^a * t^2 with every prime factor
    # of t == 2 (mod 3).  Count n <= N = floor((5*10^11)^2 / 3) of this shape
    # (distinct n <-> distinct L = sqrt(3n)).
    N = (5 * 10 ** 11) ** 2 // 3
    patterns = [(74,), (24, 2), (14, 4), (4, 4, 2)]
    SMALL1 = [7, 13, 19]  # smallest primes == 1 (mod 3), for bounds

    def iroot(x, e):
        if x <= 0:
            return 0
        r = int(round(x ** (1.0 / e)))
        while r ** e > x:
            r -= 1
        while (r + 1) ** e <= x:
            r += 1
        return r

    # plimit: largest prime that can occur in any slot of any pattern;
    # minfull: smallest possible prime-power product of a full pattern.
    plimit, minfull = 10, N
    for exps in patterns:
        full = 1
        for e, p in zip(exps, SMALL1):
            full *= p ** e
        if full <= N:
            minfull = min(minfull, full)
        for j in range(len(exps)):
            others = 1
            it = iter(SMALL1)
            for i2, e2 in enumerate(exps):
                if i2 != j:
                    others *= next(it) ** e2
            if others <= N:
                plimit = max(plimit, iroot(N // others, exps[j]))
    M = isqrt(N // minfull)  # largest possible t in a cofactor t^2

    sieve = np.ones(plimit + 1, bool)
    sieve[:2] = False
    for i in range(2, isqrt(plimit) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    primes = np.flatnonzero(sieve).astype(np.int64)
    P1 = primes[primes % 3 == 1]
    P1list = P1.tolist()

    # Tcnt[y] = #{1 <= t <= y : every prime factor of t is == 2 (mod 3)}
    ok = np.ones(M + 1, bool)
    ok[0] = False
    ok[3::3] = False
    for p in primes[primes <= M]:
        p = int(p)
        if p % 3 == 1:
            ok[p::p] = False
    Tcnt = np.cumsum(ok)

    def C(X):  # number of cofactors k = 3^a * t^2 <= X
        s, pw = 0, 1
        while pw <= X:
            s += int(Tcnt[isqrt(X // pw)])
            pw *= 3
        return s

    def C_vec(Xs):  # same, summed over an int64 array of bounds
        s, pw = 0, 1
        Xmax = int(Xs.max()) if Xs.size else 0
        while pw <= Xmax:
            Z = Xs // pw
            y = np.sqrt(Z.astype(np.float64)).astype(np.int64)
            y += (y + 1) * (y + 1) <= Z  # fix float rounding
            y -= y * y > Z
            s += int(Tcnt[y].sum())
            pw *= 3
        return s

    def rec(exps, idx, used, prod, start):
        # assign a prime == 1 (mod 3) to exponent exps[idx]; primes on equal
        # exponents are forced increasing to count each multiset once
        e = exps[idx]
        lo = start if (idx > 0 and exps[idx - 1] == e) else 0
        if idx == len(exps) - 1:
            X1 = N // prod
            hi = int(np.searchsorted(P1, iroot(X1, e), side='right'))
            if hi <= lo:
                return 0
            if e == 2 and hi - lo > 200:  # bulk case: vectorise over r
                rs = P1[lo:hi]
                for u in used:
                    rs = rs[rs != u]
                return C_vec(X1 // (rs * rs))
            tot = 0
            for r in P1list[lo:hi]:
                if r not in used:
                    tot += C(N // (prod * r ** e))
            return tot
        rest = 1  # lower bound on the product contributed by deeper levels
        for e2, p2 in zip(exps[idx + 1:], SMALL1):
            rest *= p2 ** e2
        tot, i = 0, lo
        while i < len(P1list):
            p = P1list[i]
            np_ = prod * p ** e
            if np_ * rest > N:
                break
            if p not in used:
                nstart = i + 1 if exps[idx + 1] == e else 0
                tot += rec(exps, idx + 1, used + (p,), np_, nstart)
            i += 1
        return tot

    return sum(rec(exps, 0, (), 1, 0) for exps in patterns)

if __name__ == "__main__":
    print(solve())
