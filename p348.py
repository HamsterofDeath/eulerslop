#!/usr/bin/env python3
import numpy as np

def palindromes():
    # Generate all palindromic numbers in increasing order, by digit length.
    ndigits = 1
    while True:
        half = (ndigits + 1) // 2
        for h in range(10 ** (half - 1), 10 ** half):
            s = str(h)
            yield int(s + s[::-1][ndigits % 2:])
        ndigits += 1

def solve():
    # For each palindrome P (in increasing order) count representations
    # P = a^2 + b^3 with a, b > 1: loop over cubes b^3 < P - 3 and test whether
    # the remainder is a perfect square (vectorised with numpy).
    cubes = np.arange(2, 100001, dtype=np.int64) ** 3
    found = []
    for P in palindromes():
        if P < 12:  # smallest possible sum is 2^2 + 2^3
            continue
        k = int(np.searchsorted(cubes, P - 3))
        rem = P - cubes[:k]
        r = np.sqrt(rem.astype(np.float64)).astype(np.int64)
        # correct possible floating point error of +-1
        r = np.where(r * r > rem, r - 1, r)
        r = np.where((r + 1) * (r + 1) <= rem, r + 1, r)
        count = int(np.count_nonzero((r * r == rem) & (r >= 2)))
        if count == 4:
            found.append(P)
            if len(found) == 5:
                return sum(found)

if __name__ == "__main__":
    print(solve())
