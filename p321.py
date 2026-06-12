#!/usr/bin/env python3

def solve():
    # The minimal number of moves to swap n red and n blue counters is
    # M(n) = n(n+2)  (n slides per colour plus n^2 hops; verifiable by BFS
    # for small n: 3, 8, 15, 24, 35, ...).
    #
    # M(n) triangular:  n^2 + 2n = k(k+1)/2.
    # Multiply by 8 and complete squares with u = 2n+2, v = 2k+1:
    #   2u^2 - v^2 = 7   i.e.   v^2 - 2u^2 = -7.
    # This Pell-type equation has two fundamental solution classes,
    # (v,u) = (1,2) and (5,4); all positive solutions follow from the
    # unit 3+2*sqrt(2) of Z[sqrt(2)]:  (v,u) -> (3v+4u, 2v+3u).
    # Every solution has u even, giving n = u/2 - 1.
    terms = []
    for v, u in ((1, 2), (5, 4)):
        for _ in range(25):
            n = u // 2 - 1
            if n >= 1:
                terms.append(n)
            v, u = 3 * v + 4 * u, 2 * v + 3 * u
    terms.sort()
    return sum(terms[:40])

if __name__ == "__main__":
    print(solve())
