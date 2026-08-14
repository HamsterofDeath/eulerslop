#!/usr/bin/env python3
"""Project Euler Problem 1005: Median Prime List.

Every list is a strictly increasing sequence of primes summing to 2026,
ordered lexicographically.  With C lists, the median (after dropping the
last one when C is even) is the element of rank ceil(C/2).

The number of lists with a given prefix is a subset-sum count over the
primes larger than the last element, so the median is built element by
element: try the primes p above the current bound in increasing order,
count the lists continuing with p (f[p'][s-p] with p' the next prime
after p), and descend into the first block whose cumulative size contains
the remaining rank.  The answer is the product of the primes modulo
10^9.
"""


def _median_product(n, mod):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    primes = [i for i in range(2, n + 1) if sieve[i]]
    m = len(primes)

    # f[i][s]: number of subsets of primes[i:] summing to s
    f = [[0] * (n + 1) for _ in range(m + 1)]
    f[m][0] = 1
    for i in range(m - 1, -1, -1):
        p = primes[i]
        prev = f[i + 1]
        cur = f[i]
        for s in range(n + 1):
            cur[s] = prev[s] + (prev[s - p] if s >= p else 0)

    total = f[0][n]
    rank = (total + 1) // 2
    chosen = []
    bound = 1
    while n > 0:
        for i, p in enumerate(primes):
            if p <= bound or p > n:
                continue
            cnt = f[i + 1][n - p]
            if rank > cnt:
                rank -= cnt
            else:
                chosen.append(p)
                n -= p
                bound = p
                break
        else:
            raise RuntimeError("no candidate prime")
    product = 1
    for p in chosen:
        product = product * p % mod
    return product


def solve() -> int:
    return _median_product(2026, 1_000_000_000)


if __name__ == "__main__":
    print(solve())
