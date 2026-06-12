#!/usr/bin/env python3
import numpy as np

def T(s, p, K=200):
    # Optimal nested group testing. Two interleaved DPs:
    #   f[n] = expected tests to fully screen n untested sheep (iid infected w.p. p)
    #   g[n] = expected tests to screen n sheep KNOWN to contain >= 1 infected
    # g: pool a subgroup of k (1 <= k < n).  With prob a = q^k(1-q^{n-k})/(1-q^n)
    # it is negative -> the other n-k still contain an infected one (g[n-k]);
    # otherwise the subgroup contains one (g[k]) and the rest carry no extra
    # information (f[n-k]).  g[1] = 0 (a known-infected sheep needs no test).
    # f: pool a first group of k (k = n allowed); cost c(k) = 1 + (1-q^k) g[k],
    # then f[n-k] for the rest, i.e. f[n] = min_k c(k) + f[n-k].
    # Optimal group sizes stay small (< 100 even for p = 0.01), so the exact
    # O(K^2) tables up to K suffice and f is extended to s with groups <= K.
    q = 1.0 - p
    Kc = min(K, s)
    qpow = q ** np.arange(Kc + 1)
    f = np.zeros(Kc + 1)
    g = np.zeros(Kc + 1)
    f[1] = 1.0
    for n in range(2, Kc + 1):
        k = np.arange(1, n)
        a = qpow[k] * (1.0 - qpow[n - k]) / (1.0 - qpow[n])
        rev = slice(n - 1, 0, -1)            # index n-k for k = 1..n-1
        g[n] = 1.0 + (a * g[rev] + (1.0 - a) * (g[1:n] + f[rev])).min()
        c = 1.0 + (1.0 - qpow[1:n + 1]) * g[1:n + 1]
        f[n] = (c + f[:n][::-1]).min()
    if s <= Kc:
        return f[s]
    cvec = 1.0 + (1.0 - qpow[1:]) * g[1:]    # per-group cost c(k), k = 1..K
    ff = np.empty(s + 1)
    ff[:Kc + 1] = f
    for n in range(Kc + 1, s + 1):
        ff[n] = (cvec + ff[n - Kc:n][::-1]).min()
    return ff[s]

def solve():
    assert round(T(25, 0.02), 6) == 4.155452
    assert round(T(25, 0.10), 6) == 12.702124
    total = sum(T(10000, i / 100.0) for i in range(1, 51))
    return f"{total:.6f}"

if __name__ == "__main__":
    print(solve())
