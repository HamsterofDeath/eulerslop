#!/usr/bin/env python3
"""p190: Maximising a product

Find sum_{m=2..15} floor(P_m) where P_m is the maximum value of
x_1 * x_2^2 * ... * x_m^m subject to sum_{i=1..m} x_i = m.
Using Lagrange multipliers, the optimal values are x_i = 2*i / (m+1).
"""

def P(m):
    prod = 1.0
    for i in range(1, m + 1):
        prod *= (2 * i / (m + 1))**i
    return prod

def solve():
    total = 0
    for m in range(2, 16):
        total += int(P(m))
    return total

if __name__ == "__main__":
    print(solve())
