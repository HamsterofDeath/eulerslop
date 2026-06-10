#!/usr/bin/env python3
# Project Euler 263: An Engineers' Dream Come True
#
# We need n such that:
#   * n-9, n-3, n+3, n+9 are primes forming three consecutive "sexy" pairs,
#     i.e. they are consecutive primes (so n-7, n-5, n-1, n+1, n+5, n+7 are
#     composite; the even offsets n+-2, n+-4, n+-8 are handled too since
#     n is even).
#   * n-8, n-4, n, n+4, n+8 are all practical numbers.
#
# Practical numbers > 2 are even, and since 6 cannot divide two numbers that
# differ by 4, all five practical numbers force 4 | n.
#
# Search: segmented numpy sieve; the quadruple-prime pattern p, p+6, p+12,
# p+18 with composite p+2, p+4, p+8, p+10, p+14, p+16 (p = n-9) is found
# vectorised, then the rare candidates get exact practicality tests.
#
# Practicality test (Stewart/Sierpinski): n = p1^a1 * ... * pk^ak with
# p1 < ... < pk is practical iff p1 = 2 and each p_{i+1} <= sigma(prefix)+1.
# We factor with trial division but can abort as soon as the next prime
# exceeds the current sigma+1 bound.

import numpy as np


def _small_primes(limit):
    s = np.ones(limit + 1, dtype=bool)
    s[:2] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if s[p]:
            s[p * p:: p] = False
    return np.nonzero(s)[0].tolist()


def _is_practical(n, primes):
    if n == 1:
        return True
    if n % 2:
        return False
    sigma = 1
    rem = n
    for p in primes:
        if rem == 1:
            return True
        if p > sigma + 1:
            return False  # smallest remaining factor already too large
        if p * p > rem:
            break
        if rem % p == 0:
            pk = p
            while rem % pk == 0:
                pk *= p
            pk //= p
            rem //= pk
            sigma *= (pk * p - 1) // (p - 1)
    if rem > 1:  # rem is prime
        if rem > sigma + 1:
            return False
    return True


def solve():
    SEG = 10 ** 7
    sp = _small_primes(70000)  # > sqrt of any n we will ever reach
    found = []
    lo = 0
    while len(found) < 4:
        # primality over [lo, lo+SEG+18)
        size = SEG + 18
        isp = np.ones(size, dtype=bool)
        if lo == 0:
            isp[0] = isp[1] = False
        for p in sp:
            start = max(p * p, ((lo + p - 1) // p) * p)
            if start >= lo + size:
                continue
            isp[start - lo:: p] = False
        cand = (isp[0:SEG] & isp[6:SEG + 6] & isp[12:SEG + 12]
                & isp[18:SEG + 18])
        for off in (2, 4, 8, 10, 14, 16):
            cand &= ~isp[off:SEG + off]
        for i in np.nonzero(cand)[0]:
            p = lo + int(i)  # p = n - 9
            n = p + 9
            if n % 4:
                continue
            if all(_is_practical(n + d, sp) for d in (0, -4, 4, -8, 8)):
                found.append(n)
                if len(found) == 4:
                    break
        lo += SEG
        if lo > 4 * 10 ** 9:  # safety stop
            break
    return sum(found[:4])


if __name__ == "__main__":
    print(solve())
