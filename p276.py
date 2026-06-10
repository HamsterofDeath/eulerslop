#!/usr/bin/env python3
import numpy as np

def solve():
    # Alcuin's sequence: the number of integer triangles (a <= b <= c) with
    # perimeter n is T(n) = round(n^2/48) for even n, round((n+3)^2/48) for
    # odd n. Let F(m) = sum_{n<=m} T(n) count ALL triangles with perimeter
    # <= m. Triangles with gcd(a,b,c) = d are in bijection with arbitrary
    # triangles of perimeter <= N/d, so by Mobius inversion the number of
    # primitive triangles is
    #     P(N) = sum_{d=1..N} mu(d) * F(floor(N/d)).
    N = 10 ** 7

    # Mobius function sieve (numpy).
    mu = np.ones(N + 1, dtype=np.int8)
    is_comp = np.zeros(N + 1, dtype=bool)
    for p in range(2, N + 1):
        if not is_comp[p]:
            mu[p::p] *= -1
            sq = p * p
            if sq <= N:
                is_comp[sq::p] = True
                mu[sq::sq] = 0
    mertens = np.cumsum(mu, dtype=np.int64)

    # F as a prefix sum of Alcuin's sequence; round(x/48) = floor((x+24)/48).
    n = np.arange(N + 1, dtype=np.int64)
    t = np.where(n % 2 == 0, (n * n + 24) // 48, ((n + 3) ** 2 + 24) // 48)
    t[:3] = 0  # no triangle has perimeter < 3
    F = np.cumsum(t)

    # Sum mu(d) * F(N//d) by grouping equal quotients (exact Python ints,
    # since F(N) ~ 7e18 sits close to the int64 limit).
    ans = 0
    d = 1
    while d <= N:
        q = N // d
        d2 = N // q
        ans += (int(mertens[d2]) - int(mertens[d - 1])) * int(F[q])
        d = d2 + 1
    return ans

if __name__ == "__main__":
    print(solve())
