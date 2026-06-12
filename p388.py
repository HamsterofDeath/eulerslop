#!/usr/bin/env python3
import numpy as np

def make_solver(N):
    # Each line through the origin hits exactly one primitive lattice point
    # (gcd(a,b,c) = 1), so D(N) counts points of [0,N]^3 \ {O} with gcd 1.
    # Mobius inversion over the common divisor d gives
    #   D(N) = sum_{d>=1} mu(d) * ((floor(N/d)+1)^3 - 1).
    # Group equal quotients q = N//d; each block needs Mertens M at its ends.

    L = max(1000, int(round(N ** (2 / 3))) * 2)  # sieve limit ~ 2*N^(2/3)

    # mu via numpy: flip sign once per prime factor, zero out squarefuls
    mu = np.ones(L + 1, dtype=np.int8)
    mu[0] = 0
    is_p = np.ones(L + 1, dtype=bool)
    is_p[:2] = False
    for p in range(2, int(L ** 0.5) + 1):
        if is_p[p]:
            is_p[p * p::p] = False
            mu[p::p] *= -1
            mu[p * p::p * p] = 0
    for p in np.nonzero(is_p[int(L ** 0.5) + 1:])[0] + int(L ** 0.5) + 1:
        mu[p::p] *= -1
    mert = np.cumsum(mu, dtype=np.int64)  # M(x) for x <= L

    # M(x) for large x via M(x) = 1 - sum_{d=2..x} M(x//d), blocked.
    # Only arguments of the form N//k occur; build bottom-up to avoid recursion.
    cache = {}

    def M(x):
        if x <= L:
            return int(mert[x])
        if x in cache:
            return cache[x]
        res = 1
        d = 2
        while d <= x:
            q = x // d
            d2 = x // q
            res -= (d2 - d + 1) * M(q)
            d = d2 + 1
        cache[x] = res
        return res

    for k in range(N // L, 0, -1):  # increasing arguments N//k
        M(N // k)
    return M


def D(N):
    M = make_solver(N)
    total = 0
    d = 1
    m_prev = 0  # M(d-1)
    while d <= N:
        q = N // d
        d2 = N // q
        m_cur = M(d2)
        total += (m_cur - m_prev) * ((q + 1) ** 3 - 1)
        m_prev = m_cur
        d = d2 + 1
    return total


def solve():
    assert D(10 ** 6) == 831909254469114121
    s = str(D(10 ** 10))
    return s[:9] + s[-9:]  # first nine digits followed by the last nine

if __name__ == "__main__":
    print(solve())
