#!/usr/bin/env python3
import numpy as np

# Seven-segment masks (bits: top=1, tl=2, tr=4, mid=8, bl=16, br=32, bottom=64).
# Note this problem's font: "7" uses 4 segments (incl. top-left), "9" uses 6.
MASKS = [119, 36, 93, 109, 46, 107, 123, 39, 127, 111]
POP = [bin(m).count("1") for m in MASKS]

def seg_count(digs):
    return sum(POP[d] for d in digs)

def hamming(a, b):
    # a, b: digit lists (most significant first), aligned at the right;
    # missing digit positions count as all segments off (mask 0).
    la, lb = len(a), len(b)
    n = max(la, lb)
    tot = 0
    for i in range(1, n + 1):
        ma = MASKS[a[la - i]] if i <= la else 0
        mb = MASKS[b[lb - i]] if i <= lb else 0
        tot += bin(ma ^ mb).count("1")
    return tot

def digits(n):
    return [int(c) for c in str(n)]

def solve():
    A, B = 10**7, 2 * 10**7
    # Sieve primes in [A, B].
    sieve = np.ones(B + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(B**0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = False
    primes = np.nonzero(sieve[A:])[0] + A

    total = 0
    for p in primes.tolist():
        # Chain of intermediate values down to the digital root.
        chain = [digits(p)]
        n = p
        while n >= 10:
            n = sum(chain[-1])
            chain.append(digits(n))
        # Sam: every displayed number fully on then fully off.
        sam = 2 * sum(seg_count(d) for d in chain)
        # Max: turn on first, switch only differing segments, turn off last.
        mx = seg_count(chain[0]) + seg_count(chain[-1])
        for i in range(len(chain) - 1):
            mx += hamming(chain[i], chain[i + 1])
        total += sam - mx
    return total

if __name__ == "__main__":
    print(solve())
