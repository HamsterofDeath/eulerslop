#!/usr/bin/env python3
from collections import defaultdict
from math import gcd

def count_d(d):
    # Count d-digit one-child numbers via a digit DP.
    # State: (c, k) where c[r] = number of substrings ending at the current
    # position with value ≡ r (mod d), capped at 2 (any bucket that ever
    # contributes ≥2 divisible substrings kills the number anyway), and
    # k ∈ {0,1} = divisible substrings seen so far (states reaching ≥2 drop).
    # Appending digit a maps residue r -> (10r + a) mod d and adds a new
    # length-1 substring with residue a mod d.
    if d == 1:
        return 9  # each of 1..9 has exactly one substring, divisible by 1
    coprime = gcd(10, d) == 1
    if coprime:
        # single source per target: nc[s] = c[perm_a[s]]
        inv10 = pow(10, -1, d)
        perm = [[(inv10 * (s - a)) % d for s in range(d)] for a in range(10)]
    else:
        pre = [[] for _ in range(d)]
        for r in range(d):
            pre[(10 * r) % d].append(r)
        src = [[tuple(pre[(s - a) % d]) for s in range(d)] for a in range(10)]

    states = defaultdict(int)
    for a in range(1, 10):  # leading digit nonzero
        c = [0] * d
        c[a % d] = 1
        states[(tuple(c), 1 if a % d == 0 else 0)] += 1

    for _ in range(1, d):
        new = defaultdict(int)
        for (c, k), cnt in states.items():
            for a in range(10):
                if coprime:
                    nc = [c[p] for p in perm[a]]
                else:
                    sa = src[a]
                    nc = [min(2, sum(c[r] for r in sa[s])) for s in range(d)]
                i0 = a % d
                if nc[i0] < 2:
                    nc[i0] += 1
                nk = k + nc[0]
                if nk >= 2:
                    continue  # already more than one divisible substring
                new[(tuple(nc), nk)] += cnt
        states = new
    return sum(cnt for (_, k), cnt in states.items() if k == 1)

def solve():
    # F(10^19): every one-child number below 10^19 has d = 1..19 digits.
    return sum(count_d(d) for d in range(1, 20))

if __name__ == "__main__":
    print(solve())
