#!/usr/bin/env python3
import numpy as np

def solve():
    # Golomb's self-describing sequence G: value k occurs exactly G(k) times,
    # so the prefix of G containing all values <= K has length
    #   S1(K) = sum_{k<=K} G(k),
    # and therefore G(p) = min{ K : S1(K) >= p }.
    #
    # We need G(n^3) for n < 10^6, i.e. positions p up to ~10^18.  There
    # G(p) ~ 1.3*10^11, far too large to tabulate.  But S1 itself can be
    # evaluated from a much smaller table: G is constant (= v) on the run of
    # indices k in (T1(v-1), T1(v)], where T1(v) = sum_{u<=v} G(u).  Hence
    #   S1(K) = T2(v-1) + v*(K - T1(v-1)),  v = run value at index K,
    # with T2(v) = sum_{u<=v} u*G(u).  S1 is piecewise linear in K with
    # breakpoints S1(T1(v)) = T2(v), so inverting it needs only:
    #   v = min{ v : T2(v) >= p }   (binary search in T2)
    #   G(p) = T1(v-1) + ceil((p - T2(v-1)) / v)
    # Run values v at indices K <= 1.6*10^11 stay below ~10^7, so tabulating
    # G, T1, T2 up to 1.3*10^7 covers all queries.
    M = 13_000_000

    # Bootstrap a small prefix of G by runs: value v occurs G(v) times.
    g = [0, 1, 2, 2]                # g[n] = G(n) for n = 1..3
    v = 3
    while len(g) <= 2000:
        g.extend([v] * g[v])
        v += 1
    small = np.array(g[1:], dtype=np.int64)

    # Two repeat expansions get us past M elements.
    mid = np.repeat(np.arange(1, len(small) + 1, dtype=np.int64), small)
    K = int(np.searchsorted(np.cumsum(mid), M)) + 2
    G = np.repeat(np.arange(1, K + 1, dtype=np.int64), mid[:K])[:M]

    vals = np.arange(1, M + 1, dtype=np.int64)
    T1 = np.cumsum(G)               # T1[v-1] = sum_{u<=v} G(u)
    T2 = np.cumsum(vals * G)        # T2[v-1] = sum_{u<=v} u*G(u)

    NMAX = 10 ** 6
    p = np.arange(1, NMAX, dtype=np.int64) ** 3
    assert int(T2[-1]) >= int(p[-1])

    idx = np.searchsorted(T2, p)            # v-1 for v = min{v: T2(v) >= p}
    v = idx + 1
    t1_prev = np.where(idx > 0, T1[idx - 1], 0)
    t2_prev = np.where(idx > 0, T2[idx - 1], 0)
    Gp = t1_prev + (p - t2_prev + v - 1) // v

    # Sanity checks from the problem statement.
    def G_at(pos):
        i = int(np.searchsorted(T2, pos))
        a = int(T1[i - 1]) if i else 0
        b = int(T2[i - 1]) if i else 0
        return a + (pos - b + i) // (i + 1)
    assert G_at(10 ** 3) == 86 and G_at(10 ** 6) == 6137
    assert int(Gp[: 10 ** 3 - 1].sum()) == 153506976

    return int(Gp.sum())

if __name__ == "__main__":
    print(solve())
