#!/usr/bin/env python3
import numpy as np


def solve():
    # The m-1 cut points are a uniform (m-1)-subset of the n-1 lattice points,
    # so the segment lengths are a uniformly random composition of n into m
    # positive parts, C(n-1, m-1) of them in total.  For the second-shortest
    # length X, use E[X] = sum_{t>=1} P(X >= t) with
    #   P(X >= t) = P(at most one part < t)
    #             = [#(all parts >= t) + #(exactly one part < t)] / C(n-1, m-1).
    # Compositions with all m parts >= t: C(n - m(t-1) - 1, m-1).
    # Exactly one part s < t (m choices of position, the rest >= t) telescopes
    # by the hockey-stick identity, and the upper hockey-stick end cancels the
    # all->=t term's argument, leaving
    #   P(X >= t) * C(n-1, m-1) = (1-m)*C(B, m-1) + m*C(A, m-1),
    # with B = n - m(t-1) - 1 and A = n - (m-1)(t-1) - 1.
    # Each ratio C(N, m-1)/C(n-1, m-1) = prod_{i<m-1} (N-i)/(n-1-i) is a short
    # float product (no cancellation issues: per-term absolute error ~1e-12).
    def expectation(n, m):
        T = (n - 1) // (m - 1)  # largest t with P(X >= t) > 0
        t = np.arange(1, T + 1, dtype=np.float64)
        B = n - m * (t - 1) - 1
        A = n - (m - 1) * (t - 1) - 1

        def ratio(N):
            r = np.ones_like(N)
            for i in range(m - 1):
                r *= (N - i) / (n - 1 - i)
            r[N < m - 1] = 0.0  # binomial vanishes below m-1
            return r

        p = (1 - m) * ratio(B) + m * ratio(A)
        return float(np.sum(p))

    # sanity checks from the problem statement
    assert abs(expectation(3, 2) - 2.0) < 1e-9
    assert abs(expectation(8, 3) - 16 / 7) < 1e-9

    return f"{expectation(10 ** 7, 100):.5f}"


if __name__ == "__main__":
    print(solve())
