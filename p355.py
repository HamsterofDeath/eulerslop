#!/usr/bin/env python3
import math
from bisect import bisect_right
from collections import deque


def co(n):
    # primes up to n
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, math.isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i:: i] = bytearray(len(range(i * i, n + 1, i)))
    primes = [i for i in range(2, n + 1) if sieve[i]]
    r = math.isqrt(n)

    # Greedy baseline: 1 plus, for every prime p <= n, the largest power
    # p^a <= n.  Distinct prime powers are pairwise coprime, and in a
    # coprime set each prime occurs in at most one element, so this gives
    # every prime its best stand-alone element.
    hp = {}
    base = 1
    for p in primes:
        pk = p
        while pk * p <= n:
            pk *= p
        hp[p] = pk
        base += pk

    # Improvements merge several primes into one element.  An element <= n
    # contains at most one "large" prime (> sqrt(n)) since the product of
    # two exceeds n, and a prime p > n/2 cannot be merged at all (2p > n).
    # The useful merges are q^b * p <= n (small q <= sqrt(n), large
    # p in (sqrt(n), n/2], b maximal), replacing greedy q^a and p for a
    # gain of q^b*p - q^a - p.  Each prime joins at most one element, so
    # choosing the merges is a max-weight bipartite matching small <-> large.
    small = [p for p in primes if p <= r]
    L = len(small)

    # All positive-gain edges (q, p): in the band n/q^(b+1) < p <= n/q^b the
    # merged element is q^b * p and the gain p*(q^b - 1) - q^a is positive
    # iff p > q^a / (q^b - 1).
    pos = {}
    for q in small:
        qa = hp[q]
        lst = []
        qb = q
        while qb * (r + 1) <= n:
            hi = min(n // qb, n // 2)
            lo = max(r, n // (qb * q), qa // (qb - 1))
            if hi > lo:
                i1 = bisect_right(primes, lo)
                i2 = bisect_right(primes, hi)
                for p in primes[i1:i2]:
                    lst.append((p * qb - qa - p, p))
            qb *= q
        lst.sort(reverse=True)
        pos[q] = lst

    # Rule out elements x whose support holds k >= 2 small primes.  In an
    # optimal set the other small primes occupy <= L-k large primes, so
    # swapping x out and assigning its k primes free large partners one at
    # a time always finds, among each q's top-L partners, one still free
    # (<= L-1 occupied at every step).  Each q with >= L positive edges
    # then recovers at least its L-th best gain G_L(q) (with fewer edges
    # the fallback is plain q^a: gain 0).  So if every such x satisfies
    # gain(x) <= sum_{q in x} G_L(q), no optimal set needs a multi-small
    # element and the bipartite matching below is provably optimal.
    # Enumerate every candidate x: each smooth m <= n (all prime factors
    # small) with >= 2 distinct primes, either alone (gain m - sum q^a) or
    # times the largest large prime p* <= n/m (gain p*(m-1) - sum q^a);
    # an element never holds two large primes (product > n).
    GL = {q: (pos[q][L - 1][0] if len(pos[q]) >= L else 0) for q in small}
    spf = list(range(n + 1))
    for p in small:
        for j in range(p * p, n + 1, p):
            if spf[j] == j:
                spf[j] = p
    sumhp = [0] * (n + 1)
    cnt = [0] * (n + 1)
    glsum = [0] * (n + 1)
    smooth = bytearray(n + 1)
    smooth[1] = 1
    for m in range(2, n + 1):
        p = spf[m]
        if p > r:
            continue
        rest = m // p
        while rest % p == 0:
            rest //= p
        if not smooth[rest]:
            continue
        smooth[m] = 1
        cnt[m] = cnt[rest] + 1
        sumhp[m] = sumhp[rest] + hp[p]
        glsum[m] = glsum[rest] + GL[p]
        if cnt[m] >= 2:
            assert m - sumhp[m] <= glsum[m], "merged element not dominated"
            if m * (r + 1) <= n:
                ps = primes[bisect_right(primes, n // m) - 1]
                if ps > r:
                    assert ps * (m - 1) - sumhp[m] <= glsum[m], \
                        "merged element not dominated"

    # Keeping only each small prime's top-L edges preserves an optimal
    # matching (at most L-1 of a node's better partners can be taken).
    qs = [q for q in small if pos[q]]
    kept = {}
    edges = []
    for q in qs:
        for g, p in pos[q][:L]:
            if p not in kept:
                kept[p] = len(kept)
            edges.append((q, p, g))
    Lq, R = len(qs), len(kept)

    # max-weight matching via min-cost flow (SPFA successive shortest
    # paths on costs = -gain), stopping once no augmenting path improves
    src, snk = 0, Lq + R + 1
    nn = Lq + R + 2
    graph = [[] for _ in range(nn)]

    def add(u, v, cost):
        graph[u].append([v, 1, cost, len(graph[v])])
        graph[v].append([u, 0, -cost, len(graph[u]) - 1])

    qid = {q: 1 + i for i, q in enumerate(qs)}
    for q in qs:
        add(src, qid[q], 0)
    for j in kept.values():
        add(1 + Lq + j, snk, 0)
    for q, p, g in edges:
        add(qid[q], 1 + Lq + kept[p], -g)

    gain = 0
    INF = float("inf")
    while True:
        dist = [INF] * nn
        inq = bytearray(nn)
        prevv = [0] * nn
        preve = [0] * nn
        dist[src] = 0
        dq = deque([src])
        while dq:
            u = dq.popleft()
            inq[u] = 0
            du = dist[u]
            for i, (v, cap, cost, _) in enumerate(graph[u]):
                if cap > 0 and du + cost < dist[v]:
                    dist[v] = du + cost
                    prevv[v] = u
                    preve[v] = i
                    if not inq[v]:
                        inq[v] = 1
                        dq.append(v)
        if dist[snk] >= 0:
            break
        gain -= dist[snk]
        v = snk
        while v != src:
            e = graph[prevv[v]][preve[v]]
            e[1] -= 1
            graph[v][e[3]][1] += 1
            v = prevv[v]

    return base + gain


def solve():
    assert co(10) == 30
    assert co(30) == 193
    assert co(100) == 1356
    return co(200000)


if __name__ == "__main__":
    print(solve())
