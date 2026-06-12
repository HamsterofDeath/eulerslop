#!/usr/bin/env python3
from fractions import Fraction

def solve():
    # N = first index with all 32 bits set.  Each random word sets each bit
    # independently with probability 1/2, so after k words a given bit is
    # still 0 with probability 2^-k, and
    #   P(N > k) = 1 - (1 - 2^-k)^32.
    # E[N] = sum_{k>=0} P(N > k).  Terms decay like 32*2^-k, so summing to
    # k = 600 leaves an error far below 10^-10.  Exact rational arithmetic
    # avoids any floating point accumulation issues.
    s = Fraction(0)
    for k in range(600):
        s += 1 - Fraction(2**k - 1, 2**k) ** 32
    # Round to 10 decimal places.
    scaled = (s * 10**10 + Fraction(1, 2)).__floor__()
    return f"{scaled // 10**10}.{scaled % 10**10:010d}"

if __name__ == "__main__":
    print(solve())
