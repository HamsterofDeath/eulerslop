"""Project Euler 425: sum of primes <= 10^7 that are not 2's relatives.

Two primes are connected if they have the same length and differ in one digit,
or one equals the other with one extra digit prepended. P is a 2's relative iff
there is a chain from 2 to P using only primes <= P, i.e. iff P is in the same
connected component as 2 in the graph restricted to primes <= P. Process primes
in increasing order with union-find: when adding p, union it with all smaller
prime neighbours, then test whether p's component contains 2.
"""
import numpy as np


def solve(N=10**7):
    sieve = np.ones(N, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    primes = np.flatnonzero(sieve).astype(np.int64)
    M = primes.size

    # Build all edges (p, q) with q < p, stored once from the larger endpoint p.
    ep_list, eq_list = [], []
    L = 1
    while 10 ** (L - 1) < N:
        lo, hi = 10 ** (L - 1), min(10 ** L, N)
        grp = primes[np.searchsorted(primes, lo):np.searchsorted(primes, hi)]
        if grp.size:
            # same length, one digit changed (keep same length => cand >= lo)
            for pos in range(L):
                dp = 10 ** pos
                digit = (grp // dp) % 10
                base = grp - digit * dp
                for nd in range(10):
                    cand = base + nd * dp
                    mask = (cand < grp) & (cand >= lo)
                    c = cand[mask]
                    pr = sieve[c]
                    ep_list.append(grp[mask][pr])
                    eq_list.append(c[pr])
            # strip the leading digit (inverse of "prepend a digit"); result
            # must have exactly L-1 digits
            if L >= 2:
                r = grp % (10 ** (L - 1))
                mask = r >= 10 ** (L - 2)
                c = r[mask]
                pr = sieve[c]
                ep_list.append(grp[mask][pr])
                eq_list.append(c[pr])
        L += 1

    ep = np.concatenate(ep_list)
    eq = np.concatenate(eq_list)
    pi = np.searchsorted(primes, ep)
    qi = np.searchsorted(primes, eq)
    order = np.argsort(pi, kind="stable")
    epi = pi[order].tolist()
    eqi = qi[order].tolist()
    plist = primes.tolist()

    parent = list(range(M))
    size = [1] * M

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    ptr = 0
    E = len(epi)
    for i in range(M):
        while ptr < E and epi[ptr] == i:
            a = find(i)
            b = find(eqi[ptr])
            if a != b:
                if size[a] < size[b]:
                    a, b = b, a
                parent[b] = a
                size[a] += size[b]
            ptr += 1
        if find(i) != find(0):  # index 0 is the prime 2
            total += plist[i]
    return total


if __name__ == "__main__":
    print(solve())
