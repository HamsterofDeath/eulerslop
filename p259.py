#!/usr/bin/env python3
from math import gcd

# Digits 1..9 in order, optional concatenation, binary + - * / and parentheses.
# Interval DP: vals(i,j) = set of exact rationals reachable from digits i..j-1.
# Each set contains the concatenated number plus a op b for every split point
# and every (a,b) pair from the two sub-intervals (order fixed, so only a op b).
# Rationals are stored as normalised tuples (num, den) with den > 0; integers
# (den == 1, the overwhelmingly common case) take a gcd-free fast path.
# Finally sum the distinct positive integers in vals(0,9).

DIGITS = "123456789"


def combine(L, R):
    out = set()
    add = out.add
    g = gcd
    for n1, d1 in L:
        for n2, d2 in R:
            if d1 == 1 and d2 == 1:
                # integer fast path
                add((n1 + n2, 1))
                add((n1 - n2, 1))
                add((n1 * n2, 1))
                if n2:
                    if n1 % n2 == 0:
                        add((n1 // n2, 1))
                    else:
                        nn, dd = (n1, n2) if n2 > 0 else (-n1, -n2)
                        c = g(nn, dd)
                        add((nn // c, dd // c))
            else:
                d = d1 * d2
                n = n1 * d2 + n2 * d1
                c = g(n, d)
                add((n // c, d // c))
                n = n1 * d2 - n2 * d1
                c = g(n, d)
                add((n // c, d // c))
                n = n1 * n2
                c = g(n, d)
                add((n // c, d // c))
                if n2:
                    n = n1 * d2
                    d = d1 * n2
                    if d < 0:
                        n, d = -n, -d
                    c = g(n, d)
                    add((n // c, d // c))
    return out


def solve():
    n = len(DIGITS)
    # vals[i][j] for interval [i, j)
    vals = {}
    for length in range(1, n + 1):
        for i in range(0, n - length + 1):
            j = i + length
            s = {(int(DIGITS[i:j]), 1)}
            for k in range(i + 1, j):
                s |= combine(vals[i, k], vals[k, j])
            vals[i, j] = s
    return sum(num for num, den in vals[0, n] if den == 1 and num > 0)


if __name__ == "__main__":
    print(solve())
