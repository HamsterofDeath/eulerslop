#!/usr/bin/env python3
"""Project Euler 771: pseudo-geometric sequences, G(1e18) mod 1e9+7.

A sequence needs |a_i^2 - a_{i-1}a_{i+1}| <= 2.  Writing e_i for the dets,
any window (a,b,c,d,f) with c > 8 forces c | e2^2 - e1*e3 hence
e2^2 = e1*e3, so beyond small values the det pattern is locked into one of:
  e = 0        : geometric with rational ratio p/q,
  e = const    : Vieta chains a_{i+1} = K a_i - a_{i-1},
  e alternating: chains a_{i+1} = K a_i + a_{i-1},
and for a >= 5 every pair has at most one successor (e is unique mod a).
Chain bottoms with both coords > 8 are exactly the pairs (1,P) (const:
1,P,P^2-1,...; alternating: 1,P,P^2+1,...).  Runs a,a+1,... are the K=2
chains.  Hence, counting tuples by their start pair (a0,a1):
  S   : a1 <= SB=32, full DFS (branching only while first coord <= 4),
        with deterministic tails counted analytically;
  R   : runs with a0 >= SB;
  GEO : all-geometric tuples with a1 > SB: sum_p phi(p) floor(N/p^(L-1));
  F   : (1,P) chains with P > SB (start + mid-chain windows);
  ESC : mid-chain starts (second coord > SB) of chains rooted in the small
        zone, collected during the DFS (excluding run and geometric pairs,
        which R and GEO already count).
Validated: G(6)=4, G(10)=26, G(100)=4710, G(1000)=496805, and SB-invariance.
"""
from math import gcd

MODP = 10 ** 9 + 7
SB = 32


def succs(a, b, N):
    out = []
    bb = b * b
    for e in (-2, -1, 0, 1, 2):
        v = bb + e
        if v % a == 0:
            c = v // a
            if b < c <= N:
                out.append(c)
    return out


def tail_info(a, b, N, escape):
    """Deterministic chain from pair (a,b) (requires a >= 5).
    Returns number of future successors K_max; collects escape pairs."""
    steps = 0
    while True:
        if b == a + 1:
            # run: successors b+1, b+2, ... up to N
            return steps + (N - b)
        s = succs(a, b, N)
        if not s:
            return steps
        c = s[0]
        if c > SB and c != b + 1 and (c * c) % b != 0:
            escape.add((b, c))
        a, b = b, c
        steps += 1


def count_from(a, b, ln, N, escape, need=5):
    """tuples along the deterministic chain from (a,b) with ln terms so far."""
    kmax = tail_info(a, b, N, escape)
    lo = max(1, need - ln)  # k=0 (the tuple as-is) is counted by the caller
    return kmax - lo + 1 if kmax >= lo else 0


def G(N):
    if N < 5:
        return 0
    total = 0
    escape = set()

    # --- S: start pairs with a1 <= SB ---
    for a0 in range(1, min(SB, N) + 1):
        for a1 in range(a0 + 1, min(SB, N) + 1):
            stack = [(a0, a1, 2)]
            while stack:
                a, b, ln = stack.pop()
                if a >= 5:
                    total += count_from(a, b, ln, N, escape)
                    continue
                for c in succs(a, b, N):
                    if ln + 1 >= 5:
                        total += 1
                    if c > SB and c != b + 1 and (c * c) % b != 0:
                        escape.add((b, c))
                    stack.append((b, c, ln + 1))

    # --- ESC: chains rooted in the small zone, starts beyond it ---
    seen = set()
    for (x, y) in sorted(escape):
        a, b = x, y
        while (a, b) not in seen:
            seen.add((a, b))
            # count tuples starting at (a,b)
            total += count_from(a, b, 2, N, set())
            s = succs(a, b, N)
            if not s:
                break
            a, b = b, s[0]

    # --- R: runs with a0 >= SB ---
    M = N - 3 - SB
    if M > 0:
        total += M * (M + 1) // 2

    # --- GEO: geometric tuples with a1 > SB ---
    # phi sieve up to N^(1/4)+1
    pmax = 2
    while (pmax + 1) ** 4 <= N:
        pmax += 1
    phi = list(range(pmax + 1))
    for i in range(2, pmax + 1):
        if phi[i] == i:
            for j in range(i, pmax + 1, i):
                phi[j] -= phi[j] // i
    L = 5
    while 2 ** (L - 1) <= N:
        p = 2
        while p ** (L - 1) <= N:
            total += phi[p] * (N // p ** (L - 1))
            p += 1
        L += 1
    # subtract geometric tuples with a1 = c q^(L-2) p <= SB (counted in S)
    L = 5
    while 2 ** (L - 1) <= N:
        for p in range(2, SB + 1):
            if p ** (L - 1) > N:
                break
            for q in range(1, p):
                if gcd(p, q) != 1:
                    continue
                w = q ** (L - 2) * p
                if w > SB:
                    continue
                total -= min(SB // w, N // p ** (L - 1))
        L += 1

    # --- F: (1,P) chains, P > SB ---
    for kind in (0, 1):  # 0: const (K b - a), 1: alt (K b + a)
        P = SB + 1
        while True:
            chain = [1, P]
            while True:
                c = P * chain[-1] - chain[-2] if kind == 0 else P * chain[-1] + chain[-2]
                if c > N:
                    break
                chain.append(c)
            if len(chain) < 5:
                break
            n = len(chain)
            for i in range(0, n - 4):
                total += n - i - 4
            P += 1

    return total


def G_brute(N):
    cnt = 0
    for a0 in range(1, N + 1):
        for a1 in range(a0 + 1, N + 1):
            stack = [(a0, a1, 2)]
            while stack:
                a, b, ln = stack.pop()
                for c in succs(a, b, N):
                    if ln + 1 >= 5:
                        cnt += 1
                    stack.append((b, c, ln + 1))
    return cnt


def solve() -> int:
    assert G(6) == 4 and G(10) == 26 and G(100) == 4710 and G(1000) == 496805
    assert G(1500) == G_brute(1500)
    return G(10 ** 18) % MODP


if __name__ == "__main__":
    print(solve())
