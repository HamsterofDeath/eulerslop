#!/usr/bin/env python3
"""Project Euler Problem 245: Coresilience.

For composite n, C(n) = (n - phi(n)) / (n - 1).  Sum all composite
n <= 2*10^11 for which C(n) is a unit fraction 1/k, i.e.
(n - phi(n)) divides (n - 1).

Structure of solutions:
  * n must be odd: for even n, n - phi(n) >= n/2 > (n-1)/2, forcing k = 1,
    i.e. phi(n) = 1, impossible for composite n.
  * n must be squarefree: if p^2 | n then p | n and p | phi(n), so
    p | n - phi(n) | n - 1, contradicting p | n.
  * n = p*q (p < q odd primes): n - phi(n) = p + q - 1 =: s and
    p*q - 1 = p*s - (p^2 - p + 1), so the condition is s | p^2 - p + 1.
    For each prime p <= sqrt(limit), factor p^2 - p + 1 (batch sieving by
    small primes with roots of x^2 - x + 1, then Miller-Rabin/Pollard rho)
    and test every divisor s in range; q = s - p + 1.
  * n = a*q with a a known product of >= 2 primes and q the largest prime:
    with b = a - phi(a), c = phi(a), the condition (n-1) = k*(n - phi(n))
    rearranges to q = (1 + k*c) / (a - k*b).  q(k) is strictly increasing,
    so q > max_prime(a) and q <= limit/a bound k to a small window which is
    scanned (vectorised with numpy over the second-largest prime and k).
"""

import random
from math import gcd, isqrt

import numpy as np

LIMIT = 2 * 10**11
_TRIAL_BOUND = 40000

# Set by _solve(); used for fast primality of small candidates.
_FLAGS = None
_FLAG_MAX = -1

_MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def _sieve(limit):
    """Return (bytearray of primality flags, numpy int64 array of primes)."""
    fl = bytearray([1]) * (limit + 1)
    fl[0:2] = b"\x00\x00"
    for i in range(2, isqrt(limit) + 1):
        if fl[i]:
            fl[i * i :: i] = bytearray(len(range(i * i, limit + 1, i)))
    primes = np.flatnonzero(np.frombuffer(bytes(fl), dtype=np.uint8)).astype(np.int64)
    return fl, primes


def _is_prime(n):
    if n <= _FLAG_MAX:
        return _FLAGS[n] == 1
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _MR_BASES:  # deterministic for n < 3.3e24
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _pollard(n):
    """Return a nontrivial factor of composite odd n (Brent's rho)."""
    rng = random.Random(0xE245)
    while True:
        y = rng.randrange(1, n)
        c = rng.randrange(1, n)
        m = 128
        g = r = q = 1
        x = ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r <<= 1
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
        if g != n:
            return g


def _sqrt_mod(a, p):
    """Square root of quadratic residue a modulo odd prime p (Tonelli-Shanks)."""
    a %= p
    if a == 0:
        return 0
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    if p % 8 == 5:
        x = pow(a, (p + 3) // 8, p)
        if x * x % p != a:
            x = x * pow(2, (p - 1) // 4, p) % p
        return x
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        t2, i = t, 0
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c = i, b * b % p
        t = t * c % p
        r = r * b % p
    return r


def _two_prime_solutions(limit, primes_list):
    """All n = p*q <= limit (p < q odd primes) with (n - phi(n)) | (n - 1)."""
    sq = isqrt(limit)
    fac = [None] * (sq + 1)
    fv = [0] * (sq + 1)
    plist = []
    for p in primes_list:
        if p < 3:
            continue
        if p * (p + 2) > limit:
            break
        fac[p] = []
        fv[p] = p * p - p + 1
        plist.append(p)
    if not plist:
        return []
    pmax = plist[-1]

    # Batch-remove small prime factors ell of F(p) = p^2 - p + 1.  Only
    # ell = 3 and ell == 1 (mod 3) can divide F; the roots of
    # x^2 - x + 1 = 0 (mod ell) are (1 +- sqrt(-3))/2.
    tb = min(_TRIAL_BOUND, sq)
    for ell in primes_list:
        if ell > tb:
            break
        if ell == 3:
            roots = (2,)
        elif ell % 3 == 1:
            t = _sqrt_mod(ell - 3, ell)
            inv2 = (ell + 1) // 2
            roots = ((1 + t) * inv2 % ell, (1 - t) * inv2 % ell)
        else:
            continue
        for r in roots:
            start = r
            while start < 3:
                start += ell
            for p in range(start, pmax + 1, ell):
                lst = fac[p]
                if lst is not None:
                    v = fv[p]
                    while v % ell == 0:
                        v //= ell
                        lst.append(ell)
                    fv[p] = v

    results = []
    bb = tb * tb
    for p in plist:
        lst = fac[p]
        v = fv[p]
        if v > 1:
            # All factors <= tb are stripped, and F < tb^3, so v is prime
            # or a product of exactly two primes.
            if v < bb or _is_prime(v):
                lst.append(v)
            else:
                d = _pollard(v)
                lst.append(d)
                lst.append(v // d)
        lst.sort()
        divs = [1]
        i = 0
        while i < len(lst):
            j = i
            while j < len(lst) and lst[j] == lst[i]:
                j += 1
            w = lst[i]
            pw, powers = 1, []
            for _ in range(j - i):
                pw *= w
                powers.append(pw)
            divs += [d * pe for d in divs for pe in powers]
            i = j
        lo = 2 * p - 1  # ensures q > p
        hi = p + limit // p - 1  # ensures p*q <= limit
        for s in divs:
            if lo < s <= hi:
                q = s - p + 1
                if _is_prime(q):
                    results.append(p * q)
    return results


def _icbrt(x):
    r = int(round(x ** (1.0 / 3.0)))
    while r * r * r > x:
        r -= 1
    while (r + 1) ** 3 <= x:
        r += 1
    return r


def _multi_prime_solutions(limit, primes_np):
    """All n <= limit with >= 3 distinct odd prime factors satisfying the
    divisibility condition."""
    results = []
    plist = primes_np.tolist()
    nprimes = len(plist)

    def leaf(a0, c0, pl):
        # Base a0 (product of >= 2 primes, largest pl, phi = c0); vectorise
        # over the next prime r and the quotient k to find the last prime q.
        hi = isqrt(limit // a0)
        if hi <= pl:
            return
        i0 = np.searchsorted(primes_np, pl, side="right")
        i1 = np.searchsorted(primes_np, hi, side="right")
        if i1 <= i0:
            return
        rs = primes_np[i0:i1]
        a = a0 * rs
        c = c0 * (rs - 1)
        b = a - c
        qm = limit // a
        k_hi = np.minimum((a - 1) // b, (qm * a - 1) // (c + qm * b))
        k_lo = (a * rs - 1) // (c + rs * b) + 1
        cnt = np.maximum(k_hi - k_lo + 1, 0)
        tot = int(cnt.sum())
        if tot == 0:
            return
        idx = np.repeat(np.arange(cnt.size), cnt)
        off = np.cumsum(cnt) - cnt
        k = np.arange(tot, dtype=np.int64) - off[idx] + k_lo[idx]
        av = a[idx]
        den = av - k * b[idx]
        num = 1 + k * c[idx]
        for j in np.flatnonzero(num % den == 0):
            jj = int(j)
            q = int(num[jj]) // int(den[jj])
            # k-window already enforces rs[idx] < q <= limit // a.
            if _is_prime(q):
                results.append(int(av[jj]) * q)

    def grow(a0, c0, pl, ip):
        leaf(a0, c0, pl)
        rmax = _icbrt(limit // a0)  # room needed for two more primes > r
        i = ip + 1
        while i < nprimes:
            r = plist[i]
            if r > rmax:
                break
            grow(a0 * r, c0 * (r - 1), r, i)
            i += 1

    for ip, p1 in enumerate(plist):
        if p1 < 3:
            continue
        if p1 * p1 * p1 > limit:
            break
        grow(p1, p1 - 1, p1, ip)
    return results


def _solve(limit):
    global _FLAGS, _FLAG_MAX
    sq = isqrt(limit)
    _FLAGS, primes_np = _sieve(sq)
    _FLAG_MAX = sq
    primes_list = primes_np.tolist()
    sols = _two_prime_solutions(limit, primes_list)
    sols += _multi_prime_solutions(limit, primes_np)
    return sum(sols)


def solve():
    return _solve(LIMIT)


if __name__ == "__main__":
    print(solve())
