#!/usr/bin/env python3
from math import comb

def solve():
    # With fraction f, after h heads out of 1000 tosses the capital is
    # (1+2f)^h (1-f)^(1000-h), increasing in h.  So for fixed f the winning
    # outcomes are exactly h >= some threshold, and the success probability is
    # a tail of the binomial(1000, 1/2).  We therefore want the f minimizing
    # that threshold: the smallest h for which SOME f reaches 10^9, i.e.
    # max_f [h ln(1+2f) + (1000-h) ln(1-f)] >= 9 ln 10.
    # The maximizing (Kelly) fraction solves 2h/(1+2f) = (1000-h)/(1-f),
    # giving f = (3h-1000)/2000, whence 1+2f = 3h/1000, 1-f = 3(1000-h)/2000.
    # The reachability test becomes the exact integer inequality
    #   (3h)^h * (3(1000-h))^(1000-h) >= 10^9 * 1000^h * 2000^(1000-h).
    n = 1000
    goal = 10 ** 9

    def reachable(h):
        return (3 * h) ** h * (3 * (n - h)) ** (n - h) >= goal * 1000 ** h * 2000 ** (n - h)

    # Threshold is monotone in h: binary search the smallest reachable h.
    lo, hi = n // 3 + 1, n  # need f > 0 => h > 1000/3; h = n surely reaches
    while lo < hi:
        mid = (lo + hi) // 2
        if reachable(mid):
            hi = mid
        else:
            lo = mid + 1
    h_min = lo

    # P(success) = sum_{h >= h_min} C(1000,h) / 2^1000, computed exactly and
    # rounded to 12 decimal places.
    num = sum(comb(n, h) for h in range(h_min, n + 1))
    den = 1 << n
    scaled = (num * 10 ** 12 + den // 2) // den  # round(num/den * 1e12)
    return "0.%012d" % scaled

if __name__ == "__main__":
    print(solve())
