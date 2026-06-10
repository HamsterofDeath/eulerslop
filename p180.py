#!/usr/bin/env python3
"""p180: Rational Zeros

We find the sum of all distinct s(x, y, z) = x + y + z for golden triples (x, y, z) of order 35.
A triple (x, y, z) of rationals of the form a/b with 0 < a < b <= 35 is golden if
f_n(x, y, z) = (x + y + z)(x^n + y^n - z^n) = 0 for some integer n.
Since x, y, z > 0, this is equivalent to x^n + y^n = z^n.
By Fermat's Last Theorem for rational numbers, n can only be 1, 2, -1, -2.
"""
from fractions import Fraction

def solve():
    k = 35
    # S is the set of all rational numbers of the form a/b with 0 < a < b <= k
    S = set()
    for b in range(2, k + 1):
        for a in range(1, b):
            S.add(Fraction(a, b))
            
    # For fast lookups
    S_squares = {z*z: z for z in S}
    S_inv = {1/z: z for z in S}
    S_inv_squares = {1/(z*z): z for z in S}
    
    sums = set()
    
    # Check all pairs (x, y) with x <= y to avoid duplicate sums
    for x in S:
        for y in S:
            if x > y:
                continue
                
            # n = 1: x + y = z
            z1 = x + y
            if z1 in S:
                sums.add(x + y + z1)
                
            # n = 2: x^2 + y^2 = z^2
            z2_sq = x*x + y*y
            if z2_sq in S_squares:
                z2 = S_squares[z2_sq]
                sums.add(x + y + z2)
                
            # n = -1: 1/x + 1/y = 1/z
            z_inv_1 = 1/x + 1/y
            if z_inv_1 in S_inv:
                z_neg1 = S_inv[z_inv_1]
                sums.add(x + y + z_neg1)
                
            # n = -2: 1/x^2 + 1/y^2 = 1/z^2
            z_inv_2_sq = 1/(x*x) + 1/(y*y)
            if z_inv_2_sq in S_inv_squares:
                z_neg2 = S_inv_squares[z_inv_2_sq]
                sums.add(x + y + z_neg2)
                
    total_sum = sum(sums)
    return total_sum.numerator + total_sum.denominator

if __name__ == "__main__":
    print(solve())
