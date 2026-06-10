#!/usr/bin/env python3
"""Project Euler 241: Perfection Quotients.

Find the sum of all n <= 10^18 with sigma(n)/n = k + 1/2 for a positive
integer k, i.e. 2*sigma(n) = (2k+1)*n.

Search idea: build n from coprime prime powers.  Keep track of the ratio
sigma(m)/m that the *remaining* (still to be chosen) coprime part m must
have ("need").  Since the denominator b of need = a/b (reduced) must divide
m, every prime factor of b is forced to appear in m.  So while b > 1 we
branch only over the exponent of the largest prime factor of b - a hugely
pruned, complete search.  If need is an integer > 1, m must be multiperfect
and we branch over every feasible smallest prime.  need == 1 means m = 1
and the current n is a solution.  A greedy abundancy upper bound
(prod q/(q-1) over the smallest unused primes whose product fits the
remaining budget) prunes infeasible states exactly.
"""

import random
import sys
from functools import lru_cache
from math import gcd

LIMIT = 10 ** 18


def sieve(n):
    flags = bytearray([1]) * (n + 1)
    flags[0] = flags[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if flags[i]:
            flags[i * i:: i] = bytearray(len(flags[i * i:: i]))
    return [i for i in range(n + 1) if flags[i]]


SMALL_PRIMES = sieve(1000)

_MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime(n):
    if n < 2:
        return False
    for p in _MR_BASES:
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in _MR_BASES:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_rho(n):
    if n % 2 == 0:
        return 2
    while True:
        x = random.randrange(2, n)
        y = x
        c = random.randrange(1, n)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d


@lru_cache(maxsize=None)
def largest_prime_factor(n):
    if n == 1:
        return 1
    if is_prime(n):
        return n
    for p in (2, 3, 5, 7, 11, 13):
        if n % p == 0:
            m = n
            while m % p == 0:
                m //= p
            return max(p, largest_prime_factor(m))
    d = pollard_rho(n)
    return max(largest_prime_factor(d), largest_prime_factor(n // d))


def feasible(a, b, cap, used, pmin=2):
    """Can any m <= cap, coprime to `used`, all prime factors >= pmin,
    reach sigma(m)/m >= a/b?  (Exact upper-bound test.)"""
    num = den = prod = 1
    if num * b >= a * den:
        return True
    for q in SMALL_PRIMES:
        if q < pmin or q in used:
            continue
        prod *= q
        if prod > cap:
            break
        num *= q
        den *= q - 1
        if num * b >= a * den:
            return True
    return num * b >= a * den


def solve():
    sys.setrecursionlimit(10000)
    solutions = set()

    def dfs(a, b, n, used):
        # need sigma(m)/m == a/b for some m <= LIMIT//n coprime to `used`
        if a == b:
            solutions.add(n)
            return
        if a < b:
            return
        if n * b > LIMIT:  # b must divide m
            return
        cap = LIMIT // n
        if not feasible(a, b, cap, used):
            return
        if b > 1:
            p = largest_prime_factor(b)
            if p in used:
                return
            emin = 0
            bb = b
            while bb % p == 0:
                bb //= p
                emin += 1
            pe = p ** emin
            nused = used | frozenset((p,))
            while n * pe <= LIMIT:
                s = (pe * p - 1) // (p - 1)  # sigma(p^e)
                na = a * pe
                nb = b * s
                g = gcd(na, nb)
                dfs(na // g, nb // g, n * pe, nused)
                pe *= p
        else:
            # need is an integer > 1: branch over a prime of m
            for p in SMALL_PRIMES:
                if p > cap:
                    break
                if p in used:
                    continue
                if not feasible(a, b, cap, used, pmin=p):
                    break
                nused = used | frozenset((p,))
                pe = p
                while n * pe <= LIMIT:
                    s = (pe * p - 1) // (p - 1)
                    na = a * pe
                    nb = s
                    g = gcd(na, nb)
                    dfs(na // g, nb // g, n * pe, nused)
                    pe *= p

    k = 1
    while True:
        a, b = 2 * k + 1, 2
        if not feasible(a, b, LIMIT, frozenset()):
            break
        dfs(a, b, 1, frozenset())
        k += 1

    return sum(solutions)


if __name__ == "__main__":
    print(solve())
