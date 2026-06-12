#!/usr/bin/env python3
from bisect import bisect_left, bisect_right
from math import gcd, isqrt

# n is Achilles iff n is powerful (all prime exponents >= 2) and not a perfect
# power (gcd of exponents == 1).  We count n < 10^18 with both n and phi(n)
# Achilles.
#
# Key structure: write n = prod p^e_p and phi(n) = prod p^(e_p-1) * prod (p-1).
# A prime r can only receive contributions to phi from r^(e_r-1) and from
# factors q-1 of primes q > r dividing n.  In particular the LARGEST prime P
# of n gets phi-exponent exactly e_P - 1, which must be >= 2, so e_P >= 3 and
# P <= 10^6.  We DFS over Achilles candidates adding primes in DECREASING
# order; when prime p with exponent e is added, its final phi-exponent is
# already determined: ext_p (from q-1 of previously added, larger primes)
# plus e-1, and must be >= 2, i.e. e >= max(2, 3 - ext_p).
#
# We also track "deficient" primes: primes r not (yet) in n whose current
# phi-exponent is exactly 1.  Such r can only be repaired by later adding a
# prime q >= r (q == r itself, or r | q-1 needing q > r).  Since primes are
# added in decreasing order, every later prime must be >= max(deficient),
# which prunes the search drastically.  A node counts iff no deficient prime
# remains, gcd of n's exponents is 1, and gcd of phi's exponents is 1.

def solve(limit=10 ** 18):
    pmax = int(round(limit ** (1 / 3)))
    while (pmax + 1) ** 3 <= limit:
        pmax += 1
    while pmax ** 3 > limit:
        pmax -= 1

    # sieve of smallest prime factors up to pmax
    spf = list(range(pmax + 1))
    for i in range(2, isqrt(pmax) + 1):
        if spf[i] == i:
            for j in range(i * i, pmax + 1, i):
                if spf[j] == j:
                    spf[j] = i
    primes = [i for i in range(2, pmax + 1) if spf[i] == i]

    def factorize(m):
        fs = []
        while m > 1:
            p = spf[m]
            v = 0
            while m % p == 0:
                m //= p
                v += 1
            fs.append((p, v))
        return fs

    # factorization of p-1 for every prime p
    fact_pm1 = {p: factorize(p - 1) for p in primes}

    phi = {}          # prime -> exponent in phi(n) so far
    in_n = set()      # primes dividing n
    deficient = set() # primes r not in n with phi-exponent exactly 1
    count = 0

    def upd(r, delta):
        old = phi.get(r, 0)
        new = old + delta
        if new:
            phi[r] = new
        else:
            del phi[r]
        if r not in in_n:
            if new == 1:
                deficient.add(r)
            elif old == 1:
                deficient.discard(r)

    def rec(n, bound, g):
        # current n is a candidate (g = gcd of its exponents; g == 0 at root)
        nonlocal count
        if g == 1 and not deficient:
            gg = 0
            for v in phi.values():
                gg = gcd(gg, v)
                if gg == 1:
                    break
            if gg == 1:
                count += 1
        # extend with a prime smaller than all primes used so far
        rest = limit // n
        j_hi = min(bound, bisect_right(primes, isqrt(rest)))
        j_lo = bisect_left(primes, max(deficient)) if deficient else 0
        for j in range(j_lo, j_hi):
            q = primes[j]
            ext = phi.get(q, 0)
            e_min = 2 if ext else 3   # need ext + e - 1 >= 2
            nq = n * q ** e_min
            if nq > limit:
                continue
            # apply the (q-1) part and q's membership once for all exponents
            in_n.add(q)
            deficient.discard(q)
            for r, v in fact_pm1[q]:
                upd(r, v)
            e = e_min
            base_ext = ext
            while nq <= limit:
                phi[q] = base_ext + e - 1
                rec(nq, j, gcd(g, e))
                nq *= q
                e += 1
            # undo
            if base_ext:
                phi[q] = base_ext
            else:
                del phi[q]
            for r, v in fact_pm1[q]:
                upd(r, -v)
            in_n.discard(q)
            if phi.get(q, 0) == 1:
                deficient.add(q)

    rec(1, len(primes), 0)
    return count

if __name__ == "__main__":
    print(solve())
